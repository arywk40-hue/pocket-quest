"""Check actual runtime connectivity without exposing credentials or spending audio credits."""
import json
import httpx

with httpx.Client(timeout=5, trust_env=False) as client:
    try:
        response = client.get('http://127.0.0.1:8787/api/status')
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2))
        print('Configured partner keys are not proof that an account call succeeded.')
    except httpx.HTTPError:
        raise SystemExit('Start the local companion first: python -m uvicorn backend.app:app --port 8787')
