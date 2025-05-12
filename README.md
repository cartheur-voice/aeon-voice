# aeon-voice

The voice of artificial animals.

## Background

This project has been laboring under an 8-bit voice that was fit-for-purpose but now we want to move beyond.

This repo is all about this evolution.

## The theory

There were two constructs we wanted to employ for this feature:

1. The simplest yet powerful speech synthesis,
2. Voices based on actual speakers and not AI.

For the former, the selection was to leverage the [statistical parametric synthesis](https://en.wikipedia.org/wiki/Speech_synthesis#HMM-based_synthesis) model in the context of [HTS](https://hts.sp.nitech.ac.jp).

Voices are built from recordings of natural speech, as such they have small footprints since the statistical models are stored on the Aeon hardware. Although it could be argued the
voices lack the naturalness of the synthesizers - as a matter of speech generation by combining segments of the recordings themselves - these are still intelligible and resemble the speakers who recorded the source material, which is the point to bring _humanness_ to our artificial animals as [emotional](https://emotional.toys) toys.

## Building the code


