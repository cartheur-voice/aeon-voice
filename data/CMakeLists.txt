cpack_add_component_group("data")

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

set("VOICE_evgeniy-eng_LANG" "en")
set("VOICE_daria_LANG" "en")
set("VOICE_toptygin_LANG" "en")
set("VOICE_bdl_LANG" "en")
set("VOICE_helen_LANG" "en")
set("VOICE_ksp_LANG" "en")
set("VOICE_leena_LANG" "en")

cpack_add_component_group("data"
	DISPLAY_NAME "Data files"
	DESCRIPTION "Various data required for synthesis"
	EXPANDED
)

add_subdirectory("languages")
add_subdirectory("voices")
pass_through_cpack_vars()
