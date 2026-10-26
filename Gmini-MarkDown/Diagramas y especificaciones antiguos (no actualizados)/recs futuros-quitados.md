#### **Módulo 2: Calibración del Dispositivo**

| **CAL-04**      | Limitar la configuración de calibración al Modo Avanzado                                                                                   |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                        |
| **Descripción** | El sistema solo debe permitir parametrizar la secuencia de comandos de calibración del hardware si se encuentra activado el Modo Avanzado. |

### Subsistema 2: Configuración y Toma de Mediciones
#### Módulo 1: Tipos y Estrategias de Medición

| **MED-13**      | Limitar configuración de mediciones al Modo Avanzado                                                                              |
| :-------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                               |
| **Descripción** | El sistema solo debe permitir configurar setups de medición (independientemente del tipo) si se encuentra activo el Modo Avanzado |

### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

#### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición

| **SET-06**      | Habilitar Modos de Uso                                                                                                                 |
| :-------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                    |
| **Descripción** | La aplicación debe proveer dos modos de uso intercambiables desde la interfaz gráfica, definidos como "Modo Avanzado" y "Modo Básico". |

| **SET-07**      | Habilitar Modo Avanzado                                                                                        |
| :-------------- | -------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                            |
| **Descripción** | La aplicación debe proveer un "Modo Avanzado" con acceso total a la configuración de parámetros y calibración. |

| **SET-08**      | Habilitar Modo Básico                                                                                                                                                           |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                                                             |
| **Descripción** | La aplicación debe proveer un "Modo Básico" con permisos restringidos exclusivamente a la ejecución de mediciones y ejecución de calibración (con los parámetros predefinidos). |

| **SET-09**      | Cambiar entre modos de uso                                                     |
| :-------------- | ------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario Registrado.                                                            |
| **Descripción** | El sistema tiene que permitir a un usuario realizar cambios de modo dinámicos. |

| **SET-10**      | Advertir sobre cambio de modo                                                                              |
| :-------------- | ---------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                        |
| **Descripción** | El sistema debe desplegar una alerta visual de confirmación cuando se intente alternar entre modos de uso. |

### Subsistema 5: Persistencia

#### Módulo 1: Almacenamiento y Estructura de Datos

| **PER-07**      | Limitar el guardado de setups en la base de datos al Modo Avanzado                                                                    |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                   |
| **Descripción** | Las configuraciones de calibración y medición solo podrán ser guardadas en la Base de Datos si se encuentra activado el Modo Avanzado |

| **PER-10**      | Limitar la escritura de observaciones en setups al modo Avanzado                                      |
| :-------------- | ----------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                   |
| **Descripción** | El sistema solo debe habilitar las observaciones en setups si el Modo Avanzado se encuentra activado. |
