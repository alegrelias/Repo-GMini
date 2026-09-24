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
