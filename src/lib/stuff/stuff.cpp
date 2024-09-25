#include "stuff.h"

#include <zstd.h>
#include <tiffvers.h>

#include <iostream>
#include <exception>

STUFF_EXPORT void stuff_check(void)
{
    try {
        char const * const zstdVersionStr = ZSTD_versionString();
        std::cout << "ZSTD version: " << (zstdVersionStr ? zstdVersionStr : "<unknown>") << std::endl;
        char const * const tiffVersionStr = TIFFLIB_VERSION_STR;
        std::cout << "TIFF version: " << (tiffVersionStr ? tiffVersionStr : "<unknown>") << std::endl;
    } catch(std::exception const &) {
        // ...
    }
}
