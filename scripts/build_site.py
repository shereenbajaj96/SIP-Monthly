"""Build public/index.html (the standalone site) from dashboard/page.html.

Usage: python3 scripts/build_site.py
The page markup goes into the shell; its script runs after the d3 and dash runtime shim load.
"""
import os, re

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
page = open(os.path.join(root, 'dashboard', 'page.html'), encoding='utf8').read()
shell = open(os.path.join(root, 'scripts', 'shell.html'), encoding='utf8').read()

page = re.sub(r"<meta name='dash-one-writer'>\s*", '', page)
m = re.search(r'<script>[\s\S]*</script>', page)
script, markup = m.group(0), page[:m.start()] + page[m.end():]

out = shell.replace('<!--PAGE-->', markup.strip()).replace('<!--SCRIPT-->', script)
os.makedirs(os.path.join(root, 'public'), exist_ok=True)
open(os.path.join(root, 'public', 'index.html'), 'w', encoding='utf8').write(out)
print('public/index.html', len(out))
