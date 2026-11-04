from datetime import datetime

import pytest

from Backend.app.models.measure import Measure
from Backend.app.models.measureResult import MeasureResult
from Backend.app.models.measureSetup import SingleMeasureSetup
from Backend.app.services.localServices import LocalService


def test_load_measure_from_yaml(tmp_path):
    measure_file = tmp_path / "measure.yaml"
    measure_file.write_text(
        """
measure_id: 7
date: 2026-11-04T19:22:50
file_name: demo
state: COMPLETE
device_id: 3
device_temp: 24.5
observations: loaded measure
loop_group_id: group-1
iteration_number: 2
measure_setup:
  type: single
  measure_setup_id: 4
  freq: 1000.0
  delay: 10
  count: 4
  observations: setup notes
result:
  m_resul_id: 8
  frequencies: [1000.0]
  amplitudes: [1.5]
  phases: [0.2]
  impedances: [[10.0, -2.0]]
""",
        encoding="utf-8",
    )

    measure = LocalService().load_measure(str(measure_file))
    setup = measure.get_measure_setup()
    result = measure.get_measure_result()

    assert isinstance(measure, Measure)
    assert measure.get_id() == 7
    assert measure.get_date() == datetime(2026, 11, 4, 19, 22, 50)
    assert measure.get_file_name() == "demo"
    assert measure.get_state() == "COMPLETE"
    assert measure.get_device_id() == 3
    assert measure.get_device_temp() == 24.5
    assert measure.get_observations() == "loaded measure"
    assert measure.get_loop_group_id() == "group-1"
    assert measure.get_iteration_number() == 2

    assert isinstance(setup, SingleMeasureSetup)
    assert setup.get_id() == 4
    assert setup.freq == 1000.0
    assert setup.delay == 10
    assert setup.count == 4
    assert setup._observations == "setup notes"

    assert isinstance(result, MeasureResult)
    assert result.get_id() == 8
    assert result.get_frequencies() == [1000.0]
    assert result.get_amplitudes() == [1.5]
    assert result.get_phases() == [0.2]
    assert result.get_impedances() == [complex(10.0, -2.0)]


def test_load_measure_requires_measure_setup(tmp_path):
    measure_file = tmp_path / "invalid_measure.yaml"
    measure_file.write_text("device_id: 3\n", encoding="utf-8")

    with pytest.raises(ValueError, match="measure_setup"):
        LocalService().load_measure(str(measure_file))
