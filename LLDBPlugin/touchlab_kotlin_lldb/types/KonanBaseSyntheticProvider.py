from typing import Optional

import lldb

from ..util import log, DebuggerException, kotlin_object_to_string, evaluate


class KonanBaseSyntheticProvider(object):
    def __init__(self, valobj: lldb.SBValue, type_info: lldb.value):
        super().__init__()

        self._valobj: lldb.SBValue = valobj
        self._val: lldb.value = lldb.value(valobj.GetNonSyntheticValue())
        self._type_info: lldb.value = type_info
        self._process: lldb.SBProcess = lldb.debugger.GetSelectedTarget().process

    def update(self) -> Optional[bool]:
        pass

    def read_cstring(self, address: int) -> str:
        error = lldb.SBError()
        result = self._process.ReadCStringFromMemory(
            address,
            0x1000,
            error,
        )
        if not error.Success():
            raise DebuggerException(
                'Could not read cstring at address {:#x} (error: {})'.format(
                    address,
                    error.description,
                )
            )
        return result

    def to_string(self):
        return kotlin_object_to_string(self._process, self._valobj.unsigned)