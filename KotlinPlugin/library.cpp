#include "library.h"

#include "lldb/API/SBCommandInterpreter.h"
#include "lldb/API/SBCommandReturnObject.h"
#include "lldb/API/SBDebugger.h"
#include "lldb/API/LLDB.h"

#define API __attribute__((used))

namespace lldb {
    API bool PluginInitialize(lldb::SBDebugger debugger);
}

class NyanCatCommand: public lldb::SBCommandPluginInterface {
public:
    bool DoExecute(lldb::SBDebugger debugger, char **commnds, lldb::SBCommandReturnObject& result) override {
        result.Printf("hello from nyan cat\n");
        return true;
    }
};

class ChildCommand : public lldb::SBCommandPluginInterface {
public:
    virtual bool DoExecute(lldb::SBDebugger debugger, char **command,
                           lldb::SBCommandReturnObject &result) {
        if (command) {
            const char *arg = *command;
            while (arg) {
                result.Printf("%s\n", arg);
                arg = *(++command);
            }
            return true;
        }
        return false;
    }
};

API bool lldb::PluginInitialize(lldb::SBDebugger debugger) {
    printf("hello from a plugin\n");

    lldb::SBCommandInterpreter interpreter = debugger.GetCommandInterpreter();
    lldb::SBCommand foo = interpreter.AddMultiwordCommand("custom", "my custom commands");
    foo.AddCommand("nyancat", new NyanCatCommand(), "a nyancat command");
//    lldb::SBCommandInterpreter interpreter = debugger.GetCommandInterpreter();
//    lldb::SBCommand foo = interpreter.AddMultiwordCommand("foo", NULL);
//    foo.AddCommand("child", new ChildCommand(), "a child of foo");

    SBTypeCategory category = debugger.CreateCategory("Kotlin");
//    category.AddLanguage(lldb::eLanguageTypeKotlin);

    category.AddTypeSummary(
        SBTypeNameSpecifier("ObjHeader *"),
        SBTypeSummary::CreateWithCallback([](lldb::SBValue value, lldb::SBTypeSummaryOptions options, lldb::SBStream &stream) -> bool {
            printf("TypeSummary(%llu)", value.GetLoadAddress());

            const char* fallback = value.GetValue();

            auto debug_buffer_addr = value.GetFrame().EvaluateExpression("(void*)Konan_DebugBuffer()").GetValueAsUnsigned();
            auto debug_buffer_size = value.GetFrame().EvaluateExpression("(int)Konan_DebugBufferSize()").GetValueAsUnsigned();

            auto expression = "(int)Konan_DebugObjectToUtf8Array((void*)" + std::to_string(value.GetValueAsUnsigned()) + ", (void*)" + std::to_string(debug_buffer_addr) + ", " + std::to_string(debug_buffer_size) + ");";
            auto string_len = value.GetFrame().EvaluateExpression(
                expression.c_str()
            ).GetValueAsSigned();

            SBError error;
            auto buffer = malloc(string_len);
            value.GetProcess().ReadCStringFromMemory(debug_buffer_addr, buffer, string_len, error);
            stream.Printf("%s", (char*)buffer);

            return true;
        })
    );
    category.AddTypeSynthetic(
        SBTypeNameSpecifier("ObjHeader *"),
        SBTypeSynthetic::CreateWithClassName(
            "TestClass"
        )
    );

//    category.AddTypeFormat(
//            SBTypeNameSpecifier(),
//            SBTypeFormat()
//            )

    category.SetEnabled(true);

    return true;
}

enum KnownValueType {
    Any = 0,
    String = 1,
    Array = 2,
    List = 3,
};

KnownValueType GetKnownType(lldb::SBValue value) {
//    "error! value was " + std::to_string(actualValue) + " but I expected " + std::to_string(expectedValue);
//
//
//
//    auto is_string = "(int)Konan_DebugIsInstance(" + std::to_string(value.GetLoadAddress()) + ")";
//
//    value.GetFrame().EvaluateExpression()

    return List;
}