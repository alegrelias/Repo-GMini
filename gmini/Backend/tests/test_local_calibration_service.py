import pytest

from Backend.app.models.calibrationSetup import CalibrationSetup
from Backend.app.services.localServices import LocalService


def test_load_calibration_setup_from_yaml(tmp_path):
    calibration_file = tmp_path / "calibration.yaml"
    calibration_file.write_text(
        """
cal_setup_id: 12
observations: reference resistor
channel: CH1
z_calc_value_real: 1000.5
z_calc_value_imag: -2.25
exitation_voltage: 400.0
gain: 1.0
rfbvalue: 470.0
settcycles: 15
mux_channel: [0, 1]
""",
        encoding="utf-8",
    )

    setup = LocalService().load_calibration_setup(str(calibration_file))

    assert isinstance(setup, CalibrationSetup)
    assert setup.get_id() == 12
    assert setup.get_observations() == "reference resistor"
    assert setup.get_channel() == "CH1"
    assert setup.get_z_calc_value_real() == 1000.5
    assert setup.get_z_calc_value_imag() == -2.25
    assert setup.get_exitation_voltage() == 400.0
    assert setup.get_gain() == 1.0
    assert setup.get_rfbvalue() == 470.0
    assert setup.get_settcycles() == 15
    assert setup.get_mux_channel() == [0, 1]


def test_load_calibration_setup_normalizes_single_mux_channel(tmp_path):
    calibration_file = tmp_path / "calibration.yaml"
    calibration_file.write_text(
        """
channel: CH0
z_calc_value_real: 1000.0
z_calc_value_imag: 0.0
exitation_voltage: 400.0
gain: 1.0
rfbvalue: 470.0
settcycles: 15
mux_channel: 0
""",
        encoding="utf-8",
    )

    setup = LocalService().load_calibration_setup(str(calibration_file))

    assert setup.get_mux_channel() == [0]


def test_load_calibration_setup_requires_all_fields(tmp_path):
    calibration_file = tmp_path / "invalid_calibration.yaml"
    calibration_file.write_text(
        "channel: CH1\nmux_channel: 0\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="z_calc_value_real"):
        LocalService().load_calibration_setup(str(calibration_file))
