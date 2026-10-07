# Partner setup and submission proof

This connects real accounts. Automated software tests use mocks and do not establish successful account calls. The three intended categories are Gemma, ElevenLabs, and Sentry Agent Tracing. Complete the demonstrations before claiming them.

## 1. Configure your companion

Follow the README's clone/install instructions. Edit local `.env`:

```dotenv
MODEL_BASE_URL=http://127.0.0.1:11434
MODEL_NAME=gemma3:4b
MODEL_MODE=vision
ELEVENLABS_API_KEY=your_local_key
ELEVENLABS_VOICE_ID=your_selected_voice_id
SENTRY_DSN=your_python_project_dsn
```

In ElevenLabs, create an API key with access to speech generation and the selected voice. Choose a voice available to your account and copy its voice ID. This uses `eleven_multilingual_v2`, with English or Hindi predefined scripts. Keys with restricted voice access may fail the voice lookup. Check your account's available credits before preparation.

In Sentry, create/select a Python project and copy its DSN from the project setup. A DSN is not an account auth token. The companion initializes the Python SDK and custom agent/model spans; you do not need to enable a separate autonomous AI debugging product. Trace sampling is 100% for this small demo. Check your account usage before longer sessions.

Never commit `.env` or paste keys in a submission. Restart after changing it:

```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8787
```

Open http://127.0.0.1:8787. Settings distinguishes configured connections from verified results. Photos and notes stay on your machine/local model; only predefined narration text goes to ElevenLabs. Sentry receives timing, outcome and model metadata, with request bodies and local variables excluded.

## 2. Generate narration and collect receipts

In another terminal with the same virtual environment:

```bash
python scripts/integration_check.py --prepare-audio --trace-check
```

For Hindi add `--language hi-IN`. The selected-voice check is an authenticated GET, not paid speech generation. The first audio preparation requests uncached chapters and consumes credits. The repeat must show `generated: 0`, `cache_hits: 3`, and `repeat_used_cache: true`. A previously prepared pack may show cache hits on both runs; do not describe it as a fresh generation. Actual MP3 hashes, byte counts and timings are saved in `runtime/audio-pack-receipts.jsonl`.

The script saves `runtime/integration-check.json`. Its diagnostic event/trace IDs mean the SDK attempted delivery, not that Sentry accepted it. Find those IDs in your dashboard. The diagnostic has no invented model span and does not qualify as a model run.

Prepare audio in Settings to load/persist it in the browser, play each chapter, then download the field kit. The CLI warms the server cache; it does not populate browser storage. Open the downloaded HTML on the actual phone and test playback with connectivity disabled. Report the phone/browser and any file-viewer limitations. The field kit contains audio and transcripts, not Gemma weights.

## 3. Demonstrate actual Gemma agent traces

Collect a real clue photo, import your field journal into the companion, and select **Review photo with Gemma**. Different accepted patterns must visibly change the authored mystery. Copy the review's trace ID from exported integration receipts or `runtime/review-receipts.jsonl`.

In Sentry, find `outside_case.review`. Inspect `gen_ai.invoke_agent`, `gen_ai.chat`, and response validation spans. Keep a dashboard screenshot matched to the local receipt. Record wall-clock latency and retries; provider token counts are included only when returned. No dollar cost is fabricated for local inference.

For a real failure demonstration, stop the local model service while keeping the companion running, attempt a review, and inspect the failed trace and user-visible error. This outage is caught by the readiness check: its failed workflow trace contains `check_local_model`, no fabricated agent or chat invocation, and a receipt with `attempts: 0` and `failure_type: ModelUnavailable`. Restart the model afterward. Check that the clue was not accepted. A malformed response captured during real evaluation is another useful failure to discuss. Clearly distinguish software tests and controlled outages from model accuracy observations.

If no trace arrives, verify the DSN, project/time filter, connectivity and SDK configuration. A local trace ID alone proves no remote arrival. If narration fails, check voice access, credits and network; invalid/empty audio is rejected instead of saved.

## 4. Finish the submission

Run the labelled photo evaluation in `evaluation/README.md` and record the outdoor trial in `docs/FIELD-TRIAL.md`. Keep successful, unrelated, blurry and misleading-note cases; report uncertainty, false acceptances and latency honestly.

Replace pending sections in `docs/SUBMISSION.md` with actual results. Add a public video showing listening, phone pocketed, observations, narration playback, real model response and approximate visible app time. Include real Sentry screenshots and ElevenLabs playback/cache receipts. The hosted private walkthrough is not a public judge demo.

Export integration receipts after the reviews so they include those trace IDs. Inspect all selected evidence before publication. Keep private photos, runtime files and credentials out of Git; publish only the evidence you intend to share.

References: [challenge categories](https://dev.to/challenges/hacktoberfest-week1-2026-10-05), [ElevenLabs speech API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert), [Sentry Python agent monitoring](https://docs.sentry.io/platforms/python/tracing/instrumentation/ai-agents/).
