# Neural Voice Architecture Notes

## Intent

AeonVoice currently synthesizes through an HTS-style stack. The neural experiment should run in parallel with that system, not through a risky replacement of the existing voice packaging and synthesis path.

## Design Principles

1. Keep HTS voices working exactly as they do today.
2. Introduce neural synthesis behind a backend boundary.
3. Keep output expectations simple: text in, PCM audio out.
4. Make experimental voices explicit rather than silently swapping backends under the same voice id.

## Initial Target

The first neural experiment should target:

- language: English
- speaker style: female
- deployment style: local/offline
- voice id: likely `LeenaNeural` or another clearly experimental id

## Proposed Backend Shape

At a high level, the engine should eventually be able to choose between:

- `hts_backend`
- `neural_backend`

Each backend would be responsible for:

- loading its voice/model assets
- accepting text plus resolved synthesis options
- producing PCM samples

## Why a Parallel Backend

The current HTS assets are packaged as compiled acoustic model artifacts such as:

- `voice.data`
- `dur.pdf`
- `mgc.pdf`
- `lf0.pdf`
- `tree-*.inf`

A neural stack will not naturally emit or consume that format. Trying to force a neural model into the HTS artifact contract would create confusion and likely slow the experiment down.

## Suggested Integration Direction

### Near term

- document the boundary
- prepare the data
- choose one model stack

### Medium term

- add a synthesis backend interface in native code
- keep HTS as the default implementation
- add a neural prototype backend with config-driven model paths

### Late stage

- package experimental neural voice assets
- expose backend selection through config or voice metadata

## Voice Identity

For the first experiment, avoid changing `Leena` in place.

Prefer:

- `Leena` for the existing HTS voice
- `LeenaNeural` for the experimental path

This keeps A/B comparisons simple and prevents accidental regressions in existing consumers.

## Evaluation Strategy

The neural backend should be judged against the current Leena baseline using:

- identical prompts
- equalized output loudness where possible
- subjective listening notes
- basic runtime measurements such as startup latency and synthesis time

## Out Of Scope For Phase 1 And 2

- full engine refactor
- GPU deployment strategy
- mobile packaging
- replacing all English voices
- multi-speaker blending
