from typing import List
from app.builders.baseMeasureSetupBuilder import BaseMeasureSetupBuilder
from app.models.measureSetup import MultiMeasureSetup

#Constructor concreto para mediciones de Multifrecuencia
class MultiFreqSetupBuilder(BaseMeasureSetupBuilder):
    def __init__(self):
        super().__init__()
        self._freq_list: List[float] = []

    def with_freq_list(self, freq_list: List[float]) -> 'MultiFreqSetupBuilder':
        self._freq_list = freq_list
        return self

    def build(self) -> MultiMeasureSetup:
        return MultiMeasureSetup(
            freq_list=self._freq_list,
            observations=self._observations
        )