import os,sys

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ruta_raiz not in sys.path:
    sys.path.append(ruta_raiz)
    
from Backend.app.models.measure import Measure
from Backend.app.models.calibrationSetup import CalibrationSetup
from Backend.app.models.measureSetup import MeasureSetup
# from Backend.app.models.autosequences import AutoSequence
# from Backend.app.models.sessions import ExperimentalSession
# from Backend.app.models.tokens import Token
# from Backend.app.models.figures import Figure

class LocalService:

    def load_measure(self, path: str) -> Measure:
        pass

    def load_calibration_setup(self, path: str) -> CalibrationSetup:
        pass

    def load_setup(self, path: str) -> MeasureSetup:
        pass

    # def load_auto_sequence(self, path: str) -> AutoSequence:
       # pass

    # def load_experimental_session(self, path: str) -> ExperimentalSession:
        # pass

    # def load_user_token(self, path: str) -> Token:
        # pass

    def export_setup_to_file(self, path: str, setup: MeasureSetup):
        pass

    def export_calibration_setup_to_file(self, path: str, setup: CalibrationSetup):
        pass

    def export_measure_to_file(self, path: str, measure: Measure):
        pass

    # def export_auto_sequence_to_file(self, path: str, sequence: AutoSequence):
        # pass

    # def export_experimental_session_to_file(self, path: str, exp_session: ExperimentalSession):
        # pass

    # def export_user_token(self, path: str, token: Token):
        # pass

    # def export_plot(self, path: str, figure: Figure):
        # pass

    def delete_token(self):
        pass