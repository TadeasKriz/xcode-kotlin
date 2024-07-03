from lldb import SBValue

from .base import get_field_type, get_field_address, _TYPE_CONVERSION
from ..util import log
from .KonanBaseSyntheticProvider import KonanBaseSyntheticProvider


class KonanListSyntheticProvider(KonanBaseSyntheticProvider):
    def __init__(self, valobj: SBValue):
        super().__init__(valobj)

        # self._valobj = valobj
        self._children_count = 0
        self._backing = None
        self.val = valobj.GetNonSyntheticValue()

        valobj.SetPreferSyntheticValue(True)
        # valobj.SetSyntheticChildrenGenerated(True)
        # type = self._field_type(0)

    # def num_children(self):
    #     log(lambda: "KonanListSyntheticProvider::num_children({:#x}) = {}".format(self._valobj.unsigned,
    #                                                                                self._children_count))
    #     return self._children_count
    #
    # def has_children(self):
    #     log(lambda: "KonanListSyntheticProvider::has_children({:#x}) = {}".format(self._valobj.unsigned,
    #                                                                                self._children_count > 0))
    #     return self._children_count > 0
    #
    # def get_child_index(self, name):
    #     log(lambda: "KonanListSyntheticProvider::get_child_index({:#x}, {})".format(self._valobj.unsigned, name))
    #     index = int(name)
    #     return index if (0 <= index < self._children_count) else -1
    #
    # def get_child_at_index(self, index):
    #     log(lambda: "KonanListSyntheticProvider::get_child_at_index({:#x}, {})".format(self._valobj.unsigned, index))
    #     value_type = get_field_type(self._valobj, index)
    #     address = get_field_address(self._valobj, index)
    #     return _TYPE_CONVERSION[int(value_type)](self, self._valobj, address, str(index))

    def update(self):
        log(lambda: "[BEGIN]KonanListSyntheticProvider({:#x})::update".format(self.val.unsigned))
        value_type = get_field_type(self.val, 1)
        address = get_field_address(self.val, 1)
        self._backing = _TYPE_CONVERSION[int(value_type)](self, self.val, address, str(1))
        log(lambda: "[END]KonanListSyntheticProvider::update")

    def get_value(self):
        log(lambda: "✅ KonanListSyntheticProvider::get_value")
        return self._backing

    def to_string(self):
        log(lambda: "❌ KonanListSyntheticProvider::to_string")
        return '{} items'.format(self._children_count)
