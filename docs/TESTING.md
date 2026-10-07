# Verification record — 7 October 2026

Python 3.12.14 / Node 24.19.0. Declared dependencies are pinned in requirements files; Node dependencies use package-lock.json.

- 32 Python tests: bounded image inputs, local API boundaries, structured outcomes, retries, pattern-specific branches, Gemma 2 mode refusal/labels, private receipts, evaluation failure accounting, cached ElevenLabs request contracts, Sentry in-memory transaction and gen_ai span transport, provider failure handling, voice access checks, diagnostic refusal without a DSN, and private evidence exports.
- 11 JavaScript/DOM tests: state restoration, escaping, uncertainty, different final reconstructions, player-selected patterns, field-kit generation/execution, optional simulated WebMCP.
- JS syntax and Python compilation checks.

Provider/model calls in these tests are mocked. Sentry spans are captured in memory with a dummy DSN; no remote event was sent. Contract audio bytes are not playable narration. A Starlette test-client deprecation warning remains.

No real model binary, provider credentials, actual model evaluation or outdoor recording is present. Native mobile file handling, camera, offline speech/playback, layout, keyboard and screen-reader testing remain pending. DOM tests do not measure layout. runtime/ is private and ignored; the example manifest intentionally contains no photos.
