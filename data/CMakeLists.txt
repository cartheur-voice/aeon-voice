cpack_add_component_group("data")

set("ISO639_1_NAME2CODE_Russian" "ru")
set("ISO639_1_NAME2CODE_English" "en")

function(createLangCodeToNameMapping)
	get_cmake_property(varsHere VARIABLES)
	foreach(varName ${varsHere})
		if(varName MATCHES "^ISO639_1_NAME2CODE_(.+)$")
			set("ISO639_1_CODE2NAME_${${varName}}" "${CMAKE_MATCH_1}" PARENT_SCOPE)
		endif()
	endforeach()
endfunction()
createLangCodeToNameMapping()

set("VOICE_aleksandr_LANG" "ru")
set("VOICE_aleksandr-hq_LANG" "ru")
set("VOICE_anna_LANG" "ru")
set("VOICE_vitaliy_LANG" "ru")
set("VOICE_vitaliy-ng_LANG" "ru")
set("VOICE_umka_LANG" "ru")
set("VOICE_yuriy_LANG" "ru")
set("VOICE_arina_LANG" "ru")
set("VOICE_artemiy_LANG" "ru")
set("VOICE_evgeniy-rus_LANG" "ru")
set("VOICE_elena_LANG" "ru")
set("VOICE_irina_LANG" "ru")
set("VOICE_pavel_LANG" "ru")
set("VOICE_victoria_LANG" "ru")
set("VOICE_tatiana_LANG" "ru")
set("VOICE_timofey_LANG" "ru")
set("VOICE_mikhail_LANG" "ru")
set("VOICE_vsevolod_LANG" "ru")

set("VOICE_evgeniy-eng_LANG" "en")
set("VOICE_lyubov_LANG" "en")
set("VOICE_alan_LANG" "en")
set("VOICE_bdl_LANG" "en")
set("VOICE_clb_LANG" "en")
set("VOICE_ksp_LANG" "en")
set("VOICE_slt_LANG" "en")

cpack_add_component_group("data"
	DISPLAY_NAME "Data files"
	DESCRIPTION "Various data required for synthesis"
	EXPANDED
)

add_subdirectory("languages")
add_subdirectory("voices")
pass_through_cpack_vars()
