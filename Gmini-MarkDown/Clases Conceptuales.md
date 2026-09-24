NOTA: hay una regla de seguridad inquebrantable para aplicaciones locales: las contraseñas nunca deben guardarse en texto plano en la base de datos. Debés aplicar una función de hash (como _bcrypt_) antes de guardarlas en SQLite. De esta forma, si el archivo `.db` de la aplicación se copia o transfiere, las credenciales de los miembros del laboratorio permanecen protegidas.
# Patrones a mirar
- Builder
- Strategy
- Decorator
- Facade
- Proxy
- Memento
- Template
# Clases Identificadas

+ Usuario (Abstracto)
	+ Operador
	+ Experto
+ Medicion (Abstracto) la `Medicion` representa la acción de medir
	+ Espectroscopia
	+ Monofrecuencia
	+ Multifrecuencia
+ SetupMedicion (Abstracto) El `SetupMedicion` tiene los parámetros (frecuencias, retardos)
	+ SetupEspectroscopia
	+ SetupMonofrecuencia
	+ SetupMultifrecuencia
+ SetupCalibracion
+ Placa
+ ResultadoMedicion `ResultadosMedicion` tiene los números crudos.
+ TipoConexion (Interfaz)
	+ Alambrica
	+ Inalambrica
+ ServicioMedicion
+ ServicioPersistencia
+ ServicioAutenticacion

```mermaid
classDiagram
direction LR

%% jerarquias
Usuario <|-- Experto
Usuario <|-- Operador

SetupMedicion <|-- SetupEspectroscopia
SetupMedicion <|-- SetupMonofrecuencia
SetupMedicion <|-- SetupMultifrecuencia

TipoConexion <|-- Alambrica
TipoConexion <|-- Inalambrica

Medicion <|-- Espectroscopia
Medicion <|-- Monofrecuencia
Medicion <|-- Multifrecuencia


    class Usuario {
        <<abstract>>
    }
    class Operador
    class Experto

    class Medicion {
        <<abstract>>
    }
    class Espectroscopia
    class Monofrecuencia
    class Multifrecuencia

    class SetupMedicion {
        <<abstract>>
    }
    class SetupEspectroscopia
    class SetupMonofrecuencia
    class SetupMultifrecuencia
    
    class SetupCalibracion
    class Placa
    class ResultadoMedicion

    class TipoConexion {
        <<interface>>
    }
    class Alambrica
    class Inalambrica

    class ServicioMedicion
    class ServicioPersistencia
    class ServicioAutenticacion
```

##### Subsistema 1: Comunicación e Interacción con el Hardware

##### Módulo 1: Conectividad y Estado

```mermaid
classDiagram

%% jerarquias

TipoConexion <|-- Alambrica
TipoConexion <|-- Inalambrica

%% clases

class TipoConexion {
        <<interface>>
    }
    class Alambrica
    class Inalambrica

class Operador

class Placa

ServicioMedicion

%% relaciones

Operador -- ServicioMedicion
Placa -- TipoConexion
Placa -- ServicioMedicion
```

##### Módulo 2: Calibración del Dispositivo
```mermaid
classDiagram

%% jerarquias
Usuario <|-- Experto
Usuario <|-- Operador

%% clases
class Usuario {
        <<abstract>>
    }
class Experto
class Operador
class SetupCalibracion
class Placa
class ServicioMedicion
class ServicioPersistencia

%% relaciones
Usuario -- ServicioMedicion
Placa -- ServicioMedicion
ServicioMedicion -- SetupCalibracion
SetupCalibracion -- ServicioPersistencia
```

#### Subsistema 2: Configuración y Toma de Mediciones
##### Módulo 1: Tipos y Estrategias de Medición

```mermaid
classDiagram

%% jerarquias
Usuario <|-- Experto
Usuario <|-- Operador

Medicion <|-- Espectroscopia
Medicion <|-- Monofrecuencia
Medicion <|-- Multifrecuencia

SetupMedicion <|-- SetupEspectroscopia
SetupMedicion <|-- SetupMonofrecuencia
SetupMedicion <|-- SetupMultifrecuencia

%% clases
class Usuario {
        <<abstract>>
    }
class Experto
class Operador

class Medicion{
		<<abstract>>
	}
class Espectroscopia
class Monofrecuencia
class Multifrecuencia

class SetupMedicion{
		<<abstract>>
	}
class SetupEspectroscopia
class SetupMonofrecuencia
class SetupMultifrecuencia

class Placa
class ServicioMedicion
class ResultadoMedicion

%% relaciones
Usuario -- ServicioMedicion
ServicioMedicion -- Placa
ServicioMedicion -- Medicion

Medicion -- SetupMedicion
Medicion -- ResultadoMedicion
```
#### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

##### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición
```mermaid
classDiagram

%% jerarquias
Usuario <|-- Experto
Usuario <|-- Operador

SetupMedicion <|-- SetupEspectroscopia
SetupMedicion <|-- SetupMonofrecuencia
SetupMedicion <|-- SetupMultifrecuencia

%% clases
class Usuario {
        <<abstract>>
    }
class Experto
class Operador

class SetupMedicion{
		<<abstract>>
	}
class SetupEspectroscopia
class SetupMonofrecuencia
class SetupMultifrecuencia

class ServicioAutenticacion
class ServicioPersistencia

%% relaciones
Usuario -- ServicioPersistencia
Usuario -- ServicioAutenticacion
SetupMedicion -- ServicioPersistencia
```

#### Subsistema 5: Persistencia

##### Módulo 1: Almacenamiento y Estructura de Datos

```mermaid
classDiagram

%% jerarquias
Medicion <|-- Espectroscopia
Medicion <|-- Monofrecuencia
Medicion <|-- Multifrecuencia

%% clases
class Usuario
class ServicioPersistencia
class ServicioMedicion

class Medicion{
		<<abstract>>
	}
class Espectroscopia
class Monofrecuencia
class Multifrecuencia

class ResultadoMedicion

%% relaciones
Usuario -- ServicioMedicion
Usuario -- ServicioPersistencia

ServicioMedicion -- Medicion
Medicion -- ResultadoMedicion

%% Nuevas relaciones clave para la persistencia
ServicioMedicion -- ServicioPersistencia
Medicion -- ServicioPersistencia
ResultadoMedicion -- ServicioPersistencia
```

