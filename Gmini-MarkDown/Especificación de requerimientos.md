## Requisitos específicos
### Subsistema 1: Comunicación e Interacción con el Hardware
#### Módulo 1: Conectividad y Estado

| **CON-01**      | Establecer conexión Alámbrica con el hardware                                                                      |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                 |
| **Descripción** | El sistema debe permitir establecer y gestionar la comunicación con la placa ESP32, soportando conexión alámbrica. |

| **CON-02**      | Establecer conexión inalámbrica con el hardware                                                                      |
| :-------------- | :------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                   |
| **Descripción** | El sistema debe permitir establecer y gestionar la comunicación con la placa ESP32, soportando conexión inalámbrica. |

| **CON-03**      | Notificar visualmente el estado activo de conexión                                                                     |
| :---------- | :--------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                     |
| **Descripción** | El sistema debe informar al usuario mediante indicadores visuales en la interfaz gráfica el estado activo de conexión. |

| **CON-04**      | Notificar visualmente el estado Inactivo de conexión                                                                     |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                       |
| **Descripción** | El sistema debe informar al usuario mediante indicadores visuales en la interfaz gráfica el estado inactivo de conexión. |

| **CON-05**      | Notificar visualmente el estado error de conexión                                                                                                                  |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                                                                 |
| **Descripción** | El sistema debe informar al usuario mediante indicadores visuales en la interfaz gráfica el estado de error de la comunicación con el dispositivo en todo momento. |

| **CON-06**      | Traducir comandos de control                                                              |
| :-------------- | :-------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                        |
| **Descripción** | El sistema debe permitir utilizar los comandos de la placa mediante una interfaz gráfica. |

| **CON-07**      | Persistir últimos datos generados ante un error                                                                                               |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                                            |
| **Descripción** | El sistema debe guardar automáticamente los últimos datos recolectados ante una pérdida repentina de señal durante el proceso de adquisición. |

#### **Módulo 2: Calibración del Dispositivo**
| **CAL-01**      | Configurar la calibración electrónica del equipo                                            |
| :-------------- | :---------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto                                                                             |
| **Descripción** | El sistema debe permitir parametrizar la secuencia de comandos de calibración del hardware. |

| **CAL-02**      | Ejecutar calibración electrónica del equipo                                            |
| :-------------- | :----------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                     |
| **Descripción** | El sistema debe permitir iniciar la secuencia de comandos de calibración del hardware. |

| **CAL-03**      | Bloquear ejecución por descalibración                                                                                                                                                                             |
| :-------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                                                                                                                |
| **Descripción** | El sistema debe impedir el inicio de nuevas mediciones si detecta que los parámetros críticos del hardware (ganancia, voltaje o resistencia) han sido modificados sin registrar una calibración válida posterior. |
### Subsistema 2: Configuración y Toma de Mediciones
#### Módulo 1: Tipos y Estrategias de Medición

| **MED-01**      | Configurar medición de una frecuencia  (Monofrecuencia)                                                                         |
| :-------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto.                                                                                                                |
| **Descripción** | El sistema debe permitir elegir los parámetros de medición para  mediciones continuas a una única frecuencia fija seleccionada. |

| **MED-02**      | Ejecutar medición de una frecuencia (Monofrecuencia)                                             |
| :-------------- | :--------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                               |
| **Descripción** | El sistema debe permitir ejecutar mediciones continuas a una única frecuencia fija seleccionada. |

| **MED-03**      | Configurar medición por espectroscopía (Barrido espectral)                                                                                                                                      |
| :-------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto.                                                                                                                                                                                |
| **Descripción** | El sistema debe permitir elegir los parámetros de medición para realizar una medición secuencial a intervalos fijos de frecuencias establecidas en el espectro frecuencial (sweep) determinado. |

