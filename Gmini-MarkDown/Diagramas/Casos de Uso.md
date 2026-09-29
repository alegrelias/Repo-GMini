##### Extensiones e Inclusiones
```mermaid
flowchart LR
subgraph Subsistema
	CU1([Caso de Uso Base])
	CU2([Caso de Uso Extensión])
	CU3([Caso de Uso Inclusión])
end

CU2 --extend--> CU1
CU1 --include--> CU3
```

### Diagramas de Casos de Uso
#### Subsistema 1: Comunicación e Interacción con el Hardware

##### Módulo 1: Conectividad y Estado
```mermaid
flowchart LR
%%Actores
Operador((Operador))

subgraph Conectividad y Estado
	CU1([Establecer Conexión con el Dispositivo])
	CU2([Establecer Conexión Inalámbrica])
	CU3([Establecer Conexión Alámbrica])
	CU4([Visualizar Estado de Conexión])
end

%%Asignación
Operador --> CU1
Operador --> CU4

%%Jerarquía
CU2 ==> CU1
CU3 ==> CU1
```

##### Módulo 2: Calibración del Dispositivo
```mermaid
flowchart LR
%% Actores
Operador((Operador))
Experto((Experto))

subgraph Calibración del Dispositivo
	CU1([Configurar la Calibración Electrónica])
	CU2([Ejecutar Calibración Electrónica])
end

%% Jerarquía
Experto ==> Operador

%% Asociación
Experto --> CU1
Operador --> CU2
```

#### Subsistema 2: Configuración y Toma de Mediciones
##### Módulo 1: Tipos y Estrategias de Medición


```mermaid
flowchart LR
%% Actores
Operador((Operador))
Experto((Experto))

subgraph Configuración y Toma de Mediciones
	CU1([Seleccionar canales de multiplexado])
	CU2([Configurar medición])
	CU3([Configurar medición de monofrecuencia])
	CU4([Configurar medición de multifrecuencia])
	CU5([Configurar medición de espectroscopía])
	CU6([Ejecutar medición])
	CU7([Ejecutar medición de monofrecuencia])
	CU8([Ejecutar medición de multifrecuencia])
	CU9([Ejecutar medición de espectroscopía])
	CU10([Visualizar Progreso de medición])
	CU11([Visualizar Resultados intermedios])
	CU12([Visualizar estadísticos descriptivos básicos])
	CU13([Ejecutar medición en bucle])
	
end

%% Jerarquía
Experto ==> Operador

%% Generalización
CU3 ==> CU2
CU4 ==> CU2
CU5 ==> CU2
CU7 ==> CU6
CU8 ==> CU6
CU9 ==> CU6


%% Asociaciones
Experto --> CU1
Experto --> CU2
Operador --> CU6

%% Relaciones Include/Extend
CU6 -.include.-> CU10
CU6 -.include.-> CU11
CU6 -.include.-> CU12

CU13 -.extend.-> CU6
```

#### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

##### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición


```mermaid
flowchart LR
%% Actores
Operador((Operador))

subgraph Perfiles de Usuario y Gestión de Setups de Medición
	CU1([Crear Perfil de Usuario])
	CU2([Iniciar sesión])
	CU3([Cambiar entre perfiles])
	CU4([Cerrar sesión])
	CU5([Visualizar advertencia por cambio de perfil])
	CU6([Aplicar configuraciones])
	CU7([Importar configuraciones])
	CU8([Exportar configuraciones])
	CU9([Visualizar datos guardados])
end

%% Asociaciones
Operador --> CU1
Operador --> CU2
Operador --> CU3
Operador --> CU4
Operador --> CU6
Operador --> CU7
Operador --> CU8
Operador --> CU9


%% Relaciones Include/Extend

CU3 -.include.-> CU5
```

#### Subsistema 5: Persistencia

##### Módulo 1: Almacenamiento y Estructura de Datos
```mermaid
flowchart LR
%% Actores
Operador((Operador))
Experto((Experto))

%% Jerarquía
Experto ==> Operador

subgraph Almacenamiento y Estructura de Datos
	CU1([Guardar Setups de calibración])
	CU2([Guardar Setups de medición])
	CU3([Guardar mediciones con sus resultados])
	CU4([Configurar directorio raíz])
	CU5([Renombrar archivo manualmente])
end

%% Asociaciones
Experto --> CU1
Experto --> CU2
Operador --> CU3
Operador --> CU4

%% Relaciones Include/Extend
CU5 -.extend.-> CU3
```

