//
// Created by Tadeas Kriz on 2024-06-28.
//

#include "language.h"

#include "lldb/Core/PluginManager.h"

#include "lldb/DataFormatters/DataVisualization.h"

#include "lldb/Symbol/CompileUnit.h"
#include "lldb/Symbol/Function.h"

using namespace lldb;
using namespace lldb_private;

LLDB_PLUGIN_DEFINE(KotlinLanguage);

void KotlinLanguage::Initialize() {
    printf("Initialize!");
}

void KotlinLanguage::Terminate() {
    printf("Terminate!");
}

lldb_private::ConstString KotlinLanguage::GetPluginNameStatic() {
    static ConstString g_name("kotlin");
    return g_name;
}

bool KotlinLanguage::SymbolNameFitsToLanguage(lldb_private::Mangled mangled) const {
    printf("KotlinLanguage::SymbolNameFitsToLanguage(%s)", mangled.GetMangledName().GetCString());
    return true;
}

bool KotlinLanguage::IsTopLevelFunction(lldb_private::Function &function) {
    static ConstString g_main("main");
    if (CompileUnit* comp_unit = function.GetCompileUnit()) {
        if (comp_unit->GetLanguage() == lldb::eLanguageTypeKotlin) {
            if (function.GetMangled().GetMangledName() == g_main) {
                return true;
            }
        }
    }
    return false;
}

std::vector<Language::MethodNameVariant> KotlinLanguage::GetMethodNameVariants(
        lldb_private::ConstString method_name) const {
    std::vector<Language::MethodNameVariant> variant_names;

    // NOTE:  We need to do this because we don't have a proper parser for Kotlin
    // function name syntax so we try to ensure that if we autocomplete to
    // something, we'll look for its mangled equivalent and use the mangled
    // version as a lookup as well.

    ConstString counterpart;
    if (method_name.GetMangledCounterpart(counterpart)) {
        if (false /*SwiftLanguageRuntime::IsSwiftMangledName(counterpart.GetStringRef())*/) {
            variant_names.emplace_back(counterpart, eFunctionNameTypeFull);
        }
    }
    return variant_names;
}

static void LoadKotlinFormatters(lldb::TypeCategoryImplSP kotlin_category_sp) {

}

lldb::TypeCategoryImplSP KotlinLanguage::GetFormatters() {
    static std::once_flag g_initialize;
    static TypeCategoryImplSP g_category;

    std::call_once(g_initialize, [this]() -> void {
        DataVisualization::Categories::GetCategory(ConstString(GetPluginName()), g_category);

        if (g_category) {
            LoadKotlinFormatters(g_category);
        }
    });
    return g_category;
}

HardcodedFormatters::HardcodedSummaryFinder KotlinLanguage::GetHardcodedSummaries() {
    static std::once_flag g_initialize;
    static HardcodedFormatters::HardcodedSummaryFinder g_formatters;

    std::call_once(g_initialize, []() -> void {

    });
    return g_formatters;
}

HardcodedFormatters::HardcodedSyntheticFinder KotlinLanguage::GetHardcodedSynthetics() {
    static std::once_flag g_initialize;
    static ConstString g_runtime_synths_category_name("runtime-synthetics");
    static HardcodedFormatters::HardcodedSyntheticFinder g_formatters;

    std::call_once(g_initialize, []() -> void {

    });
    return g_formatters;
}

bool KotlinLanguage::IsSourceFile(llvm::StringRef file_path) const {
    return file_path.endswith(".kt");
}

//std::vector<ConstString> KotlinLanguage::GetPossibleFormattersMatches(
//        lldb_private::ValueObject &valobj, lldb::DynamicValueType use_dynamic) {
//    std::vector<ConstString> result;
//
//    if (use_dynamic == lldb::eNoDynamicValues) {
//        return result;
//    }
//
//    return result;
//}

std::unique_ptr<Language::TypeScavenger> KotlinLanguage::GetTypeScavenger() {
    return nullptr;
}

const char* KotlinLanguage::GetLanguageSpecificTypeLookupHelp() {
    return "\nFor Kotlin, in addition to a simple type name (such as String, Int, "
           "NSObject, ..), one can also provide:\n"
           "- a mangled type name (e.g. $sSiD)\n"
           "- the name of a function, even if multiple overloads of it exist\n"
           "- the name of an operator\n"
           "- the name of a module available in the current target, which will "
           "print all types and declarations available in that module";
}

//bool KotlinLanguage::GetFormatterPrefixSuffix(lldb_private::ValueObject &valobj, lldb_private::ConstString type_hint,
//                                              std::string &prefix, std::string &suffix) {
//
//    return false;
//}

DumpValueObjectOptions::DeclPrintingHelper KotlinLanguage::GetDeclPrintingHelper() {
    return [](ConstString type_name, ConstString var_name, const DumpValueObjectOptions &options, Stream &stream) -> bool {
        std::string type_name_str(type_name ? type_name.GetCString() : "");

        return true;
    };
}

LazyBool KotlinLanguage::IsLogicalTrue(lldb_private::ValueObject &valobj, lldb_private::Status &error) {
    error.SetErrorString("not a Kotlin boolean type");
    return eLazyBoolNo;
}

bool KotlinLanguage::IsUninitializedReference(lldb_private::ValueObject &valobj) {
    return true;
}

bool KotlinLanguage::GetFunctionDisplayName(const lldb_private::SymbolContext *sc,
                                            const lldb_private::ExecutionContext *exe_ctx,
                                            lldb_private::Language::FunctionNameRepresentation representation,
                                            lldb_private::Stream &s) {
    return false;
}

void KotlinLanguage::GetExceptionResolverDescription(bool catch_on, bool throw_on, lldb_private::Stream &s) {
    s.Printf("Kotlin Error breakpoint");
}

Language* KotlinLanguage::CreateInstance(lldb::LanguageType language) {
    switch (language) {
        case lldb::eLanguageTypeKotlin:
            return new KotlinLanguage();
        default:
            return nullptr;
    }
}