| **MED-04**      | Ejecutar medición por espectroscopía (Barrido espectral)                                                                                                 |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                                                       |
| **Descripción** | El sistema debe permitir ejecutar una medición secuencial a intervalos fijos de frecuencias establecidas en el espectro frecuencial (sweep) determinado. |

| **MED-05**      | Configurar medición de multifrecuencia                                                                               |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto.                                                                                                     |
| **Descripción** | El sistema debe permitir elegir los parámetros de medición para una cantidad de frecuencias discretas y específicas. |

| **MED-06**      | Ejecutar medición multifrecuencia                                                                                         |
| :-------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                        |
| **Descripción** | El sistema permite ejecutar una cantidad de mediciones a las mismas frecuencias discretas y especificadas por el usuario. |

| **MED-07**      | Mostrar progreso de la medición                                                                                                                     |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                                                  |
| **Descripción** | El sistema debe proporcionar una indicación visual en pantalla que informe al usuario que un proceso de medición se encuentra actualmente en curso. |

| **MED-08**      | Ejecutar mediciones en bucle                                                               |
| :-------------- | :--------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                         |
| **Descripción** | El sistema debe permitir ejecutar mediciones continuas del mismo tipo a través del tiempo. |

| **MED-09**      | Seleccionar canales de multiplexado (Llaves/Electrodos)                                                                     |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario experto.                                                                                                            |
| **Descripción** | El sistema debe permitir seleccionar qué canal de electrodos o impedancia interna se utilizará para la toma de la medición. |

| **MED-10**      | Calcular estadísticos descriptivos básicos                                                                                |
| :---------- | :---------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                        |
| **Descripción** | El sistema debe ser capaz de calcular estadísticos descriptivos a partir de los datos crudos obtenidos en las mediciones. |

| **MED-11**      | Presentar estadísticos descriptivos básicos                               |
| :---------- | :------------------------------------------------------------------------ |
| **Usuarios**    | Usuario experto, Usuario operador.                                        |
| **Descripción** | El sistema debe ser capaz de presentar métricas estadísticas automáticas. |

| **MED-11**      | Mostrar resultados intermedios                                                                                                 |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                             |
| **Descripción** | El sistema debe proporcionar en pantalla los datos de mediciones intermedias realizadas durante procesos de medición ciclicos. |

### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

#### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición
| **SET-01**      | Habilitar usuario experto                                                                                     |
| :-------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto.                                                                                              |
| **Descripción** | La aplicación debe proveer un "Modo Experto" con acceso total a la configuración de parámetros y calibración. |

| **SET-02**      | Habilitar usuario operador                                                                                                                                                                       |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario operador.                                                                                                                                                                                |
| **Descripción** | La aplicación debe proveer un "Modo Operador" con permisos restringidos exclusivamente a la ejecución de mediciones y ejecución de calibración (con los parámetros predefinidos por el experto). |

| **SET-03**      | Advertir sobre cambio de perfiles                                                                               |
| :-------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                              |
| **Descripción** | El sistema debe desplegar una alerta visual de confirmación cuando se intente alternar entre tipos de perfiles. |

| **SET-04**      | Exportar configuraciones de medición                                                                                      |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario Operador.                                                                                        |
| **Descripción** | El sistema debe permitir al usuario exportar las configuraciones guardadas en la base de datos a su almacenamiento local. |

| **SET-05**      | Cargar configuraciones                                                                                                                |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario Operador.                                                                                                    |
| **Descripción** | El sistema debe permitir al usuario operador importar configuraciones desde el almacenamiento local y guardarlos en la base de datos. |

| **SET-06**      | Aplicar configuraciones                                                                 |
| :-------------- | --------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario Operador.                                                      |
| **Descripción** | El sistema debe permitir al usuario seleccionar una configuración previamente guardada. |

| **SET-07**      | Adjuntar metadatos y observaciones libres                                                                                                                                               |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                                                                                      |
| **Descripción** | El sistema debe proveer un campo de entrada de texto libre para documentar observaciones contextuales sobre el objeto o tejido medido, vinculando este texto al paquete de datos final. |

