### Clases Software
#### Lista de Clases

```mermaid
classDiagram
direction LR

%% jerarquias

MeasureSetup <|-- SpecMeasureSetup
MeasureSetup <|-- SingleMeasureSetup
MeasureSetup <|-- MultiMeasureSetup

BaseMeasureSetupBuilder <|-- SpectroSetupBuilder
BaseMeasureSetupBuilder <|-- SingleFreqSetupBuilder
BaseMeasureSetupBuilder <|-- MultiFreqSetupBuilder

ConnectionType <|-- Wire
ConnectionType <|-- WireLess

ConnectionState <|.. ConnectedState
ConnectionState <|.. DisconnectedState
ConnectionState <|.. ConnectionErrorState

DeviceState <|.. FreeDeviceState
DeviceState <|.. CalibratedState
DeviceState <|.. MeasuringState
DeviceState <|.. DeviceErrorState
DeviceState <|.. UncalibratedState

%% clases

class User {
	- user_id : int
	- user_name : str
	- email : str
	- password : str
	- root_directory : str
	
}

class Token {
	- user_id : int
	- token_string : str
	- created_at : DateTime
}

class Measure {
	- measureSetup : MeasureSetup
	- date : DateTime
	- file_name : str
	- state : ['EXECUTING', 'COMPLETE', 'ERROR']
	- device_temp : float
	- result : MeasureResult
	- observations : str
	- loop_group_id : str
	- iteration_number : int
	+ set_state(new_state : str)
	+ get_state() : str
}

class MeasureSetup {
	<<abstract>>
	- observations : str
	- exitation_voltage : float
	- gain : float
	- rfbvalue : float
	- settcycles : int
	- mux_channel : [0, 1, 2, 3]
	+ get_command() : str
}
class SpecMeasureSetup{
	- startfreq : float
	- incfreq : float
	- steps : int
	- repeat : int
}
class SingleMeasureSetup{
	- freq : float
	- delay : int
	- count : int
}
class MultiMeasureSetup{
	- freq_list :[float]
}

class CalibrationSetup{
	- observations : str
	- channel : ["RCAL1":0, "RCAL2":1, "Other":2/3]
	- z_calc_value_real : float
	- z_calc_value_imag : float
	+ get_command() : str
}

class Device{
	- device_id : int
	- connection_type : ConnectionType
	- device_state : DeviceState
	+ set_state(new_state : DeviceState)
	+ get_state() : DeviceState
}

class MeasureResult{
	- frequencies : [float]
	- amplitudes : [float]
	- phases : [float]
	- impedances : [complex]
	+ measure_mean() : [float]
	+ measure_std() : [float]
}

class ConnectionType {
	<<abstract>>
	- connection_state : ConnectionState
	+ connect(device)
	+ disconnect()
	+ send(data : str)
	+ receive() : str
	+ set_state(new_state : ConnectionState)
	+ get_state() : ConnectionState
}
class Wire{
	- baudrate : int
	- port_name : str
	- timeout : int
}
class WireLess{
	- protocol : str
}

%% servicios

class MeasureService{
	+ execute_measure(measure : Measure)
	+ finish_measure() : [MeasureResult]
	- update_progress()
}

class LocalService{
	- local_root : str
	%% operaciones en archivos
	+ load_measure() : Measure
	+ load_calibration_setup() : CalibrationSetup
	+ load_setup() : MeasureSetup
	+ export_setup_to_file(setup : MeasureSetup)
	+ export_calibration_setup_to_file(setup : CalibrationSetup)
	+ export_measure_to_file(measure : Measure)
}
class DataBaseService{
	- db_root : str
	%% operaciones en db
	+ save_user(user : User)
	+ save_measure(measure : Measure)
	+ save_calibration_setup(cal_setup : CalibrationSetup)
	+ save_measure_setup(m_setup : MeasureSetup)
	+ get_measures_by_user(user_id : int) : [Measure]
	+ get_calibration_setups_by_user(user_id : int) : [CalibrationSetup]
	+ get_measure_setups_by_user(user_id : int) : [MeasureSetup]
}


class AuthService{
	+ login(user_name, email, password) : Token
	+ logout()
	+ register(user_name, email, password) : Token
	
}

class SessionManager{
	- current_user : User
	- advanced_mode_active : boolean
	- active_token : Token
}

class ConnectionService{
	+ connect(device : Device, connection_type : ConnectionType)
	+ disconnect()
}
class CalibrationService{
	+ calibrate_device(device : Device, cal_setup : CalibrationSetup)
}

%% state patern

class DeviceState{
		<<interface>>
	}
	class FreeDeviceState
	class CalibratedState
	class MeasuringState
	class DeviceErrorState
	
class ConnectionState{
		<<interface>>
		+ connect(context : ConnectionType, device : Device)
		+ disconnect(context : ConnectionType)
		+ send(context : ConnectionType, data: str)
		+ receive(context : ConnectionType) : str
	}
class ConnectedState
class DisconnectedState
class ConnectionErrorState

%% observer patern
class IObserver{
	<<interface>>
	+ update(observable : IObservable, event_info : str)
}

class IObservable{
	<<interface>>
	+ attach()
	+ detach()
	+ notify()
}

%% builder patern
class BaseMeasureSetupBuilder{
	<<abstract>>
	- observations : str
	- exitation_voltage : float
	- gain : float
	- rfbvalue : float
	- settcycles : int
	- mux_channel : [0, 1, 2, 3]
	+ build() : MeasureSetup
	+ with_observations()
	+ with_voltage()
	+ with_gain()
	+ with_rfb_value()
	+ with_cycles()
	+ with_mux_channel()
}

class SpectroSetupBuilder{
	- startfreq : float
	- incfreq : float
	- steps : int
	- repeat : int
	+ build() : SpecMeasureSetup
	+ with_start_freq(startfreq : float) : self
	+ with_inc_freq(incfreq : float) : self
	+ with_steps(steps : int) : self
	+ with_repeat(repeat : int) : self
}

class SingleFreqSetupBuilder{
	- freq : float
	- delay : int
	- count : int
	+ build() : SingleMeasureSetup
	+ with_freq(freq : float) : self
	+ with_delay(delay : int) : self
	+ with_count(count : int) : self
}

class MultiFreqSetupBuilder{
	- freq_list :[float]
	+ build() : MultiMeasureSetup
	+ with_freq_list(freq_list :[float]) : self
}

%% factory method
class ConnectionFactory{ 
	+ create_connection(type : str) : ConnectionType 
} 
class MeasureSetupBuilderFactory{ 
	+ create_builder(mode : str) : BaseMeasureSetupBuilder 
}
```

