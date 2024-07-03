/Library/Developer/Toolchains/swift-6.0-DEVELOPMENT-SNAPSHOT-2024-06-22-a.xctoolchain/usr/bin/lldb \
  /Users/tadeaskriz/Library/Developer/Xcode/DerivedData/KaMPKitiOS-eantjetnniifucfzdwialmcepcxt/Build/Products/Debug/KaMPKitiOS.app/Contents/MacOS/KaMPKitiOS \
  -o 'command script import touchlab_kotlin_lldb' \
  -o 'breakpoint set -f Weird.kt -l 32' \
  -o 'env DYLD_FRAMEWORK_PATH=/Users/tadeaskriz/Library/Developer/Xcode/DerivedData/KaMPKitiOS-eantjetnniifucfzdwialmcepcxt/Build/Products/Debug' \
  -o 'process launch' \
  -o 'fr v --ptr-depth 2 -- dataList'