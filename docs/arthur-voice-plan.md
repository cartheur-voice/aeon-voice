# Arthur Voice Plan

## Goal

Create a usable voice for Arthur that is pleasant, youthful, playful, calm, and intentionally a blend of robotic and natural.

The goal is not maximum realism.
The goal is a characterful local voice that works well enough for robot interaction.

## Guiding Decision

Because Arthur does not require a perfectly polished human voice, we should optimize for:

- intelligibility
- fast iteration
- local/offline runtime
- consistent personality

This favors `HTS` for near-term delivery and keeps `Piper` as the longer-path experimental track.

## Track 1: HTS First

### Objective

Get the best quickly shippable Arthur voice from the existing engine on `main`.

### Work

- inspect current voice tuning controls and prompt/test paths
- define Arthur evaluation lines
- tune rate, phrasing, brightness, and pause behavior toward the Arthur profile
- compare multiple HTS variants by ear
- keep changes simple enough to ship without engine destabilization

### Success

- Arthur sounds clearly distinct from Leena
- the voice is pleasant and understandable
- the robotic/natural balance feels intentional

## Track 2: Piper In Parallel

### Objective

Keep the neural path alive, but use it as an experiment until it beats HTS by ear.

### Current State

- pipeline setup works
- dataset prep works
- checkpoint synthesis works
- the `10`-step sample is only a buzz
- ONNX export is currently blocked by Torch exporter compatibility

### Work

- keep direct checkpoint rendering available
- continue from the current checkpoint only when more CPU time is acceptable
- render checkpoint samples at larger intervals instead of chasing every small step
- replace the proxy speaker later with a better Arthur-matched source if the stack proves worthwhile

### Success

- a later checkpoint produces intelligible speech
- the resulting voice sounds more appealing than the HTS Arthur baseline

## Immediate Next Steps

1. Use the Arthur profile as the selection rule for all voice decisions.
2. Move short-term improvement work to the HTS path on `main`.
3. Preserve the current Piper branch as a reproducible experiment.
4. Only invest more CPU training time when we are specifically testing whether neural can beat the tuned HTS baseline.

## Evaluation Checklist

Arthur should sound:

- youthful, not childlike
- playful, not hyper
- calm, not flat
- robotic, but not harsh
- natural, but not fully human

## Decision Rule

If a tuned `HTS` Arthur voice is already pleasant and usable, ship that first.

If a later `Piper` checkpoint clearly sounds better by ear without unacceptable runtime complexity, then the neural path becomes worth promoting.
