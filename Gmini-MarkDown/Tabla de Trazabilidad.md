##### Subsistema 1: Comunicación e Interacción con el Hardware

##### Módulo 1: Conectividad y Estado

| **Requisito** | Caso de uso                                          | Clase/servicio                                         | Persistencia |
| ------------- | ---------------------------------------------------- | ------------------------------------------------------ | ------------ |
| **CON-01**    | Establecer conexión alámbrica                        | ConnectionService/Wire                                 | -            |
| **CON-02**    | Establecer conexión inalámbrica                      | ConnectionService/Wireless                             | -            |
| **CON-03**    | Traducir comandos de control                         | Pendiente                                              | -            |
| **CON-04**    | Notificar visualmente el estado activo de conexión   | ConnectionService/ConnectionState/ConnectedState       | -            |
| **CON-05**    | Notificar visualmente el estado Inactivo de conexión | ConnectionService/ConnectionState/DisconnectedState    | -            |
| **CON-06**    | Notificar visualmente el estado error de conexión    | ConnectionService/ConnectionState/ConnectionErrorState | -            |
| **CON-07**    | Persistir últimos datos generados ante un error      | MeasureService/PersistenceService                      | MEASURE      |

##### Módulo 2: Calibración del Dispositivo
| **Requisito** | Caso de uso                                              | Clase/servicio                       | Persistencia |
| ------------- | -------------------------------------------------------- | ------------------------------------ | ------------ |
| **CAL-01**    | Configurar la calibración electrónica del equipo         | CalibrationService/CalibrationSetup  | -            |
| **CAL-02**    | Ejecutar calibración electrónica del equipo              | CalibrationService                   | -            |
| **CAL-03**    | Bloquear ejecución por descalibración                    | Device/DeviceState/UncalibratedState | -            |
| **CAL-04**    | Limitar la configuración de calibración al Modo Avanzado | SessionManager                       | -            |

#### Subsistema 2: Configuración y Toma de Mediciones
##### Módulo 1: Tipos y Estrategias de Medición

| **Requisito** | Caso de uso                                                | Clase/servicio                  | Persistencia  |
| ------------- | ---------------------------------------------------------- | ------------------------------- | ------------- |
| **MED-01**    | Configurar apartados comunes a una medición                | Measure                         | -             |
| **MED-02**    | Configurar medición de una frecuencia  (Monofrecuencia)    | MeasureSetup/SingleMeasureSetup | -             |
| **MED-03**    | Ejecutar medición de una frecuencia (Monofrecuencia)       | MeasureService                  | MeasureResult |
| **MED-04**    | Configurar medición por espectroscopía (Barrido espectral) | MeasureSetup/SpecMeasureSetup   | -             |
| **MED-05**    | Ejecutar medición por espectroscopía (Barrido espectral)   | MeasureService                  | MeasureResult |
| **MED-06**    | Configurar medición de multifrecuencia                     | MeasureSetup/MultiMeasureSetup  | -             |
| **MED-07**    | Ejecutar medición multifrecuencia                          | MeasureService                  | MeasureResult |
| **MED-08**    | Ejecutar mediciones en bucle                               | MeasureService                  | MeasureResult |
| **MED-11**    | Calcular estadísticos descriptivos básicos                 | Clase Pendiente                 | -             |
| **MED-13**    | Limitar configuración de mediciones al Modo Avanzado       | SessionManager                  | -             |

#### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

##### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición

| **Requisito** | Caso de uso                                 | Clase/servicio     | Persistencia                    |
| ------------- | ------------------------------------------- | ------------------ | ------------------------------- |
| **SET-01**    | Crear Perfil de Usuario                     | AuthService        | USER                            |
| **SET-02**    | Iniciar Sesión                              | AuthService        | -                               |
| **SET-03**    | Cerrar Sesión                               | AuthService        | -                               |
| **SET-04**    | Habilitar Modos de Uso                      | SessionManager     | -                               |
| **SET-05**    | Habilitar Modo Avanzado                     | SessionManager     | -                               |
| **SET-06**    | Habilitar Modo Básico                       | SessionManager     | -                               |
| **SET-07**    | Cambiar entre modos de uso                  | SessionManager     | -                               |
| **SET-09**    | Aplicar configuraciones                     | PersistenceService | -                               |
| **SET-10**    | Cargar configuraciones                      | PersistenceService | CALIBRATION_SETUP/MEASURE_SETUP |
| **SET-11**    | Exportar configuraciones de medición        | PersistenceService | -                               |
| **SET-13**    | Mantener la sesión activa en el dispositivo | SessionManager     | -                               |

#### Subsistema 5: Persistencia

##### Módulo 1: Almacenamiento y Estructura de Datos

| **Requisito** | Caso de uso                                                      | Clase/servicio                                                             | Persistencia                           |
| ------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------- |
| **PER-01**    | Almacenar setups de medición y calibración en una Base de Datos  | PersistenceService/MeasureSetup<br><br>PersistenceService/CalibrationSetup | MEASURE_SETUP<br><br>CALIBRATION_SETUP |
| **PER-02**    | Almacenar mediciones y sus resultados en una Base de Datos       | PersistenceService/Measure<br><br>PersistenceService/MeasureResult<br><br> | MEASURE<br><br>MEASURE_RESULT          |
| **PER-03**    | Configurar directorios                                           | PersistenceService                                                         | -                                      |
| **PER-04**    | Generar nomenclatura predeterminada de archivos                  | Measure                                                                    | MEASURE                                |
| **PER-05**    | Renombramiento manual de archivos                                | Measure                                                                    | MEASURE                                |
| **PER-06**    | Estructurar cabeceras de metadatos integrados                    | Mesaure                                                                    | MEASURE                                |
| **PER-07**    | Limitar el guardado de setups al Modo Avanzado                   | SessionManager                                                             | -                                      |
| **PER-08**    | Adjuntar metadatos y observaciones libres sobre mediciones       | Mesaure                                                                    | MEASURE                                |
| **PER-09**    | Adjuntar metadatos y observaciones libres sobre setups           | PersistenceService/MeasureSetup<br><br>PersistenceService/CalibrationSetup | MEASURE_SETUP<br><br>CALIBRATION_SETUP |
| **PER-10**    | Limitar la escritura de observaciones en setups al modo Avanzado | SessionManager                                                             | -                                      |
