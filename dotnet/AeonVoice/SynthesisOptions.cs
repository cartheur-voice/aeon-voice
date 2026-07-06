namespace AeonVoice;

public sealed class SynthesisOptions
{
    public double RelativeRate { get; init; } = 1.0;

    public double RelativePitch { get; init; } = 1.0;

    public double RelativeVolume { get; init; } = 1.0;

    internal void Validate()
    {
        if (RelativeRate <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(RelativeRate), "Relative rate must be greater than zero.");
        }

        if (RelativePitch <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(RelativePitch), "Relative pitch must be greater than zero.");
        }

        if (RelativeVolume <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(RelativeVolume), "Relative volume must be greater than zero.");
        }
    }
}
