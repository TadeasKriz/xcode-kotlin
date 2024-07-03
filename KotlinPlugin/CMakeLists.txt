cmake_minimum_required(VERSION 3.28)
project(KotlinPlugin)

set(CMAKE_OSX_ARCHITECTURES x86_64)
set(LLVM_DIR /opt/homebrew/Cellar/llvm/18.1.5/lib/cmake/llvm/)
find_package(LLVM REQUIRED CONFIG)

message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}, ${LLVM_INCLUDE_DIRS}, ${LLVM_BINARY_DIR}")

# Set your project compile flags.
# E.g. if using the C++ header files
# you will need to enable C++11 support
# for your compiler.
include_directories(${LLVM_INCLUDE_DIRS})
separate_arguments(LLVM_DEFINITIONS_LIST NATIVE_COMMAND ${LLVM_DEFINITIONS})
add_definitions(${LLVM_DEFINITIONS_LIST})

find_library(lib_lldb1 NAMES LLDB PATHS /Applications/Xcode.app/Contents/SharedFrameworks/)
message(STATUS "Found LLDB ${lib_lldb1}")

set(CMAKE_CXX_STANDARD 26)

# Now build our tools
add_library(KotlinPlugin SHARED library.cpp)

# Find the libraries that correspond to the LLVM components
# that we wish to use
llvm_map_components_to_libnames(llvm_libs support core irreader)

# Link against LLVM libraries
target_link_libraries(KotlinPlugin ${lib_lldb1})
