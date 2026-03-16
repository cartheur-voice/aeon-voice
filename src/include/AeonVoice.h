/* SPDX-License-Identifier: GPL-3.0-or-later */

/* This program is free software: you can redistribute it and/or modify */
/* it under the terms of the GNU General Public License as published by */
/* the Free Software Foundation, either version 3 of the License, or */
/* (at your option) any later version. */

/* This program is distributed in the hope that it will be useful, */
/* but WITHOUT ANY WARRANTY; without even the implied warranty of */
/* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the */
/* GNU General Public License for more details. */

/* You should have received a copy of the GNU General Public License */
/* along with this program.  If not, see <https://www.gnu.org/licenses/>. */

#ifndef RHVOICE_H
#define RHVOICE_H

#include "AeonVoice_common.h"

#ifdef __cplusplus
extern "C" {
#else
#include <stddef.h>
#endif

  struct AeonVoice_tts_engine_struct;
  typedef struct AeonVoice_tts_engine_struct* AeonVoice_tts_engine;

typedef struct
{
  /* These are the functions the caller is *required* to provide. */
/* This function will be called first. It will be called again if the sampling rate changes. Return 0 to signal an error. */
  int (*set_sample_rate)(int sample_rate,void* user_data);
  /* Return 0 to stop synthesis. */
  int (*play_speech)(const short* samples,unsigned int count,void* user_data);
  /* These functions are optional, */
  /* but please make sure to set unused function pointers to 0. */
  int (*process_mark)(const char* name,void* user_data);
  int (*word_starts)(unsigned int position,unsigned int length,void* user_data);
  int (*word_ends)(unsigned int position,unsigned int length,void* user_data);
  int (*sentence_starts)(unsigned int position,unsigned int length,void* user_data);
  int (*sentence_ends)(unsigned int position,unsigned int length,void* user_data);
  int(*play_audio)(const char* src,void *user_data);
  void (*done)(void* user_data);
} AeonVoice_callbacks;

  typedef enum {
    AeonVoice_preload_voices=1
  } AeonVoice_init_option;
  typedef unsigned int AeonVoice_init_options;

  typedef struct
  {
    /* The paths should be encoded as utf-8 strings. */
    const char *data_path,*config_path;
    /* A list of paths to language and voice data. */
    /* It should be used when it is not possible to collect all the data in one place. */
    /* The last item in the array should be NULL. */
    const char** resource_paths;
    AeonVoice_callbacks callbacks;
    AeonVoice_init_options options;
  } AeonVoice_init_params;

  typedef enum {
    AeonVoice_message_text,
    AeonVoice_message_ssml,
    AeonVoice_message_characters,
    AeonVoice_message_key
  } AeonVoice_message_type;

  struct AeonVoice_message_struct;
  typedef struct AeonVoice_message_struct* AeonVoice_message;

  typedef struct
  {
    /* Language code. */
    const char* language;
    const char* name;
    AeonVoice_voice_gender gender;
    /* Country code. */
    const char* country;
  } AeonVoice_voice_info;

  typedef struct
  {
    /* One of the predefined voice profiles or a custom one, e.g. */
    /* Aleksandr+Alan. Voice names should be ordered according to their */
    /* priority, but they must not speak the same language. If the */
    /* combination includes more than one voice, automatic language */
    /* switching may be used. The voice which speaks the primary language */
    /* should be placed first. AeonVoice will use one of the other voices */
    /* from the list, if it detects the corresponding language. The */
    /* detection algorithm is not very smart at the moment. It will not */
    /* handle languages with common letters. For example, if you set this */
    /* field to "Helen+Spomenka", it will always choose Helen for latin */
    /* letters. Spomenka might still be used, if Esperanto is requested */
    /* through SSML. */
    const char* voice_profile;
    /* The values must be between -1 and 1. */
    /*     They are normalized this way, because users can set different */
    /* parameters for different voices in the configuration file. */
    double absolute_rate,absolute_pitch,absolute_volume;
    /* Relative values, in case someone needs them. */
    /* If you don't, just set each of them to 1. */
    double relative_rate,relative_pitch,relative_volume;
    /* Set to AeonVoice_punctuation_default to allow the synthesizer to decide */
    AeonVoice_punctuation_mode punctuation_mode;
    /* Optional */
    const char* punctuation_list;
    /* This mode only applies to reading by characters. */
    /* If your program doesn't support this setting, set to AeonVoice_capitals_default. */
    AeonVoice_capitals_mode capitals_mode;
/* Set to 0 for defaults. */
    int flags;
  } AeonVoice_synth_params;

  const char* AeonVoice_get_version();

  AeonVoice_tts_engine AeonVoice_new_tts_engine(const AeonVoice_init_params* init_params);
  void AeonVoice_delete_tts_engine(AeonVoice_tts_engine tts_engine);

  unsigned int AeonVoice_get_number_of_voices(AeonVoice_tts_engine tts_engine);
  const AeonVoice_voice_info* AeonVoice_get_voices(AeonVoice_tts_engine tts_engine);
  unsigned int AeonVoice_get_number_of_voice_profiles(AeonVoice_tts_engine tts_engine);
  char const * const * AeonVoice_get_voice_profiles(AeonVoice_tts_engine tts_engine);
  int AeonVoice_are_languages_compatible(AeonVoice_tts_engine tts_engine,const char* language1,const char* language2);

  /* Text should be a valid utf-8 string */
  AeonVoice_message AeonVoice_new_message(AeonVoice_tts_engine tts_engine,const char* text,unsigned int length,AeonVoice_message_type message_type,const AeonVoice_synth_params* synth_params,void* user_data);

  /* On Windows the library is now built with MSVC instead of Mingw, */
  /* so wchar_t will always mean utf-16 there */
  AeonVoice_message AeonVoice_new_message_w(AeonVoice_tts_engine tts_engine,const wchar_t* text,unsigned int length,AeonVoice_message_type message_type,const AeonVoice_synth_params* synth_params,void* user_data);

  void AeonVoice_delete_message(AeonVoice_message message);

  int AeonVoice_speak(AeonVoice_message message);

#ifdef __cplusplus
}
#endif
#endif
