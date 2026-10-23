### Diagramas de Casos de Uso

#### Subsistema 1: Comunicación e Interacción con el Hardware

##### Módulo 1: Conectividad y Estado

```mermaid
flowchart LR
%%Actores
Usuario((Usuario Registrado))

subgraph Conectividad y Estado
	CU1([Establecer Conexión con el Dispositivo])
	CU2([Establecer Conexión Inalámbrica])
	CU3([Establecer Conexión Alámbrica])
	CU4([Visualizar Estado de Conexión])
	CU_D4([Enviar comandos por consola de diagnóstico])
end

%%Asignación
Usuario --> CU1
Usuario --> CU4
Usuario --> CU_D4

%%Jerarquía
CU2 ==> CU1
CU3 ==> CU1
```

##### Módulo 2: Calibración del Dispositivo

```mermaid
flowchart LR
%% Actores
Usuario((Usuario Registrado))

subgraph Calibración del Dispositivo
	CU5([Configurar la Calibración Electrónica])
	CU6([Ejecutar Calibración Electrónica])
	CU_D1([Seleccionar canal y patrones físicos])
	CU_D6([Ejecutar recalibración automática])
end

%% Asociación
Usuario --> CU5
Usuario --> CU6
Usuario --> CU_D1

%% Relaciones Extend
CU_D6 -.extend.-> CU6
```

#### Subsistema 2: Configuración y Toma de Mediciones

##### Módulo 1: Tipos y Estrategias de Medición

```mermaid
flowchart LR
%% Actores
Usuario((Usuario Registrado))

subgraph Configuración y Toma de Mediciones
	CU7([Configurar medición])
	CU8([Configurar medición de monofrecuencia])
	CU9([Configurar medición de multifrecuencia])
	CU10([Configurar medición de espectroscopía])
	CU11([Ejecutar medición])
	CU12([Ejecutar medición de monofrecuencia])
	CU13([Ejecutar medición de multifrecuencia])
	CU14([Ejecutar medición de espectroscopía])
	CU15([Visualizar Progreso y Tiempo de medición])
	CU19([Visualizar resultados intermedios])
	CU_D2([Cancelar medición en curso])

	%% Casos de Uso de Automatización incorporados
	CU_A1([Configurar secuencia de automatización])
	CU_A2([Exportar secuencia de automatización])
	CU_A3([Importar secuencia de automatización])
	CU_A4([Ejecutar secuencia de automatización])
end

%% Generalización
CU8 ==> CU7
CU9 ==> CU7
CU10 ==> CU7
CU12 ==> CU11
CU13 ==> CU11
CU14 ==> CU11

%% Asociaciones
Usuario --> CU7
Usuario --> CU11
Usuario --> CU_A1
Usuario --> CU_A2
Usuario --> CU_A3
Usuario --> CU_A4

%% Relaciones Include/Extend
CU11 -.include.-> CU15
CU11 -.include.-> CU19
CU_D2 -.extend.-> CU11
CU_A4 -.include.-> CU11
```

#### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

##### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición

```mermaid
flowchart LR
%% Actores
Usuario((Usuario Registrado))

subgraph Perfiles de Usuario y Gestión de Sesiones
	CU20([Inicializar entorno de trabajo])
	CU21([Crear Perfil de Usuario])
	CU22([Iniciar sesión])
	CU24([Cerrar sesión])
	CU26([Aplicar configuraciones])
	CU27([Importar Datos])
	CU29([Importar Configuraciones])
	CU30([Exportar Configuraciones])
	CU31([Importar Mediciones])
	CU32([Exportar Mediciones])
	CU33([Visualizar datos guardados])
	CU34([Exportar gráficas generadas])
	CU_B7([Crear nueva sesión experimental])
	CU_B8([Importar sesión experimental])
	CU_B9([Cargar sesión experimental])
	CU_B10([Renombrar sesión experimental])
end

%% Asociaciones
Usuario --> CU20
Usuario --> CU21
Usuario --> CU22
Usuario --> CU24
Usuario --> CU26
Usuario --> CU29
Usuario --> CU31
Usuario --> CU30
Usuario --> CU32
Usuario --> CU34
Usuario --> CU33
Usuario --> CU_B7
Usuario --> CU_B8
Usuario --> CU_B9
Usuario --> CU_B10

```

##### Módulo 2: Análisis y Visualización (Workspace)

```mermaid
flowchart LR
%% Actores
Usuario((Usuario Registrado))

subgraph Análisis y Visualización
	CU_B1([Manipular curvas de medición])
	CU_B2([Navegar en gráficos de espectroscopía])
	CU_B3([Visualizar datos en formato tabular])
	CU_B4([Manipular datos en tabla interactiva])
	CU_B6([Calcular estadística descriptiva])
	CU_C1([Aplicar ajuste de modelo matemático])
	CU_C2([Configurar modelo de circuito equivalente predefinido])
end

%% Asociaciones
Usuario --> CU_B1
Usuario --> CU_B2
Usuario --> CU_B3
Usuario --> CU_B4
Usuario --> CU_B6
Usuario --> CU_C1
Usuario --> CU_C2
```

#### Subsistema 4: Entorno de Ejecución y Plataforma

##### Módulo 1: Interfaz y Trazabilidad

```mermaid
flowchart LR
%% Actores
Usuario((Usuario Registrado))

subgraph Interfaz y Trazabilidad
	CU_D3([Visualizar registro de eventos - Logs])
	CU_D7([Personalizar distribución de paneles])
end

%% Asociaciones
Usuario --> CU_D3
Usuario --> CU_D7
```

#### Subsistema 5: Persistencia

##### Módulo 1: Almacenamiento y Estructura de Datos

```mermaid
flowchart LR
%% Actores
Usuario((Usuario Registrado))

subgraph Almacenamiento y Estructura de Datos
	CU35([Guardar Setups de calibración])
	CU36([Guardar Setups de medición])
	CU37([Guardar mediciones con sus resultados])
	CU38([Configurar directorio raíz])
	CU39([Renombrar archivo manualmente])
	CU40([Redactar observaciones])
	CU41([Guardar Sesión Experimental])
	CU42([Guardar Secuencia Automatica ])
end

%% Asociaciones
Usuario --> CU35
Usuario --> CU36
Usuario --> CU37
Usuario --> CU38
Usuario --> CU41
Usuario --> CU42

%% Relaciones Include/Extend
CU39 -.extend.-> CU37
CU40 -.extend.-> CU35
CU40 -.extend.-> CU36
CU40 -.extend.-> CU37
CU39 -.extend.-> CU41
CU39 -.extend.-> CU42
```
