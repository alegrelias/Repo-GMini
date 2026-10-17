
#### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

##### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición

##### Crear Perfil de Usuario

```mermaid
sequenceDiagram
autonumber

actor U as Usuario
participant G as Interfaz (GUI)
participant auth as AuthService


U->>G: Solicitud de Registro
G->>auth: register(user_name, email, password)


participant dbs as DataBaseService
participant db as Base de Datos

auth->>dbs: get_user_by_email(email)
dbs->>db: SELECT * FROM USER WHERE email = @email_param
alt Usuario Inexistente
	db-->>dbs: NULL
	dbs-->>auth: null
	auth->>auth: hashed_password = rehash_password(password)
	create participant user as User
	auth->>user: new User(user_name, email, hashed_password, null)
	user-->>auth: Instancia creada
	auth->>dbs: save_user(user : User)
	dbs->>db: INSERT INTO USER (user_name, email, password, root_directory) VALUES(user_name, email, hashed_password, null)
	db-->>dbs: Confirmacion de Guardado
	dbs->>db: SELECT last_insert_rowid()
	db-->>dbs: user_id
	dbs->>user: set_user_id(user_id)
	dbs-->>auth: Confirmacion de Guardado
	auth-->>G: True
	G-->>U: Registro exitoso
else
	db-->>dbs: USER.user_name, USER.email, USER.password, USER.root_directory
	dbs-->>auth: User
	auth-->>G: False
	G-->>U: Usuario no registrado
end
```

##### Iniciar Sesión
```mermaid
sequenceDiagram
autonumber

actor U as Usuario
participant G as Interfaz (GUI)
participant auth as AuthService

U->>G: Solicitud de Inicio de Sesión
G->>auth: login(user_name, password)
participant dbs as DataBaseService
participant db as Base de Datos
auth->>dbs: get_user_by_name(user_name)
dbs->>db: SELECT * FROM USER WHERE user_name = @user_name_param
alt Usuario Registrado
	db-->>dbs: USER.user_name, USER.email, USER.password, USER.root_directory
	dbs-->>auth: User
	auth->>auth: verify_password(password)
	alt Contraseña Correcta
		participant session as SessionManager
		auth->>session: set_current_user(user)
		auth->>auth: token_string = generate_token()
		create participant T as Token
		auth->>T: new Token(user_id, token_string, created_at)
		T-->>auth: Instancia Creada
		auth->>session: set_active_token(token)
		participant local as LocalService
		auth->>local: export_user_token(path, token)
		local-->>auth: Guardado exitoso
		auth->>session: set_active_mode(False)
		auth-->>G: True
		G-->>U: Inicio de sesión exitoso
	
	else Contraseña Incorrecta
			auth-->>G: False
			G-->>U: Inicio de sesión rechazado
	end
	
else Usuario Inexistente
	db-->>dbs: NULL
	dbs-->>auth: null
	auth-->>G: False
	G-->>U: Inicio de sesión rechazado
end
```

##### Alternar entre Modos de Uso

```mermaid
sequenceDiagram
autonumber

actor U as Usuario
participant G as Interfaz (GUI)
participant session as SessionManager

U->>G: Solicitud de Cambio de Modo de Uso
G->>U: Solicitud de Confirmación
alt Usuario Acepta 
	U-->>G: Aceptar
	G->>session: switch_user_mode()
	session->>session: notify()
	session->>G: update(observable, event_info)
	G->>session: get_active_mode()
	alt Cambia a Modo Avanzado
		session-->>G: True
		G-->>U: Cambio de modo (avanzado) aplicado
	else Cambia a Modo Básico
		session-->>G: False
		G-->>U: Cambio de modo (básico) aplicado
	end
	
else Usuario Cancela
	U-->>G: Cancelar
	G-->>U: Cambio de modo cancelado
end


```

