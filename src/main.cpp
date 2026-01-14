#include "clang/Basic/Version.h"
#include "llvm/Support/raw_ostream.h"
#include <iostream>

int main() {
    llvm::outs() << "Hello from Clang and LLVM!\n";
    llvm::outs() << "Clang version: " << CLANG_VERSION_STRING << "\n";
    return 0;
}
