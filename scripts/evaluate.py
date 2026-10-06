"""Run a prelabelled photo set against a LIVE local companion. No model mocks."""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import math
import time
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse
import httpx


def percentile(values, fraction):
    if not values:
        return None
    ordered = sorted(values)
    return round(ordered[max(0, math.ceil(len(ordered) * fraction) - 1)], 1)


def metrics(rows):
    ok = [r for r in rows if r.get('status') in {'accepted', 'uncertain', 'rejected'}]
    negative = [r for r in rows if r['expected'] != 'accepted']
    positive = [r for r in rows if r['expected'] == 'accepted']
    false_accepts = sum(r.get('status') == 'accepted' for r in negative)
    false_rejects = sum(r.get('status') == 'rejected' for r in positive)
    return {
        'total': len(rows), 'completed': len(ok), 'failures': len(rows) - len(ok),
        'exact_status_matches': sum(r.get('status') == r['expected'] for r in ok),
        'negative_cases': len(negative), 'false_acceptances': false_accepts,
        'false_acceptance_rate_all_negative_cases': false_accepts / len(negative) if negative else None,
        'positive_cases': len(positive), 'false_rejections': false_rejects,
        'uncertainty_count': sum(r.get('status') == 'uncertain' for r in ok),
        'outcomes': dict(Counter(r.get('status', 'error') for r in rows)),
        'p50_ms_all_requests': percentile([r['elapsed_ms'] for r in rows], .5),
        'p95_ms_all_requests': percentile([r['elapsed_ms'] for r in rows], .95),
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest', type=Path)
    p.add_argument('--base-url', default='http://127.0.0.1:8787')
    p.add_argument('--out', type=Path, default=Path('runtime/evaluation'))
    args = p.parse_args()
    if urlparse(args.base_url).hostname not in {'localhost', '127.0.0.1', '::1'}:
        p.error('Use the loopback local companion, not a hosted inference service.')
    raw = args.manifest.read_bytes()
    items = [json.loads(line) for line in raw.decode().splitlines() if line.strip()]
    if not items:
        p.error('Manifest must contain real labelled photos.')
    ids = set()
    for item in items:
        if item['id'] in ids or item['expected'] not in {'accepted', 'uncertain', 'rejected'}:
            p.error('IDs must be unique and expected statuses valid.')
        ids.add(item['id'])
        if item['clue_id'] not in {'leaf', 'bark', 'ground'} or item['group'] not in {'valid', 'unrelated', 'blurry', 'misleading_note'}:
            p.error('Unknown clue or evaluation group.')
        path = args.manifest.parent / item['image']
        if not path.is_file() or path.suffix.lower() not in {'.jpg', '.jpeg', '.png', '.webp'}:
            p.error(f"Supply a real JPEG/PNG/WebP for {item['id']} before running.")
        item['_path'] = path
    rows = []
    with httpx.Client(timeout=180, trust_env=False) as client:
        status = client.get(args.base_url.rstrip('/') + '/api/status').raise_for_status().json()
        if not status.get('model') or status.get('model_mode') != 'vision':
            p.error('Load a vision model. Gemma 2 note interpretation cannot be evaluated as photo review.')
        for item in items:
            image_bytes = item['_path'].read_bytes()
            mime = {'jpg': 'jpeg', 'jpeg': 'jpeg', 'png': 'png', 'webp': 'webp'}[item['_path'].suffix.lower()[1:]]
            payload = {'clue_id': item['clue_id'], 'note': item['note'], 'image': 'data:image/' + mime + ';base64,' + base64.b64encode(image_bytes).decode()}
            started = time.perf_counter()
            row = {k: item[k] for k in ('id', 'clue_id', 'group', 'expected')}
            row['image_sha256'] = hashlib.sha256(image_bytes).hexdigest()
            row['note_sha256'] = hashlib.sha256(item['note'].encode()).hexdigest()
            try:
                response = client.post(args.base_url.rstrip('/') + '/api/review', json=payload)
                row['http_status'] = response.status_code
                response.raise_for_status()
                result = response.json()
                if result.get('review_kind') != 'vision' or result.get('status') not in {'accepted','uncertain','rejected'}:
                    raise ValueError('Response was not a vision review')
                # Raw output is a private local evaluation artifact; no photos/notes copied.
                row.update(result)
            except (httpx.HTTPError, ValueError) as error:
                row['error_type'] = type(error).__name__
            row['elapsed_ms'] = round((time.perf_counter() - started) * 1000, 1)
            rows.append(row)
            print(item['id'], row.get('status', 'error'), row['elapsed_ms'], 'ms', flush=True)
    report = {'manifest_sha256': hashlib.sha256(raw).hexdigest(), 'model': status['model_name'],
              'model_mode': status['model_mode'], 'summary': metrics(rows),
              'by_group': {group: metrics([r for r in rows if r['group'] == group]) for group in sorted({r['group'] for r in rows})},
              'cases': rows, 'notice': 'Small labelled sample, not general accuracy. Failed requests are counted separately. Hardware and actual weight hashes must be recorded separately.'}
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    (args.out / 'report.md').write_text('# Live photo evaluation\n\nModel: ' + status['model_name'] + '\n\nManifest SHA-256: `' + report['manifest_sha256'] + '`\n\n```json\n' + json.dumps(report['summary'], indent=2) + '\n```\n\nResults include failures. Review results.json privately before publishing any excerpts.\n')
    print('Saved', args.out / 'report.md')

if __name__ == '__main__':
    main()
