# Configuration file

This file allows the user to customize the behavior of AeonVoice. It is read-only once at startup, so changes will take effect only after restarting the application which is using AeonVoice.

On Windows, the configuration file is named `AeonVoice.ini`. on other platforms it is named `AeonVoice.conf`.

## Path

### Linux

The path to the directory where the settings are stored is determined at compile time. It can be redefined by setting the value of the `sysconfdir` variable when executing `scons`. By default, the value is `$prefix/etc`, which, if the default value of the `prefix` variable is used, meaning `/usr/local/etc`.

The full path to the configuration file is `$sysconfdir/AeonVoice/AeonVoice.conf`.

### Windows

#### SAPI5

The path is `%APPDATA%\AeonVoice\AeonVoice.ini`.

## Format

AeonVoice uses the classic ini format. But as this format is not defined by a formal standard and implementations differ, here are some implementation details users should keep in mind.

* The file must be saved in UTF-8.
* Semicolons are used to indicate comments. Only the whole line can be commented out.
* Periods are used as decimal separators.
* Characters in values may be represented with their numeric codes. The format is similar to numeric character references in XML, but the initial ampersand sign is omitted. For example, the English letter A can be written as `#65;`.
* If an option takes only two boolean values, on or off,  use the following keywords to enable the corresponding behavior: `true`, `yes`, `on` or `1`, and to disable it, use `false`, `no`, `off` or `0`.

## General and specific settings

Some options can be applied to a specific installed voice.

### English-wide settings

The following format is used:

```ini
languages.<language>.<key>=<value>
```

AeonVoice supports English only. Use `English`, `en`, or `eng`.

Examples:

```ini
languages.english.default_rate=0.8
languages.eng.default_rate=0.8
```

### Voice-specific settings

The following format is used:

```ini
voices.<name>.<key>=<value>
```

Example:

```ini
voices.leena.enabled=no
```

## Available options

### Rate, pitch and volume

The settings in this group determine how AeonVoice interprets the values of rate, pitch and volume it receives from client programs.

The value `1` corresponds to the standard behavior of the voices.

For example, for an expression of the value of speech rate as a percentage, AeonVoice interprets 50% as the default speech rate (`default_rate`), and 100% is interpreted as the maximum speech rate (`max_rate`). The following table lists all the options in this group.

| Setting          | Description    | Default value | Minimum value | Maximum value |
| ---------------- | -------------- | ------------- | ------------- | ------------- |
| `default_rate`   | default rate   | 1             | `min_rate`    | `max_rate`    |
| `min_rate`       | minimum rate   | 0.5           | 0.2           | 1             |
| `max_rate`       | maximum rate   | 2             | 1             | 5             |
| `default_pitch`  | default pitch  | 1             | `min_pitch`   | `max_pitch`   |
| `min_pitch`      | minimum pitch  | 0.5           | 0.5           | 1             |
| `max_pitch`      | maximum pitch  | 2             | 1             | 2             |
| `default_volume` | default volume | 1             | `min_volume`  | `max_volume`  |
| `min_volume`     | minimum volume | 0.25          | 0.25          | 1             |
| `max_volume`     | maximum volume | 2             | 1             | 4             |

These settings can be applied to all voices, English as a whole, or an individual voice.

Examples:

```ini
default_volume=0.8
languages.english.default_rate=1.5
voices.alan.default_pitch=0.9
```

#### Using the Sonic library

AeonVoice can use [the Sonic library](https://github.com/waywardgeek/sonic) for changing speech rate. The native algorithm of speech rate modification in AeonVoice was improved in version 1.4.0, and this library is not included in the builds provided by the AeonVoice project. So the following setting is only supported in custom builds with Sonic enabled.

The `min_sonic_rate` setting specifies the minimum rate value starting from which Sonic will be used instead of the built-in algorithm. By default the built-in algorithm is always used on Android, and on other platforms Sonic is used to speed up speech, that is the synthesizer behaves as if the user wrote in the configuration file:

```ini
min_sonic_rate=1
```

### Voice profiles

AeonVoice currently synthesizes English only. A voice profile selects one
installed English voice for clients that support profile selection. The engine
also makes an individual profile available for each installed voice.

The `voice_profiles` setting is a comma-separated list of profile names. The
included configuration declares the `Alan` and `Leena` profiles:

```ini
voice_profiles=Alan,Leena
```

### Speech quality

The `quality` setting allows the user to choose one of the three available speech quality options.  The lower the quality, the better the performance: most importantly, the less time it will take for the synthesizer to start speaking. The available modes are described in the following table.

| Value      | Sampling rate (kHz) | Optimized response time |
| ---------- | ------------------- | ----------------------- |
| `max`      | 24                  | no                      |
| `standard` | 24                  | yes                     |
| `min`      | 16                  | yes                     |

The standard quality is used by default, that is the synthesizer behaves as if the user wrote in the configuration file:

```ini
quality=standard
```

### Punctuation

Despite the title, the settings in this group apply to other non-alphabetic characters as well, even though, strictly speaking, they can't be considered punctuation marks.

#### Punctuation mode

The `punctuation_mode` setting determines whether punctuation marks and other symbols will be spoken. The following modes are supported.

| Value  | Description                      |
| ------ | -------------------------------- |
| `none` | don't read any symbols (default) |
| `some` | selective reading                |
| `all`  | read all symbols                 |

For example, reading of all punctuation is enabled this way:

```ini
punctuation_mode=all
```

#### Selective reading of punctuation

The `punctuation_list` setting is used to specify which symbols to speak when the punctuation mode is set to `some`. For example:

```ini
punctuation_list=@$/\
```

#### Names of symbols

The built-in dictionary of punctuation marks and other symbols can't be called comprehensive.  But users can define the names of additional symbols in the user dictionary.

### Capital letters

The following settings determine whether and how the synthesizer will indicate capital letters when it reads individual characters.

#### Capital letter indication mode

This mode is specified by the `indicate_capitals` setting. The following values are supported.

| Value   | Description                   |
| ------- | ----------------------------- |
| `no`    | disabled (default)            |
| `word`  | say "capital" before a letter |
| `pitch` | change speech pitch           |
| `sound` | play a short sound            |

Example:

```ini
indicate_capitals=pitch
```

#### Changing pitch to indicate capital letters

If capital letters are indicated by a change in pitch, than the `cap_pitch_factor` setting specifies how much to change the pitch in this situation. This setting can be applied both to the synthesizer as a whole and to individual voices. The following example specifies a thirty percent increase:

```ini
cap_pitch_factor=1.3
```

### Disabling individual languages and voices

You can disable English or an individual voice. The following example disables English and Alan:

```ini
languages.english.enabled=false
voices.alan.enabled=false
```
