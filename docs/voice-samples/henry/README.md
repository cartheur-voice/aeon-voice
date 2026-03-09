# Henry Voice Samples

These are warm voice samples for the first toy character, **Henry**.

## Files

Female:
- `docs/voice-samples/henry/henry-warm-gentle-helen.wav`
- `docs/voice-samples/henry/henry-warm-gentle-leena.wav`
- `docs/voice-samples/henry/henry-warm-storytime-helen.wav`
- `docs/voice-samples/henry/henry-warm-sleepy-daria.wav`

Male:
- `docs/voice-samples/henry/henry-warm-gentle-alan.wav`
- `docs/voice-samples/henry/henry-warm-storytime-ksp.wav`
- `docs/voice-samples/henry/henry-warm-sleepy-evgeniy-eng.wav`

## Settings Used

- `henry-warm-gentle-helen.wav`
  - profile: `Helen`
  - rate: `92`
  - pitch: `95`
  - volume: `108`
- `henry-warm-storytime-helen.wav`
  - profile: `Helen`
  - rate: `88`
  - pitch: `93`
  - volume: `110`
- `henry-warm-gentle-leena.wav`
  - profile: `Leena`
  - rate: `90`
  - pitch: `94`
  - volume: `108`
- `henry-warm-sleepy-daria.wav`
  - profile: `Daria`
  - rate: `86`
  - pitch: `92`
  - volume: `106`
- `henry-warm-gentle-alan.wav`
  - profile: `Alan`
  - rate: `90`
  - pitch: `92`
  - volume: `108`
- `henry-warm-storytime-ksp.wav`
  - profile: `Ksp`
  - rate: `88`
  - pitch: `90`
  - volume: `110`
- `henry-warm-sleepy-evgeniy-eng.wav`
  - profile: `Evgeniy-Eng`
  - rate: `86`
  - pitch: `90`
  - volume: `106`

## Reuse In Another Codebase

1. Copy the WAV files from `docs/voice-samples/henry/`.
2. Keep the same synthesis settings above if you want to regenerate with the same tone.
3. For runtime synthesis, use this command pattern:

```bash
echo "Your text here" | AeonVoice-test -p <Profile> -r <Rate> -t <Pitch> -v <Volume> -o output.wav
```

Environment used in this repo:

```bash
AEONVOICE_DATA_PATH=<repo>/data
LD_LIBRARY_PATH=<repo>/build/linux/core:<repo>/build/linux/audio:<repo>/build/linux/lib
```
