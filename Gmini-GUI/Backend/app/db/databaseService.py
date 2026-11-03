import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from app.models.user import User
from app.models.measure import Measure
from app.models.measureResult import MeasureResult
from app.models.calibrationSetup import CalibrationSetup
from app.models.measureSetup import (MeasureSetup, SpecMeasureSetup, SingleMeasureSetup, MultiMeasureSetup)
from app.models.experimentalSession import ExperimentalSession
from app.builders.spectroSetupBuilder import SpectroSetupBuilder
from app.builders.singleFreqSetupBuilder import SingleFreqSetupBuilder
from app.builders.multiFreqSetupBuilder import MultiFreqSetupBuilder


class DataBaseService:
    def __init__(self, db_root: str = "gmini_database.db"):
        self._db_root = db_root
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_root)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Crea todas las tablas del MER/DER si no existen."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            #Tabla USER
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS USER (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    user_name TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    root_directory TEXT
                )
            """)

            #Tabla DEVICE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS DEVICE (
                    device_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_name TEXT
                )
            """)

            #Tabla EXPERIMENTAL_SESSION
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS EXPERIMENTAL_SESSION (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    observations TEXT,
                    FOREIGN KEY (user_id) REFERENCES USER(user_id)
                )
            """)

            #Tabla CALIBRATION_SETUP
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS CALIBRATION_SETUP (
                    cal_setup_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    observations TEXT,
                    channel TEXT,
                    z_calc_value_real REAL,
                    z_calc_value_imag REAL,
                    exitation_voltage REAL,
                    gain REAL,
                    rfbvalue REAL,
                    settcycles INTEGER,
                    mux_channel INTEGER,
                    FOREIGN KEY (user_id) REFERENCES USER(user_id)
                )
            """)

            #Tabla Padre MEASURE_SETUP
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS MEASURE_SETUP (
                    measure_setup_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    observations TEXT,
                    exitation_voltage REAL,
                    gain REAL,
                    rfbvalue REAL,
                    settcycles INTEGER,
                    mux_channel INTEGER,
                    FOREIGN KEY (user_id) REFERENCES USER(user_id)
                )
            """)

            #ablas Hijas de MEASURE_SETUP 
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS SPEC_MEASURE_SETUP (
                    spec_ms_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    m_setup INTEGER NOT NULL,
                    startfreq REAL,
                    incfreq REAL,
                    steps INTEGER,
                    repeat INTEGER,
                    FOREIGN KEY (m_setup) REFERENCES MEASURE_SETUP(measure_setup_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS SINGLE_MEASURE_SETUP (
                    single_ms_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    m_setup INTEGER NOT NULL,
                    freq REAL,
                    delay INTEGER,
                    count INTEGER,
                    FOREIGN KEY (m_setup) REFERENCES MEASURE_SETUP(measure_setup_id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS MULTI_MEASURE_SETUP (
                    multi_ms_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    m_setup INTEGER NOT NULL,
                    frequencies_list TEXT,
                    FOREIGN KEY (m_setup) REFERENCES MEASURE_SETUP(measure_setup_id)
                )
            """)

            #Tabla MEASURE_RESULT
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS MEASURE_RESULT (
                    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    frequencies TEXT,
                    amplitudes TEXT,
                    phases TEXT,
                    impedances_real TEXT,
                    impedances_imag TEXT
                )
            """)

            #Tabla MEASURE
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS MEASURE (
                    measure_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_id INTEGER,
                    measure_setup INTEGER,
                    result INTEGER,
                    device_id INTEGER,
                    date TEXT,
                    state TEXT,
                    device_temp REAL,
                    file_name TEXT,
                    observations TEXT,
                    loop_group_id TEXT,
                    iteration_number INTEGER,
                    FOREIGN KEY (user_id) REFERENCES USER(user_id),
                    FOREIGN KEY (session_id) REFERENCES EXPERIMENTAL_SESSION(session_id),
                    FOREIGN KEY (measure_setup) REFERENCES MEASURE_SETUP(measure_setup_id),
                    FOREIGN KEY (result) REFERENCES MEASURE_RESULT(result_id),
                    FOREIGN KEY (device_id) REFERENCES DEVICE(device_id)
                )
            """)
            conn.commit()

    #Gestion de Usuarios 
    def save_user(self, user: User) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO USER (user_name, email, password, root_directory)
                VALUES (?, ?, ?, ?)
            """, (
                getattr(user, "_user_name", getattr(user, "username", "")),
                getattr(user, "_email", ""),
                getattr(user, "_password", ""),
                user.get_root_directory() if hasattr(user, "get_root_directory") else None
            ))
            conn.commit()
            if hasattr(user, "set_user_id"):
                user.set_user_id(cursor.lastrowid)
            return True

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM USER WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            return self._row_to_user(row) if row else None

    def get_user_by_email(self, email: str) -> Optional[User]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM USER WHERE email = ?", (email,))
            row = cursor.fetchone()
            return self._row_to_user(row) if row else None

    def get_user_by_name(self, user_name: str) -> Optional[User]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM USER WHERE user_name = ?", (user_name,))
            row = cursor.fetchone()
            return self._row_to_user(row) if row else None

    def update_user_directory(self, user_id: int, path: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE USER SET root_directory = ? WHERE user_id = ?", (path, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def _row_to_user(self, row: sqlite3.Row) -> User:
        try:
            u = User(row["user_name"], row["email"], row["password"], row["root_directory"])
            u.set_user_id(row["user_id"])
            return u
        except TypeError:
            u = User(row["user_id"], row["user_name"])
            if hasattr(u, "set_root_directory"):
                u.set_root_directory(row["root_directory"])
            return u

    # Gestión de Sesiones Experimentales, Setups y Mediciones
    def save_experimental_session(self, session: ExperimentalSession) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO EXPERIMENTAL_SESSION (user_id, name, date, observations)
                VALUES (?, ?, ?, ?)
            """, (
                session.get_user_id(),
                session.get_name(),
                session.get_date().isoformat(),
                session.get_observations()
            ))
            conn.commit()
            session_id = cursor.lastrowid
            session.set_id(session_id)

        for measure in session.get_measures():
            if hasattr(measure, "set_experimental_session_id"):
                measure.set_experimental_session_id(session_id)
            else:
                measure._experimental_session_id = session_id
            self.save_measure(session.get_user_id(), measure)

        return session_id

    def save_calibration_setup(self, user_id: int, cal_setup: CalibrationSetup) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO CALIBRATION_SETUP (
                    user_id, observations, channel, z_calc_value_real, z_calc_value_imag,
                    exitation_voltage, gain, rfbvalue, settcycles, mux_channel
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                cal_setup.get_observations() if hasattr(cal_setup, "get_observations") else "",
                str(getattr(cal_setup, "_channel", getattr(cal_setup, "_mux_channel", 0))),
                getattr(cal_setup, "_z_calc_value_real", 470.0),
                getattr(cal_setup, "_z_calc_value_imag", 0.0),
                getattr(cal_setup, "_exitation_voltage", 400.0),
                getattr(cal_setup, "_gain", 1.0),
                getattr(cal_setup, "_rfbvalue", 470.0),
                getattr(cal_setup, "_settcycles", 15),
                getattr(cal_setup, "_mux_channel", 0)
            ))
            conn.commit()
            return cursor.lastrowid

    def save_measure_setup(self, user_id: int, m_setup: MeasureSetup) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO MEASURE_SETUP (
                    user_id, observations, exitation_voltage, gain, rfbvalue, settcycles, mux_channel
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                m_setup.get_observations() if hasattr(m_setup, "get_observations") else "",
                getattr(m_setup, "_exitation_voltage", None),
                getattr(m_setup, "_gain", None),
                getattr(m_setup, "_rfbvalue", None),
                getattr(m_setup, "_settcycles", None),
                getattr(m_setup, "_mux_channel", None)
            ))
            setup_id = cursor.lastrowid

            if isinstance(m_setup, SpecMeasureSetup):
                cursor.execute("""
                    INSERT INTO SPEC_MEASURE_SETUP (m_setup, startfreq, incfreq, steps, repeat)
                    VALUES (?, ?, ?, ?, ?)
                """, (setup_id, m_setup.get_start_freq(), m_setup.get_inc_freq(), m_setup.get_steps(), m_setup.get_repeat()))

            elif isinstance(m_setup, SingleMeasureSetup):
                cursor.execute("""
                    INSERT INTO SINGLE_MEASURE_SETUP (m_setup, freq, delay, count)
                    VALUES (?, ?, ?, ?)
                """, (setup_id, m_setup.get_freq(), getattr(m_setup, "_delay", 0), getattr(m_setup, "_count", 1)))

            elif isinstance(m_setup, MultiMeasureSetup):
                cursor.execute("""
                    INSERT INTO MULTI_MEASURE_SETUP (m_setup, frequencies_list)
                    VALUES (?, ?)
                """, (setup_id, json.dumps(m_setup.get_freq_list())))

            conn.commit()
            if hasattr(m_setup, "_measure_setup_id"):
                m_setup._measure_setup_id = setup_id
            return setup_id

    def save_measure(self, user_id: int, measure: Measure) -> int:
        result = measure.get_measure_result()
        result_id = None

        with self._get_connection() as conn:
            cursor = conn.cursor()

            if result and result.get_impedances():
                freqs = result.get_frequencies()
                imps = result.get_impedances()
                reals = [z.real for z in imps]
                imags = [z.imag for z in imps]
                amps = [abs(z) for z in imps]
                phases = getattr(result, "_phases", [])

                cursor.execute("""
                    INSERT INTO MEASURE_RESULT (
                        frequencies, amplitudes, phases, impedances_real, impedances_imag
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    json.dumps(freqs),
                    json.dumps(amps),
                    json.dumps(phases),
                    json.dumps(reals),
                    json.dumps(imags)
                ))
                result_id = cursor.lastrowid

            m_setup = measure.get_measure_setup()
            setup_id = None
            if m_setup:
                setup_id = m_setup.get_id() if hasattr(m_setup, "get_id") else None
                if not setup_id:
                    setup_id = self.save_measure_setup(user_id, m_setup)

            date_val = getattr(measure, "_date", datetime.now())
            date_str = date_val.isoformat() if hasattr(date_val, "isoformat") else str(date_val)
            session_id = getattr(measure, "_experimental_session_id", None)

            cursor.execute("""
                INSERT INTO MEASURE (
                    user_id, session_id, measure_setup, result, device_id, date,
                    state, device_temp, file_name, observations, loop_group_id, iteration_number
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                session_id,
                setup_id,
                result_id,
                measure.get_device_id(),
                date_str,
                measure.get_state(),
                getattr(measure, "_device_temp", 0.0),
                measure.get_file_name(),
                measure.get_observations(),
                getattr(measure, "_loop_group_id", ""),
                getattr(measure, "_iteration_number", 1)
            ))
            conn.commit()
            measure_id = cursor.lastrowid
            if hasattr(measure, "set_measure_id"):
                measure.set_measure_id(measure_id)
            else:
                measure._measure_id = measure_id
            return measure_id
        
    """Recupera una Measure puntual desde la BD para poder abrirla y graficarla"""
    def get_measure_by_id(self, measure_id: int) -> Optional[Measure]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.*, r.frequencies, r.impedances_real, r.impedances_imag
                FROM MEASURE m
                LEFT JOIN MEASURE_RESULT r ON m.result = r.result_id
                WHERE m.measure_id = ?
            """, (measure_id,))
            row = cursor.fetchone()
            return self._row_to_measure(conn, row) if row else None

    def get_measures_by_user(self, user_id: int) -> List[Measure]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.*, r.frequencies, r.impedances_real, r.impedances_imag
                FROM MEASURE m
                LEFT JOIN MEASURE_RESULT r ON m.result = r.result_id
                WHERE m.user_id = ?
                ORDER BY m.date DESC
            """, (user_id,))
            return [self._row_to_measure(conn, r) for r in cursor.fetchall()]

    def get_calibration_setups_by_user(self, user_id: int) -> List[CalibrationSetup]:
        setups: List[CalibrationSetup] = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CALIBRATION_SETUP WHERE user_id = ?", (user_id,))
            for row in cursor.fetchall():
                cal = CalibrationSetup(
                    exitation_voltage=row["exitation_voltage"] or 400.0,
                    gain=int(row["gain"] or 1),
                    rfbvalue=int(row["rfbvalue"] or 470),
                    settcycles=int(row["settcycles"] or 15),
                    mux_channel=int(row["mux_channel"] or 0)
                )
                if hasattr(cal, "set_observations"):
                    cal.set_observations(row["observations"] or "")
                setups.append(cal)
        return setups

    def get_measure_setups_by_user(self, user_id: int) -> List[MeasureSetup]:
        setups: List[MeasureSetup] = []
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT measure_setup_id FROM MEASURE_SETUP WHERE user_id = ?", (user_id,))
            for row in cursor.fetchall():
                s = self._load_setup_by_id(conn, row["measure_setup_id"])
                if s:
                    setups.append(s)
        return setups

    def _row_to_measure(self, conn: sqlite3.Connection, row: sqlite3.Row) -> Measure:
        setup = self._load_setup_by_id(conn, row["measure_setup"])
        m = Measure(measure_setup=setup, device_id=row["device_id"])
        m._measure_id = row["measure_id"]
        m.set_file_name(row["file_name"] or "")
        m.set_observations(row["observations"] or "")
        m.set_state(row["state"])

        if row["frequencies"]:
            freqs = json.loads(row["frequencies"])
            reals = json.loads(row["impedances_real"])
            imags = json.loads(row["impedances_imag"])
            imps = [complex(r, i) for r, i in zip(reals, imags)]
            res = MeasureResult(frequencies=freqs, impedances=imps)
            if hasattr(m, "set_result"):
                m.set_result(res)
            else:
                m._result = res
        return m

    def _load_setup_by_id(self, conn: sqlite3.Connection, setup_id: int) -> Optional[MeasureSetup]:
        if not setup_id:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM MEASURE_SETUP WHERE measure_setup_id = ?", (setup_id,))
        base = cursor.fetchone()
        if not base:
            return None
        obs = base["observations"] or ""

        cursor.execute("SELECT * FROM SPEC_MEASURE_SETUP WHERE m_setup = ?", (setup_id,))
        spec = cursor.fetchone()
        if spec:
            return (
                SpectroSetupBuilder()
                .with_start_freq(spec["startfreq"])
                .with_inc_freq(spec["incfreq"])
                .with_steps(spec["steps"])
                .with_repeat(spec["repeat"])
                .with_observations(obs)
                .build()
            )

        cursor.execute("SELECT * FROM SINGLE_MEASURE_SETUP WHERE m_setup = ?", (setup_id,))
        single = cursor.fetchone()
        if single:
            b = SingleFreqSetupBuilder().with_freq(single["freq"]).with_observations(obs)
            if hasattr(b, "with_delay"):
                b.with_delay(single["delay"])
            if hasattr(b, "with_count"):
                b.with_count(single["count"])
            return b.build()

        cursor.execute("SELECT * FROM MULTI_MEASURE_SETUP WHERE m_setup = ?", (setup_id,))
        multi = cursor.fetchone()
        if multi:
            return (
                MultiFreqSetupBuilder()
                .with_freq_list(json.loads(multi["frequencies_list"]))
                .with_observations(obs)
                .build()
            )
        return None