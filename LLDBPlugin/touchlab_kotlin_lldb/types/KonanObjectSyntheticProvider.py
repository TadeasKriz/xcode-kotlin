import lldb
from lldb import SBError, SBValue

from .base import get_field_type, get_field_address, _TYPE_CONVERSION
from ..util import log, DebuggerException, evaluate, kotlin_object_to_string
from .KonanBaseSyntheticProvider import KonanBaseSyntheticProvider


class KonanObjectSyntheticProvider(KonanBaseSyntheticProvider):
    def __init__(self, valobj: SBValue):
        super().__init__(valobj)

        self._children = None
        self._process = lldb.debugger.GetSelectedTarget().GetProcess()
        self._valobj = valobj

        log(lambda: "KonanObjectSyntheticProvider")
        self._children_count = evaluate("(int)Konan_DebugGetFieldCount({:#x})".format(valobj.unsigned)).signed
        log(lambda: "KonanObjectSyntheticProvider::__init__({:#x}) _children_count:{}".format(
            valobj.unsigned,
            self._children_count,
        ))

    def _field_name(self, index):
        log(lambda: "KonanObjectSyntheticProvider::_field_name({:#x}, {})".format(self._valobj.unsigned, index))
        error = SBError()
        name = self._process.ReadCStringFromMemory(
            evaluate("(char *)Konan_DebugGetFieldName({:#x}, (int){})".format(
                self._valobj.unsigned,
                index
            )).unsigned,
            0x1000,
            error,
        )
        if not error.Success():
            raise DebuggerException()
        log(lambda: "KonanObjectSyntheticProvider::_field_name({:#x}, {}) = {}".format(self._valobj.unsigned,
                                                                                       index, name))
        return name

    def _read_string(self, expr, error):
        return self._process.ReadCStringFromMemory(evaluate(expr).unsigned, 0x1000, error)

    def num_children(self):
        log(lambda: "KonanObjectSyntheticProvider::num_children({:#x}) = {}".format(self._valobj.unsigned,
                                                                                    self._children_count))
        return self._children_count

    def has_children(self):
        log(lambda: "KonanObjectSyntheticProvider::has_children({:#x}) = {}".format(self._valobj.unsigned,
                                                                                    self._children_count > 0))
        return self._children_count > 0

    def get_child_index(self, name):
        log(lambda: "KonanObjectSyntheticProvider::get_child_index({:#x}, {})".format(self._valobj.unsigned, name))
        if self._children is None:
            self._children = [self._field_name(i) for i in range(self._children_count)]

        index = self._children.index(name)
        log(lambda: "KonanObjectSyntheticProvider::get_child_index({:#x}) index={}".format(self._valobj.unsigned,
                                                                                           index))
        return index

    # def get_value(self):
    #     log(lambda: "KonanObjectSyntheticProvider::get_value({:#x})".format(self._valobj.unsigned))
    #     return self._valobj.Clone('something')

    def get_child_at_index(self, index):
        log(lambda: "KonanObjectSyntheticProvider::get_child_at_index({:#x}, {})".format(self._valobj.unsigned, index))
        value_type = get_field_type(self._valobj, index)
        address = get_field_address(self._valobj, index)
        res = _TYPE_CONVERSION[int(value_type)](self, self._valobj, address, self._field_name(index))
        log(lambda: "KonanObjectSyntheticProvider::get_child_at_index({:#x}, {}) = {:#x}".format(self._valobj.unsigned, index, res.unsigned))
        return res

    def to_string(self):
        log(lambda: "to_string:{:#x}".format(self._valobj.unsigned))
        return kotlin_object_to_string(self._process, self._valobj.unsigned)
