from gmini.Backend.app.builders.baseMeasureSetupBuilder import BaseMeasureSetupBuilder
from gmini.Backend.app.builders.spectroSetupBuilder import SpectroSetupBuilder
from gmini.Backend.app.builders.singleFreqSetupBuilder import SingleFreqSetupBuilder
from gmini.Backend.app.builders.multiFreqSetupBuilder import MultiFreqSetupBuilder


class MeasureSetupBuilderFactory:
    @staticmethod
    def create_builder(mode: str) -> BaseMeasureSetupBuilder:
        clean_mode = mode.strip().lower()
        if clean_mode in ("spectro", "sweep", "spec", "espectroscopia"):
            return SpectroSetupBuilder()
        elif clean_mode in ("single", "singlefreq", "monofrecuencia"):
            return SingleFreqSetupBuilder()
        elif clean_mode in ("multi", "multifreq", "multifrecuencia"):
            return MultiFreqSetupBuilder()
        else:
            raise ValueError(f"Modo de builder desconocido: {mode}")