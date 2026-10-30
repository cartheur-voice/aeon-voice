# Female Natural: custom-voice starter

This corpus belongs to a different performer from `../male-natural/`.  Keep
their recordings, metadata, consent records, train/evaluation splits, and
resulting trained models separate.  Combining two speakers in a single
single-speaker HTS corpus would blur the voice identity rather than improve it.

`corpus/wav/female-01.wav` is the untouched multi-prompt source recording.
It has been verified as 24 kHz, mono, 16-bit PCM WAV.  The recording contains
natural long pauses, so split it against the written prompt sequence and
listen to every boundary before accepting clips.  Do not use simple silence
splitting alone.

Use the same prompt text as the first corpus:
[`../male-natural/prompts/seed.psv`](../male-natural/prompts/seed.psv).
For each accepted clip, create a separate WAV in `corpus/wav/` and write the
matching `id|transcript` row to `corpus/metadata.psv`.  The technical checker
is shared too:

```bash
python3 ../male-natural/tools/validate_corpus.py \
  --wav-dir corpus/wav \
  --metadata corpus/metadata.psv
```

Do not add the multi-prompt source file to `metadata.psv`; only segmented
utterances belong in a trainable corpus.
