## Compiling & Installing on Linux

To compile AeonVoice the following programs are prerequsities:

* [GCC](https://gcc.gnu.org)
* [Pkg-config](https://www.freedesktop.org/wiki/Software/pkg-config/)
* [SCons](https://github.com/SCons/scons)

## Dependencies

Before compiling AeonVoice, make sure that at least one of the following audio libraries is installed:

* [PulseAudio](https://www.freedesktop.org/wiki/Software/PulseAudio/)
* [Libao](https://www.xiph.org/ao/)
* [PortAudio](http://www.portaudio.com) V19
* [Speech Dispatcher](https://freebsoft.org/speechd)

Please note that many distributions provide a separate development package for a library, which is necessary to compile the programs using the library. It is advised to install both runtime and development packages.

## Compilation

To start compilation, execute the command:

```bash
scons
```

To change some compilation options, check scons help:

```bash
scons -h
```

## Installation

To install AeonVoice execute the following command:

```bash
scons install
```

Now you can check if the synthesizer is working:

```bash
echo test|AeonVoice-test
```