#### Diagramas de Clases
###### Subsistema 1: Comunicación e Interacción con el Hardware

###### Módulo 1: Conectividad y Estado

```mermaid
classDiagram

%% jerarquias
ConnectionType <|-- Wire
ConnectionType <|-- WireLess

DeviceState <|.. FreeDeviceState
DeviceState <|.. CalibratedState
DeviceState <|.. MeasuringState
DeviceState <|.. DeviceErrorState
DeviceState <|.. UncalibratedState

ConnectionState <|.. ConnectedState
ConnectionState <|.. DisconnectedState
ConnectionState <|.. ConnectionErrorState

%% clases

class ConnectionType {
	<<abstract>>
	- connection_state : ConnectionState
	+ connect(device)
	+ disconnect()
	+ send(data : str)
	+ receive() : str
	+ set_state(new_state : ConnectionState)
	+ get_state() : ConnectionState
}
class Wire{
	- baudrate : int
	- port_name : str
	- timeout : int
}
class WireLess{
	- protocol : str
}

class User {
	- user_id : int
	- user_name : str
	- email : str
	- password : str
	- root_directory : str
	
}

class Device{
	- device_id : int
	- connection_type : ConnectionType
	- device_state : DeviceState
	+ set_state(new_state : DeviceState)
	+ get_state() : DeviceState
}

%% state patern
	
class ConnectionState{
		<<interface>>
		+ connect(context : ConnectionType, device : Device)
		+ disconnect(context : ConnectionType)
		+ send(context : ConnectionType, data: str)
		+ receive(context : ConnectionType) : str
	}
class ConnectedState
class DisconnectedState
class ConnectionErrorState

class DeviceState{
		<<interface>>
	}
	class FreeDeviceState
	class CalibratedState
	class MeasuringState
	class DeviceErrorState

%% observer patern
class IObserver{
	<<interface>>
	+ update(observable : IObservable, event_info : str)
}

class IObservable{
	<<interface>>
	+ attach()
	+ detach()
	+ notify()
}

%% servicios
class MeasureService{
	+ execute_measure(measure : Measure)
	+ finish_measure() : [MeasureResult]
	- update_progress()
}

class DataBaseService{
	- db_root : str
	%% operaciones en db
	+ save_user(user : User)
	+ save_measure(measure : Measure)
	+ save_calibration_setup(cal_setup : CalibrationSetup)
	+ save_measure_setup(m_setup : MeasureSetup)
	+ get_measures_by_user(user_id : int) : [Measure]
	+ get_calibration_setups_by_user(user_id : int) : [CalibrationSetup]
	+ get_measure_setups_by_user(user_id : int) : [MeasureSetup]
}

class ConnectionService{
	+ connect(device : Device, connection_type : ConnectionType)
	+ disconnect()
}

%% factory method
class ConnectionFactory{ 
	+ create_connection(type : str) : ConnectionType 
}

%% relaciones

User "1"-->"1" Device : conecta

ConnectionService ..> ConnectionFactory
ConnectionFactory ..> ConnectionType

Device "1" o-- "1" ConnectionType
Device "1" *-- "1" DeviceState
Device ..|> IObservable

MeasureService ..|> IObserver
MeasureService .. Device : observa
MeasureService ..> DataBaseService : invoca guardado de emergencia


ConnectionService ..>  Device

ConnectionType "1" *-- "1" ConnectionState
```


