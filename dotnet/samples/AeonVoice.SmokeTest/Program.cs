using AeonVoice;

string resourceRoot = Path.Combine(AppContext.BaseDirectory, "aeonvoice");
string voiceDirectory = Path.Combine(resourceRoot, "data", "voices", "leena");
string configFile = Path.Combine(resourceRoot, "config", "AeonVoice.conf");

if (!Directory.Exists(voiceDirectory) || !File.Exists(configFile))
{
    throw new InvalidOperationException("AeonVoice package data assets were not copied to the application output.");
}

using var engine = new AeonVoiceEngine();
SynthesisResult result = engine.SynthesizeToPcm16("Hello from AeonVoice.", "Leena");
if (result.SampleRate <= 0 || result.Samples.Length == 0)
{
    throw new InvalidOperationException("AeonVoice did not produce PCM audio.");
}

string outputPath = Path.Combine(AppContext.BaseDirectory, "aeonvoice-smoke.wav");
result.WriteWave(outputPath);
if (!File.Exists(outputPath) || new FileInfo(outputPath).Length <= 44)
{
    throw new InvalidOperationException("AeonVoice did not write a valid non-empty WAV file.");
}

Console.WriteLine($"AeonVoice {AeonVoiceEngine.Version}: wrote {outputPath}");
