# Neural Voice Plan

## Goal

Explore a neural voice path for Leena without destabilizing the existing HTS-based AeonVoice engine.

This branch is for an experimental track, not an immediate engine rewrite.

## Success Criteria

The first experiment is successful if it gives us:

1. A reproducible single-speaker training subset derived from the Libre English corpus.
2. A documented parallel architecture for HTS-backed and neural-backed voices.
3. A first neural voice prototype that can be compared against current Leena on the same prompts.

## Constraints

- The existing HTS pipeline remains the production baseline.
- Current voices must continue to work unchanged.
- The first neural experiment is English, female, offline, and local-only.
- We prefer a single-speaker corpus before attempting style transfer or multi-speaker adaptation.

## Phases

### Phase 1: Define target and architecture

- Keep HTS as the stable fallback.
- Add a parallel neural backend rather than replacing the engine internals up front.
- Define one experimental neural voice target, likely `LeenaNeural`.
- Keep the public synthesis contract focused on PCM output so backend switching is easier.

Deliverables:

- `docs/neural-voice-plan.md`
- `docs/neural-voice-architecture.md`

### Phase 2: Prepare experimental data

- Inspect Libre English manifests and identify one strong female speaker subset.
- Export that subset into a deterministic single-speaker workspace.
- Convert FLAC to mono WAV at `24000` Hz.
- Produce transcript files and held-out eval prompts.

Deliverables:

- `scripts/prepare-libre-english-subset.py`
- exported corpus under a user-chosen workspace directory

### Phase 3: Choose neural stack

- Select one practical training stack for single-speaker fine-tuning.
- Select one inference/runtime format that can be wrapped locally.
- Avoid coupling the model format to the old HTS asset layout.

### Phase 3 Decision

The chosen first stack for this branch is **Piper**.

More specifically:

- training/inference family: `Piper`
- implementation target: the active Open Home Foundation continuation, `OHF-Voice/piper1-gpl`
- deployment direction: local/offline inference
- export direction: Piper-native deployment artifacts, with ONNX-capable export supported by the Piper training flow

### Why Piper

Piper matches this branch better than the alternatives because:

- it is explicitly designed for fast, local TTS
- it has a documented training flow for new voices
- its dataset format is already very close to the corpus shape we generated
- it has a C/C++ API story that is easier to imagine alongside AeonVoice than a Python-only runtime

### Why Not The Others First

Coqui TTS remains useful for future experiments, but it is a broader toolkit than we need for the first end-to-end pipeline proof.

NeMo remains attractive for larger-scale model experimentation, but it is heavier than necessary for the current pilot goal.

### Phase 4: Integrate runtime prototype

- Add a backend abstraction for synthesis.
- Leave the HTS backend untouched.
- Introduce a neural backend stub and experimental voice registration path.

### Phase 5: Train and compare

- Train a first-pass neural voice on the prepared subset.
- Render the same prompts used for Leena evaluation.
- Compare naturalness, intelligibility, latency, and footprint.

### Phase 6: Productize only if it wins

- Define packaging conventions for neural assets.
- Document runtime requirements.
- Decide whether neural voices are optional, experimental, or default.

## Immediate Work

This branch starts with:

1. Recording the plan and architecture.
2. Building a reproducible Libre English subset prep flow.
3. Deferring engine-side neural runtime work until the data path is solid.

## Current Assumptions

- Libre English is valuable as source material, but should not be mixed across many speakers for one first-pass voice.
- The first best experiment is a single speaker plus a clean evaluation set.
- We will compare against Leena, not overwrite Leena immediately.

## Current Reality

For forward progress, this branch is currently using a **proxy single-speaker corpus** to validate the workflow, not a verified final Leena source voice.

That means:

- the prep pipeline work is real
- the pilot workspace is real
- the source speaker identity can still be swapped later
- any early training result from this corpus should be treated as an integration/prototyping checkpoint, not a final Leena voice candidate

## Initial Corpus Scan

Using `scripts/prepare-libre-english-subset.py list-subsets`, the largest clean training subsets currently visible in the downloaded corpus are:

- `6097_clean/13657` with about `6.36` hours
- `6097_clean/14411` with about `5.98` hours
- `6097_clean/14843` with about `4.40` hours

These are strong first candidates for a pilot export and listening pass.

## Active Pilot Source

The current branch pilot uses:

- subset: `6097_clean/13657`
- extracted source root: `work/leena-neural-source/hi_fi_tts_v0/`
- pilot workspace: `work/leena-neural-pilot/`
- pilot export: `500` clips, split into `475` train and `25` eval

This choice is provisional and may be replaced later without changing the surrounding prep flow.
