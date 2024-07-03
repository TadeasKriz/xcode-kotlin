import os

from lldb import SBDebugger, SBTarget, LLDB_ARCH_DEFAULT, SBEvent, SBListener, SBProcess, eStateStopped
from touchlab_kotlin_lldb import __lldb_init_module

exe = '/Users/tadeaskriz/Library/Developer/Xcode/DerivedData/KaMPKitiOS-eantjetnniifucfzdwialmcepcxt/Build/Products/Debug/KaMPKitiOS.app/Contents/MacOS/KaMPKitiOS'
framework_path = '/Users/tadeaskriz/Library/Developer/Xcode/DerivedData/KaMPKitiOS-eantjetnniifucfzdwialmcepcxt/Build/Products/Debug'

# Initialize the debugger before making any API calls.
SBDebugger.Initialize()
# Create a new debugger instance in your module if your module
# can be run from the command line. When we run a script from
# the command line, we won't have any debugger object in
# lldb.debugger, so we can just create it if it will be needed
debugger: SBDebugger = SBDebugger.Create()

# When we step or continue, don't return from the function until the process
# stops. Otherwise we would have to handle the process events ourselves which, while doable is
# a little tricky.  We do this by setting the async mode to false.
debugger.SetAsync(False)

# Next, do whatever work this module should do when run as a command.
debugger.HandleCommand('command script import touchlab_kotlin_lldb')

target: SBTarget = debugger.CreateTargetWithFileAndArch(exe, LLDB_ARCH_DEFAULT)

if target:
    breakpoint = target.BreakpointCreateByLocation('Weird.kt', 32)
    print(breakpoint)
    target.EnableAllBreakpoints()

    process = target.LaunchSimple(None, ['DYLD_FRAMEWORK_PATH={}'.format(framework_path)], os.getcwd())

    if process:
        debugger.HandleCommand('fr v --ptr-depth 9 -- dataList')
        # debugger.HandleCommand('fr v --ptr-depth 9 -- dataList->backing')

        process.Kill()

        # my_thread.join()

# Finally, dispose of the debugger you just made.
SBDebugger.Destroy(debugger)
# Terminate the debug session
SBDebugger.Terminate()
