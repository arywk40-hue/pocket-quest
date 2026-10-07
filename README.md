# Outside Case

**A familiar walk becomes a short detective mystery. The story is fictional; your observations are real.**

Listen to a chapter, pocket your phone, collect a leaf/bark/ground observation, and return with a notebook. Local Gemma interprets evidence into a constrained pattern. That pattern changes the fictional reveal and final reconstruction. For example, parallel leaf veins suggest a ruled page; branching veins suggest a connected record. Flaky bark suggests a layered archive; smooth bark casts doubt on the fictional witness. No species identification or generated navigation.

New project begun October 6, 2026 for the Hacktoberfest Week 1 **Touch Grass** challenge. Source: MIT; model weights and dependencies have their own terms.

## Clone and run

Use Python 3.12+ and install [Ollama](https://ollama.com/download). Clone the public source repository:

```bash
git clone https://github.com/arywk40-hue/pocket-quest.git
cd pocket-quest
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
ollama pull gemma3:4b
```

Keep Ollama running (the macOS app starts its service; CLI installations can run `ollama serve` in another terminal). Start the companion:

```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8787
```

Open **http://127.0.0.1:8787**. Settings identifies the connected model/mode. The default `.env` uses local Ollama at port 11434 and **Gemma 3 4B vision**. No OpenAI key is used. Initial model acquisition needs internet; keep the weights cached for local offline inference. Memory requirements and latency depend on your machine.

### If you mean Gemma 2

**Gemma 2 is text-only. It cannot review photos.** Use this honest note-interpretation mode:

```bash
ollama pull gemma2:2b
```

Set these lines in `.env`, then restart the companion:

```dotenv
MODEL_BASE_URL=http://127.0.0.1:11434
MODEL_NAME=gemma2:2b
MODEL_MODE=text
```

Gemma interprets your written note into a story branch; no photo is sent. Every result stays `uncertain` and is labelled **note interpretation, no photo review**. You may confirm your observation yourself. Do not report this as vision accuracy or AI photographic verification. A Gemma 2 model configured in vision mode is refused.

[Google's Gemma 2 model card](https://ai.google.dev/gemma/docs/core/model_card_2) documents text input. [Gemma vision documentation](https://ai.google.dev/gemma/docs/capabilities/vision) lists vision-capable variants; Gemma 3 1B is not a vision substitute.

### Gemma 4 or llama.cpp

For Ollama, use a downloaded vision-capable Gemma 4 model and its actual local model name from `ollama list`, with `MODEL_MODE=vision`. To use llama.cpp, start its multimodal server with your downloaded matching model and projector, then set `MODEL_BASE_URL=http://127.0.0.1:8080` and `MODEL_NAME` to its served alias. The adapter uses `/v1/models` and `/v1/chat/completions`; [Ollama documents that protocol](https://docs.ollama.com/api/openai-compatibility).

The mode and model name are declared configuration, not attestation of the loaded weights. Record actual model versions/hashes in your evaluation.

## What is implemented

- One authored case with three observation tasks and twelve constrained pattern outcomes, including uncertainty. The final interpretation combines all three clues.
- Local notebook, photos in IndexedDB, journal export/import, manual confirmation labelled separately.
- Downloadable single HTML field kit containing transcripts and any prepared narration.
- Local Gemma evidence adapter: image normalization and EXIF stripping, structured decisions, one retry, fail-closed errors. Schema checks constrain output; they do not establish that the model interpreted an image correctly.
- Optional ElevenLabs English/Hindi narration cached on disk and in browser storage, plus Sentry agent/model/validation spans.
- Real-run photo evaluation CLI; software tests and GitHub Actions workflow.

A rejected or uncertain photo cannot select a resolved branch. Text mode can suggest a branch from a note but cannot independently confirm it. Editing or importing evidence clears prior model review. Generated summaries are escaped before display. Story passages and final branches are authored, selected by the model's structured pattern rather than unrestricted model prose.

## Take it outside

Prepare narration if desired, then choose **Download field kit**. Test the file in your actual phone browser with connectivity disabled before leaving: phone file viewers vary. Collect observations along a familiar public path, export the journal and import it into the local companion afterward for review. Imported evidence is reset to pending.

**The portable field kit does not contain model weights and does not run Gemma on a disconnected phone.** This version supports collect outside / review on your laptop. Device speech may require installed voices; transcripts remain available. Visible app time excludes pocket mode and hidden-tab time; it is approximate app time, not OS-wide screen time. See [field trial](docs/FIELD-TRIAL.md) and [demo script](docs/DEMO-SCRIPT.md).

## Partner evidence

Follow [the partner setup and proof guide](docs/PARTNER-SETUP.md). Put `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`, and `SENTRY_DSN` in local `.env`, then restart the companion. Credentials stay on the companion computer.

Settings includes **Check connections**, **Send tracing check**, **Prepare audio for offline use**, and **Export integration receipts**. A voice lookup checks access without generating speech. A tracing check is labelled diagnostic; confirm its arrival in your Sentry dashboard. Neither is a substitute for a real model run.

With the companion running, collect real account checks and narration cache receipts:

```bash
python scripts/integration_check.py --prepare-audio --trace-check
```

First audio generation uses ElevenLabs credits. The command prepares three chapters twice and checks that the repeat uses the disk cache. It saves metadata in `runtime/integration-check.json`; it does not export audio, keys, photos or notes. Existing cached chapters require no new generation. Only predefined chapter scripts go to ElevenLabs.

Perform real Gemma reviews next. Sentry records agent invocation, model requests, response validation and failures. Local receipts include trace IDs, latency, outcomes and token counts when supplied by the model provider. Request bodies and local variables are excluded. Match a successful review and a real failure to dashboard traces before entering the tracing category.

```bash
python scripts/doctor.py
```

## Evaluate real photo reviews

Copy `evaluation/manifest.example.jsonl` to your private test manifest. Supply your own real photos and labels **before** testing. The example is a specification; no field photos or fabricated results are included. Include valid clues, unrelated objects, blurry views and misleading notes; expand it to at least 20 cases covering all clue types. Keep a held-out set after prompt tuning.

```bash
python scripts/evaluate.py evaluation/manifest.jsonl --out runtime/evaluation
```

The command checks the local vision model, calls the live API, records per-case results and image/note hashes, and writes `results.json` plus `report.md`. Reports contain false acceptances, false rejections, uncertainty, failures and p50/p95 request latency. Inspect private summaries before publishing. It refuses text mode and missing files. Record hardware, weight hashes, warm/cold state and label protocol separately. Small samples do not establish general accuracy.

## Software verification

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
npm ci
npm test
```

Node 24 is used for the DOM harness; running the app does not require Node. Tests mock model/provider contracts and cover branch selection, privacy, refusal and downloadable-kit execution. They are not real model evaluations.

## Submission status

Implementation and software checks are available. **Real model runs, ElevenLabs generation, remote Sentry traces, native phone testing and a filmed outdoor trial remain pending.** No model binary or provider credentials were available in this editing environment. Do those steps before claiming the partner categories. The hosted walkthrough supports player review only.

See [submission draft](docs/SUBMISSION.md), [architecture](docs/ARCHITECTURE.md), [evaluation protocol](evaluation/README.md), and [verification record](docs/TESTING.md).
