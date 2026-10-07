"""Collect real account diagnostics/receipts. No mocks, keys or photos printed."""
import argparse
import json
from pathlib import Path
import httpx

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--prepare-audio',action='store_true',help='Generate three predefined chapters; first generation uses ElevenLabs credits.')
p.add_argument('--language',choices=['en-IN','hi-IN'],default='en-IN')
p.add_argument('--trace-check',action='store_true',help='Send a labelled diagnostic to your configured Sentry project.')
p.add_argument('--out',type=Path,default=Path('runtime/integration-check.json'))
a=p.parse_args()
try:
    with httpx.Client(base_url='http://127.0.0.1:8787',timeout=180,trust_env=False) as client:
        status=client.get('/api/status').raise_for_status().json()
        report={'status':status,'connections':client.post('/api/integrations/check').raise_for_status().json()}
        if a.prepare_audio:
            first=client.post('/api/audio-pack',json={'language':a.language}).raise_for_status().json()
            second=client.post('/api/audio-pack',json={'language':a.language}).raise_for_status().json()
            report['audio']={'first':first['receipt'],'repeat':second['receipt'],
                             'repeat_used_cache':second['receipt']['generated']==0 and second['receipt']['cache_hits']==3}
        if a.trace_check:
            report['trace_diagnostic']=client.post('/api/trace-check').raise_for_status().json()
        report['evidence']=client.get('/api/integrations/evidence').raise_for_status().json()
        report['notice']='Inspect real Sentry traces in dashboard; this diagnostic is not model evidence. Audio playback and an outdoor trial need separate verification.'
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2))
        print('Saved',a.out)
except httpx.HTTPStatusError as error:
    raise SystemExit(f'Companion returned HTTP {error.response.status_code}. Check its settings and account configuration.')
except httpx.HTTPError:
    raise SystemExit('Could not reach the companion. Start python -m uvicorn backend.app:app --port 8787 first.')
