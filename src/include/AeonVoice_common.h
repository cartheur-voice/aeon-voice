/* Copyright (C) 2012, 2014, 2020  Olga Yakovleva <yakovleva.o.v@gmail.com> */

/* This program is free software: you can redistribute it and/or modify */
/* it under the terms of the GNU Lesser General Public License as published by */
/* the Free Software Foundation, either version 2.1 of the License, or */
/* (at your option) any later version. */

/* This program is distributed in the hope that it will be useful, */
/* but WITHOUT ANY WARRANTY; without even the structied warranty of */
/* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the */
/* GNU Lesser General Public License for more details. */

/* You should have received a copy of the GNU Lesser General Public License */
/* along with this program.  If not, see <https://www.gnu.org/licenses/>. */

#ifndef RHVOICE_COMMON_H
#define RHVOICE_COMMON_H

typedef enum {
  AeonVoice_voice_gender_unknown,
  AeonVoice_voice_gender_male,
  AeonVoice_voice_gender_female
} AeonVoice_voice_gender;

typedef enum {
  AeonVoice_punctuation_default,
  AeonVoice_punctuation_none,
  AeonVoice_punctuation_all,
  AeonVoice_punctuation_some
} AeonVoice_punctuation_mode;

typedef enum {
  AeonVoice_capitals_default,
  AeonVoice_capitals_off,
  AeonVoice_capitals_word,
  AeonVoice_capitals_pitch,
  AeonVoice_capitals_sound
} AeonVoice_capitals_mode;

typedef enum
  {
    AeonVoice_log_level_trace,
    AeonVoice_log_level_debug,
    AeonVoice_log_level_info,
    AeonVoice_log_level_warning,
    AeonVoice_log_level_error
  } AeonVoice_log_level;

typedef enum {
              AeonVoice_synth_flag_dont_clip_rate=1
} AeonVoice_synth_flag;
#endif
