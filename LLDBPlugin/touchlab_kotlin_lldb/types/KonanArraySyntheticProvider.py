from lldb import SBSyntheticValueProvider, SBValue

from ..util import log, evaluate
from .base import _TYPE_CONVERSION, get_field_type, get_field_address
from .KonanBaseSyntheticProvider import KonanBaseSyntheticProvider


class KonanArraySyntheticProvider(KonanBaseSyntheticProvider):
    def __init__(self, valobj: SBValue):
        super().__init__(valobj)

        self._valobj = valobj
        self._children_count = None

        # valobj.SetSyntheticChildrenGenerated(True)
        # type = self._field_type(0)

    def update(self):
        self._children_count = evaluate("(int)Konan_DebugGetFieldCount({:#x})".format(self._valobj.unsigned)).signed

    def num_children(self):
        log(lambda: "KonanArraySyntheticProvider::num_children = {}".format(self._children_count))
        return self._children_count

    def has_children(self):
        log(lambda: "KonanArraySyntheticProvider::has_children = {}".format(self._children_count > 0))
        return self._children_count > 0

    def get_child_index(self, name):
        log(lambda: "KonanArraySyntheticProvider::get_child_index({})".format(name))
        index = int(name)
        return index if (0 <= index < self._children_count) else -1

    def get_child_at_index(self, index):
        log(lambda: "KonanArraySyntheticProvider::get_child_at_index({})".format(index))
        value_type = get_field_type(self._valobj, index)
        address = get_field_address(self._valobj, index)
        return _TYPE_CONVERSION[int(value_type)](self, self._valobj, address, '[{}]'.format(index))

    def to_string(self):
        log(lambda: "✅ KonanArraySyntheticProvider::to_string({})".format(self._children_count))
        if self._children_count == 1:
            return '1 value'
        else:
            return '{} values'.format(self._children_count)
