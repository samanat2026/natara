#!/usr/bin/env python3
"""Genera demo/index.html y consola-demo/index.html desde index.html (la app real)
y copia todo a docs/. Uso: python3 tools/build.py"""
import pathlib, shutil, sys
R = pathlib.Path(__file__).resolve().parent.parent
src = (R / 'index.html').read_text(encoding='utf-8')

def must(s, a, b):
    if a not in s: sys.exit(f'No encontré el texto para reemplazar: {a[:70]!r}')
    return s.replace(a, b)

DESC_R = '<meta name="description" content="Inventario, caja, ingresos y egresos para tu negocio.">'
DESC_D = '<meta name="description" content="Prueba Natara gratis: inventario, caja, ingresos y egresos para tu negocio.">'
OGT_R = '<meta property="og:title" content="Natara · by Samanat">'
OGT_D = '<meta property="og:title" content="Natara · Demo">'
OGD_R = '<meta property="og:description" content="Inventario, caja, ingresos y egresos para tu negocio.">'
OGD_D = '<meta property="og:description" content="Prueba Natara gratis: inventario, caja, ingresos y egresos para tu negocio.">'
OGU_R = '<meta property="og:url" content="https://natara.com.co/">'
OGU_D = '<meta property="og:url" content="https://natara.com.co/demo/">'
MODE = '<script>window.NATARA_MODE="real";</script>\n'

s0 = src.index('<script>window.NATARA_FB_CONFIG=')
s1 = src.index('</script>', src.index('window.dispatchEvent(new Event(\'fb-ready\'));')) 
real_fb = src[s0:s1]
# bloque de Firebase de la demo (solo Firestore para la llave pública)
cfg = real_fb[real_fb.index('{apiKey'):real_fb.index('};</script>')+1]
mod_start = real_fb.index('<script type="module">') if '<script type="module">' in real_fb else None
head = real_fb[real_fb.index('</script>')+len('</script>\n'):]
head = head[:head.index('import ')]
demo_fb = (head + 'import {initializeApp} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";\n'
           'import {getFirestore,doc,getDoc,setDoc,increment} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";\n'
           'const app=initializeApp(' + cfg + ');\n'
           'window.FB={app,db:getFirestore(app),doc,getDoc,setDoc,increment};\n'
           'window.dispatchEvent(new Event(\'fb-ready\'));\n')

def demo_common(s, title, extra_meta=''):
    s = must(s, DESC_R, DESC_D + extra_meta)
    s = must(s, OGT_R, OGT_D); s = must(s, OGD_R, OGD_D); s = must(s, OGU_R, OGU_D)
    s = must(s, '<title>Natara</title>', f'<title>{title}</title>')
    s = s[:s.index(real_fb)] + demo_fb + s[s.index(real_fb)+len(real_fb):]
    return s

demo = demo_common(src, 'Natara · Demo')
demo = must(demo, MODE, '')
cons = demo_common(src, 'Natara · Consola demo', '\n<meta name="robots" content="noindex,nofollow">')
cons = must(cons, MODE, '<script>window.NATARA_DEMO_ADMIN=true;</script>\n')

(R/'demo/index.html').write_text(demo, encoding='utf-8')
(R/'consola-demo/index.html').write_text(cons, encoding='utf-8')
for p in ['index.html','demo/index.html','consola-demo/index.html','diagnostico/index.html']:
    shutil.copyfile(R/p, R/'docs'/p)
print('Listo: demo, consola-demo y docs/ regenerados.')
