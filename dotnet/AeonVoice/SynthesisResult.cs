namespace AeonVoice;

public readonly record struct SynthesisResult(int SampleRate, short[] Samples)
{
    /// <summary>Writes this mono PCM16 synthesis result as a standard WAV file.</summary>
    public void WriteWave(string path) => WaveFile.WriteWave(path, this);
}
