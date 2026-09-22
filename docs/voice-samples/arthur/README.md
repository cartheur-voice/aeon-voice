# Arthur Voice Samples

These are `HTS` baseline samples for Arthur on `main`.

The target character is:

- male
- youthful
- playful
- calm
- partly robotic
- partly natural

These samples are not the final answer.
They are meant to identify which existing male English voice is the best starting point for Arthur packaging work.

## Current Baseline Decision

`Toptygin` is the chosen first baseline for Arthur on `main`.

`arthur-steady-toptygin.wav` is the chosen direction inside the Toptygin set.

That means:

- `arthur-steady-toptygin.wav` is the primary Arthur reference
- the other Toptygin samples are comparison and tuning history
- the next tuning pass should focus on refining `Toptygin` toward the Arthur profile

After the first pass, the two Toptygin variants sounded too similar.
The second pass therefore uses larger tuning jumps so the character differences are easier to hear.

## Evaluation Text

All samples currently use:

```text
Hello, I am Arthur. I am glad to meet you. We can explore together, one small step at a time.
```

## Files

- `docs/voice-samples/arthur/arthur-bright-toptygin.wav`
- `docs/voice-samples/arthur/arthur-calm-toptygin.wav`
- `docs/voice-samples/arthur/arthur-quick-toptygin.wav`
- `docs/voice-samples/arthur/arthur-steady-toptygin.wav`
- `docs/voice-samples/arthur/arthur-robot-toptygin.wav`

## Settings Used

- `arthur-bright-toptygin.wav`
  - profile: `Toptygin`
  - rate: `102`
  - pitch: `108`
  - volume: `104`
- `arthur-calm-toptygin.wav`
  - profile: `Toptygin`
  - rate: `98`
  - pitch: `104`
  - volume: `105`
- `arthur-quick-toptygin.wav`
  - profile: `Toptygin`
  - rate: `112`
  - pitch: `116`
  - volume: `102`
- `arthur-steady-toptygin.wav`
  - profile: `Toptygin`
  - rate: `90`
  - pitch: `98`
  - volume: `106`
- `arthur-robot-toptygin.wav`
  - profile: `Toptygin`
  - rate: `106`
  - pitch: `112`
  - volume: `100`

## Why These Settings

The settings bias Arthur toward:

- a lighter and younger tone than the warm male Henry samples
- slightly quicker pacing
- clear articulation
- enough synthetic edge to still feel like a robot

## Next Step

Next session should start from `arthur-steady-toptygin.wav` and move from sample selection into package preparation.

Current outcome:

1. base voice chosen: `Toptygin`
2. first-pass observation: `bright` and `calm` were too similar
3. chosen second-pass direction: `steady`

Recommended next-session tasks:

1. clone the `Toptygin` baseline into an Arthur-specific package direction
2. decide whether Arthur needs one more small tuning pass around the steady settings
3. define the package shape the robot software will consume
4. keep the output suitable for public reuse by other projects

## Regeneration

Environment used in this repo:

```bash
export AEONVOICE_DATA_PATH="$(pwd)/data"
export LD_LIBRARY_PATH="$(pwd)/build/linux/core:$(pwd)/build/linux/audio:$(pwd)/build/linux/lib"
```

Command pattern:

```bash
echo "Your text here" | build/linux/test/AeonVoice-test -p <Profile> -r <Rate> -t <Pitch> -v <Volume> -o output.wav
```
