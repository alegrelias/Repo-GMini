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
	CU1([Configurar la Calibración Electrónica])
	CU2([Ejecutar Calibración Electrónica])
end

%% Asociación
Usuario --> CU1
Usuario --> CU2
```

#### Subsistema 2: Configuración y Toma de Mediciones
##### Módulo 1: Tipos y Estrategias de Medición


```mermaid
flowchart LR
%% Actores
Usuario((Usuario))

subgraph Configuración y Toma de Mediciones
	CU1([Configurar medición])
	CU2([Configurar medición de monofrecuencia])
	CU3([Configurar medición de multifrecuencia])
	CU4([Configurar medición de espectroscopía])
	CU5([Ejecutar medición])
	CU6([Ejecutar medición de monofrecuencia])
	CU7([Ejecutar medición de multifrecuencia])
	CU8([Ejecutar medición de espectroscopía])
	CU9([Visualizar Progreso de medición])
	CU10([Visualizar estadísticos descriptivos básicos])
	CU11([Ejecutar medición en bucle])
	CU12([Visualizar gráficas a partir de resultados])
end

%% Generalización
CU2 ==> CU1
CU3 ==> CU1
CU4 ==> CU1
CU6 ==> CU5
CU7 ==> CU5
CU8 ==> CU5


%% Asociaciones
Usuario --> CU1
Usuario --> CU5
Usuario --> CU10
Usuario --> CU12

%% Relaciones Include/Extend
CU5 -.include.-> CU9
CU11 -.extend.-> CU5
```

#### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

##### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición


```mermaid
flowchart LR
%% Actores
Usuario((Usuario))

subgraph Perfiles de Usuario y Gestión de Setups de Medición
	CU1([Crear Perfil de Usuario])
	CU2([Iniciar sesión])
	CU3([Alternar entre Modos de Uso])
	CU4([Cerrar sesión])
	CU5([Visualizar advertencia por cambio de modo])
	CU6([Aplicar configuraciones])
	CU7([Importar configuraciones])
	CU8([Exportar configuraciones])
	CU9([Visualizar datos guardados])
end

%% Asociaciones
Usuario --> CU1
Usuario --> CU2
Usuario --> CU3
Usuario --> CU4
Usuario --> CU6
Usuario --> CU7
Usuario --> CU8
Usuario --> CU9


%% Relaciones Include/Extend

CU3 -.include.-> CU5
```

#### Subsistema 5: Persistencia

##### Módulo 1: Almacenamiento y Estructura de Datos
```mermaid
flowchart LR
%% Actores
Usuario((Usuario))

subgraph Almacenamiento y Estructura de Datos
	CU1([Guardar Setups de calibración])
	CU2([Guardar Setups de medición])
	CU3([Guardar mediciones con sus resultados])
	CU4([Configurar directorio raíz])
	CU5([Renombrar archivo manualmente])
	CU6([Redactar observaciones])
	CU7([Exportar gráficas generadas])
end

%% Asociaciones
Usuario --> CU1
Usuario --> CU2
Usuario --> CU3
Usuario --> CU4
Usuario --> CU7

%% Relaciones Include/Extend
CU5 -.extend.-> CU3
CU6 -.extend.-> CU1
CU6 -.extend.-> CU2
CU6 -.extend.-> CU3
```