| **SET-8**       | Cambiar entre perfiles de usuario                                                  |
| :-------------- | ---------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operado                                                   |
| **Descripción** | El sistema tiene que permitir a un usuario realizar cambios de perfiles dinámicos. |

| **SET-9**       | Visualizar datos guardados                                                                                               |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                       |
| **Descripción** | El sistema debe permitir visualizar datos (mediciones realizadas y setups) anteriores aunque la placa no esté conectada. |

| **SET-10**      | Crear Perfil de Usuario                             |
| :-------------- | --------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                  |
| **Descripción** | El sistema debe permitir crear perfiles de usuario. |

| **SET-11**      | Iniciar Sesión                                          |
| :-------------- | ------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                      |
| **Descripción** | El sistema debe permitir a los usuarios iniciar sesión. |

### Subsistema 4: Entorno de Ejecución y Plataforma

#### Módulo 1: Compatibilidad del Sistema

| **COM-01**      | Proveer entorno de aplicación de escritorio                                                                                                            |
| :-------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                                                     |
| **Descripción** | El software debe ser diseñado, compilado y distribuido como una aplicación de escritorio orientada a computadoras personales y portátiles (notebooks). |

| **COM-02**      | Garantizar ejecución nativa en Microsoft Windows                                                                                                                                          |
| :-------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                                                                                        |
| **Descripción** | El sistema debe garantizar total compatibilidad, estabilidad y funcionalidad de todos sus módulos (especialmente la comunicación de puertos) bajo el sistema operativo Microsoft Windows. |

| **COM-03**      | Proveer soporte secundario para entornos Linux                                                                                                                |
| :-------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                                                            |
| **Descripción** | El sistema debe contemplar en su arquitectura la portabilidad necesaria para poder ser ejecutado en distribuciones de escritorio del sistema operativo Linux. |

| **COM-04**      | Garantizar el funcionamiento sin conexión a internet                                                   |
| :-------------- | ------------------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                     |
| **Descripción** | El sistema debe ser capaz de funcionar de manera completa aunque no se establezca conexión a internet. |
### Subsistema 5: Persistencia

#### Módulo 1: Almacenamiento y Estructura de Datos

| **PER-01**      | Almacenar mediciones y sus resultados en una Base de Datos                                                                      |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                              |
| **Descripción** | El sistema debe guardar todas las mediciones completadas junto con sus resultados directamente en una base de datos relacional. |

| **PER-01**      | Almacenar setups de medición y calibración en una Base de Datos                                                                                  |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario experto.                                                                                                                                 |
| **Descripción** | El sistema debe guardar todos las configuraciones de calibración y medición establecidas por el usuario experto en una base de datos relacional. |

| **PER-02**      | Generar nomenclatura predeterminada de archivos                                                                                                              |
| :-------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                                                           |
| **Descripción** | El sistema debe asignar automáticamente a cada archivo de salida un nombre basado en la fecha y hora de la medición, utilizando el estándar ISO 8601 básico. |

| **PER-03**      | Configurar directorios                                                                                                |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                    |
| **Descripción** | El sistema debe permitir al usuario seleccionar un directorio raíz específico para el almacenamiento de sus campañas. |

| **PER-04**      | Renombramiento manual de archivos                                                                             |
| :-------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                            |
| **Descripción** | El sistema debe permitir al usuario sobrescribir el nombre automático del archivo antes de su guardado final. |

| **PER-05**      | Estructurar cabeceras de metadatos integrados                                                                                                                                                                                |
| :-------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario experto, Usuario operador.                                                                                                                                                                                           |
| **Descripción** | El sistema debe incluir en el archivo final exportado tanto los datos duros de la medición, como una cabecera que contenga el estado exacto de todos los parámetros de configuración utilizados y el texto de observaciones. |
