# Neural voice-training track

This track replaces the unavailable HTK/HTS training dependency with a modern
neural TTS workflow.  It does not change the existing AeonVoice runtime or
pretend that a neural checkpoint can be packaged as an HTS `voice.data` file.
Runtime integration is a later, separate decision.

## Dataset contract

`export_nemo_manifest.py` produces standard JSONL manifests with one utterance
per line.  Each entry contains a WAV path relative to `corpus/wav/`, its
transcript, duration, language, and speaker ID.  This matches the dataset
shape used by NVIDIA NeMo TTS tools.

Generate the manifests from the repository root:

```bash
python3 voices/custom/male-natural/neural/export_nemo_manifest.py \
  --audio-root voices/custom/male-natural/corpus/wav \
  --metadata voices/custom/male-natural/corpus/metadata.psv \
  --evaluation-ids voices/custom/male-natural/corpus/evaluation-ids.txt \
  --output-dir voices/custom/male-natural/neural/manifests
```

The master `batch-xx.wav` files are never included because they have no
utterance ID in `metadata.psv`.

## Candidate training runtime

NVIDIA NeMo is the initial candidate because its current Magpie-TTS workflow
supports speaker adaptation from manifest-based datasets.  Its model checkpoint
and dataset terms must be reviewed before downloading or training.  Start with
the manifests only; they remain useful if another neural runtime is selected.

The present corpus is a 120-clip, roughly five-minute pipeline pilot.  It is
not enough to judge a custom neural voice fairly.  Continue recording toward
the existing 1,200-utterance target while the training environment is prepared.
