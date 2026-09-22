namespace AeonVoice;

/// <summary>Utilities for writing AeonVoice PCM16 output as WAV audio.</summary>
public static class WaveFile
{
    /// <summary>Writes mono, signed 16-bit PCM samples to a WAV file.</summary>
    public static void WriteWave(string path, SynthesisResult synthesis)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(path);
        ArgumentOutOfRangeException.ThrowIfLessThanOrEqual(synthesis.SampleRate, 0);
        ArgumentNullException.ThrowIfNull(synthesis.Samples);

        const int channels = 1;
        const int bitsPerSample = 16;
        const int bytesPerSample = bitsPerSample / 8;
        int dataLength = checked(synthesis.Samples.Length * bytesPerSample);
        int byteRate = checked(synthesis.SampleRate * channels * bytesPerSample);

        using var stream = new FileStream(path, FileMode.Create, FileAccess.Write, FileShare.None);
        using var writer = new BinaryWriter(stream);
        writer.Write("RIFF"u8.ToArray());
        writer.Write(checked(36 + dataLength));
        writer.Write("WAVE"u8.ToArray());
        writer.Write("fmt "u8.ToArray());
        writer.Write(16);
        writer.Write((short)1);
        writer.Write((short)channels);
        writer.Write(synthesis.SampleRate);
        writer.Write(byteRate);
        writer.Write((short)(channels * bytesPerSample));
        writer.Write((short)bitsPerSample);
        writer.Write("data"u8.ToArray());
        writer.Write(dataLength);

        foreach (short sample in synthesis.Samples)
        {
            writer.Write(sample);
        }
    }
}
