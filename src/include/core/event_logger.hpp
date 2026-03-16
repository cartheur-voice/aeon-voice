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

#ifndef RHVOICE_EVENT_LOGGER_HPP
#define RHVOICE_EVENT_LOGGER_HPP

#include <string>
#include "AeonVoice_common.h"

namespace AeonVoice
{
  class event_logger
  {
  public:
    event_logger()
    {
    }

    virtual ~event_logger()
    {
    }

    virtual void log(const std::string& tag,AeonVoice_log_level level,const std::string& message) const
    {
    }

  private:
    event_logger(const event_logger&);
    event_logger& operator=(const event_logger&);
  };
}
#endif