###### Módulo 2: Calibración del Dispositivo
```mermaid
classDiagram
DeviceState <|.. FreeDeviceState
DeviceState <|.. CalibratedState
DeviceState <|.. MeasuringState
DeviceState <|.. DeviceErrorState
DeviceState <|.. UncalibratedState

%% clases
class User {
	- user_id : int
	- user_name : str
	- email : str
	- password : str
	- root_directory : str
	
}

class CalibrationSetup{
	- observations : str
	- channel : ["RCAL1":0, "RCAL2":1, "Other":2/3]
	- z_calc_value_real : float
	- z_calc_value_imag : float
	+ get_command() : str
}

class Device{
	- device_id : int
	- connection_type : ConnectionType
	- device_state : DeviceState
	+ set_state(new_state : DeviceState)
	+ get_state() : DeviceState
}

class DeviceState{
		<<interface>>
	}
	class FreeDeviceState
	class CalibratedState
	class MeasuringState
	class DeviceErrorState

class CalibrationService{
	+ calibrate_device(device : Device, cal_setup : CalibrationSetup)
}

class SessionManager{
	- current_user : User
	- advanced_mode_active : boolean
	- active_token : Token
}

class Token {
	- user_id : int
	- token_string : str
	- created_at : DateTime
}

%% relaciones
User "1"-->"1" Device : calibra

Device "1"*--"1" DeviceState

SessionManager "1"o--"0..1" Token
SessionManager "1"o--"0..1" User

CalibrationService ..> Device
CalibrationService ..> CalibrationSetup
CalibrationService ..> SessionManager
```

##### Subsistema 2: Configuración y Toma de Mediciones
###### Módulo 1: Tipos y Estrategias de Medición

