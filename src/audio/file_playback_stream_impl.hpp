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

#ifndef RHVOICE_AUDIO_FILE_HPP
#define RHVOICE_AUDIO_FILE_HPP

#include <string>
#include <fstream>
#include "playback_stream_impl.hpp"

namespace AeonVoice
{
  namespace audio
  {
    class file_playback_stream_impl: public playback_stream_impl
    {
    public:
      explicit file_playback_stream_impl(const playback_params& params);
      void write(const short* samples,std::size_t count);
      void open(uint32_t sample_rate);
      bool is_open() const;
      void close();

    private:

      template<typename T> void write_number(T num)
      {
        stream.write(reinterpret_cast<char*>(&num),sizeof(num));
}

      const std::string file_path;
      const bool piping;
      std::ofstream fstream;
      std::ostream& stream;
      bool header_written;
      std::size_t num_samples;
    };
  }
}
#endif

