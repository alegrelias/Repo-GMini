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

%% interfaces
ConnectionState <|.. ConnectedState
ConnectionState <|.. DisconnectedState
ConnectionState <|.. ConnectionErrorState

DeviceState <|.. FreeDeviceState
DeviceState <|.. CalibratedState
DeviceState <|.. MeasuringState
DeviceState <|.. DeviceErrorState
DeviceState <|.. UncalibratedState

IMeasureAdapter <|.. GminiMeasureAdapter

ICalibrationAdapter <|.. GminiCalibrationAdapter


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
	- device_int : int
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
}

class Device{
	- device_id : int
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
	+ connect()
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
	+ get_user_by_id(user_id : int): User
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
	+ restore_session(token : str)
}

class SessionManager{
	- current_user : User
	- advanced_mode_active : boolean
	- active_token : Token
}

class ConnectionService{
	+ active_conections : [device : connection_type]
	+ connect(device : Device, connection_type : ConnectionType)
	+ disconnect(device : Device)
	+ send(device : Device, command : str)
	+ receive(device : Device) : str
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
	class UncalibratedState
	
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

%% patron adapter
class ICalibrationAdapter{ 
	<<interface>>
	+ encode(setup : CalibrationSetup) : str 
	+ decode(response : str) : bool 
}

class GminiCalibrationAdapter{ 
	+ encode(setup : CalibrationSetup) : str 
	+ decode(response : str) : bool 
} 

class IMeasureAdapter{ 
	<<interface>>
	+ encode(setup : MeasureSetup) : str 
	+ decode(response : str) : MeasureResult 
}

class GminiMeasureAdapter{ 
	+ encode(setup : MeasureSetup) : str 
	+ decode(response : str) : MeasureResult 
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

class Device{
	- device_id : int
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
	class UncalibratedState

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

class ConnectionService{
	+ active_conections : [device : connection_type]
	+ connect(device : Device, connection_type : ConnectionType)
	+ disconnect(device : Device)
	+ send(device : Device, command : str)
	+ receive(device : Device) : str
}

%% factory method
class ConnectionFactory{ 
	+ create_connection(type : str) : ConnectionType 
}

%% relaciones

Device ..|> IObservable : implementa

MeasureService ..|> IObserver : implementa
ConnectionService ..|> IObserver : implementa

ConnectionType ..|> IObservable : implementa

DeviceState <|.. FreeDeviceState : implementa
DeviceState <|.. CalibratedState : implementa
DeviceState <|.. MeasuringState : implementa
DeviceState <|.. DeviceErrorState : implementa
DeviceState <|.. UncalibratedState : implementa

ConnectionState <|.. ConnectedState : implementa
ConnectionState <|.. DisconnectedState : implementa
ConnectionState <|.. ConnectionErrorState : implementa

ConnectionFactory --> ConnectionType : crea

ConnectionType o-- ConnectionState
Device o-- DeviceState

ConnectionService --> Device : establece conexión
ConnectionService --> ConnectionType : establece conexión
ConnectionService --> ConnectionState : observa
```


###### Módulo 2: Calibración del Dispositivo
```mermaid
classDiagram
DeviceState <|.. FreeDeviceState : implementa
DeviceState <|.. CalibratedState : implementa
DeviceState <|.. MeasuringState : implementa
DeviceState <|.. DeviceErrorState : implementa
DeviceState <|.. UncalibratedState : implementa

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

class ConnectionService{
	+ active_conections : [device : connection_type]
	+ connect(device : Device, connection_type : ConnectionType)
	+ disconnect(device : Device)
	+ send(device : Device, command : str)
	+ receive(device : Device) : str
}

class Token {
	- user_id : int
	- token_string : str
	- created_at : DateTime
}

%% patron adapter
class ICalibrationAdapter{ 
	<<interface>>
	+ encode(setup : CalibrationSetup) : str 
	+ decode(response : str) : bool 
}

class GminiCalibrationAdapter{ 
	+ encode(setup : CalibrationSetup) : str 
	+ decode(response : str) : bool 
} 

%% relaciones
User "1"-->"1" Device : calibra

Device "1"*--"1" DeviceState

SessionManager "1"o--"0..1" Token
SessionManager "1"o--"0..1" User

ICalibrationAdapter <|.. GminiCalibrationAdapter : implementa

CalibrationService ..> ConnectionService : envía comandos y espera devolución
CalibrationService ..> Device : establece calibración
CalibrationService ..> CalibrationSetup : crea setup
CalibrationService ..> SessionManager : verifica usuario
CalibrationService ..> ICalibrationAdapter : envía objetos y espera comandos
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

DeviceState <|.. FreeDeviceState : implementa
DeviceState <|.. CalibratedState : implementa
DeviceState <|.. MeasuringState : implementa
DeviceState <|.. DeviceErrorState : implementa
DeviceState <|.. UncalibratedState : implementa

Device ..|> IObservable : implementa

MeasureService ..|> IObserver : implementa

%% clases
class User {
	- user_id : int
	- user_name : str
	- email : str
	- password : str
	- root_directory : str
	
}

class Device{
	- device_id : int
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
	class UncalibratedState

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

class ConnectionService{
	+ active_conections : [device : connection_type]
	+ connect(device : Device, connection_type : ConnectionType)
	+ disconnect(device : Device)
	+ send(device : Device, command : str)
	+ receive(device : Device) : str
}

class DataBaseService{
	- db_root : str
	%% operaciones en db
	+ save_user(user : User)
	+ get_user_by_id(user_id : int): User
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

%% factory method
class MeasureSetupBuilderFactory{ 
	+ create_builder(mode : str) : BaseMeasureSetupBuilder 
}

class IMeasureAdapter{ 
	<<interface>>
	+ encode(setup : MeasureSetup) : str 
	+ decode(response : str) : MeasureResult 
}

class GminiMeasureAdapter{ 
	+ encode(setup : MeasureSetup) : str 
	+ decode(response : str) : MeasureResult 
}

%% relaciones

MeasureSetupBuilderFactory ..> BaseMeasureSetupBuilder : construye

Measure "1"o--"1" MeasureSetup
Measure "1"*--"1" MeasureResult
Measure --> Device : conoce

BaseMeasureSetupBuilder ..> MeasureSetup : instancia

MeasureService ..> Measure : ejecuta medición
MeasureService ..> SessionManager : verifica usuario
MeasureService ..> IMeasureAdapter : envía setups y recibe comandos
MeasureService ..> ConnectionService : envía comandos y espera devolución
MeasureService --> DeviceState : observa
MeasureService --> DataBaseService : invoca guardado de emergencia

SessionManager "1"o--"0..1" Token
SessionManager "1"o--"0..1" User

IMeasureAdapter <|.. GminiMeasureAdapter : implementa

Device "1"*--"1" DeviceState
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
	+ get_user_by_id(user_id : int): User
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

BaseMeasureSetupBuilder ..> MeasureSetup : instancia

AuthService ..> User : crea usuario
AuthService ..> DataBaseService : guarda usuario
AuthService ..> SessionManager : establece usuario
AuthService ..> Token : crea

SessionManager "1"o--"0..1" Token
SessionManager "1"o--"0..1" User

LocalService ..> CalibrationSetup : exporta/importa
LocalService ..> MeasureSetup : exporta/importa

MeasureSetupBuilderFactory ..> BaseMeasureSetupBuilder : construye
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
	+ get_user_by_id(user_id : int): User
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
MeasureSetupBuilderFactory ..> BaseMeasureSetupBuilder : construye

Measure "1"*--"1" MeasureResult
Measure "1"o--"1" MeasureSetup

BaseMeasureSetupBuilder ..> MeasureSetup : instancia

CalibrationService ..> SessionManager : verifica usuario
CalibrationService ..> CalibrationSetup : modifica datos

MeasureService ..> SessionManager : verifica usuario
MeasureService ..> Measure : modifica datos

SessionManager "1"o--"0..1" Token
SessionManager "1"o--"0..1" User

DataBaseService ..> Measure : persiste la medición
LocalService ..> Measure : importa/exporta la medición

DataBaseService ..> MeasureSetup : persiste el setup
LocalService ..> MeasureSetup : importa/exporta el setup

DataBaseService ..> CalibrationSetup : persiste el setup
LocalService ..> CalibrationSetup : importa/exporta el setup

User "1"-->"0..*" Measure : guarda
User "1"-->"0..*" MeasureSetup : guarda
User "1"-->"0..*" CalibrationSetup : guarda
```

