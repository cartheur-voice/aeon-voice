# -*- mode: Python; indent-tabs-mode: t; tab-width: 4 -*-

add_executable("AeonVoice-test" "${CMAKE_CURRENT_SOURCE_DIR}/test.cpp")
target_link_libraries("AeonVoice-test" "AeonVoice" "AeonVoice_audio")
target_include_directories("AeonVoice-test" PRIVATE "${TCLAP_INCLUDE_DIR}" "${HTS_LABELS_KIT_INCLUDES}")
harden("AeonVoice-test")
add_sanitizers("AeonVoice-test")

if(WITH_CLI11)
	target_compile_definitions(AeonVoice-test PRIVATE WITH_CLI11)
endif(WITH_CLI11)

if(BUILD_TESTING)
	add_test(
		NAME AeonVoice_SmokeSynthesis
		COMMAND "${CMAKE_COMMAND}" -E env
			"RHVOICE_DATA_PATH=${CMAKE_SOURCE_DIR}/data"
			"RHVOICE_CONFIG_PATH=${CMAKE_SOURCE_DIR}/config"
			"$<TARGET_FILE:AeonVoice-test>"
			"-i" "${CMAKE_SOURCE_DIR}/README.md"
			"-o" "${CMAKE_CURRENT_BINARY_DIR}/AeonVoice-smoke.wav"
	)
endif()

cpack_add_component(test
	DISPLAY_NAME "Standalone CLI application"
	DESCRIPTION "Provides a CLI application that allows you to synthesize speech using AeonVoice"
	GROUP "binaries"
	DEPENDS "audio"
)
list(APPEND CPACK_COMPONENTS_ALL "test")

install(TARGETS "AeonVoice-test"
	RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
	COMPONENT "test"
)
set("CPACK_DEBIAN_TEST_PACKAGE_NAME" "aeonvoice-test")
set(CPACK_DEBIAN_TEST_PACKAGE_DEPENDS "${CPACK_DEBIAN_CORE_PACKAGE_NAME}, ${CPACK_DEBIAN_AUDIO_PACKAGE_NAME}")


pass_through_cpack_vars()
