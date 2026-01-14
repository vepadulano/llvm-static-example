# LLVM Static Example - Conda-Forge Recipe

Attempt at creating an executable that links against a Clang library and LLVM statically - as a conda-forge recipe.

## Directory Structure

```
.
├── recipe/
│   ├── meta.yaml       # Conda recipe metadata
│   └── build.sh        # Build script
├── src/
│   └── main.cpp        # Minimal C++ program
├── CMakeLists.txt      # CMake configuration
├── build-locally.py    # Local build script
├── LICENSE
└── README.md
```

## Build

```bash
python build-locally.py
```

## Check the created executable

```
conda debug $PATH_TO_CREATED_CONDA_PACKAGE
```

This will print the location of the test environment, e.g.

```
## Package Plan ##

  environment location: $HOME/.pixi/envs/conda-build/conda-bld/debug_1768376663508/_test_e
```

Then check if the executable links against LLVM and/or Clang dynamically

```
ldd $CONDA_DEBUG_ENV_LOCATION/bin/llvm-static-example
```

At least on my machine (Linux x86\_64), I see

```
	linux-vdso.so.1 (0x00007f62ddcb5000)
	libLLVM.so.21.1 => /lib64/libLLVM.so.21.1 (0x00007f62d5200000)
	libstdc++.so.6 => [MYHOMEPATH]/.pixi/envs/conda-build/conda-bld/debug_1768376663508/_test_e/bin/../lib/libstdc++.so.6 (0x00007f62d4e00000)
	libc.so.6 => /lib64/libc.so.6 (0x00007f62d4c0d000)
	libffi.so.8 => /lib64/libffi.so.8 (0x00007f62ddc79000)
	libedit.so.0 => /lib64/libedit.so.0 (0x00007f62ddc3f000)
	libm.so.6 => /lib64/libm.so.6 (0x00007f62d510b000)
	libz.so.1 => [MYHOMEPATH]/.pixi/envs/conda-build/conda-bld/debug_1768376663508/_test_e/bin/../lib/libz.so.1 (0x00007f62ddc22000)
	libzstd.so.1 => /lib64/libzstd.so.1 (0x00007f62d4b4a000)
	libxml2.so.2 => /lib64/libxml2.so.2 (0x00007f62d49ec000)
	libgcc_s.so.1 => [MYHOMEPATH]/.pixi/envs/conda-build/conda-bld/debug_1768376663508/_test_e/bin/../lib/libgcc_s.so.1 (0x00007f62ddbf5000)
	libdl.so.2 => /lib64/libdl.so.2 (0x00007f62ddbef000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f62ddcb7000)
	libtinfo.so.6 => /lib64/libtinfo.so.6 (0x00007f62ddbc2000)
	liblzma.so.5 => /lib64/liblzma.so.5 (0x00007f62ddb8d000)
```

Which means that it's actually linking against LLVM dynamically. I believe this dependency is inherited transitively from `libclangBasic.a` via the CMake target that can be seen by calling `conda debug PATH_TO_RECIPE_DIR` and then looking in the `_h_env` directory for the file `PATH_TO_CONDA_DEBUG_DIR/_h_env/lib/cmake/clang/ClangTargets.cmake`, which contains

```
add_library(clangBasic STATIC IMPORTED)

set_target_properties(clangBasic PROPERTIES
  INTERFACE_LINK_LIBRARIES "LLVM"
)
```

Hence it means that this target is transitively forcing the link against `libLLVM.so`
