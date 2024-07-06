# Before running this, add LLDB to your PYTHONPATH (e.g. PYTHONPATH=`lldb -P`)

import os
import subprocess

import lldb

gradle_invoke = subprocess.Popen(['./gradlew', 'compileSwift'], cwd='test_project')
gradle_exit_code = gradle_invoke.wait()

if gradle_exit_code != 0:
    exit(gradle_exit_code)

exe = 'test_project/build/swift/app'

# Initialize the debugger before making any API calls.
lldb.SBDebugger.Initialize()
# Create a new debugger instance in your module if your module
# can be run from the command line. When we run a script from
# the command line, we won't have any debugger object in
# lldb.debugger, so we can just create it if it will be needed
debugger: lldb.SBDebugger = lldb.SBDebugger.Create()

# When we step or continue, don't return from the function until the process
# stops. Otherwise we would have to handle the process events ourselves which, while doable is
# a little tricky.  We do this by setting the async mode to false.
debugger.SetAsync(False)

# debugger.HandleCommand('log enable lldb default')

# Import our module
debugger.HandleCommand('command script import touchlab_kotlin_lldb')

target: lldb.SBTarget = debugger.CreateTargetWithFileAndArch(exe, lldb.LLDB_ARCH_DEFAULT)

if target:
    # target.BreakpointCreateByLocation("main.swift", 14)
    target.BreakpointCreateByLocation('main.kt', 47)

    process: lldb.SBProcess = target.LaunchSimple(None, None, os.getcwd())

    if process:
        import time
        start = time.perf_counter()
        debugger.HandleCommand('fr v --ptr-depth 16')
        print('HandleCommand took {:.6}s'.format(time.perf_counter() - start))
        process.Continue()
        # debugger.HandleCommand('fr v --ptr-depth 16 -- data')
        debugger.HandleCommand('fr v --ptr-depth 16')

        process.Kill()

# Finally, dispose of the debugger you just made.
lldb.SBDebugger.Destroy(debugger)
# Terminate the debug session
lldb.SBDebugger.Terminate()