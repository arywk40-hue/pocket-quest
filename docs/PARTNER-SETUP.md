# Partner setup and submission proof

This connects real accounts. Automated software tests use mocks and do not establish successful account calls. The intended categories are Gemma and Sentry Agent Tracing. Complete the demonstrations before claiming them. ElevenLabs narration is optional and is not part of this submission plan.

## 1. Configure your companion

Follow the README's clone/install instructions. Edit local `.env`:

```dotenv
MODEL_BASE_URL=http://127.0.0.1:11434
MODEL_NAME=gemma3:4b
MODEL_MODE=vision
SENTRY_DSN=your_python_project_dsn
```

In Sentry, create/select a Python project and copy its DSN from the project setup. A DSN is not an account auth token. The companion initializes the Python SDK and custom agent/model spans; you do not need to enable a separate autonomous AI debugging product. Trace sampling is 100% for this small demo. Check your account usage before longer sessions.

Never commit `.env` or paste keys in a submission. Restart after changing it:

```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8787
```

Open http://127.0.0.1:8787. Settings distinguishes configured connections from verified results. Photos and notes stay on your machine/local model; only predefined narration text goes to ElevenLabs. Sentry receives timing, outcome and model metadata, with request bodies and local variables excluded.

## 2. Check Sentry and collect receipts

In another terminal with the same virtual environment:

```bash
python scripts/integration_check.py --trace-check
```

The script saves `runtime/integration-check.json`. Its diagnostic event/trace IDs mean the SDK attempted delivery, not that Sentry accepted it. Find those IDs in your dashboard. The diagnostic has no invented model span and does not qualify as a model run.

Download the field kit and open it on the actual phone with connectivity disabled. Check transcripts, device speech if available, journal export and photo capture. Report the phone/browser and any file-viewer limitations. The field kit does not contain Gemma weights.

If you later choose to demonstrate ElevenLabs, configure its key and voice ID in `.env` and run `python scripts/integration_check.py --prepare-audio`. First generation consumes account credits; repeats should use cached chapters. Prepare audio in Settings too, because the CLI does not populate browser storage. Keep this optional demonstration separate from the Gemma and Sentry category claims.

## 3. Demonstrate actual Gemma agent traces

Collect a real clue photo, import your field journal into the companion, and select **Review photo with Gemma**. Different accepted patterns must visibly change the authored mystery. Copy the review's trace ID from exported integration receipts or `runtime/review-receipts.jsonl`.

In Sentry, find `outside_case.review`. Inspect `gen_ai.invoke_agent`, `gen_ai.chat`, and response validation spans. Keep a dashboard screenshot matched to the local receipt. Record wall-clock latency and retries; provider token counts are included only when returned. No dollar cost is fabricated for local inference.

For a real failure demonstration, stop the local model service while keeping the companion running, attempt a review, and inspect the failed trace and user-visible error. This outage is caught by the readiness check: its failed workflow trace contains `check_local_model`, no fabricated agent or chat invocation, and a receipt with `attempts: 0` and `failure_type: ModelUnavailable`. Restart the model afterward. Check that the clue was not accepted. A malformed response captured during real evaluation is another useful failure to discuss. Clearly distinguish software tests and controlled outages from model accuracy observations.

If no trace arrives, verify the DSN, project/time filter, connectivity and SDK configuration. A local trace ID alone proves no remote arrival.

## 4. Finish the submission

Run the labelled photo evaluation in `evaluation/README.md` and record the outdoor trial in `docs/FIELD-TRIAL.md`. Keep successful, unrelated, blurry and misleading-note cases; report uncertainty, false acceptances and latency honestly.

Replace pending sections in `docs/SUBMISSION.md` with actual results. The [public player walkthrough](https://outside-case.arywk40.chatgpt.site) demonstrates the browser story. Add an outdoor video showing listening, phone pocketed, observations, real model response and approximate visible app time if available. Include real Sentry screenshots for the tracing category. The hosted walkthrough does not run the local integrations.

Export integration receipts after the reviews so they include those trace IDs. Inspect all selected evidence before publication. Keep private photos, runtime files and credentials out of Git; publish only the evidence you intend to share.

References: [challenge categories](https://dev.to/challenges/hacktoberfest-week1-2026-10-05), [ElevenLabs speech API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert), [Sentry Python agent monitoring](https://docs.sentry.io/platforms/python/tracing/instrumentation/ai-agents/).
