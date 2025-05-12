include(FindPackageHandleStandardArgs) 

find_path(Sonic_INCLUDE_DIRS "sonic.h")

find_library(Sonic_LIBRARIES NAMES "sonic")

find_package_handle_standard_args(Sonic
	REQUIRED_VARS Sonic_INCLUDE_DIRS Sonic_LIBRARIES
)
