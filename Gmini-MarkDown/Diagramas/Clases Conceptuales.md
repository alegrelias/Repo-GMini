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
	- device_id : int
	- device_temp : float
	- result : MeasureResult
	- observations : str
	- loop_group_id : str
	- iteration_number : int
	+ set_state(new_state : str)
	+ get_state() : str
	+ set_default_name()
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
	+ apply_setup(device : Device, setup : MeasureSetup)
	+ execute_loop(device : Device, base_setup : MeasureSetup, iterations : int, delay : float)
	- update_progress()
}

class LocalService{
	%% operaciones en archivos
	+ load_measure(path : str) : Measure
	+ load_calibration_setup(path : str) : CalibrationSetup
	+ load_setup(path : str) : MeasureSetup
	+ load_user_token(path : str) : Token
	+ export_setup_to_file(path : str, setup : MeasureSetup)
	+ export_calibration_setup_to_file(path : str, setup : CalibrationSetup)
	+  export_measure_to_file(path : str, measure : Measure)
	+ export_user_token(path : str, token : Token)
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
	+ update_user_directory(user_id : int, path : str) 
}


class AuthService{
	+ user_token_file_path : str
	+ login(user_name, email, password) : Token
	+ logout()
	+ register(user_name, email, password) : Token
	+ restore_session(token : str)
}

class SessionManager{
	- current_user : User
	- advanced_mode_active : boolean
	- active_token : Token
	+ switch_user_mode()
	+ get_current_user() : User
	+ set_current_user(user : User)
	+ get_active_mode() : boolean
	+ set_active_mode(mode : boolean)
	+ get_active_token() : Token
	+ set_active_token(token : Token)
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
		+ can_measure() : boolean
	}
	class FreeDeviceState
	class CalibratedState
	class MeasuringState
	class DeviceErrorState
	class UncalibratedState
	
class ConnectionState{
		<<interface>>
		+ connect(context : ConnectionType)
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
	+ encode_setup(setup : MeasureSetup) : str 
	+ encode_execution(setup : MeasureSetup) : str 
	+ decode(response : str) : MeasureResult 
}

