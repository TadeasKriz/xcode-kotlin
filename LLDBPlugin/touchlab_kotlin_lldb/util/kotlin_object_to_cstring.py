from lldb import SBProcess, SBError

from .DebuggerException import DebuggerException
from .expression import evaluate
from .log import log
from ..cache import LLDBCache


def GetDebugBufferAddr() -> int:
    self = LLDBCache.instance()
    if self._debug_buffer_addr is None:
        self._debug_buffer_addr = int(evaluate("(void *)Konan_DebugBuffer()").unsigned)
    return self._debug_buffer_addr


def GetDebugBufferSize() -> int:
    self = LLDBCache.instance()
    if self._debug_buffer_size is None:
        self._debug_buffer_size = int(evaluate("(int)Konan_DebugBufferSize()").unsigned)
    return self._debug_buffer_size


def kotlin_object_to_string(process: SBProcess, object_addr):
    debug_buffer_addr = GetDebugBufferAddr()
    debug_buffer_size = GetDebugBufferSize()
    string_len = evaluate(
        '(int)Konan_DebugObjectToUtf8Array((void*){:#x}, (void *){:#x}, {});'.format(
            object_addr,
            debug_buffer_addr,
            debug_buffer_size,
        )
    ).signed

    if not string_len:
        return None

    error = SBError()
    s = process.ReadCStringFromMemory(debug_buffer_addr, int(string_len), error)
    if not error.Success():
        raise DebuggerException()
    return s
