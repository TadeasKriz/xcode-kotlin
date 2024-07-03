from lldb import SBValue

from .base import get_known_type, KnownValueType
from .KonanStringSyntheticProvider import KonanStringSyntheticProvider
from .KonanArraySyntheticProvider import KonanArraySyntheticProvider
from .KonanListSyntheticProvider import KonanListSyntheticProvider
from .KonanObjectSyntheticProvider import KonanObjectSyntheticProvider
from .KonanBaseSyntheticProvider import KonanBaseSyntheticProvider
from ..util import log


def select_provider(valobj: SBValue) -> KonanBaseSyntheticProvider:
    log(lambda: "[BEGIN] select_provider")
    known_type = get_known_type(valobj)
    if known_type == KnownValueType.STRING:
        ret = KonanStringSyntheticProvider(valobj)
    elif known_type == KnownValueType.ARRAY:
        ret = KonanArraySyntheticProvider(valobj)
    elif known_type == KnownValueType.ANY:
        ret = KonanObjectSyntheticProvider(valobj)
    elif known_type == KnownValueType.LIST:
        # ret = KonanObjectSyntheticProvider(valobj)
        ret = KonanListSyntheticProvider(valobj)
    else:
        # TODO: Log warning that we didn't handle a known_type
        ret = KonanObjectSyntheticProvider(valobj)

    log(lambda: "[END] select_provider = {} (known_type: {})".format(
        ret,
        known_type,
    ))
    return ret