class GminiMeasureAdapter{ 
	+ encode_setup(setup : MeasureSetup) : str 
	+ encode_execution(setup : MeasureSetup) : str 
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

class Device{
	- device_id : int
	- device_state : DeviceState
	+ set_state(new_state : DeviceState)
	+ get_state() : DeviceState
}

%% state patern
	
class ConnectionState{
		<<interface>>
		+ connect(context : ConnectionType)
		+ disconnect(context : ConnectionType)
		+ send(context : ConnectionType, data: str)
		+ receive(context : ConnectionType) : str
	}
class ConnectedState
class DisconnectedState
class ConnectionErrorState

class DeviceState{
		<<interface>>
		+ can_measure() : boolean
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

ConnectionService ..|> IObserver : implementa
ConnectionService ..|> IObservable : implementa
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

ConnectionService --> ConnectionType : establece conexión
ConnectionService --> Device : establece conexión
ConnectionService --> ConnectionType : observa
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
	- device_state : DeviceState
	+ set_state(new_state : DeviceState)
	+ get_state() : DeviceState
}

class DeviceState{
		<<interface>>
		+ can_measure() : boolean
	}
	class FreeDeviceState
	class CalibratedState
	class MeasuringState
	class DeviceErrorState
	class UncalibratedState

class CalibrationService{
	+ calibrate_device(device : Device, cal_setup : CalibrationSetup)
}

class SessionManager{
	- current_user : User
	- advanced_mode_active : boolean
	- active_token : Token
	+ switch_user_mode()
	+ get_current_user() : User
	+ set_current_user(user : User)
	+ get_active_mode() : boolean
	+ set_active_mode(mode : boolean)
	+ get_active_token() : Token
	+ set_active_token(token : Token)
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

ConnectionService ..|> IObservable : implementa

MeasureService ..|> IObserver : implementa
MeasureService ..|> IObservable : implementa

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
		+ can_measure() : boolean
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
	- device_id : int
	- device_temp : float
	- result : MeasureResult
	- observations : str
	- loop_group_id : str
	- iteration_number : int
	+ set_state(new_state : str)
	+ get_state() : str
	+ set_default_name()
}

class SessionManager{
	- current_user : User
	- advanced_mode_active : boolean
	- active_token : Token
	+ switch_user_mode()
	+ get_current_user() : User
	+ set_current_user(user : User)
	+ get_active_mode() : boolean
	+ set_active_mode(mode : boolean)
	+ get_active_token() : Token
	+ set_active_token(token : Token)
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
	+ apply_setup(device : Device, setup : MeasureSetup)
	+ execute_loop(device : Device, base_setup : MeasureSetup, iterations : int, delay : float)
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
	+ update_user_directory(user_id : int, path : str)
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

%% adapter pattern
class IMeasureAdapter{ 
	<<interface>>
	+ encode_setup(setup : MeasureSetup) : str 
	+ encode_execution(setup : MeasureSetup) : str 
	+ decode(response : str) : MeasureResult 
}

class GminiMeasureAdapter{ 
	+ encode_setup(setup : MeasureSetup) : str 
	+ encode_execution(setup : MeasureSetup) : str 
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
MeasureService --> ConnectionService : envía comandos y observa
MeasureService --> DataBaseService : invoca guardado de emergencia
MeasureService ..> Device : verifica y actualiza estado

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
	+ user_token_file_path : str
	+ login(user_name, email, password) : Token
	+ logout()
	+ register(user_name, email, password) : Token
	+ restore_session(token : str)
}

class Token {
	- user_id : int
	- token_string : str
	- created_at : DateTime
}

class LocalService{
	%% operaciones en archivos
	+ load_measure(path : str) : Measure
	+ load_calibration_setup(path : str) : CalibrationSetup
	+ load_setup(path : str) : MeasureSetup
	+ load_user_token(path : str) : Token
	+ export_setup_to_file(path : str, setup : MeasureSetup)
	+ export_calibration_setup_to_file(path : str, setup : CalibrationSetup)
	+  export_measure_to_file(path : str, measure : Measure)
	+ export_user_token(path : str, token : Token)
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
	+ update_user_directory(user_id : int, path : str)
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
	+ switch_user_mode()
	+ get_current_user() : User
	+ set_current_user(user : User)
	+ get_active_mode() : boolean
	+ set_active_mode(mode : boolean)
	+ get_active_token() : Token
	+ set_active_token(token : Token)
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
BaseMeasureSetupBuilder ..> MeasureSetup : instancia

AuthService ..> User : crea usuario
AuthService ..> DataBaseService : guarda usuario
AuthService ..> SessionManager : establece usuario
AuthService ..> Token : crea
AuthService ..> LocalService : periste/recupera token

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
class IObservable{
	<<interface>>
	+ attach()
	+ detach()
	+ notify()
}

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
	- device_id : int
	- device_temp : float
	- result : MeasureResult
	- observations : str
	- loop_group_id : str
	- iteration_number : int
	+ set_state(new_state : str)
	+ get_state() : str
	+ set_default_name()
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
	+ switch_user_mode()
	+ get_current_user() : User
	+ set_current_user(user : User)
	+ get_active_mode() : boolean
	+ set_active_mode(mode : boolean)
	+ get_active_token() : Token
	+ set_active_token(token : Token)
}

class Token {
	- user_id : int
	- token_string : str
	- created_at : DateTime
}

class MeasureService{
	+ execute_measure(measure : Measure)
	+ finish_measure() : [MeasureResult]
	+ apply_setup(device : Device, setup : MeasureSetup)
	+ execute_loop(device : Device, base_setup : MeasureSetup, iterations : int, delay : float)
	- update_progress()
}

class CalibrationService{
	+ calibrate_device(device : Device, cal_setup : CalibrationSetup)
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
	+ update_user_directory(user_id : int, path : str)
}

class LocalService{
	%% operaciones en archivos
	+ load_measure(path : str) : Measure
	+ load_calibration_setup(path : str) : CalibrationSetup
	+ load_setup(path : str) : MeasureSetup
	+ load_user_token(path : str) : Token
	+ export_setup_to_file(path : str, setup : MeasureSetup)
	+ export_calibration_setup_to_file(path : str, setup : CalibrationSetup)
	+  export_measure_to_file(path : str, measure : Measure)
	+ export_user_token(path : str, token : Token)
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

LocalService ..> Measure : importa/exporta la medición
LocalService ..> MeasureSetup : importa/exporta el setup
LocalService ..> CalibrationSetup : importa/exporta el setup

DataBaseService ..> Measure : persiste la medición
DataBaseService ..> MeasureSetup : persiste el setup
DataBaseService ..> CalibrationSetup : persiste el setup

MeasureService ..|> IObservable : implementa
```

