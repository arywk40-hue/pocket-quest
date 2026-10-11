# Local models and partner setup — 6 October 2026

The downloaded Ollama models were inspected on this Mac. Ollama 0.35.1 reports Apple M1 / Metal. The companion is configured in the private, ignored `.env` for `gemma3:4b` at `http://127.0.0.1:11434`, in vision mode.

| Downloaded model | Size | Reported capability | Role for this project |
| --- | --- | --- | --- |
| `gemma3:4b` | 3.3 GB | Text and vision | Configured evidence reviewer; Gemma category |
| `gemma3:1b` | 815 MB | Text only | Possible note interpretation with `MODEL_MODE=text` |
| `qwen2.5vl:3b` | 3.2 GB | Text and vision | Available for future comparisons; current adapter requires Gemma |
| `glm-ocr:q8_0` | 1.6 GB | Text, vision, tools | Available for OCR experiments; current adapter requires Gemma |
| `qwen2.5:1.5b` | 986 MB | Text | Available text baseline; current adapter requires Gemma |
| `qwen2.5:3b` | 1.9 GB | Text | Available text baseline; current adapter requires Gemma |
| `nomic-embed-text:latest` | 274 MB | Embeddings | Retrieval experiments; cannot review evidence |

Configured Gemma manifest ID: `a2af6cc3eb7f`; reported quantization `Q4_K_M`, 4.3B parameters. All referenced blob files exist and match their declared sizes. A live synthetic blank-image review returned a structured rejection in 38.6 seconds including initial loading. Inventory, declared capabilities, and this smoke check do not establish photo accuracy. See [verification record](TESTING.md).

## Start the local app

From the project directory, keep Ollama running and start the companion:

```bash
ollama serve
```

In another terminal:

```bash
.venv/bin/python -m uvicorn backend.app:app --host 127.0.0.1 --port 8787
```

Open <http://127.0.0.1:8787>. Check configuration without revealing credentials or generating paid audio:

```bash
.venv/bin/python scripts/doctor.py
```

## Categories already selected

The submission draft lists three intended categories. The [Week 1 challenge page](https://dev.to/challenges/hacktoberfest-week1-2026-10-05) includes all three.

| Category | Configuration | Evidence still required |
| --- | --- | --- |
| Best Use of Gemma | Local `gemma3:4b` vision model | Real field photos, prelabelled evaluation, successful and uncertain/failed examples |
| Best Use of ElevenLabs | Add `ELEVENLABS_API_KEY` and `ELEVENLABS_VOICE_ID` to `.env` | Prepare English/Hindi narration in Settings, check playback, retain actual account receipt |
| Best Use of Sentry Agent Tracing | Add `SENTRY_DSN` to `.env` | Run a review and error case; inspect remote agent/model/validation spans and retain trace screenshots |

Get an ElevenLabs API key from the account dashboard and a voice ID from the chosen voice. Get the Sentry DSN from a Python project's **Settings → Client Keys (DSN)**. Keep these values in `.env`, then restart the companion. The voice ID is an identifier; the API key is a secret. Do not put either provider's credentials in browser code or submission attachments.

Partner credits are linked from the challenge page at <https://hacktoberfest.com/my/promos>. A configured credential does not demonstrate a successful integration.

## Week 2 timing

As checked on October 6, the [Week 2 page](https://dev.to/challenges/hacktoberfest-week2-2026-10-12) lists October 12–18 and has not revealed a theme or category list. The challenge FAQ requires each project and repository to start and finish during its own window. This October 6 project remains a Week 1 project. Check the Week 2 announcement before starting a separate entry; do not represent this existing project as a new Week 2 build.
