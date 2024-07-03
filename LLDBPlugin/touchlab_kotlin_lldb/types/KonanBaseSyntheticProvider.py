from lldb import SBSyntheticValueProvider, SBValue


class KonanBaseSyntheticProvider(SBSyntheticValueProvider):
    def __init__(self, valobj: SBValue):
        super().__init__(valobj)
