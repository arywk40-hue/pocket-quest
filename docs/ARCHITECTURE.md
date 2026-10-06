# Architecture and trust boundaries

The browser holds the authored mystery, branching passages and final reconstruction. Progress uses localStorage; photos use IndexedDB. Export carries photos and notes; importing resets review status. The portable HTML embeds scripts, cover, progress and prepared narration. It contains no model weights.

The local FastAPI companion normalizes pixels and strips EXIF. In vision mode it sends image + note to local Gemma through Ollama or llama.cpp's OpenAI-compatible endpoint. In text mode only the note is sent; the result is never photo-accepted. A configured Gemma 2 vision mode is refused. An alias/mode is configuration, not a cryptographic proof of model capabilities.

The model returns status, summary and a pattern from the current clue's vocabulary. Unknown patterns, malformed responses and resolved patterns on rejected/uncertain evidence are refused. One retry is allowed. Pattern selection drives authored fictional passages; arbitrary model-generated instructions do not drive the story. Schema validity does not establish visual truth. Human-labelled held-out examples are needed to evaluate that boundary.

Final story reconstruction combines leaf (branching/fan/parallel), bark (ridged/flaky/smooth), and ground (covered/bare/similar). Every clue also has unclear. Manual selection remains player-confirmed. Text-only interpretation remains unverified until the player chooses to confirm it. Changed evidence clears prior interpretation; a review finishing after its evidence changes is discarded.

Optional ElevenLabs receives predefined scripts only. Audio is cached by voice/model/script digest and embedded in the portable kit. This cache avoids repeated generation calls; it does not remove the first call's cost.

Optional Sentry records agent/model/validation spans, correlation IDs, retry counts and token usage. Bodies and local variables are excluded; no summaries, photos, or notes are assigned to spans. The SDK's current gen_ai spans use its separate span transport. The test suite captures that transport in memory; remote project acceptance still needs a real account run.

Local receipts contain timing, IDs, mode, pattern and outcome. Private evaluation results include model summaries and image/note hashes. runtime/ is ignored. The hosted Site serves static player review only; it does not host the model or companion.
