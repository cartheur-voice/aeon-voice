namespace AeonVoice;

/// <summary>Optional, per-message controls for synthesis.</summary>
public sealed record SynthesisOptions(
    double RelativeRate = 1.0,
    double RelativePitch = 1.0,
    double RelativeVolume = 1.0)
{
    internal void Validate()
    {
        ValidateMultiplier(RelativeRate, nameof(RelativeRate));
        ValidateMultiplier(RelativePitch, nameof(RelativePitch));
        ValidateMultiplier(RelativeVolume, nameof(RelativeVolume));
    }

    private static void ValidateMultiplier(double value, string name)
    {
        if (!double.IsFinite(value) || value < 0.5 || value > 2.0)
        {
            throw new ArgumentOutOfRangeException(name, value, "Value must be between 0.5 and 2.0.");
        }
    }
}
