import pytest

from gmini.Backend.app.models.measureSetup import (
    MultiMeasureSetup,
    SingleMeasureSetup,
    SpecMeasureSetup,
)
from gmini.Backend.app.services.localServices import LocalService


def test_load_single_setup_from_yaml(tmp_path):
    setup_file = tmp_path / "single_setup.yaml"
    setup_file.write_text(
        """
type: single
measure_setup_id: 4
freq: 1000.0
delay: 10
count: 4
observations: setup notes
""",
        encoding="utf-8",
    )

    setup = LocalService().load_setup(str(setup_file))

    assert isinstance(setup, SingleMeasureSetup)
    assert setup.get_id() == 4
    assert setup.freq == 1000.0
    assert setup.delay == 10
    assert setup.count == 4
    assert setup._observations == "setup notes"


@pytest.mark.parametrize(
    ("yaml_content", "setup_type"),
    [
        (
            """
type: spectro
startfreq: 10000.0
incfreq: 500.0
steps: 10
repeat: 2
""",
            SpecMeasureSetup,
        ),
        (
            """
type: multi
freq_list: [1000.0, 5000.0, 10000.0]
""",
            MultiMeasureSetup,
        ),
    ],
)
def test_load_setup_supports_all_setup_types(tmp_path, yaml_content, setup_type):
    setup_file = tmp_path / "setup.yaml"
    setup_file.write_text(yaml_content, encoding="utf-8")

    setup = LocalService().load_setup(str(setup_file))

    assert isinstance(setup, setup_type)


def test_load_setup_accepts_measure_setup_wrapper(tmp_path):
    setup_file = tmp_path / "wrapped_setup.yaml"
    setup_file.write_text(
        """
measure_setup:
  type: single
  freq: 2000.0
  delay: 1
  count: 2
""",
        encoding="utf-8",
    )

    setup = LocalService().load_setup(str(setup_file))

    assert isinstance(setup, SingleMeasureSetup)
    assert setup.freq == 2000.0


def test_load_setup_rejects_non_mapping_yaml(tmp_path):
    setup_file = tmp_path / "invalid_setup.yaml"
    setup_file.write_text("- single\n- 1000\n", encoding="utf-8")

    with pytest.raises(ValueError, match="mapping"):
        LocalService().load_setup(str(setup_file))
