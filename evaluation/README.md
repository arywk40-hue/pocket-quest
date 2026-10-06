# Live evaluation protocol

1. Capture your own photos: each clue should have clear relevant views, unrelated objects and ambiguous/blurry views. Add misleading notes to unrelated photos and contradicted notes to relevant photos. The label concerns the photo AND note, not whether a plant looks plausible.
2. Have a human label each expected decision before any model output is seen. A second reviewer and recorded disagreements improve the evidence. Ground comparisons should show both patches; photos do not prove moisture or temperature.
3. Freeze the JSONL manifest. Each line needs a unique id, clue_id, group, expected, image path relative to the manifest, and note. Use group valid/unrelated/blurry/misleading_note and expected accepted/uncertain/rejected.
4. Run the live command in README. It records the manifest hash and per-image/note hashes. Preserve your labelled source separately; the public source contains no field photos.
5. Report every case, including request failures. The false acceptance denominator is all cases labelled rejected OR uncertain. Failures have no decision; report their count alongside that rate. Report false rejection among expected accepted cases separately from positive cases that become uncertain.
6. Measure cold startup separately. p50/p95 here cover end-to-end review requests, including status checks, queueing and retries. Record hardware and model version/weight hashes.
7. Prompt changes invalidate a claim that the same set was held out. Keep a second frozen set for final results. This sample is a project demonstration, not a scientific accuracy estimate.

Text-only Gemma 2 runs may be compared for note interpretation, but the photo evaluation command intentionally refuses them. No measured model results have been supplied yet.
