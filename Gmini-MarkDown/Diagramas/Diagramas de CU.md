### Diagramas de Casos de Uso
#### Subsistema 1: Comunicación e Interacción con el Hardware

##### Módulo 1: Conectividad y Estado
```mermaid
flowchart LR
%%Actores
Usuario((Usuario))

subgraph Conectividad y Estado
	CU1([Establecer Conexión con el Dispositivo])
	CU2([Establecer Conexión Inalámbrica])
	CU3([Establecer Conexión Alámbrica])
	CU4([Visualizar Estado de Conexión])
end

%%Asignación
Usuario --> CU1
Usuario --> CU4

%%Jerarquía
CU2 ==> CU1
CU3 ==> CU1
```

##### Módulo 2: Calibración del Dispositivo
```mermaid
flowchart LR
%% Actores
Usuario((Usuario))

subgraph Calibración del Dispositivo
	CU5([Configurar la Calibración Electrónica])
	CU6([Ejecutar Calibración Electrónica])
end

%% Asociación
Usuario --> CU5
Usuario --> CU6
```

#### Subsistema 2: Configuración y Toma de Mediciones
##### Módulo 1: Tipos y Estrategias de Medición


```mermaid
flowchart LR
%% Actores
Usuario((Usuario))

subgraph Configuración y Toma de Mediciones
	CU7([Configurar medición])
	CU8([Configurar medición de monofrecuencia])
	CU9([Configurar medición de multifrecuencia])
	CU10([Configurar medición de espectroscopía])
	CU11([Ejecutar medición])
	CU12([Ejecutar medición de monofrecuencia])
	CU13([Ejecutar medición de multifrecuencia])
	CU14([Ejecutar medición de espectroscopía])
	CU15([Visualizar Progreso de medición])
	CU16([Visualizar estadísticos descriptivos básicos])
	CU17([Ejecutar medición en bucle])
	CU18([Visualizar gráficas a partir de resultados])
	CU19([Visualizar resultados intermedios])
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

%% Relaciones Include/Extend
CU11 -.include.-> CU15
CU16 -.extend.-> CU11
CU17 -.extend.-> CU11
CU18 -.extend.-> CU11
CU17 -.include.-> CU19
```

#### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

##### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición


```mermaid
flowchart LR
%% Actores
Usuario((Usuario))

subgraph Perfiles de Usuario y Gestión de Setups de Medición
	CU20([Crear Perfil de Usuario])
	CU21([Iniciar sesión])
	CU22([Alternar entre Modos de Uso])
	CU23([Cerrar sesión])
	CU24([Visualizar advertencia por cambio de modo])
	CU25([Aplicar configuraciones])
	CU26([Importar Datos])
	CU27([Exportar Datos])
	CU28([Importar Configuraciones])
	CU29([Exportar Configuraciones])
	CU30([Importar Mediciones])
	CU31([Exportar Mediciones])
	CU32([Visualizar datos guardados])
end

%% Asociaciones
Usuario --> CU20
Usuario --> CU21
Usuario --> CU22
Usuario --> CU23
Usuario --> CU25
Usuario --> CU26
Usuario --> CU27
Usuario --> CU32

%% Relaciones Include/Extend

CU22 -.include.-> CU24

%% generalización

CU28 ==> CU26
CU30 ==> CU26

CU29 ==> CU27
CU31 ==> CU27
```

#### Subsistema 5: Persistencia

##### Módulo 1: Almacenamiento y Estructura de Datos
```mermaid
flowchart LR
%% Actores
Usuario((Usuario))

subgraph Almacenamiento y Estructura de Datos
	CU33([Guardar Setups de calibración])
	CU34([Guardar Setups de medición])
	CU35([Guardar mediciones con sus resultados])
	CU36([Configurar directorio raíz])
	CU37([Renombrar archivo manualmente])
	CU38([Redactar observaciones])
	CU39([Exportar gráficas generadas])
end

%% Asociaciones
Usuario --> CU33
Usuario --> CU34
Usuario --> CU35
Usuario --> CU36

%% Relaciones Include/Extend
CU37 -.extend.-> CU35
CU38 -.extend.-> CU33
CU38 -.extend.-> CU34
CU38 -.extend.-> CU35
CU39 -.extend.-> CU35
```

