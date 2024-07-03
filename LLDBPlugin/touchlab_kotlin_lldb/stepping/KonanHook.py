from lldb import SBDebugger

from .KonanStepIn import KonanStepIn
from .KonanStepOut import KonanStepOut
from .KonanStepOver import KonanStepOver

KONAN_LLDB_DONT_SKIP_BRIDGING_FUNCTIONS = 'KONAN_LLDB_DONT_SKIP_BRIDGING_FUNCTIONS'
MAX_SIZE_FOR_STOP_REASON = 20
PLAN_FROM_STOP_REASON = {
    'step in': KonanStepIn.__name__,
    'step out': KonanStepOut.__name__,
    'step over': KonanStepOver.__name__,
}


class KonanHook:
    @classmethod
    def register_stop_hook(cls, debugger: SBDebugger, module_name):
        # Avoid Kotlin/Native runtime
        debugger.HandleCommand('settings set target.process.thread.step-avoid-regexp ^::Kotlin_')
        debugger.HandleCommand('target stop-hook add -P {}.{}'.format(module_name, cls.__name__))

    def __init__(self, target, extra_args, _):
        pass

    def handle_stop(self, execution_context, stream) -> bool:
        execution_context.frame.Clear()

        is_bridging_functions_skip_enabled = not execution_context.target.GetEnvironment().Get(
            KONAN_LLDB_DONT_SKIP_BRIDGING_FUNCTIONS
        )

        def is_kotlin_bridging_function() -> bool:
            addr = execution_context.frame.addr
            function_name = addr.function.name
            if function_name is None:
                return False
            file_name = addr.line_entry.file.basename
            if file_name is None:
                return False
            return function_name.startswith('objc2kotlin_') and file_name == '<compiler-generated>'

        if is_bridging_functions_skip_enabled and is_kotlin_bridging_function():
            stop_reason = execution_context.frame.thread.GetStopDescription(MAX_SIZE_FOR_STOP_REASON)
            plan = PLAN_FROM_STOP_REASON.get(stop_reason)
            if plan is not None:
                execution_context.thread.StepUsingScriptedThreadPlan('{}.{}'.format(__name__, plan))
        return True