import os
import sys
import yaml
from datetime import datetime
from typing import Any, Mapping

    
from gmini.Backend.app.models.measure import Measure
from gmini.Backend.app.models.measureResult import MeasureResult
from gmini.Backend.app.models.measureSetup import (
    MultiMeasureSetup,
    SingleMeasureSetup,
    SpecMeasureSetup,
)
from gmini.Backend.app.models.calibrationSetup import CalibrationSetup
from gmini.Backend.app.models.measureSetup import MeasureSetup
# from gmini.Backend.app.models.autosequences import AutoSequence
# from gmini.Backend.app.models.sessions import ExperimentalSession
# from gmini.Backend.app.models.tokens import Token
# from gmini.Backend.app.models.figures import Figure

class LocalService:

    def load_measure(self, path: str) -> Measure:
        with open(path, "r", encoding="utf-8") as measure_file:
            data = yaml.safe_load(measure_file)

        if not isinstance(data, Mapping):
            raise ValueError("A measure YAML file must contain a mapping at its root")

        measure_setup = self.load_setup(
            self._value(data, "measure_setup", required=True)
        )
        device_id = self._value(data, "device_id", required=True)
        measure = Measure(measure_setup=measure_setup, device_id=int(device_id))

        if self._has_value(data, "measure_id"):
            measure.set_id(int(self._value(data, "measure_id")))
        if self._has_value(data, "date"):
            measure._date = self._parse_date(self._value(data, "date"))
        if self._has_value(data, "file_name"):
            measure.set_file_name(str(self._value(data, "file_name")))
        if self._has_value(data, "state"):
            measure.set_state(self._value(data, "state"))
        if self._has_value(data, "device_temp"):
            measure.set_device_temp(float(self._value(data, "device_temp")))
        if self._has_value(data, "observations"):
            measure.set_observations(str(self._value(data, "observations")))
        if self._has_value(data, "loop_group_id"):
            measure._loop_group_id = str(self._value(data, "loop_group_id"))
        if self._has_value(data, "iteration_number"):
            measure.set_iteration_number(int(self._value(data, "iteration_number")))
        if self._has_value(data, "result") and self._value(data, "result") is not None:
            measure.set_result(self._load_measure_result(self._value(data, "result")))

        return measure

    def _load_measure_result(self, data: Any) -> MeasureResult:
        if not isinstance(data, Mapping):
            raise ValueError("'result' must be a mapping")

        impedances = []
        for impedance in self._value(data, "impedances", default=[]):
            if isinstance(impedance, (list, tuple)) and len(impedance) == 2:
                impedances.append(complex(float(impedance[0]), float(impedance[1])))
            else:
                impedances.append(complex(impedance))

        result = MeasureResult(
            frequencies=list(self._value(data, "frequencies", default=[])),
            amplitudes=list(self._value(data, "amplitudes", default=[])),
            phases=list(self._value(data, "phases", default=[])),
            impedances=impedances,
        )
        if self._has_value(data, "m_resul_id"):
            result.set_id(int(self._value(data, "m_resul_id")))
        return result

    @staticmethod
    def _value(
        data: Mapping[str, Any],
        name: str,
        default: Any = None,
        required: bool = False,
    ) -> Any:
        for key in (name, f"_{name}"):
            if key in data:
                return data[key]
        if required:
            raise ValueError(f"Missing required measure field: '{name}'")
        return default

    @classmethod
    def _has_value(cls, data: Mapping[str, Any], name: str) -> bool:
        return name in data or f"_{name}" in data

    @staticmethod
    def _parse_date(value: Any) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError as exc:
                raise ValueError(
                    "The measure date must be an ISO 8601 datetime"
                ) from exc
        raise ValueError("The measure date must be an ISO 8601 datetime")

    def load_calibration_setup(self, path: str) -> CalibrationSetup:
        with open(path, "r", encoding="utf-8") as calibration_file:
            data = yaml.safe_load(calibration_file)

        if not isinstance(data, Mapping):
            raise ValueError(
                "A calibration setup YAML file must contain a mapping at its root"
            )

        mux_channel = self._value(data, "mux_channel", required=True)
        if isinstance(mux_channel, (list, tuple)):
            mux_channels = [int(channel) for channel in mux_channel]
        else:
            # Existing database records can contain a single channel value.
            mux_channels = [int(mux_channel)]

        calibration_setup = CalibrationSetup(
            channel=str(self._value(data, "channel", required=True)),
            z_calc_value_real=float(
                self._value(data, "z_calc_value_real", required=True)
            ),
            z_calc_value_imag=float(
                self._value(data, "z_calc_value_imag", required=True)
            ),
            exitation_voltage=float(
                self._value(data, "exitation_voltage", required=True)
            ),
            gain=float(self._value(data, "gain", required=True)),
            rfbvalue=float(self._value(data, "rfbvalue", required=True)),
            settcycles=int(self._value(data, "settcycles", required=True)),
            mux_channel=mux_channels,
        )

        if self._has_value(data, "cal_setup_id"):
            calibration_setup.set_id(int(self._value(data, "cal_setup_id")))
        if self._has_value(data, "observations"):
            calibration_setup.set_observations(
                str(self._value(data, "observations"))
            )

        return calibration_setup

    def load_setup(self, path: str | Mapping[str, Any]) -> MeasureSetup:
        if isinstance(path, Mapping):
            data = path
        else:
            with open(path, "r", encoding="utf-8") as setup_file:
                data = yaml.safe_load(setup_file)

        if not isinstance(data, Mapping):
            raise ValueError("A setup YAML file must contain a mapping at its root")

        setup_data = self._value(data, "measure_setup", default=data)
        if not isinstance(setup_data, Mapping):
            raise ValueError("'measure_setup' must be a mapping")

        setup_type = self._value(setup_data, "type")
        if setup_type is None:
            if self._has_value(setup_data, "freq"):
                setup_type = "single"
            elif self._has_value(setup_data, "startfreq"):
                setup_type = "spectro"
            elif self._has_value(setup_data, "freq_list"):
                setup_type = "multi"
        if setup_type is None:
            raise ValueError(
                "'measure_setup' must specify a type or recognizable setup fields"
            )

        setup_type = str(setup_type).lower()
        observations = str(self._value(setup_data, "observations", default=""))
        if setup_type in {"single", "singlemeasuresetup"}:
            setup = SingleMeasureSetup(
                freq=float(self._value(setup_data, "freq", required=True)),
                delay=int(self._value(setup_data, "delay", default=0)),
                count=int(self._value(setup_data, "count", default=0)),
            )
        elif setup_type in {"spectro", "spec", "specmeasuresetup"}:
            setup = SpecMeasureSetup(
                startfreq=float(
                    self._value(setup_data, "startfreq", required=True)
                ),
                incfreq=float(self._value(setup_data, "incfreq", required=True)),
                steps=int(self._value(setup_data, "steps", required=True)),
                repeat=int(self._value(setup_data, "repeat", default=1)),
            )
        elif setup_type in {"multi", "multimeasuresetup"}:
            setup = MultiMeasureSetup(
                freq_list=list(
                    self._value(setup_data, "freq_list", required=True)
                )
            )
        else:
            raise ValueError(f"Unknown measure setup type: {setup_type}")

        if self._has_value(setup_data, "measure_setup_id"):
            setup.set_id(int(self._value(setup_data, "measure_setup_id")))
        setup.set_observations(observations)
        return setup

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