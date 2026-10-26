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
Usuario --> CU16
Usuario --> CU18

%% Relaciones Include/Extend
CU11 -.include.-> CU15
CU17 -.extend.-> CU11
CU17 -.include.-> CU19
```

#### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

##### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición


```mermaid
flowchart LR
%% Actores
Usuario((Usuario))

subgraph Perfiles de Usuario y Gestión de Setups de Medición
	CU20([Iniciar la aplicación])
	CU21([Crear Perfil de Usuario])
	CU22([Iniciar sesión])
	CU23([Alternar entre Modos de Uso])
	CU24([Cerrar sesión])
	CU25([Visualizar advertencia por cambio de modo])
	CU26([Aplicar configuraciones])
	CU27([Importar Datos])
	CU28([Exportar Datos])
	CU29([Importar Configuraciones])
	CU30([Exportar Configuraciones])
	CU31([Importar Mediciones])
	CU32([Exportar Mediciones])
	CU33([Visualizar datos guardados])
	CU34([Exportar gráficas generadas])
end

%% Asociaciones
Usuario --> CU20
Usuario --> CU21
Usuario --> CU22
Usuario --> CU23
Usuario --> CU24
Usuario --> CU26
Usuario --> CU27
Usuario --> CU28
Usuario --> CU33

%% Relaciones Include/Extend

CU23 -.include.-> CU25

%% generalización

CU29 ==> CU27
CU31 ==> CU27

CU30 ==> CU28
CU32 ==> CU28
CU34 ==> CU28
```

#### Subsistema 5: Persistencia

##### Módulo 1: Almacenamiento y Estructura de Datos
```mermaid
flowchart LR
%% Actores
Usuario((Usuario))

subgraph Almacenamiento y Estructura de Datos
	CU35([Guardar Setups de calibración])
	CU36([Guardar Setups de medición])
	CU37([Guardar mediciones con sus resultados])
	CU38([Configurar directorio raíz])
	CU39([Renombrar archivo manualmente])
	CU40([Redactar observaciones])
end

%% Asociaciones
Usuario --> CU35
Usuario --> CU36
Usuario --> CU37
Usuario --> CU38

%% Relaciones Include/Extend
CU39 -.extend.-> CU37
CU40 -.extend.-> CU35
CU40 -.extend.-> CU36
CU40 -.extend.-> CU37
```

