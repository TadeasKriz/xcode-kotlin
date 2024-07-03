//
// Created by Tadeas Kriz on 2024-06-28.
//

#ifndef KOTLINPLUGIN_LANGUAGE_H
#define KOTLINPLUGIN_LANGUAGE_H

#include "lldb/Target/Language.h"
#include "lldb/lldb-private.h"

namespace lldb_private {

    class KotlinLanguage: public Language {
    public:
        virtual ~KotlinLanguage() = default;

        KotlinLanguage() = default;

        lldb::LanguageType GetLanguageType() const override {
            return lldb::eLanguageTypeKotlin;
        }

        bool IsTopLevelFunction(Function &function) override;

        std::vector<Language::MethodNameVariant>
        GetMethodNameVariants(ConstString method_name) const override;

        lldb::TypeCategoryImplSP GetFormatters() override;

        HardcodedFormatters::HardcodedSummaryFinder GetHardcodedSummaries() override;

        HardcodedFormatters::HardcodedSyntheticFinder
        GetHardcodedSynthetics() override;

        bool IsSourceFile(llvm::StringRef file_path) const override;

//        std::vector<ConstString>
//        GetPossibleFormattersMatches(ValueObject &valobj,
//                                     lldb::DynamicValueType use_dynamic) override;


        std::unique_ptr<TypeScavenger> GetTypeScavenger() override;

        const char *GetLanguageSpecificTypeLookupHelp() override;

//        bool GetFormatterPrefixSuffix(ValueObject &valobj, ConstString type_hint,
//                                      std::string &prefix,
//                                      std::string &suffix) override;

//        virtual std::pair<llvm::StringRef, llvm::StringRef>
//        GetFormatterPrefixSuffix(llvm::StringRef type_hint);

        DumpValueObjectOptions::DeclPrintingHelper GetDeclPrintingHelper() override;

        LazyBool IsLogicalTrue(ValueObject &valobj, Status &error) override;

        bool IsUninitializedReference(ValueObject &valobj) override;

        bool GetFunctionDisplayName(const SymbolContext *sc,
                                    const ExecutionContext *exe_ctx,
                                    FunctionNameRepresentation representation,
                                    Stream &s) override;

        void GetExceptionResolverDescription(bool catch_on, bool throw_on,
                                             Stream &s) override;

        ConstString
        GetDemangledFunctionNameWithoutArguments(Mangled mangled) const override;

        //------------------------------------------------------------------
        // Static Functions
        //------------------------------------------------------------------
        static void Initialize();

        static void Terminate();

        static lldb_private::Language* CreateInstance(lldb::LanguageType language);

        static lldb_private::ConstString GetPluginNameStatic();

        bool SymbolNameFitsToLanguage(Mangled mangled) const override;

        //------------------------------------------------------------------
        // PluginInterface protocol
        //------------------------------------------------------------------
        llvm::StringRef GetPluginName() override {
            return GetPluginNameStatic().GetStringRef();
        }
    };
}

#endif //KOTLINPLUGIN_LANGUAGE_H
