namespace AeonVoice;

public readonly record struct SynthesisResult(int SampleRate, short[] Samples);
