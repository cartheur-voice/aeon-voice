
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

set("VOICE_talgat_LICENSE" "Proprietary, non-commercial") # Tatar
set("VOICE_natia_LICENSE" "Proprietary, personal use only") # Georgian
set("VOICE_Leticia-F123_LICENSE" "by-sa-4.0") # Brazilian Portuguese

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

set("VOICE_volodymyr_LANG" "uk")
set("VOICE_marianna_LANG" "uk")
set("VOICE_anatol_LANG" "uk")
set("VOICE_natalia_LANG" "uk")

set("VOICE_Leticia-F123_LANG" "${ISO639_1_NAME2CODE_Brazilian-Portuguese}")

set("VOICE_spomenka_LANG" "eo")

set("VOICE_natia_LANG" "ka")

set("VOICE_azamat_LANG" "ky")
set("VOICE_nazgul_LANG" "ky")

set("VOICE_kiko_LANG" "mk")
set("VOICE_suze_LANG" "mk")

set("VOICE_hana_LANG" "sq")

set("VOICE_talgat_LANG" "tt")

set("VOICE_alicja_LANG" "pl")
set("VOICE_cezary_LANG" "pl")
set("VOICE_magda_LANG" "pl")
set("VOICE_michal_LANG" "pl")
set("VOICE_natan_LANG" "pl")
set("VOICE_zdenek_LANG" "cs")
set("VOICE_radek_LANG" "cs")
set("VOICE_ondro_LANG" "sk")
set("VOICE_jasietka_LANG" "sk")
set("VOICE_sevinch_LANG" "uz")
set("VOICE_islom_LANG" "uz")
set("VOICE_dilnavoz_LANG" "uz")
set("VOICE_dragana_LANG" "sr")
set("VOICE_karmela_LANG" "hr")
set("VOICE_mateo_LANG" "es")
set("VOICE_seva_LANG" "ru")

cpack_add_component_group("data"
	DISPLAY_NAME "Data files"
	DESCRIPTION "Various data required for synthesis"
	EXPANDED
)

add_subdirectory("languages")
add_subdirectory("voices")
pass_through_cpack_vars()
