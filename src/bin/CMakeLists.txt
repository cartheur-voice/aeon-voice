# -*- mode: Python; indent-tabs-mode: t; tab-width: 4 -*-
# Copyright (C) 2012, 2014, 2018  Olga Yakovleva <yakovleva.o.v@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

pkg_check_modules(DBUS REQUIRED dbus)

add_executable("AeonVoice-client" "${CMAKE_CURRENT_SOURCE_DIR}/aeonvoice-client.c")
target_include_directories("AeonVoice-client" PRIVATE "${DBUS_INCLUDE_DIRS}")
target_link_libraries("AeonVoice-client" PRIVATE "AeonVoice_core" "${DBUS_LIBRARIES}")
harden("AeonVoice-client")
add_sanitizers("AeonVoice-client")
target_compile_definitions("AeonVoice-client" PRIVATE "-DVERSION=\"${VERSION}\"")

#add_executable("AeonVoice" "${CMAKE_CURRENT_SOURCE_DIR}/main.cpp")
#target_link_libraries("AeonVoice" "AeonVoice_core")
#target_compile_definitions(AeonVoice PRIVATE "-DPACKAGE=\"AeonVoice\"")
#harden("AeonVoice")
#add_sanitizers("AeonVoice")

cpack_add_component(client
	DISPLAY_NAME "AeonVoice D-Bus service client"
	DESCRIPTION "Provides a client allowing to speak text using AeonVoice DBus client. Deprecated. Use speech-dispatcher."
	GROUP "binaries"
	DEPENDS "core"
)
list(APPEND CPACK_COMPONENTS_ALL "client")

install(TARGETS "AeonVoice-client"
	RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
	COMPONENT "client"
)

set("CPACK_DEBIAN_CLIENT_PACKAGE_NAME" "aeonvoice-client")
set(CPACK_DEBIAN_CLIENT_PACKAGE_DEPENDS "${CPACK_DEBIAN_CORE_PACKAGE_NAME}, ${CPACK_DEBIAN_AUDIO_PACKAGE_NAME}")

pass_through_cpack_vars()
