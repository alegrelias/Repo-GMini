from gmini.Backend.app.adapters.iCalibrationAdapter import ICalibrationAdapter
from gmini.Backend.app.models.calibrationSetup import CalibrationSetup

"""Adaptador concreto de calibración para la placa Guanaco Mini"""
class GminiCalibrationAdapter(ICalibrationAdapter):
    RFB_VALUE_TO_BANK = {
        470: 0,
        470.0: 0,
        150: 1,
        150.0: 1,
        1000: 2,
        1000.0: 2
    }

    CHANNEL_MAP = {
        "RCAL1": 0,
        "RCAL2": 1,
        "DUT1": 2,
        "DUT2": 3,
        "OTHER": 2
    }

    def encode(self, setup: CalibrationSetup) -> str:
        commands = []

        voltage = getattr(setup, "_exitation_voltage", None)
        if hasattr(setup, "get_exitation_voltage"):
            voltage = setup.get_exitation_voltage()

        gain = getattr(setup, "_gain", None)
        if hasattr(setup, "get_gain"):
            gain = setup.get_gain()

        rfb_val = getattr(setup, "_rfbvalue", None)
        if hasattr(setup, "get_rfbvalue"):
            rfb_val = setup.get_rfbvalue()

        cycles = getattr(setup, "_settcycles", None)
        if hasattr(setup, "get_settcycles"):
            cycles = setup.get_settcycles()

        if voltage is not None:
            commands.append(f"voltage {int(voltage)}")
        if gain is not None:
            commands.append(f"gain {int(gain)}")
        if rfb_val is not None:
            bank_idx = self.RFB_VALUE_TO_BANK.get(rfb_val, int(rfb_val) if int(rfb_val) in [0, 1, 2, 3] else 0)
            commands.append(f"setrfb {bank_idx}")
        if cycles is not None:
            commands.append(f"settcycles {int(cycles)}")

        raw_channel = getattr(setup, "_channel", getattr(setup, "_mux_channel", 0))
        if hasattr(setup, "get_mux_channel"):
            raw_channel = setup.get_mux_channel()
        elif hasattr(setup, "get_channel"):
            raw_channel = setup.get_channel()

        if isinstance(raw_channel, str):
            ch_upper = raw_channel.strip().upper()
            channel_idx = self.CHANNEL_MAP.get(ch_upper, int(ch_upper) if ch_upper.isdigit() else 0)
        else:
            channel_idx = int(raw_channel)

        z_real = getattr(setup, "_z_calc_value_real", None)
        if hasattr(setup, "get_z_calc_value_real"):
            z_real = setup.get_z_calc_value_real()

        if channel_idx in (2, 3) and z_real is not None and z_real > 0:
            commands.append(f"calibrate {channel_idx} {z_real}")
        else:
            commands.append(f"calibrate {channel_idx}")

        return "\n".join(commands) + "\n"

    def decode(self, response: str) -> bool:
        if response is None:
            return False

        clean = response.strip().upper()
        if clean == "" or clean == "0" or "OK" in clean:
            return True

        error_tokens = ["-1", "-2", "-3", "-4", "-5", "ERR", "FAIL", "RES_"]
        for token in error_tokens:
            if clean == token or token in clean:
                return False

        return True