cmake_minimum_required(VERSION 3.13)
project(llvm-static-example CXX)

# Don't force a specific C++ standard - let it use what's needed
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find LLVM's dependencies first (required by LLVM's CMake config)
find_package(ZLIB REQUIRED)

# Find LLVM
find_package(LLVM REQUIRED CONFIG)
message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")

# Find Clang
find_package(Clang REQUIRED CONFIG)
message(STATUS "Found Clang")

include_directories(${LLVM_INCLUDE_DIRS})
include_directories(${CLANG_INCLUDE_DIRS})
add_definitions(${LLVM_DEFINITIONS})


# Create an executable and force linking only against static libraries
add_executable(llvm-static-example src/main.cpp)

# Knowledge of the LLVM targets is obscure, it comes from having built manually
# Clang with LLVM_LINK_LLVM_DYLIB=OFF and looking at the generated ClangTargets.cmake
set(link_libs
        clangBasic
        LLVMSupport
        LLVMTargetParser
        LLVMFrontendOpenMP
)

if (LLVM_LINK_LLVM_DYLIB)
	message(WARNING "Detected LLVM_LINK_LLVM_DYLIB")
endif()

# Get rid of libLLVM.so in dependent link libraries
# Inspired by https://github.com/compiler-research/CppInterOp/blob/c0c0bb34de13ce15dcccb271f1cb9a7475582242/lib/CppInterOp/CMakeLists.txt#L58
foreach(lib ${link_libs})
	if(NOT TARGET ${lib})
                continue()
        endif()
	message(STATUS "Looking at target ${lib}")
        get_target_property(cur_link_libs ${lib} INTERFACE_LINK_LIBRARIES)
	if(NOT cur_link_libs)
		continue()
	endif()
	message(STATUS "INTERFACE_LINK_LIBRARIES=${cur_link_libs}")
	foreach(cur_lib ${cur_link_libs})
		if(NOT TARGET ${cur_lib})
			continue()
		endif()
		get_target_property(lib_type ${cur_lib} TYPE)
		if("${lib_type}" STREQUAL "STATIC_LIBRARY")
			list(APPEND static_libs ${cur_lib})
		endif()
	endforeach()
        message(STATUS "Extracted static libraries: ${static_libs}")
        set_target_properties(${lib} PROPERTIES INTERFACE_LINK_LIBRARIES "${static_libs}")
endforeach()

target_link_libraries(llvm-static-example PRIVATE
	${link_libs}
)

# Debug: Print final link line
get_target_property(LINK_LIBS llvm-static-example LINK_LIBRARIES)
message(STATUS "=== Final LINK_LIBRARIES ===")
foreach(lib ${LINK_LIBS})
    message(STATUS "  ${lib}")
endforeach()
message(STATUS "=============================")

# Install
install(TARGETS llvm-static-example RUNTIME DESTINATION bin)