```mermaid
classDiagram

MeasureSetup <|-- SpecMeasureSetup
MeasureSetup <|-- SingleMeasureSetup
MeasureSetup <|-- MultiMeasureSetup

BaseMeasureSetupBuilder <|-- SpectroSetupBuilder
BaseMeasureSetupBuilder <|-- SingleFreqSetupBuilder
BaseMeasureSetupBuilder <|-- MultiFreqSetupBuilder

%% clases
class User {
	- user_id : int
	- user_name : str
	- email : str
	- password : str
	- root_directory : str
	
}

class Measure {
	- measureSetup : MeasureSetup
	- date : DateTime
	- file_name : str
	- state : ['EXECUTING', 'COMPLETE', 'ERROR']
	- device_temp : float
	- result : MeasureResult
	- observations : str
	- loop_group_id : str
	- iteration_number : int
	+ set_state(new_state : str)
	+ get_state() : str
}

class SessionManager{
	- current_user : User
	- advanced_mode_active : boolean
	- active_token : Token
}

class Token {
	- user_id : int
	- token_string : str
	- created_at : DateTime
}

class MeasureSetup {
	<<abstract>>
	- observations : str
	- exitation_voltage : float
	- gain : float
	- rfbvalue : float
	- settcycles : int
	- mux_channel : [0, 1, 2, 3]
	+ get_command() : str
}
class SpecMeasureSetup{
	- startfreq : float
	- incfreq : float
	- steps : int
	- repeat : int
}
class SingleMeasureSetup{
	- freq : float
	- delay : int
	- count : int
}
class MultiMeasureSetup{
	- freq_list :[float]
}

class MeasureResult{
	- frequencies : [float]
	- amplitudes : [float]
	- phases : [float]
	- impedances : [complex]
	+ measure_mean() : [float]
	+ measure_std() : [float]
}

class MeasureService{
	+ execute_measure(measure : Measure)
	+ finish_measure() : [MeasureResult]
	- update_progress()
}

%% builder patern
class BaseMeasureSetupBuilder{
	<<abstract>>
	- observations : str
	- exitation_voltage : float
	- gain : float
	- rfbvalue : float
	- settcycles : int
	- mux_channel : [0, 1, 2, 3]
	+ build() : MeasureSetup
	+ with_observations()
	+ with_voltage()
	+ with_gain()
	+ with_rfb_value()
	+ with_cycles()
	+ with_mux_channel()
}

class SpectroSetupBuilder{
	- startfreq : float
	- incfreq : float
	- steps : int
	- repeat : int
	+ build() : SpecMeasureSetup
	+ with_start_freq(startfreq : float) : self
	+ with_inc_freq(incfreq : float) : self
	+ with_steps(steps : int) : self
	+ with_repeat(repeat : int) : self
}

class SingleFreqSetupBuilder{
	- freq : float
	- delay : int
	- count : int
	+ build() : SingleMeasureSetup
	+ with_freq(freq : float) : self
	+ with_delay(delay : int) : self
	+ with_count(count : int) : self
}

class MultiFreqSetupBuilder{
	- freq_list :[float]
	+ build() : MultiMeasureSetup
	+ with_freq_list(freq_list :[float]) : self
}

%% factory method
class MeasureSetupBuilderFactory{ 
	+ create_builder(mode : str) : BaseMeasureSetupBuilder 
}

%% relaciones
User "1"-->"1..*" Measure : mide

MeasureSetupBuilderFactory ..> BaseMeasureSetupBuilder

Measure "1"o--"1" MeasureSetup
Measure "1"*--"1" MeasureResult

BaseMeasureSetupBuilder ..> MeasureSetup

MeasureService ..> Measure
MeasureService ..> SessionManager

SessionManager "1"o--"0..1" Token
SessionManager "1"o--"0..1" User
```
##### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

###### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición
```mermaid
classDiagram

%% jerarquias

MeasureSetup <|-- SpecMeasureSetup
MeasureSetup <|-- SingleMeasureSetup
MeasureSetup <|-- MultiMeasureSetup

BaseMeasureSetupBuilder <|-- SpectroSetupBuilder
BaseMeasureSetupBuilder <|-- SingleFreqSetupBuilder
BaseMeasureSetupBuilder <|-- MultiFreqSetupBuilder

class User {
	- user_id : int
	- user_name : str
	- email : str
	- password : str
	- root_directory : str
	
}

class AuthService{
	+ login(user_name, email, password) : Token
	+ logout()
	+ register(user_name, email, password) : Token
}

class Token {
	- user_id : int
	- token_string : str
	- created_at : DateTime
}

class LocalService{
	- local_root : str
	%% operaciones en archivos
	+ load_measure() : Measure
	+ load_calibration_setup() : CalibrationSetup
	+ load_setup() : MeasureSetup
	+ export_setup_to_file(setup : MeasureSetup)
	+ export_calibration_setup_to_file(setup : CalibrationSetup)
	+ export_measure_to_file(measure : Measure)
}
class DataBaseService{
	- db_root : str
	%% operaciones en db
	+ save_user(user : User)
	+ save_measure(measure : Measure)
	+ save_calibration_setup(cal_setup : CalibrationSetup)
	+ save_measure_setup(m_setup : MeasureSetup)
	+ get_measures_by_user(user_id : int) : [Measure]
	+ get_calibration_setups_by_user(user_id : int) : [CalibrationSetup]
	+ get_measure_setups_by_user(user_id : int) : [MeasureSetup]
}

class MeasureSetup {
	<<abstract>>
	- observations : str
	- exitation_voltage : float
	- gain : float
	- rfbvalue : float
	- settcycles : int
	- mux_channel : [0, 1, 2, 3]
	+ get_command() : str
}
class SpecMeasureSetup{
	- startfreq : float
	- incfreq : float
	- steps : int
	- repeat : int
}
class SingleMeasureSetup{
	- freq : float
	- delay : int
	- count : int
}
class MultiMeasureSetup{
	- freq_list :[float]
}

class CalibrationSetup{
	- observations : str
	- channel : ["RCAL1":0, "RCAL2":1, "Other":2/3]
	- z_calc_value_real : float
	- z_calc_value_imag : float
	+ get_command() : str
}

class SessionManager{
	- current_user : User
	- advanced_mode_active : boolean
	- active_token : Token
}

%% builder patern
class BaseMeasureSetupBuilder{
	<<abstract>>
	- observations : str
	- exitation_voltage : float
	- gain : float
	- rfbvalue : float
	- settcycles : int
	- mux_channel : [0, 1, 2, 3]
	+ build() : MeasureSetup
	+ with_observations()
	+ with_voltage()
	+ with_gain()
	+ with_rfb_value()
	+ with_cycles()
	+ with_mux_channel()
}

class SpectroSetupBuilder{
	- startfreq : float
	- incfreq : float
	- steps : int
	- repeat : int
	+ build() : SpecMeasureSetup
	+ with_start_freq(startfreq : float) : self
	+ with_inc_freq(incfreq : float) : self
	+ with_steps(steps : int) : self
	+ with_repeat(repeat : int) : self
}

class SingleFreqSetupBuilder{
	- freq : float
	- delay : int
	- count : int
	+ build() : SingleMeasureSetup
	+ with_freq(freq : float) : self
	+ with_delay(delay : int) : self
	+ with_count(count : int) : self
}

class MultiFreqSetupBuilder{
	- freq_list :[float]
	+ build() : MultiMeasureSetup
	+ with_freq_list(freq_list :[float]) : self
}

%% factory method 
class MeasureSetupBuilderFactory{ 
	+ create_builder(mode : str) : BaseMeasureSetupBuilder 
} 

%% relaciones
User "1"-->"0..*" MeasureSetup : aplica
User "1"-->"0..*" CalibrationSetup : aplica

BaseMeasureSetupBuilder ..> MeasureSetup

AuthService ..> User
AuthService ..> DataBaseService
AuthService ..> SessionManager
AuthService ..> Token

SessionManager "1"o--"0..1" Token
SessionManager "1"o--"0..1" User

LocalService ..> CalibrationSetup
LocalService ..> MeasureSetup

MeasureSetupBuilderFactory ..> BaseMeasureSetupBuilder
```

##### Subsistema 5: Persistencia

###### Módulo 1: Almacenamiento y Estructura de Datos

