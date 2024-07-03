import lldb
from lldb import SBExpressionOptions
from .log import log


def initialize_expression_options():
    options = SBExpressionOptions()
    options.SetIgnoreBreakpoints(True)
    options.SetAutoApplyFixIts(False)
    options.SetFetchDynamicValue(False)
    options.SetGenerateDebugInfo(False)
    options.SetSuppressPersistentResult(True)
    return options


EXPRESSION_OPTIONS = initialize_expression_options()


def evaluate(expr):
    log(lambda: "evaluate: target={}".format(lldb.debugger.GetSelectedTarget()))
    result = lldb.debugger.GetSelectedTarget().EvaluateExpression(expr, EXPRESSION_OPTIONS)
    log(lambda: "evaluate: {} => {}".format(expr, result))
    return result
