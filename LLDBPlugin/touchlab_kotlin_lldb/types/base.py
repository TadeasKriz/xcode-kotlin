import lldb
from lldb import SBValue, SBTypeNameSpecifier

from ..util import strip_quotes, log, evaluate
from ..cache import LLDBCache

KOTLIN_NATIVE_TYPE = 'ObjHeader *'
KOTLIN_CATEGORY = 'Kotlin'

_TYPE_CONVERSION = [
    lambda obj, value, address, name: value.CreateValueFromExpression(name, "(void *){:#x}".format(address)),
    lambda obj, value, address, name: value.CreateValueFromAddress(name, address, value.type),
    lambda obj, value, address, name: value.CreateValueFromExpression(name, "(int8_t *){:#x}".format(address)),
    lambda obj, value, address, name: value.CreateValueFromExpression(name, "(int16_t *){:#x}".format(address)),
    lambda obj, value, address, name: value.CreateValueFromExpression(name, "(int32_t *){:#x}".format(address)),
    lambda obj, value, address, name: value.CreateValueFromExpression(name, "(int64_t *){:#x}".format(address)),
    lambda obj, value, address, name: value.CreateValueFromExpression(name, "(float *){:#x}".format(address)),
    lambda obj, value, address, name: value.CreateValueFromExpression(name, "(double *){:#x}".format(address)),
    lambda obj, value, address, name: value.CreateValueFromExpression(name, "(void **){:#x}".format(address)),
    lambda obj, value, address, name: value.CreateValueFromExpression(name, "(bool *){:#x}".format(address)),
    lambda obj, value, address, name: None
]

_TYPES = [
    lambda x: x.GetType().GetBasicType(lldb.eBasicTypeVoid).GetPointerType(),
    lambda x: x.GetType(),
    lambda x: x.GetType().GetBasicType(lldb.eBasicTypeChar),
    lambda x: x.GetType().GetBasicType(lldb.eBasicTypeShort),
    lambda x: x.GetType().GetBasicType(lldb.eBasicTypeInt),
    lambda x: x.GetType().GetBasicType(lldb.eBasicTypeLongLong),
    lambda x: x.GetType().GetBasicType(lldb.eBasicTypeFloat),
    lambda x: x.GetType().GetBasicType(lldb.eBasicTypeDouble),
    lambda x: x.GetType().GetBasicType(lldb.eBasicTypeVoid).GetPointerType(),
    lambda x: x.GetType().GetBasicType(lldb.eBasicTypeBool)
]


def get_runtime_type(variable):
    return strip_quotes(evaluate("(char *)Konan_DebugGetTypeName({:#x})".format(variable.unsigned)).summary)


def get_field_address(parent: SBValue, index):
    return evaluate('(void*)Konan_DebugGetFieldAddress({:#x}, {})'.format(parent.unsigned, index)).unsigned


def get_field_type(parent: SBValue, index):
    return evaluate('(int)Konan_DebugGetFieldType({:#x}, {})'.format(parent.unsigned, index)).unsigned


def _symbol_loaded_address(name, debugger):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    frame = thread.GetSelectedFrame()
    candidates = frame.module.symbol[name]
    # take first
    for candidate in candidates:
        address = candidate.GetStartAddress().GetLoadAddress(target)
        log(lambda: "_symbol_loaded_address:{} {:#x}".format(name, address))
        return address

    return 0


def GetStringSymbolAddress() -> int:
    self = LLDBCache.instance()
    if self._string_symbol_addr is None:
        self._string_symbol_addr = _symbol_loaded_address('kclass:kotlin.String', lldb.debugger)
    return self._string_symbol_addr


def GetListSymbolAddress() -> int:
    self = LLDBCache.instance()
    if self._list_symbol_addr is None:
        self._list_symbol_addr = _symbol_loaded_address('kclass:kotlin.collections.List', lldb.debugger)
    return self._list_symbol_addr


def is_string_or_array(value):
    soa = evaluate(
        "(int)Konan_DebugIsInstance({0:#x}, {1:#x}) ? 1 : ((int)Konan_DebugIsArray({0:#x}) ? 2 : 0)".format(
            value.unsigned,
            GetStringSymbolAddress(),
        )
    ).unsigned
    log(lambda: "is_string_or_array:{:#x}:{}".format(value.unsigned, soa))
    return soa


class KnownValueType:
    ANY = 0
    STRING = 1
    ARRAY = 2
    LIST = 3

    entries = [ANY, STRING, ARRAY, LIST]

    @staticmethod
    def value_of(raw: int):
        assert KnownValueType.ANY <= raw <= KnownValueType.LIST
        return KnownValueType.entries[raw]


def get_known_type(value: SBValue):
    is_string = '(int)Konan_DebugIsInstance({:#x}, {:#x}) ? {}'.format(
        value.unsigned,
        GetStringSymbolAddress(),
        KnownValueType.STRING,
    )
    is_array = '(int)Konan_DebugIsArray({:#x}) ? {}'.format(
        value.unsigned,
        KnownValueType.ARRAY,
    )
    is_list = '(int)Konan_DebugIsInstance({:#x}, {:#x}) ? {}'.format(
        value.unsigned,
        GetListSymbolAddress(),
        KnownValueType.LIST,
    )

    raw = evaluate(
        '{} : {} : {} : {}'.format(
            is_string,
            is_array,
            is_list,
            KnownValueType.ANY,
        )
    ).unsigned
    log(lambda: "get_known_type:{}".format(raw))
    known_type = KnownValueType.value_of(raw)
    log(lambda: "get_known_type:{}".format(known_type))
    return known_type


def type_info(value):
    """
    This method checks self-referencing of pointer of first member of TypeInfo including case when object has an
    meta-object pointed by TypeInfo. Two lower bits are reserved for memory management needs see runtime/src/main/cpp/Memory.h.
    """
    log(lambda: "type_info({:#x}: {})".format(value.unsigned, value.GetTypeName()))
    if value.GetTypeName() != KOTLIN_NATIVE_TYPE:
        return None
    expr = "*(void **)((uintptr_t)(*(void**){0:#x}) & ~0x3) == **(void***)((uintptr_t)(*(void**){0:#x}) & ~0x3) " \
           "? *(void **)((uintptr_t)(*(void**){0:#x}) & ~0x3) : (void *)0".format(value.unsigned)
    result = evaluate(expr)

    return result.unsigned if result.IsValid() and result.unsigned != 0 else None
