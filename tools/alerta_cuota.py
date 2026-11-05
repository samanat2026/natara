#!/usr/bin/env python3
"""Revisa cuánto lleva gastado hoy Firestore en el plan gratis y avisa por WhatsApp (CallMeBot)
cuando pasa el 80 %, el 90 % y el 95 % de lecturas, escrituras o borrados. Cada aviso sale una sola vez al día.

La cuota gratis se reinicia a la medianoche de la hora del Pacífico (2 o 3 a. m. en Colombia).
Las cifras de Google llegan con unos minutos de retraso.

Variables de entorno (secretos de GitHub):
  GCP_SA_KEY        JSON de la cuenta de servicio con el rol "Visualizador de Monitoring"
  CALLMEBOT_PHONE   tu WhatsApp en formato internacional, por ejemplo +573001234567
  CALLMEBOT_APIKEY  la clave que te mandó CallMeBot
Opcionales: GCP_PROJECT (natara-96555), UMBRALES (80,90,95), PRUEBA=1 manda el estado de hoy aunque no pase nada.
Uso local sin enviar nada: python3 tools/alerta_cuota.py --simular 41200 3100 0
"""
import json, os, pathlib, sys, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

PACIFICO, COLOMBIA = ZoneInfo('America/Los_Angeles'), ZoneInfo('America/Bogota')
# Cuota gratis diaria de Firestore (plan Spark)
LIMITES = {'lecturas': ('document/read_count', 50000), 'escrituras': ('document/write_count', 20000), 'borrados': ('document/delete_count', 20000)}
ESTADO = pathlib.Path(os.environ.get('ALERTAS_DIR', '.alertas')) / 'enviadas.json'


def inicio_del_dia():
    ahora = datetime.now(PACIFICO)
    return ahora.replace(hour=0, minute=0, second=0, microsecond=0)


def medir(proyecto, credenciales_json):
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    cred = service_account.Credentials.from_service_account_info(
        json.loads(credenciales_json), scopes=['https://www.googleapis.com/auth/monitoring.read'])
    s = AuthorizedSession(cred)
    ini, fin = inicio_del_dia().astimezone(timezone.utc), datetime.now(timezone.utc)
    periodo = max(60, int((fin - ini).total_seconds()) + 60)
    usado = {}
    for nombre, (metrica, _) in LIMITES.items():
        r = s.get(f'https://monitoring.googleapis.com/v3/projects/{proyecto}/timeSeries', params={
            'filter': f'metric.type="firestore.googleapis.com/{metrica}"',
            'interval.startTime': ini.isoformat().replace('+00:00', 'Z'),
            'interval.endTime': fin.isoformat().replace('+00:00', 'Z'),
            'aggregation.alignmentPeriod': f'{periodo}s',
            'aggregation.perSeriesAligner': 'ALIGN_SUM',
            'aggregation.crossSeriesReducer': 'REDUCE_SUM',
        }, timeout=30)
        if r.status_code != 200:
            sys.exit(f'Google respondió {r.status_code} al pedir {nombre}: {r.text[:300]}')
        total = 0
        for serie in r.json().get('timeSeries', []):
            for p in serie.get('points', []):
                v = p['value']
                total += int(v.get('int64Value', v.get('doubleValue', 0)))
        usado[nombre] = total
    return usado


def miles(n):
    return f'{n:,}'.replace(',', '.')


def mensaje(usado, nuevos):
    reinicio = (inicio_del_dia() + timedelta(days=1)).astimezone(COLOMBIA)
    hora = reinicio.strftime('%I:%M %p').lstrip('0').replace('AM', 'a. m.').replace('PM', 'p. m.')
    lineas = []
    for nombre, (_, lim) in LIMITES.items():
        pct = usado[nombre] * 100 // lim
        marca = '⚠️ ' if pct >= 80 else ''
        lineas.append(f'{marca}{nombre.capitalize()}: {miles(usado[nombre])} de {miles(lim)} ({pct} %)')
    cab = f'Natara · Firebase pasó el {max(nuevos.values())} % de la cuota gratis de hoy' if nuevos else 'Natara · Firebase hoy'
    pie = f'Se reinicia a las {hora} (hora Colombia).'
    if nuevos and max(nuevos.values()) >= 95:
        pie += ' Si llega al 100 %, Natara deja de guardar hasta esa hora.'
    return '\n'.join([cab, *lineas, pie])


def enviar(texto, telefono, clave):
    url = 'https://api.callmebot.com/whatsapp.php?' + urllib.parse.urlencode({'phone': telefono, 'text': texto, 'apikey': clave})
    with urllib.request.urlopen(url, timeout=30) as r:
        cuerpo = r.read().decode('utf-8', 'replace')
    if r.status != 200 or 'error' in cuerpo.lower():
        sys.exit(f'CallMeBot no mandó el mensaje ({r.status}): {cuerpo[:300]}')


def main():
    umbrales = sorted(int(x) for x in os.environ.get('UMBRALES', '80,90,95').split(','))
    simular = '--simular' in sys.argv
    if simular:
        i = sys.argv.index('--simular')
        usado = dict(zip(LIMITES, (int(x) for x in sys.argv[i + 1:i + 4])))
    else:
        usado = medir(os.environ.get('GCP_PROJECT', 'natara-96555'), os.environ['GCP_SA_KEY'])
    dia = inicio_del_dia().date().isoformat()
    estado = json.loads(ESTADO.read_text()) if ESTADO.exists() else {}
    if estado.get('dia') != dia:
        estado = {'dia': dia, 'enviados': {}}
    # el umbral más alto que pasó cada contador y que todavía no se avisó hoy
    nuevos = {}
    for nombre, (_, lim) in LIMITES.items():
        pct = usado[nombre] * 100 / lim
        pasados = [u for u in umbrales if pct >= u and u > estado['enviados'].get(nombre, 0)]
        if pasados:
            nuevos[nombre] = max(pasados)
    print(json.dumps({'dia': dia, 'usado': usado, 'nuevos': nuevos}, ensure_ascii=False))
    prueba = os.environ.get('PRUEBA') == '1'
    if not nuevos and not prueba:
        return
    texto = mensaje(usado, nuevos)
    if simular:
        print(texto)
    else:
        enviar(texto, os.environ['CALLMEBOT_PHONE'], os.environ['CALLMEBOT_APIKEY'])
        print('Mensaje enviado por WhatsApp')
    estado['enviados'].update(nuevos)
    ESTADO.parent.mkdir(parents=True, exist_ok=True)
    ESTADO.write_text(json.dumps(estado))
    out = os.environ.get('GITHUB_OUTPUT')
    if out and nuevos:
        with open(out, 'a') as f:
            f.write('cambio=si\n')


if __name__ == '__main__':
    main()
