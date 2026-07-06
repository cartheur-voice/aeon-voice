#!/usr/bin/env python3

"""Synthesize a WAV directly from a Piper training checkpoint."""

import argparse
import json
import wave
from pathlib import Path

import numpy as np
import torch

from piper.config import PiperConfig
from piper.phoneme_ids import phonemes_to_ids
from piper.phonemize_espeak import EspeakPhonemizer
from piper.train.vits.lightning import VitsModel

MAX_WAV_VALUE = 32767.0


def synthesize_sentence(
    model_g,
    phonemizer: EspeakPhonemizer,
    config: PiperConfig,
    text: str,
) -> np.ndarray:
    sentence_phonemes = phonemizer.phonemize(
        config.espeak_voice,
        text,
        vowel_clusters=config.vowel_clusters,
    )
    phoneme_ids = []
    for phonemes in sentence_phonemes:
        phoneme_ids.extend(phonemes_to_ids(phonemes, id_map=config.phoneme_id_map))

    text_tensor = torch.LongTensor(phoneme_ids).unsqueeze(0)
    text_lengths = torch.LongTensor([len(phoneme_ids)])

    audio = model_g.infer(
        text_tensor,
        text_lengths,
        noise_scale=config.noise_scale,
        length_scale=config.length_scale,
        noise_scale_w=config.noise_w_scale,
        sid=None,
    )[0]

    return audio.squeeze().detach().cpu().numpy()


def write_wav(path: Path, sample_rate: int, audio: np.ndarray) -> None:
    audio = np.clip(audio * MAX_WAV_VALUE, -MAX_WAV_VALUE, MAX_WAV_VALUE).astype(
        np.int16
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True, help="Path to Piper .ckpt file")
    parser.add_argument("--config", required=True, help="Path to Piper config JSON")
    parser.add_argument("--output", required=True, help="Path to output WAV")
    parser.add_argument("--text", required=True, help="Text to synthesize")
    args = parser.parse_args()

    config_dict = json.loads(Path(args.config).read_text(encoding="utf-8"))
    config = PiperConfig.from_dict(config_dict)

    model = VitsModel.load_from_checkpoint(args.checkpoint, map_location="cpu")
    model_g = model.model_g
    model_g.eval()

    with torch.no_grad():
        model_g.dec.remove_weight_norm()
        phonemizer = EspeakPhonemizer()
        audio = synthesize_sentence(model_g, phonemizer, config, args.text)

    write_wav(Path(args.output), config.sample_rate, audio)


if __name__ == "__main__":
    main()
