cmake_minimum_required(VERSION 3.13)
project(llvm-static-example CXX)

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

add_executable(llvm-static-example src/main.cpp)

target_link_libraries(llvm-static-example PRIVATE 
    clangBasic
)

# Debug: Print exactly what libraries will be linked
get_target_property(LINK_LIBS llvm-static-example LINK_LIBRARIES)
message(STATUS "=== Direct link libraries ===")
foreach(lib ${LINK_LIBS})
    message(STATUS "  ${lib}")
endforeach()
message(STATUS "=============================")

# Debug: Print the location of clangBasic
if(TARGET clangBasic)
    get_target_property(CLANG_BASIC_LOCATION clangBasic LOCATION)
    message(STATUS "clangBasic location: ${CLANG_BASIC_LOCATION}")
    
    get_target_property(CLANG_BASIC_LINK_LIBS clangBasic INTERFACE_LINK_LIBRARIES)
    message(STATUS "=== clangBasic transitive dependencies ===")
    foreach(lib ${CLANG_BASIC_LINK_LIBS})
        message(STATUS "  ${lib}")
    endforeach()
    message(STATUS "==========================================")
endif()

install(TARGETS llvm-static-example RUNTIME DESTINATION bin)
