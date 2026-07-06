# Neural Training Handoff

## Date

- `2026-07-06`

## Current Status

The first `Piper` pilot training run completed successfully on CPU.

It was a short smoke-test run to prove that the end-to-end stack works on this machine with the current pilot corpus.

## Active Inputs

- training stack: `OHF-Voice/piper1-gpl`
- Python venv: `work/piper1-gpl/src/python/.venv`
- corpus root: `work/piper-leena-pilot/`
- metadata file: `work/piper-leena-pilot/metadata_piper.csv`
- audio directory: `work/piper-leena-pilot/wav`
- espeak voice: `en-us`
- sample rate: `24000`

## Completed Training Run

The completed run used:

```bash
python -m piper.train fit \
  --trainer.accelerator cpu \
  --trainer.devices 1 \
  --trainer.max_steps 10 \
  --trainer.limit_val_batches 1 \
  --trainer.log_every_n_steps 1 \
  --trainer.default_root_dir work/piper-runs/leena-pilot \
  --model.sample_rate 24000 \
  --data.voice_name leena-pilot \
  --data.csv_path work/piper-leena-pilot/metadata_piper.csv \
  --data.audio_dir work/piper-leena-pilot/wav \
  --data.espeak_voice en-us \
  --data.cache_dir work/piper-cache/leena-pilot \
  --data.config_path work/piper-runs/leena-pilot/leena-pilot-config.json \
  --data.batch_size 4 \
  --data.validation_split 0.05 \
  --data.num_test_examples 5 \
  --data.num_workers 0
```

The run stopped cleanly at:

- `max_steps=10`

## Produced Artifacts

- config: `work/piper-runs/leena-pilot/leena-pilot-config.json`
- checkpoint: `work/piper-runs/leena-pilot/lightning_logs/version_0/checkpoints/epoch=0-step=10.ckpt`
- Lightning config: `work/piper-runs/leena-pilot/lightning_logs/version_0/config.yaml`
- hyperparameters: `work/piper-runs/leena-pilot/lightning_logs/version_0/hparams.yaml`
- TensorBoard events: `work/piper-runs/leena-pilot/lightning_logs/version_0/events.out.tfevents.*`
- feature/cache outputs: `work/piper-cache/leena-pilot/`

## Machine Context

The current machine reports:

- CPU: `AMD Ryzen 9 5950X 16-Core Processor`
- logical CPUs: `32`
- current training mode: CPU only

## Working Time Estimate

These are planning estimates for this machine and this pipeline, not guaranteed runtimes:

- `10` steps: minutes
- `100` steps: about `30` to `90` minutes
- `1,000` steps: about `5` to `12` hours
- `10,000` steps: about `2` to `7` days

For this stack, a checkpoint starts becoming useful for rough evaluation in the low thousands of steps, while better quality will usually require significantly more.

## Recommended Next Step

Resume from the existing checkpoint and run a longer continuation, ideally at least `100` steps first to get a better machine-specific timing read.

Checkpoint to resume from:

- `work/piper-runs/leena-pilot/lightning_logs/version_0/checkpoints/epoch=0-step=10.ckpt`

## Notes

- The current pilot corpus is a proxy source voice, not the intended final Leena voice.
- `work/` is ignored by git, so training artifacts are local-only unless explicitly exported.
- There is also a local untracked `_skbuild/` build artifact in the repo root from the earlier native extension build.
