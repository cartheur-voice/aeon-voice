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

#ifndef RHVOICE_CURL_HPP
#define RHVOICE_CURL_HPP

#include <memory>
#include <functional>
#include <string>
#include <curl/curl.h>

namespace AeonVoice
{
  class curl final
  {
  private:
    curl();
    ~curl();

  public:
    using easy_handle=std::unique_ptr<CURL, decltype(curl_easy_cleanup)*>;
    using write_callback_t=std::function<bool(const char*, std::size_t)>;
    using progress_callback_t=std::function<bool(double, double)>;
    curl(curl&) =delete;
    curl& operator= (curl&) = delete;
    static curl& get_instance();
    easy_handle easy_init();
    void do_http_get(easy_handle& h, const std::string& url, write_callback_t w_callback, progress_callback_t p_callback=progress_callback_t());
  };
}
#endif
