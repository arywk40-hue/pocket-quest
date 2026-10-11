"""Check actual runtime connectivity without exposing credentials or spending audio credits."""
import json
import os
from pathlib import Path
import httpx
from dotenv import dotenv_values

root = Path(__file__).resolve().parents[1]
settings = dotenv_values(root / '.env')
for partner, keys in {
    'ElevenLabs': ('ELEVENLABS_API_KEY', 'ELEVENLABS_VOICE_ID'),
    'Sentry Agent Tracing': ('SENTRY_DSN',),
}.items():
    missing = [key for key in keys if not os.environ.get(key, settings.get(key))]
    if missing:
        print(f'{partner}: add {", ".join(missing)} to {root / ".env"}')
    else:
        print(f'{partner}: settings present; restart the companion after changes.')

with httpx.Client(timeout=5, trust_env=False) as client:
    try:
        response = client.get('http://127.0.0.1:8787/api/status')
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2))
        print('Configured partner keys are not proof that an account call succeeded.')
    except httpx.HTTPError:
        raise SystemExit('Start the local companion first: python -m uvicorn backend.app:app --port 8787')