```mermaid
classDiagram

%% jerarquias
MeasureSetup <|-- SpecMeasureSetup
MeasureSetup <|-- SingleMeasureSetup
MeasureSetup <|-- MultiMeasureSetup

BaseMeasureSetupBuilder <|-- SpectroSetupBuilder
BaseMeasureSetupBuilder <|-- SingleFreqSetupBuilder
BaseMeasureSetupBuilder <|-- MultiFreqSetupBuilder

%% clases
class User {
	- user_id : int
	- user_name : str
	- email : str
	- password : str
	- root_directory : str
	
}

class Measure {
	- measureSetup : MeasureSetup
	- date : DateTime
	- file_name : str
	- state : ['EXECUTING', 'COMPLETE', 'ERROR']
	- device_temp : float
	- result : MeasureResult
	- observations : str
	- loop_group_id : str
	- iteration_number : int
	+ set_state(new_state : str)
	+ get_state() : str
}

class MeasureResult{
	- frequencies : [float]
	- amplitudes : [float]
	- phases : [float]
	- impedances : [complex]
	+ measure_mean() : [float]
	+ measure_std() : [float]
}

class MeasureSetup {
	<<abstract>>
	- observations : str
	- exitation_voltage : float
	- gain : float
	- rfbvalue : float
	- settcycles : int
	- mux_channel : [0, 1, 2, 3]
	+ get_command() : str
}
class SpecMeasureSetup{
	- startfreq : float
	- incfreq : float
	- steps : int
	- repeat : int
}
class SingleMeasureSetup{
	- freq : float
	- delay : int
	- count : int
}
class MultiMeasureSetup{
	- freq_list :[float]
}

class CalibrationSetup{
	- observations : str
	- channel : ["RCAL1":0, "RCAL2":1, "Other":2/3]
	- z_calc_value_real : float
	- z_calc_value_imag : float
	+ get_command() : str
}

class SessionManager{
	- current_user : User
	- advanced_mode_active : boolean
	- active_token : Token
}

class Token {
	- user_id : int
	- token_string : str
	- created_at : DateTime
}

class MeasureService{
	+ execute_measure(measure : Measure)
	+ finish_measure() : [MeasureResult]
	- update_progress()
}

class CalibrationService{
	+ calibrate_device(device : Device, cal_setup : CalibrationSetup)
}

class LocalService{
	- local_root : str
	%% operaciones en archivos
	+ load_measure() : Measure
	+ load_calibration_setup() : CalibrationSetup
	+ load_setup() : MeasureSetup
	+ export_setup_to_file(setup : MeasureSetup)
	+ export_calibration_setup_to_file(setup : CalibrationSetup)
	+ export_measure_to_file(measure : Measure)
}
class DataBaseService{
	- db_root : str
	%% operaciones en db
	+ save_user(user : User)
	+ save_measure(measure : Measure)
	+ save_calibration_setup(cal_setup : CalibrationSetup)
	+ save_measure_setup(m_setup : MeasureSetup)
	+ get_measures_by_user(user_id : int) : [Measure]
	+ get_calibration_setups_by_user(user_id : int) : [CalibrationSetup]
	+ get_measure_setups_by_user(user_id : int) : [MeasureSetup]
}

%% builder patern
class BaseMeasureSetupBuilder{
	<<abstract>>
	- observations : str
	- exitation_voltage : float
	- gain : float
	- rfbvalue : float
	- settcycles : int
	- mux_channel : [0, 1, 2, 3]
	+ build() : MeasureSetup
	+ with_observations()
	+ with_voltage()
	+ with_gain()
	+ with_rfb_value()
	+ with_cycles()
	+ with_mux_channel()
}

class SpectroSetupBuilder{
	- startfreq : float
	- incfreq : float
	- steps : int
	- repeat : int
	+ build() : SpecMeasureSetup
	+ with_start_freq(startfreq : float) : self
	+ with_inc_freq(incfreq : float) : self
	+ with_steps(steps : int) : self
	+ with_repeat(repeat : int) : self
}

class SingleFreqSetupBuilder{
	- freq : float
	- delay : int
	- count : int
	+ build() : SingleMeasureSetup
	+ with_freq(freq : float) : self
	+ with_delay(delay : int) : self
	+ with_count(count : int) : self
}

class MultiFreqSetupBuilder{
	- freq_list :[float]
	+ build() : MultiMeasureSetup
	+ with_freq_list(freq_list :[float]) : self
}

%% factory method 
class MeasureSetupBuilderFactory{ 
	+ create_builder(mode : str) : BaseMeasureSetupBuilder 
} 

%% relaciones
MeasureSetupBuilderFactory ..> BaseMeasureSetupBuilder

Measure "1"*--"1" MeasureResult
Measure "1"o--"1" MeasureSetup

BaseMeasureSetupBuilder ..> MeasureSetup

CalibrationService ..> SessionManager
CalibrationService ..> CalibrationSetup

MeasureService ..> SessionManager
MeasureService ..> Measure

SessionManager "1"o--"0..1" Token
SessionManager "1"o--"0..1" User

DataBaseService ..> SessionManager
LocalService ..> SessionManager

User "1"-->"0..*" Measure : guarda
User "1"-->"0..*" MeasureSetup : guarda
User "1"-->"0..*" CalibrationSetup : guarda
```

