using System.Runtime.InteropServices;

namespace AeonVoice;

internal static class NativeMethods
{
    internal const string LibraryName = "AeonVoice";

    internal enum AeonVoiceMessageType : uint
    {
        Text = 0,
        Ssml = 1,
        Characters = 2,
        Key = 3
    }

    internal enum AeonVoicePunctuationMode : uint
    {
        Default = 0,
        None = 1,
        All = 2,
        Some = 3
    }

    internal enum AeonVoiceCapitalsMode : uint
    {
        Default = 0,
        Off = 1,
        Word = 2,
        Pitch = 3,
        Sound = 4
    }

    [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
    internal delegate int SetSampleRateCallback(int sampleRate, IntPtr userData);

    [UnmanagedFunctionPointer(CallingConvention.Cdecl)]
    internal delegate int PlaySpeechCallback(IntPtr samples, uint count, IntPtr userData);

    [StructLayout(LayoutKind.Sequential)]
    internal struct AeonVoiceCallbacks
    {
        internal SetSampleRateCallback? set_sample_rate;
        internal PlaySpeechCallback? play_speech;
        internal IntPtr process_mark;
        internal IntPtr word_starts;
        internal IntPtr word_ends;
        internal IntPtr sentence_starts;
        internal IntPtr sentence_ends;
        internal IntPtr play_audio;
        internal IntPtr done;
    }

    [StructLayout(LayoutKind.Sequential)]
    internal struct AeonVoiceInitParams
    {
        internal IntPtr data_path;
        internal IntPtr config_path;
        internal IntPtr resource_paths;
        internal AeonVoiceCallbacks callbacks;
        internal uint options;
    }

    [StructLayout(LayoutKind.Sequential)]
    internal struct AeonVoiceSynthParams
    {
        internal IntPtr voice_profile;
        internal double absolute_rate;
        internal double absolute_pitch;
        internal double absolute_volume;
        internal double relative_rate;
        internal double relative_pitch;
        internal double relative_volume;
        internal AeonVoicePunctuationMode punctuation_mode;
        internal IntPtr punctuation_list;
        internal AeonVoiceCapitalsMode capitals_mode;
        internal int flags;
    }

    [DllImport(LibraryName, CallingConvention = CallingConvention.Cdecl)]
    internal static extern IntPtr AeonVoice_get_version();

    [DllImport(LibraryName, CallingConvention = CallingConvention.Cdecl)]
    internal static extern IntPtr AeonVoice_new_tts_engine(in AeonVoiceInitParams initParams);

    [DllImport(LibraryName, CallingConvention = CallingConvention.Cdecl)]
    internal static extern void AeonVoice_delete_tts_engine(IntPtr ttsEngine);

    [DllImport(LibraryName, CallingConvention = CallingConvention.Cdecl)]
    internal static extern IntPtr AeonVoice_new_message(
        IntPtr ttsEngine,
        IntPtr text,
        uint length,
        AeonVoiceMessageType messageType,
        in AeonVoiceSynthParams synthParams,
        IntPtr userData);

    [DllImport(LibraryName, CallingConvention = CallingConvention.Cdecl)]
    internal static extern int AeonVoice_speak(IntPtr message);

    [DllImport(LibraryName, CallingConvention = CallingConvention.Cdecl)]
    internal static extern void AeonVoice_delete_message(IntPtr message);
}
