# Verification record — 7 October 2026

Python 3.12.14 / Node 24.19.0. Declared dependencies are pinned in requirements files; Node dependencies use package-lock.json.

- 32 Python tests: bounded image inputs, local API boundaries, structured outcomes, retries, pattern-specific branches, Gemma 2 mode refusal/labels, private receipts, evaluation failure accounting, cached ElevenLabs request contracts, Sentry in-memory transaction and gen_ai span transport, provider failure handling, voice access checks, diagnostic refusal without a DSN, and private evidence exports.
- 11 JavaScript/DOM tests: state restoration, escaping, uncertainty, different final reconstructions, player-selected patterns, field-kit generation/execution, optional simulated WebMCP.
- JS syntax and Python compilation checks.

Provider/model calls in these tests are mocked. Sentry spans are captured in memory with a dummy DSN; no remote event was sent. Contract audio bytes are not playable narration. A Starlette test-client deprecation warning remains.

The original software-verification environment contained no model binary or provider credentials. Native mobile file handling, camera, offline speech/playback, layout, keyboard and screen-reader testing remain pending. DOM tests do not measure layout. runtime/ is private and ignored; the example manifest intentionally contains no photos.

## Local Gemma smoke check — 6 October 2026

Python 3.13.0 / Node 22.23.2 on Apple M1. At that time, **26 Python tests and 10 JavaScript/DOM tests passed**. The subsequent integration update expanded this to 32 Python and 11 JavaScript/DOM checks, as recorded above. The Starlette test-client deprecation warning remains.

All seven Ollama manifests have their referenced blobs present with matching declared file sizes; this is not a cryptographic integrity check. Ollama 0.35.1 reports vision capability for the configured `gemma3:4b`, manifest ID `a2af6cc3eb7f`, Q4_K_M. Chrome Settings shows local Gemma photo review available, with ElevenLabs and Sentry disconnected.

A real request through `/api/review` sent a **synthetic blank white image**, explicitly labelled as a test, to local Gemma. The API returned HTTP 200, `status=rejected`, `pattern=unclear`, and a summary explaining that no leaf was visible. End-to-end latency was 38.6 seconds, including first model loading. The private result is in `runtime/live-smoke.json`, with a corresponding review receipt. This checks real integration, not outdoor-photo accuracy or general model performance. Real-photo evaluation, provider-account demonstrations, and outdoor recording remain pending.
