#lldb -o 'plugin load cmake-build-debug/libKotlinPlugin.dylib' -o 'q'
#
#
lldb \
  /Users/tadeaskriz/Library/Developer/Xcode/DerivedData/KaMPKitiOS-eantjetnniifucfzdwialmcepcxt/Build/Products/Debug/KaMPKitiOS.app/Contents/MacOS/KaMPKitiOS \
  -o 'plugin load cmake-build-debug/libKotlinPlugin.dylib' \
  -o 'breakpoint set -f Weird.kt -l 32' \
  -o 'env DYLD_FRAMEWORK_PATH=/Users/tadeaskriz/Library/Developer/Xcode/DerivedData/KaMPKitiOS-eantjetnniifucfzdwialmcepcxt/Build/Products/Debug' \
  -o 'process launch' \
  -o 'fr v --ptr-depth 2 -- dataList'