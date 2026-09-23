from abc import ABC, abstractmethod


"""
NOTA: las fuciones 'do_measure' solo son de referencia
"""
class Measure(ABC):
    def __init__(self, measure_setup):
        self.measure_setup = measure_setup

    @abstractmethod
    def do_measure(self):
        pass

class SingleFreq(Measure):
    def __init__(self, measure_setup):
        super().__init__(measure_setup)

    def do_measure(self):
        return self.measure_setup.x + self.measure_setup.y + self.measure_setup.z

class MultiFreq(Measure):
    def __init__(self, measure_setup):
            super().__init__(measure_setup)

    def do_measure(self):
            return (self.measure_setup.x * self.measure_setup.y) + self.measure_setup.z

class Spectroscopy(Measure):
    def __init__(self, measure_setup):
            super().__init__(measure_setup)
    
    def do_measure(self):
            return (self.measure_setup.x * self.measure_setup.y) - self.measure_setup.z

class MeasureSetup:
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None

    def __str__(self):
        return (f"  - X: {self.x}\n"
                f"  - Y: {self.y}\n"
                f"  - Z: {self.z}\n")

class MeasureSetupBuilder:
    def __init__(self):
        self.m_setup = MeasureSetup()

    def set_x(self, x):
        self.m_setup.x = x
        return self

    def set_y(self, y):
            self.m_setup.y = y
            return self

    def set_z(self, z):
            self.m_setup.z = z
            return self

    def build(self) -> MeasureSetup:
        return self.m_setup

class MeasureService:

    def make_hw_configuration(self, x, y, z) -> MeasureSetup:
        hw_config = (MeasureSetupBuilder()
                    .set_x(x)
                    .set_y(y)
                    .set_z(z)
                    .build())

        return hw_config

    def ejecute_measure(self, measure):
        result = measure.do_measure()
        print(f"measure result: ({type(measure).__name__}) {result}")

m_service = MeasureService()

hw_config = m_service.make_hw_configuration(1, 2, 3)

my_sfreq_measure = SingleFreq(hw_config)

m_service.ejecute_measure(my_sfreq_measure)
