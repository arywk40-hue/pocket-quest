"""Produce a clean source archive without runtime data, secrets, hosting IDs or model weights."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'dist/Outside-Case-Source.zip'
files=[]
for name in ['README.md','LICENSE','requirements.txt','requirements-dev.txt','package.json','package-lock.json','.env.example','.gitignore']:
    files.append(ROOT/name)
for directory in ['backend','dist','docs','scripts','tests','evaluation','.github']:
    files.extend(p for p in (ROOT/directory).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p!=out)
with ZipFile(out,'w',ZIP_DEFLATED) as z:
    for p in sorted(set(files)):
        z.write(p,'outside-case/'+str(p.relative_to(ROOT)))
print(out)
