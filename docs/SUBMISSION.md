---
title: "Outside Case: a local Gemma mystery that asks you to put your phone away"
published: false
tags: devchallenge, hf26challenge, ai, opensource
main_image: https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/fj3cu220ilhlp0l18zic.webp
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05).*

## What I Built

Outside Case turns a familiar walk into a short detective mystery. I wanted a reason to look closely at ordinary things outside: a fallen leaf, a tree's bark, and the ground beneath it.

The first case, **The Missing Field Notes**, asks you to listen or read a chapter, pocket your phone, and make an observation. You return with a note and an optional photograph. Local Gemma reviews the evidence and selects a pattern that changes the fictional reconstruction.

A leaf with parallel veins suggests a ruled page in the story; branching veins suggest a connected record. Flaky bark points toward a layered archive. These are authored story meanings. The app does not identify species or generate walking routes.

Unclear evidence keeps a clue open. Players can also confirm their own observations, with those confirmations labelled separately from model reviews.

## Demo

**[Try the public player walkthrough](https://outside-case.arywk40.chatgpt.site).**

The walkthrough demonstrates the story and notebook. Gemma photo review runs through the local companion on your computer. The portable field kit supports collecting observations outside and reviewing them on the laptop afterward.

![Outside Case player walkthrough showing The Missing Field Notes](https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/z3purm4be4w6nmtntrfp.png)

*The public player walkthrough; local Gemma review runs in the companion.*

## Code

**[GitHub: arywk40-hue/pocket-quest](https://github.com/arywk40-hue/pocket-quest)**

I started this project on October 6, 2026. The source is MIT licensed; model weights and dependencies retain their own terms. Setup instructions, the evaluation runner, and tests are included in the repository.

## How I Built It

The browser app uses plain HTML, CSS, and JavaScript. Notes stay in browser storage and photos in IndexedDB. Journal export/import connects the phone workflow to a FastAPI companion.

The companion uses **Gemma 3 4B vision through local Ollama**. It normalizes photographs, strips EXIF, and requests structured output: a decision, summary, and allowed clue pattern. Accepted patterns select authored story passages. Invalid output gets one retry and then a visible failure. Editing or importing evidence clears earlier model review.

**Sentry** instruments the review workflow, including model readiness, agent invocation, model calls, validation, retries, and failures. Local receipts record trace IDs, outcomes, and timing. Request bodies and local variables are excluded, and default PII capture is disabled. The Sentry project is configured; remote dashboard verification is still pending.

**Verification:** 32 Python tests and 11 JavaScript/DOM tests pass. They check software behavior using mocked providers. A separate live Gemma smoke request rejected a synthetic blank white image as unrelated evidence, taking 38.6 seconds including initial loading. That demonstrates a real integration request, not field-photo accuracy.

An outdoor trial, real-photo evaluation, and native phone testing remain future verification work. I have not measured general model accuracy or claimed an outdoor test that has not happened.

## Why Does Open Innovation Matter?

The evidence reviewer runs on a computer the player controls. After downloading the weights, photographs and notes can stay with the local model rather than being sent to a hosted inference provider.

The prompts, allowed patterns, and story mapping are inspectable. I can change the model or prompts and evaluate them against labelled examples. This matters because an unrelated photo should not unlock a resolved clue.

Local inference still needs memory and compute. The downloaded phone field kit contains the story and notebook, not Gemma's weights. Sentry remains an optional hosted service for trace metadata.

## My Agent Session

I built this with Codex assistance and checked the implementation with automated tests. The cover is an AI-generated illustration, not a field photograph.

## Prize Categories

- **Best Use of Gemma:** local Gemma 3 4B vision reviews evidence that determines the story's branches.
- **Best Use of Sentry Agent Tracing — intended:** review instrumentation is implemented and the project is configured; remote trace verification remains pending.

What would you change to make a walk feel like a mystery while keeping the screen time short? I'd welcome questions and feedback in the comments.

Author: Ariyan Bhakat.
