# Neural Pilot QA

## Scope

This note records a lightweight QA pass over the current pilot corpus:

- source subset: `6097_clean/13657`
- pilot workspace: `work/leena-neural-pilot/`

## Integrity Checks

The pilot passed the basic file-level checks:

- `500` WAV files present
- `500` transcript rows in `text.csv`
- `500` metadata rows in `metadata.csv`
- no missing WAVs
- no zero-length WAVs
- no empty transcripts
- no ID mismatches between text and metadata

## Audio Format

All pilot WAV files are consistent:

- sample rate: `24000`
- channels: `1`
- sample width: `16-bit PCM` (`2` bytes)

No malformed WAV files were detected in the pass.

## Duration Profile

The exported duration range is sensible for a first-pass training corpus:

- min: `1.03s`
- max: `9.32s`
- mean: `2.952s`
- median: `2.56s`

## Transcript Profile

The normalized transcript set is structurally usable, with these broad characteristics:

- mean words per clip: `9.26`
- median words per clip: `8`
- mean characters per clip: `47.35`
- median characters per clip: `42`

Observed style quirks:

- many lines are lowercase due to normalized text
- punctuation is common, especially semicolons and colons
- the material is narrational/book-style rather than assistant-dialogue style

These are not blockers for pipeline validation, but they will shape prosody and voice behavior in early training results.

## Spot Check

Representative transcripts from the pack look coherent and aligned with the exported durations:

- `000001` `8.50s`: "ONCE upon a time amidst the mountains and hills and falling streams of a fair land there was a town or thorp in a certain valley."
- `000025` `1.90s`: "there were other waters in the Dale."
- `000100` `2.88s`: "and were very mindful of the old story-lays,"
- `000250` `2.82s`: "nor yesterday a thing which they would fain forget:"
- `000500` `1.56s`: "and all men drank,"

## Conclusion

The current pilot corpus is good enough for:

- first neural training experiments
- backend integration work
- pipeline validation

It is not yet a guarantee of the final LeenaNeural voice identity or speaking style.
