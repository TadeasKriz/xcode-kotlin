from lldb import SBDebugger, SBValue

from .KonanArraySyntheticProvider import KonanArraySyntheticProvider
from .KonanObjectSyntheticProvider import KonanObjectSyntheticProvider
from .KonanProxyTypeProvider import KonanProxyTypeProvider, select_provider
from .KonanStringSyntheticProvider import KonanStringSyntheticProvider
from .KonanListSyntheticProvider import KonanListSyntheticProvider
from .base import KOTLIN_NATIVE_TYPE, KOTLIN_CATEGORY, type_info
from ..util import log, NULL


def configure_type_provider(debugger: SBDebugger, module_name):
    # debugger.HandleCommand(
    #     'type summary add --no-value --expand --python-function {}.{} "{}" --category {}'.format(
    #         module_name,
    #         kotlin_object_type_summary.__name__,
    #         KOTLIN_NATIVE_TYPE,
    #         KOTLIN_CATEGORY,
    #     )
    # )

    debugger.HandleCommand(
        'type summary add "ObjHeader *" --expand --summary-string "${svar%#} items"'
    )

    KonanProxyTypeProvider.register_type_provider(debugger, module_name)

    debugger.HandleCommand('type category enable {}'.format(KOTLIN_CATEGORY))

def kotlin_object_type_summary(valobj: SBValue, internal_dict):
    """Hook that is run by lldb to display a Kotlin object."""
    log(lambda: "kotlin_object_type_summary({:#x}: {})".format(valobj.unsigned, valobj.type.name))
    if valobj.GetTypeName() != KOTLIN_NATIVE_TYPE:
        if valobj.GetValue() is None:
            return NULL
        return valobj.GetValue()

    if valobj.unsigned == 0:
        return NULL
    tip = internal_dict["type_info"] if "type_info" in internal_dict.keys() else type_info(valobj)

    if not tip:
        return valobj.GetValue()

    provider = select_provider(valobj)
    log(lambda: "kotlin_object_type_summary({:#x} - {})".format(valobj.unsigned, type(provider).__name__))
    return '{} (from: {})'.format(provider.to_string(), type(provider).__name__)
