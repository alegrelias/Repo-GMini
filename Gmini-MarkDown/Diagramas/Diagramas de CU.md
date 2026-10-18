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
```

#### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

##### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición


```mermaid
flowchart LR
%% Actores
Usuario((Usuario))

subgraph Perfiles de Usuario y Gestión de Setups de Medición
	CU19([Crear Perfil de Usuario])
	CU20([Iniciar sesión])
	CU21([Alternar entre Modos de Uso])
	CU22([Cerrar sesión])
	CU23([Visualizar advertencia por cambio de modo])
	CU24([Aplicar configuraciones])
	CU25([Importar Datos])
	CU26([Exportar Datos])
	CU27([Importar Configuraciones])
	CU28([Exportar Configuraciones])
	CU29([Importar Mediciones])
	CU30([Exportar Mediciones])
	CU31([Visualizar datos guardados])
end

%% Asociaciones
Usuario --> CU19
Usuario --> CU20
Usuario --> CU21
Usuario --> CU22
Usuario --> CU24
Usuario --> CU25
Usuario --> CU26
Usuario --> CU31

%% Relaciones Include/Extend

CU21 -.include.-> CU23

%% generalización

CU27 ==> CU25
CU29 ==> CU25

CU28 ==> CU26
CU30 ==> CU26
```

#### Subsistema 5: Persistencia

##### Módulo 1: Almacenamiento y Estructura de Datos
```mermaid
flowchart LR
%% Actores
Usuario((Usuario))

subgraph Almacenamiento y Estructura de Datos
	CU32([Guardar Setups de calibración])
	CU33([Guardar Setups de medición])
	CU34([Guardar mediciones con sus resultados])
	CU35([Configurar directorio raíz])
	CU36([Renombrar archivo manualmente])
	CU37([Redactar observaciones])
	CU38([Exportar gráficas generadas])
end

%% Asociaciones
Usuario --> CU32
Usuario --> CU33
Usuario --> CU34
Usuario --> CU35

%% Relaciones Include/Extend
CU36 -.extend.-> CU34
CU37 -.extend.-> CU32
CU37 -.extend.-> CU33
CU37 -.extend.-> CU34
CU38 -.extend.-> CU34
```

