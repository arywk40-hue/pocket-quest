---
title: "Outside Case: solve a mystery by noticing what is already outside"
published: false
tags: devchallenge, hf26challenge, ai, opensource
---

> Unpublished draft. Software checks pass. Live model evaluation, partner-account demonstrations, phone testing and real outdoor video remain pending. Fill the evidence gaps before publication.

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05).*

## What I Built

Outside Case turns a familiar walk into a short audio detective mystery. Its first case, **The Missing Field Notes**, begins with Mira's fictional notebook and a missing final page. Her clues ask you to look at a fallen leaf, a tree's bark, and two nearby patches of ground.

Listen, pocket the phone, and observe. There is no countdown and no generated route. You bring back a note and an optional photo.

What you observe changes the fictional reconstruction. Parallel leaf veins suggest a ruled page; branching veins suggest a connected record. Flaky bark suggests a layered archive; smooth bark casts doubt on the fictional witness. A ground comparison with no visible difference is a valid result, not a reason to invent one. These are story meanings, not botanical or historical claims.

Gemma selects a structured pattern; authored passages combine those patterns into the final page. Unclear evidence leaves the corresponding clue open. Player confirmations are labelled separately from model photo review.

## Demo

[Author's private walkthrough](https://outside-case.arywk40.chatgpt.site) — static player-review version. It is not currently judge-accessible and does not run the local integrations.

**Public video:** pending. The recording will show actual narration preparation, a phone being pocketed, outdoor clue collection, journal import and a real local model response, including a failure or uncertainty. No outdoor trial has yet been recorded.

## Code

**GitHub:** [arywk40-hue/pocket-quest](https://github.com/arywk40-hue/pocket-quest).

The new project's MIT source includes the browser mystery, FastAPI companion, constrained story branches, local model configuration, live evaluation runner, software tests, and an outdoor recording guide. Model weights and dependencies retain their own terms.

## How I Built It

The frontend uses plain HTML, CSS and JavaScript. Notes stay in browser storage and photographs in IndexedDB. A downloaded field kit includes transcripts, progress and any prepared audio. Export/import carries the notebook between the phone and the companion laptop. Import clears old model review so it is not treated as a fresh check.

The companion supports local Gemma through Ollama or llama.cpp. Vision mode normalizes the image, strips EXIF, and requests a status, summary and pattern. Only the clue's allowed patterns can select story passages. Invalid responses get one retry and then a visible failure. Prompting and JSON validation cannot prove a model's visual judgment is correct.

There is also an explicit Gemma 2 mode. Gemma 2 accepts text only, so that mode interprets written notes without receiving photographs. It never reports photographic acceptance. The documented default for photo review is Gemma 3 4B; a vision-capable Gemma 4 can also be configured.

ElevenLabs prepares predefined English/Hindi chapters, cached by script and voice. No player's notes or images go to that service. Sentry instruments agent invocation, model calls, validation and retries. Request bodies and local variables are excluded; correlation IDs connect local receipts to traces.

**Software verification:** 25 Python checks and 10 JavaScript/DOM checks pass. This includes distinct branches, text-mode boundaries, malformed response refusal, private receipts, offline kit execution, cached narration contracts and Sentry's in-memory span transport. These are software checks with mocked inference, not model accuracy or successful remote account tests.

## Why Does Open Innovation Matter?

Open weights and an open inference runtime let the evidence review run on a computer the player controls. After downloading the model, that step does not need a hosted inference account or send private photographs and notes to a remote model provider.

The prompts, pattern vocabulary and story mapping are inspectable. I can swap models and measure them using the same labelled cases. That matters here because accepting an unrelated photograph would weaken the entire game mechanic.

There are real limits: weights need an initial download, memory and compute are not free, and this field kit does not run a model inside a disconnected phone. The intended portable flow is to collect outside and review on the laptop afterward. Optional ElevenLabs and Sentry are hosted services. I have not yet demonstrated an offline model run or measured an advantage over a closed API.

## Taking It Outside

Pending actual results. Before publishing, replace this section with:

- Hardware, browser, model version/weight hashes and inference settings.
- Whether the portable kit opened and played prepared narration without connectivity.
- Actual walking duration and approximate visible app time.
- Human-labelled evaluation of valid, unrelated, blurry and misleading-note cases; report false acceptances, uncertainty, failures and latency.
- A specific observation that changed the fictional reconstruction, plus one thing that failed.

The cover is an AI-generated illustration, not a field photograph.

## My Agent Session

Built with Codex assistance. Add a genuine exported session link if available.

## Prize Categories

**Intended, pending demonstration:** Best Use of Gemma, Best Use of ElevenLabs, and Best Use of Sentry Agent Tracing. Claim only integrations actually run and evidenced in the final post.

Author: Ariyan Bhakat.
