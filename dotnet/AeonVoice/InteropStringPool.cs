using System.Runtime.InteropServices;

namespace AeonVoice;

internal sealed class InteropStringPool : IDisposable
{
    private readonly List<IntPtr> _allocations = new();

    public IntPtr AddUtf8(string? value)
    {
        if (string.IsNullOrEmpty(value))
        {
            return IntPtr.Zero;
        }

        IntPtr ptr = Marshal.StringToCoTaskMemUTF8(value);
        _allocations.Add(ptr);
        return ptr;
    }

    public IntPtr AddUtf8Array(IReadOnlyList<string>? values)
    {
        if (values is null || values.Count == 0)
        {
            return IntPtr.Zero;
        }

        IntPtr[] pointers = new IntPtr[values.Count + 1];
        for (int i = 0; i < values.Count; i++)
        {
            pointers[i] = AddUtf8(values[i]);
        }

        int size = IntPtr.Size * pointers.Length;
        IntPtr block = Marshal.AllocCoTaskMem(size);
        _allocations.Add(block);

        for (int i = 0; i < pointers.Length; i++)
        {
            Marshal.WriteIntPtr(block, i * IntPtr.Size, pointers[i]);
        }

        return block;
    }

    public void Dispose()
    {
        foreach (IntPtr ptr in _allocations)
        {
            Marshal.FreeCoTaskMem(ptr);
        }

        _allocations.Clear();
    }
}