##### Cerrar Sesión
```mermaid
sequenceDiagram
autonumber

actor U as Usuario
participant G as Interfaz (GUI)
participant auth as AuthService
participant session as SessionManager
participant local as LocalService

U->>G: Solicitud de Cierre de Sesión
G->>auth: logout()
auth->>local: delete_token()
local-->>auth: Eliminación exitosa
auth->>session: set_active_token(null)
auth->>session: set_current_user(null)
session->>session: notify()
session->>G: update(observable, event_info)
auth-->>G: True
G-->>U: Cierre de Sesión exitoso


```

##### Exportar Configuraciones

```mermaid
sequenceDiagram
autonumber

actor U as Usuario
participant G as Interfaz (GUI)
participant local as LocalService

U->>G: Solicita exportar configuraciones
G->>U: Desplegar selector de directorios
alt Usuario Selecciona un directorio
	U-->>G: Seleccionar ruta
	alt La configuración es de calibración
		G->>local: export_calibration_setup_to_file(path, CalibrationSetup)
		local-->>G: True
		G-->>U: Confirmación de guardado
	else La configuración es de medición
		G->>local: export_setup_to_file(path, MeasureSetup)
		local-->>G: True
		G-->>U: Confirmación de guardado
	end
else Usuario cancela
	U-->>G: Cancelar guardado
	G-->>U: Guardado de archivo cancelado
end
```
##### Importar Configuraciones

```mermaid
sequenceDiagram
autonumber

actor U as Usuario
participant G as Interfaz (GUI)
participant local as LocalService
participant dbs as DataBaseService
participant session as SessionManager
participant db as Base de Datos

U->>G: Solicita importar configuraciones
G->>U: Desplegar selector de directorios
alt Usuario Selecciona un directorio
	U-->>G: Seleccionar ruta
	alt La configuración es de calibración
		G->>local: load_calibration_setup_to_file(path)
		create participant C as CalibrationSetup
		local->>C: new CalibrationSetup(observations, channel, z_calc_value_real, z_calc_value_imag)
		C-->>local: Instancia creada
		local->>dbs: save_calibration_setup(cal_setup)
		dbs->>session: get_current_user()
		session-->>dbs: User
		dbs->>db: INSERT INTO CALIBRATION_SETUP(user_id, ...) VALUES(user_id,...)
		db-->>dbs: Confirmación de guardado
		dbs-->>local: True
		local-->>G: True
		G-->>U: Importación exitosa
		
	else La configuración es de medición	
		G->>local: load_setup_to_file(path)
		create participant M as MeasureSetup
		local->>M: new MeasureSetup(observations, exitation_voltage, gain, rfbvalue, settcycles, mux_channel)
		M-->>local: Instancia creada
		local->>dbs: save_measure_setup(m_setup)
		dbs->>session: get_current_user()
		session-->>dbs: User
		dbs->>db: INSERT INTO MEASURE_SETUP (user_id, ...) VALUES (user_id, ...)
		db-->>dbs: Confirmación de guardado
		dbs-->>local: True
		local-->>G: True
		G-->>U: Importación exitosa
	end
else Usuario cancela
	U-->>G: Cancelar importación
	G-->>U: Importación de archivo cancelada
end
```


#### Subsistema 5: Persistencia

##### Módulo 1: Almacenamiento y Estructura de Dato

##### Configurar directorio raíz
```mermaid
sequenceDiagram
autonumber

actor U as Usuario
participant G as Interfaz (GUI)
participant session as SessionManager
participant dbs as DataBaseService
participant db as Base de Datos
participant user as User

U->>G: Solicitud de cambio de directorio
G->>session: get_current_user()
session-->>G: User
G->>U: Desplegar selector de directorios
alt Usuario Confirma
	U-->>G: Seleccionar ruta
	G->>dbs: update_user_directory(user_id, path)
	dbs->>db: UPDATE USER SET root_directory = @param_root_directory WHERE user_id = @param_user_id
	db-->>dbs: Confirmación de actualización
	dbs-->>G: True
	G->>user: set_root_directory(path)
	G-->>U: Cambio de directorio exitoso
else Usuario Cancela
	U-->>G: Cancelar Cambio
	G-->>U: Cambio de directorio cancelado
end
```
