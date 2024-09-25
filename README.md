# conan_test_tiff

Test the linkage of latest libtiff and libzstd versions.

## Build

Conan version: 2.6.0

```text
conan build . --build missing
```

The build works OK when using zstd version 1.5.5. However when using zstd version 1.5.6, it breaks. See requirements() section in root conanfile.py:

```text
# This works OK, but uses old version of zstd - I need to use latest version 1.5.6:
self.requires('zstd/1.5.5')

# This doesn't work (conan package version conflict: libtiff requires hardcoded zstd version 1.5.5):
# ERROR: Version conflict: Conflict between zstd/1.5.5 and zstd/1.5.6 in the graph.
# Conflict originates from libtiff/4.7.0
self.requires('zstd/1.5.6')

# This doesn't work (conan install is OK, but zstd.h is not found at compile-time):
# src/lib/stuff/stuff.cpp:3:10: fatal error: 'zstd.h' file not found
# #include <zstd.h>
#          ^~~~~~~~
self.requires('zstd/1.5.6', override=True)

# This doesn't work (conan install is OK, but zstd.h is not found at compile-time):
# src/lib/stuff/stuff.cpp:3:10: fatal error: 'zstd.h' file not found
# #include <zstd.h>
#          ^~~~~~~~
self.requires('zstd/1.5.6', override=True, headers=True, libs=True)
```
