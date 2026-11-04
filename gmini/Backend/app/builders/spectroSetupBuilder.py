from app.builders.baseMeasureSetupBuilder import BaseMeasureSetupBuilder
from app.models.measureSetup import SpecMeasureSetup

#constructor concreto para mediciones por Espectroscopia (Barrido espectral)
class SpectroSetupBuilder(BaseMeasureSetupBuilder):
    
    def __init__(self):
        super().__init__()
        self._startfreq: float = 0.0
        self._incfreq: float = 0.0
        self._steps: int = 0
        self._repeat: int = 1 

    def with_start_freq(self, startfreq: float) -> 'SpectroSetupBuilder':
        self._startfreq = startfreq
        return self

    def with_inc_freq(self, incfreq: float) -> 'SpectroSetupBuilder':
        self._incfreq = incfreq
        return self

    def with_steps(self, steps: int) -> 'SpectroSetupBuilder':
        self._steps = steps
        return self

    def with_repeat(self, repeat: int) -> 'SpectroSetupBuilder':
        self._repeat = repeat
        return self

    def build(self) -> SpecMeasureSetup:
        #Instancia la entidad pura con los parámetros del espectro
        setup = SpecMeasureSetup(
            startfreq=self._startfreq,
            incfreq=self._incfreq,
            steps=self._steps,
            repeat=self._repeat
        )
        #Asigna los atributos comunes heredados del BaseMeasureSetupBuilder
        setup.set_observations(self._observations)
        
        return setup