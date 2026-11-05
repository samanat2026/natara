#!/usr/bin/env python3
"""Revisa que el JavaScript de las páginas no tenga errores de sintaxis (node --check)
y que demo/, consola-demo/ y docs/ estén generados desde index.html. Uso: python3 tools/check.py"""
import pathlib, re, subprocess, sys, tempfile
R = pathlib.Path(__file__).resolve().parent.parent
bad = 0
for page in ['index.html', 'demo/index.html', 'consola-demo/index.html', 'diagnostico/index.html']:
    html = (R / page).read_text(encoding='utf-8')
    for i, m in enumerate(re.finditer(r'<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>', html, re.S)):
        code = m.group(2)
        if not code.strip():
            continue
        ext = '.mjs' if 'module' in m.group(1) else '.js'
        with tempfile.NamedTemporaryFile('w', suffix=ext, delete=False, encoding='utf-8') as f:
            f.write(code)
        r = subprocess.run(['node', '--check', f.name], capture_output=True, text=True)
        if r.returncode:
            bad += 1
            print(f'Error de sintaxis en {page}, script {i + 1}:\n{r.stderr}')
# las copias generadas deben coincidir con lo que produce build.py
subprocess.run([sys.executable, str(R / 'tools/build.py')], check=True, capture_output=True)
diff = subprocess.run(['git', 'diff', '--name-only', '--', 'demo', 'consola-demo', 'docs'], cwd=R, capture_output=True, text=True).stdout.strip()
if diff:
    bad += 1
    print('Las copias no estaban al día con index.html. Corre python3 tools/build.py y vuelve a subir:\n' + diff)
print('Todo bien' if not bad else f'{bad} problema(s)')
sys.exit(1 if bad else 0)
