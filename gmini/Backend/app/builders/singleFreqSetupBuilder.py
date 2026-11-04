from app.builders.baseMeasureSetupBuilder import BaseMeasureSetupBuilder
from app.models.measureSetup import SingleMeasureSetup

class SingleFreqSetupBuilder(BaseMeasureSetupBuilder):
    """Constructor concreto para mediciones de Monofrecuencia."""
    def __init__(self):
        super().__init__()
        self._freq: float = 0.0
        self._delay: int = 0
        self._count: int = 0

    def with_freq(self, freq: float) -> 'SingleFreqSetupBuilder':
        self._freq = freq
        return self

    def with_delay(self, delay: int) -> 'SingleFreqSetupBuilder':
        self._delay = delay
        return self

    def with_count(self, count: int) -> 'SingleFreqSetupBuilder':
        self._count = count
        return self
          #Construye la entidad solo con sus parámetros especificos
    def build(self) -> SingleMeasureSetup:
        setup = SingleMeasureSetup(
            freq=self._freq,
            delay=self._delay,
            count=self._count
        )
        setup.set_observations(self._observations)
        return setup