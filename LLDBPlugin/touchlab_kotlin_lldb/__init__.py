import os

import inspect


from lldb import SBDebugger

from .stepping.KonanHook import KonanHook
from .types import configure_type_provider
from .util.log import log
from .commands import FieldTypeCommand, SymbolByNameCommand, TypeByAddressCommand

# TODO: We need to surface these two so LLDB sees them. Maybe it'd be easier to pass in FQN?
# noinspection PyUnresolvedReferences
from .types import kotlin_object_type_summary, KonanProxyTypeProvider

from .cache import LLDBCache

os.environ['CLIENT_TYPE'] = 'Xcode'

import traceback
import os
import faulthandler
import sys


def __lldb_init_module(debugger: SBDebugger, _):
    print(os.getpid())
    faulthandler.dump_traceback(file=sys.stderr, all_threads=True)

    log(lambda: "init start")

    LLDBCache.reset()

    configure_type_provider(debugger, __name__)

    FieldTypeCommand.register_lldb_command(debugger, __name__)
    SymbolByNameCommand.register_lldb_command(debugger, __name__)
    TypeByAddressCommand.register_lldb_command(debugger, __name__)

    KonanHook.register_stop_hook(debugger, __name__)

    log(lambda: "init end")
