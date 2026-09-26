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
	CU1([Configurar Medición])
	CU2([Ejecutar Medición])
	CU3([Ejecutar Medición en Bucle])
	CU4([Mostrar Progreso de la Medición])
	CU5([Ejecutar Medición de Monofrecuencia])
	CU6([Ejecutar Medición de Espectroscopía])
	CU7([Ejecutar Medición de Multifrecuencia])
	CU8([Configurar Medición de Monofrecuencia])
	CU9([Configurar Medición de Espectroscopía])
	CU10([Configurar Medición de Multifrecuencia])
	CU11([Seleccionar Canales de Multiplexado])
	CU12([Presentar Estadísticos Descriptivos])
end

%% Jerarquía
Experto ==> Operador

%% Generalización
CU5 ==> CU2
CU6 ==> CU2
CU7 ==> CU2
CU8 ==> CU1
CU9 ==> CU1
CU10 ==> CU1

%% Asociaciones
Experto --> CU1
Experto --> CU11
Operador --> CU2

%% Relaciones Include/Extend
CU3 --extend--> CU2
CU2 --include--> CU4
CU2 --include--> CU12
```

#### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

##### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición


```mermaid
flowchart LR
%% Actores
Operador((Operador))
Experto((Experto))

subgraph Perfiles de Usuario y Gestión de Setups de Medición
	CU1([Guardar Configuración])
	CU2([Exportar Configuración])
	CU3([Importar Configuración])
	CU4([Aplicar Configuración])
	CU5([Adjuntar Observaciones])
	CU6([Cambiar de Perfil])
	CU7([Visualizar Advertencia por Cambio de Perfil])
	CU8([Visualizar Configuraciones Previas])
	CU9([Crear Perfil])
	CU10([Iniciar Sesión])
end

%% Jerarquía
Experto ==> Operador

%% Asociaciones
Experto --> CU1
Operador --> CU2
Operador --> CU3
Operador --> CU4
Operador --> CU8
Operador --> CU5
Operador --> CU6
Operador --> CU9
Operador --> CU10


%% Relaciones Include/Extend
CU6 --include--> CU7
CU4 --extend--> CU8
```

#### Subsistema 5: Persistencia

##### Módulo 1: Almacenamiento y Estructura de Datos
```mermaid
flowchart LR
%% Actores
Operador((Operador))

subgraph Almacenamiento y Estructura de Datos
	CU1([Configurar Directorio Raíz])
	CU2([Renombrar Archivo Manualmente])
	CU4([Guardar Medición])
end

%% Asociaciones
Operador --> CU1
Operador --> CU4

%% Relaciones Include/Extend
CU2 --extend--> CU4
```

