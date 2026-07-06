using System.Runtime.InteropServices;
using System.Text;
using System.IO;

namespace AeonVoice;

public sealed class AeonVoiceEngine : IDisposable
{
    private readonly NativeMethods.SetSampleRateCallback _setSampleRateCallback;
    private readonly NativeMethods.PlaySpeechCallback _playSpeechCallback;
    private readonly GCHandle _engineHandle;
    private IntPtr _nativeEngine;
    private bool _disposed;

    private int _sampleRate;
    private readonly List<short> _samples = new();

    public AeonVoiceEngine(string? dataPath = null, string? configPath = null, IReadOnlyList<string>? resourcePaths = null)
    {
        if (string.IsNullOrWhiteSpace(dataPath))
        {
            string packagedDataPath = Path.Combine(AppContext.BaseDirectory, "aeonvoice", "data");
            if (Directory.Exists(packagedDataPath))
            {
                dataPath = packagedDataPath;
            }
        }

        if (string.IsNullOrWhiteSpace(configPath))
        {
            string packagedConfigPath = Path.Combine(AppContext.BaseDirectory, "aeonvoice", "config");
            if (Directory.Exists(packagedConfigPath))
            {
                configPath = packagedConfigPath;
            }
        }

        _setSampleRateCallback = OnSetSampleRate;
        _playSpeechCallback = OnPlaySpeech;
        _engineHandle = GCHandle.Alloc(this, GCHandleType.Normal);

        using var pool = new InteropStringPool();

        var initParams = new NativeMethods.AeonVoiceInitParams
        {
            data_path = pool.AddUtf8(dataPath),
            config_path = pool.AddUtf8(configPath),
            resource_paths = pool.AddUtf8Array(resourcePaths),
            callbacks = new NativeMethods.AeonVoiceCallbacks
            {
                set_sample_rate = _setSampleRateCallback,
                play_speech = _playSpeechCallback,
                process_mark = IntPtr.Zero,
                word_starts = IntPtr.Zero,
                word_ends = IntPtr.Zero,
                sentence_starts = IntPtr.Zero,
                sentence_ends = IntPtr.Zero,
                play_audio = IntPtr.Zero,
                done = IntPtr.Zero
            },
            options = 0
        };

        _nativeEngine = NativeMethods.AeonVoice_new_tts_engine(in initParams);
        if (_nativeEngine == IntPtr.Zero)
        {
            _engineHandle.Free();
            throw new InvalidOperationException("Failed to create AeonVoice engine. Ensure voice data and native libraries are present.");
        }
    }

    public static string Version
    {
        get
        {
            IntPtr ptr = NativeMethods.AeonVoice_get_version();
            return ptr == IntPtr.Zero ? string.Empty : Marshal.PtrToStringUTF8(ptr) ?? string.Empty;
        }
    }

    public SynthesisResult SynthesizeToPcm16(string text, string voiceProfile)
    {
        return SynthesizeToPcm16(text, voiceProfile, options: null);
    }

    public SynthesisResult SynthesizeToPcm16(string text, string voiceProfile, SynthesisOptions? options)
    {
        ThrowIfDisposed();

        ArgumentException.ThrowIfNullOrWhiteSpace(text);
        ArgumentException.ThrowIfNullOrWhiteSpace(voiceProfile);
        options ??= new SynthesisOptions();
        options.Validate();

        _sampleRate = 0;
        _samples.Clear();

        using var pool = new InteropStringPool();

        byte[] textBytes = Encoding.UTF8.GetBytes(text);
        IntPtr textPtr = Marshal.AllocCoTaskMem(textBytes.Length + 1);
        try
        {
            Marshal.Copy(textBytes, 0, textPtr, textBytes.Length);
            Marshal.WriteByte(textPtr, textBytes.Length, 0);

            var synthParams = new NativeMethods.AeonVoiceSynthParams
            {
                voice_profile = pool.AddUtf8(voiceProfile),
                absolute_rate = 0,
                absolute_pitch = 0,
                absolute_volume = 0,
                relative_rate = options.RelativeRate,
                relative_pitch = options.RelativePitch,
                relative_volume = options.RelativeVolume,
                punctuation_mode = NativeMethods.AeonVoicePunctuationMode.Default,
                punctuation_list = IntPtr.Zero,
                capitals_mode = NativeMethods.AeonVoiceCapitalsMode.Default,
                flags = 0
            };

            IntPtr message = NativeMethods.AeonVoice_new_message(
                _nativeEngine,
                textPtr,
                checked((uint)textBytes.Length),
                NativeMethods.AeonVoiceMessageType.Text,
                in synthParams,
                GCHandle.ToIntPtr(_engineHandle));

            if (message == IntPtr.Zero)
            {
                throw new InvalidOperationException("Failed to create AeonVoice message.");
            }

            try
            {
                int ok = NativeMethods.AeonVoice_speak(message);
                if (ok == 0)
                {
                    throw new InvalidOperationException("AeonVoice synthesis failed.");
                }
            }
            finally
            {
                NativeMethods.AeonVoice_delete_message(message);
            }
        }
        finally
        {
            Marshal.FreeCoTaskMem(textPtr);
        }

        if (_sampleRate <= 0)
        {
            throw new InvalidOperationException("AeonVoice did not provide a sample rate.");
        }

        return new SynthesisResult(_sampleRate, _samples.ToArray());
    }

    public void Dispose()
    {
        if (_disposed)
        {
            return;
        }

        if (_nativeEngine != IntPtr.Zero)
        {
            NativeMethods.AeonVoice_delete_tts_engine(_nativeEngine);
            _nativeEngine = IntPtr.Zero;
        }

        if (_engineHandle.IsAllocated)
        {
            _engineHandle.Free();
        }

        _disposed = true;
        GC.SuppressFinalize(this);
    }

    ~AeonVoiceEngine()
    {
        Dispose();
    }

    private static AeonVoiceEngine GetInstance(IntPtr userData)
    {
        if (userData == IntPtr.Zero)
        {
            throw new InvalidOperationException("Callback user data is null.");
        }

        var handle = GCHandle.FromIntPtr(userData);
        if (handle.Target is not AeonVoiceEngine engine)
        {
            throw new InvalidOperationException("Invalid callback user data for AeonVoice engine.");
        }

        return engine;
    }

    private static int OnSetSampleRate(int sampleRate, IntPtr userData)
    {
        AeonVoiceEngine engine = GetInstance(userData);
        engine._sampleRate = sampleRate;
        return 1;
    }

    private static int OnPlaySpeech(IntPtr samples, uint count, IntPtr userData)
    {
        AeonVoiceEngine engine = GetInstance(userData);
        if (count == 0)
        {
            return 1;
        }

        short[] chunk = new short[count];
        Marshal.Copy(samples, chunk, 0, checked((int)count));
        engine._samples.AddRange(chunk);
        return 1;
    }

    private void ThrowIfDisposed()
    {
        if (_disposed)
        {
            throw new ObjectDisposedException(nameof(AeonVoiceEngine));
        }
    }
}
