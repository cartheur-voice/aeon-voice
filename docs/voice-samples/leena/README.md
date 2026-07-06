# Leena Audition Set

This folder holds the only listening samples that proved useful in the Leena naturalness investigation.

Files:

- `leena-midpoint.txt`: the exact input text used for `leena-midpoint.wav`
- `leena-midpoint.wav`: halfway step between baseline and tuned defaults
- `leena-i-uppercase.wav`: focused check for the pronoun `I`
- `leena-i-lowercase.wav`: lowercase control sample for the same phrase

To regenerate:

```bash
PYTHONPATH=/tmp/aeonvoice-pydeps python3 -m SCons -j2
./scripts/render-leena-audition.sh
```

The midpoint sample remains the best wrapper-side reference.
The `I` pair remains useful as a diagnostic proving capitalization is not the source of the observed rise.
