### Diagramas de Casos de Uso

#### Subsistema 1: Comunicación e Interacción con el Hardware

##### Módulo 1: Conectividad y Estado

```mermaid
usecase-beta

actor user("Usuario Registrado")


systemBoundary "Conectividad y Estado"
	CU1("Establecer Conexión con el Dispositivo")
	CU2("Establecer Conexión Inalámbrica")
	CU3("Establecer Conexión Alámbrica")
	CU4("Visualizar Estado de Conexión")
	CU5("Enviar comandos por consola de diagnóstico")
end

user --> CU1
user --> CU4
user --> CU5

CU2 --hereda--> CU1
CU3 --hereda--> CU1
```


##### Módulo 2: Calibración del Dispositivo

```mermaid
usecase-beta
%% Actores
actor user("Usuario Registrado")

systemBoundary "Calibración del Dispositivo"
	CU5("Configurar la Calibración Electrónica")
	CU6("Ejecutar Calibración Electrónica")
	CU_D1("Seleccionar canal y patrones físicos")
	CU_D6("Ejecutar recalibración automática")
end

%% Asociación
user --> CU5
user --> CU6
user --> CU_D1

%% Relaciones Extend
CU_D6 --extend--> CU6
```

#### Subsistema 2: Configuración y Toma de Mediciones

##### Módulo 1: Tipos y Estrategias de Medición

```mermaid
usecase-beta
%% Actores
actor user("Usuario Registrado")

systemBoundary "Configuración y Toma de Mediciones"
	CU7("Configurar medición")
	CU8("Configurar medición de monofrecuencia")
	CU9("Configurar medición de multifrecuencia")
	CU10("Configurar medición de espectroscopía")
	CU11("Ejecutar medición")
	CU12("Ejecutar medición de monofrecuencia")
	CU13("Ejecutar medición de multifrecuencia")
	CU14("Ejecutar medición de espectroscopía")
	CU15("Visualizar Progreso y Tiempo de medición")
	CU19("Visualizar resultados intermedios")
	CU_D2("Cancelar medición en curso")

	%% Casos de Uso de Automatización incorporados
	CU_A1("Configurar secuencia de automatización")
	CU_A4("Ejecutar secuencia de automatización")
end

%% Generalización
CU8 --hereda--> CU7
CU9 --hereda--> CU7
CU10 --hereda--> CU7
CU12 --hereda--> CU11
CU13 --hereda--> CU11
CU14 --hereda--> CU11

%% Asociaciones
user --> CU7
user --> CU11
user --> CU_A1
user --> CU_A4

%% Relaciones Include/Extend
CU11 --include--> CU15
CU11 --include--> CU19
CU_D2 --extend--> CU11
CU_A4 --include--> CU11
```

#### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

##### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición

```mermaid
usecase-beta
%% Actores
actor user("Usuario Registrado")

systemBoundary "Perfiles de Usuario y Gestión de Sesiones"
	CU20("Inicializar entorno de trabajo")
	CU21("Crear Perfil de Usuario")
	CU22("Iniciar sesión")
	CU24("Cerrar sesión")
	CU26("Aplicar configuraciones")
	CU29("Importar Configuraciones")
	CU30("Exportar Configuraciones")
	CU31("Importar Mediciones")
	CU32("Exportar Mediciones")
	CU33("Visualizar datos guardados")
	CU34("Exportar gráficas generadas")
	CU_B7("Crear nueva sesión experimental")
	CU_B8("Importar sesión experimental")
	CU_B9("Cargar sesión experimental")
	CU_B10("Renombrar sesión experimental")
	CU_A2("Exportar secuencia de automatización")
	CU_A3("Importar secuencia de automatización")
end

%% Asociaciones
user --> CU20
user --> CU21
user --> CU22
user --> CU24
user --> CU26
user --> CU29
user --> CU31
user --> CU30
user --> CU32
user --> CU34
user --> CU33
user --> CU_B7
user --> CU_B8
user --> CU_B9
user --> CU_B10
user --> CU_A2
user --> CU_A3

```

##### Módulo 2: Análisis y Visualización (Workspace)

```mermaid
usecase-beta
%% Actores
actor user("Usuario Registrado")

systemBoundary "Análisis y Visualización"
	CU_B1("Manipular curvas de medición")
	CU_B2("Navegar en gráficos de espectroscopía")
	CU_B3("Visualizar datos en formato tabular")
	CU_B4("Manipular datos en tabla interactiva")
	CU_B6("Calcular estadística descriptiva")
	CU_C1("Aplicar ajuste de modelo matemático")
	CU_C2("Configurar modelo de circuito equivalente predefinido")
end

%% Asociaciones
user --> CU_B1
user --> CU_B2
user --> CU_B3
user --> CU_B4
user --> CU_B6
user --> CU_C1
user --> CU_C2
```

#### Subsistema 4: Entorno de Ejecución y Plataforma

##### Módulo 2: Interfaz y Trazabilidad

```mermaid
usecase-beta
%% Actores
actor user("Usuario Registrado")

systemBoundary "Interfaz y Trazabilidad"
	CU_D3("Visualizar registro de eventos - Logs")
	CU_D7("Personalizar distribución de paneles")
end

%% Asociaciones
user --> CU_D3
user --> CU_D7
```

#### Subsistema 5: Persistencia

##### Módulo 1: Almacenamiento y Estructura de Datos

```mermaid
usecase-beta
%% Actores
actor user("Usuario Registrado")

systemBoundary "Almacenamiento y Estructura de Datos"
	CU35("Guardar Setups de calibración")
	CU36("Guardar Setups de medición")
	CU37("Guardar mediciones con sus resultados")
	CU38("Configurar directorio raíz")
	CU39("Renombrar archivo manualmente")
	CU40("Redactar observaciones")
	CU41("Guardar Sesión Experimental")
	CU42("Guardar Secuencia Automatica ")
end

%% Asociaciones
user --> CU35
user --> CU36
user --> CU37
user --> CU38
user --> CU41
user --> CU42

%% Relaciones Include/Extend
CU39 --extend--> CU37
CU40 --extend--> CU35
CU40 --extend--> CU36
CU40 --extend--> CU37
CU39 --extend--> CU41
CU39 --extend--> CU42
```
