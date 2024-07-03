from lldb import SBDebugger, SBValue, SBTypeCategory, SBTypeSynthetic

from .base import KOTLIN_NATIVE_TYPE, KOTLIN_CATEGORY, type_info
from .KonanNotInitializedObjectSyntheticProvider import KonanNotInitializedObjectSyntheticProvider
from .KonanNullSyntheticProvider import KonanNullSyntheticProvider
from ..util.log import log
from .select_provider import select_provider


class KonanProxyTypeProvider:
    @classmethod
    def register_type_provider(cls, debugger: SBDebugger, module_name):
        debugger.HandleCommand(
            'type synthetic add "{}" --python-class {}.{} --category {}'.format(
                KOTLIN_NATIVE_TYPE,
                module_name,
                cls.__name__,
                KOTLIN_CATEGORY,
            )
        )

    def __init__(self, valobj: SBValue, internal_dict):
        import traceback
        print(f"⭐️ KonanProxyTypeProvider {valobj.name}")
        traceback.print_stack()
        log(lambda: "[BEGIN] KonanProxyTypeProvider")
        if valobj.unsigned == 0:
            log(lambda: "[END] KonanProxyTypeProvider NULL synthetic {}".format(valobj.IsValid()))
            self._proxy = KonanNullSyntheticProvider(valobj)
            return

        tip = type_info(valobj)
        if not tip:
            log(lambda: "[END] KonanProxyTypeProvider not initialized synthetic {}".format(valobj.IsValid()))
            self._proxy = KonanNotInitializedObjectSyntheticProvider(valobj)
            return
        self._proxy = select_provider(valobj)
        log(lambda: "[END] KonanProxyTypeProvider = {}".format(type(self._proxy).__name__))

    def __getattr__(self, item):
        return getattr(self._proxy, item)


