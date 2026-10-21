## Requisitos específicos

### Subsistema 1: Comunicación e Interacción con el Hardware

#### Módulo 1: Conectividad y Estado

| **CON-01**      | Establecer conexión Alámbrica con el hardware                                                                      |
| :-------------- | :----------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                |
| **Descripción** | El sistema debe permitir establecer y gestionar la comunicación con la placa ESP32, soportando conexión alámbrica. |

| **CON-02**      | Establecer conexión inalámbrica con el hardware                                                                      |
| :-------------- | :------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                  |
| **Descripción** | El sistema debe permitir establecer y gestionar la comunicación con la placa ESP32, soportando conexión inalámbrica. |

| **CON-03**      | Traducir comandos de control                                                              |
| :-------------- | :---------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                       |
| **Descripción** | El sistema debe permitir utilizar los comandos de la placa mediante una interfaz gráfica. |

| **CON-04**      | Notificar visualmente el estado activo de conexión                                                                     |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                    |
| **Descripción** | El sistema debe informar al usuario mediante indicadores visuales en la interfaz gráfica el estado activo de conexión. |

| **CON-05**      | Notificar visualmente el estado Inactivo de conexión                                                                     |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                      |
| **Descripción** | El sistema debe informar al usuario mediante indicadores visuales en la interfaz gráfica el estado inactivo de conexión. |

| **CON-06**      | Notificar visualmente el estado error de conexión                                                                                                                  |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                                                |
| **Descripción** | El sistema debe informar al usuario mediante indicadores visuales en la interfaz gráfica el estado de error de la comunicación con el dispositivo en todo momento. |

#### **Módulo 2: Calibración del Dispositivo**

| **CAL-01**      | Configurar la calibración electrónica del equipo                                            |
| :-------------- | :------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario Registrado.                                                                         |
| **Descripción** | El sistema debe permitir parametrizar la secuencia de comandos de calibración del hardware. |

| **CAL-02**      | Ejecutar calibración electrónica del equipo                                            |
| :-------------- | :------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                    |
| **Descripción** | El sistema debe permitir iniciar la secuencia de comandos de calibración del hardware. |

| **CAL-03**      | Bloquear ejecución por descalibración                                                                                                                                                                             |
| :-------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                                                                                               |
| **Descripción** | El sistema debe impedir el inicio de nuevas mediciones si detecta que los parámetros críticos del hardware (ganancia, voltaje o resistencia) han sido modificados sin registrar una calibración válida posterior. |


### Subsistema 2: Configuración y Toma de Mediciones

#### Módulo 1: Tipos y Estrategias de Medición

| **MED-01**      | Configurar apartados comunes a una medición                                                                                                                                |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                                                        |
| **Descripción** | El sistema debe permitir establecer los apartados comunes a todos los tipos de medición (voltaje de excitación, ganancia, ciclos, canales de multiplexado y valor de rfb). |

| **MED-02**      | Configurar medición de una frecuencia (Monofrecuencia)                                                                         |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                            |
| **Descripción** | El sistema debe permitir elegir los parámetros de medición para mediciones continuas a una única frecuencia fija seleccionada. |

| **MED-03**      | Ejecutar medición de una frecuencia (Monofrecuencia)                                             |
| :-------------- | :----------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                              |
| **Descripción** | El sistema debe permitir ejecutar mediciones continuas a una única frecuencia fija seleccionada. |

| **MED-04**      | Configurar medición por espectroscopía (Barrido espectral)                                                                                                                                      |
| :-------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                                                                             |
| **Descripción** | El sistema debe permitir elegir los parámetros de medición para realizar una medición secuencial a intervalos fijos de frecuencias establecidas en el espectro frecuencial (sweep) determinado. |

| **MED-05**      | Ejecutar medición por espectroscopía (Barrido espectral)                                                                                                 |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                                      |
| **Descripción** | El sistema debe permitir ejecutar una medición secuencial a intervalos fijos de frecuencias establecidas en el espectro frecuencial (sweep) determinado. |

| **MED-06**      | Configurar medición de multifrecuencia                                                                               |
| :-------------- | :------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                  |
| **Descripción** | El sistema debe permitir elegir los parámetros de medición para una cantidad de frecuencias discretas y específicas. |

| **MED-07**      | Ejecutar medición multifrecuencia                                                                                         |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario Registrado.                                                                                                       |
| **Descripción** | El sistema permite ejecutar una cantidad de mediciones a las mismas frecuencias discretas y especificadas por el usuario. |

| **MED-08**      | Ejecutar mediciones en bucle                                                               |
| :-------------- | :----------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                        |
| **Descripción** | El sistema debe permitir ejecutar mediciones continuas del mismo tipo a través del tiempo. |

| **MED-09**      | Mostrar progreso de la medición                                                                                                                     |
| :-------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                                 |
| **Descripción** | El sistema debe proporcionar una indicación visual en pantalla que informe al usuario que un proceso de medición se encuentra actualmente en curso. |

| **MED-10**      | Mostrar resultados intermedios                                                                                                 |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                            |
| **Descripción** | El sistema debe proporcionar en pantalla los datos de mediciones intermedias realizadas durante procesos de medición ciclicos. |

| **MED-11**      | Calcular estadísticos descriptivos básicos                                                                                |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario Registrado.                                                                                                       |
| **Descripción** | El sistema debe ser capaz de calcular estadísticos descriptivos a partir de los datos crudos obtenidos en las mediciones. |

| **MED-12**      | Presentar estadísticos descriptivos básicos                                                                |
| :-------------- | :--------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                        |
| **Descripción** | El sistema debe ser capaz de presentar métricas estadísticas básicas a partir de los resultados obtenidos. |


| **MED-13**          | Persistir últimos datos generados ante un error                                                                                               |
| :-------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                           |
| **Descripción** | El sistema debe guardar automáticamente los últimos datos recolectados ante una pérdida repentina de señal durante el proceso de adquisición. |

| **MED-14**          | Renderizar gráficas a partir de los resultados                                                                   |
| :-------------- | :--------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                              |
| **Descripción** | El sistema debe ser capaz de generar gráficos utilizando los resultados obtenidos y los parámetros establecidos. |

### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

#### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición

| **SET-01**      | Inicializar entorno de trabajo                                                         |
| :-------------- | -------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario.                                                                               |
| **Descripción** | El usuario debe poder ingresar a la aplicación y recuperar la sesión activa si existe. |

| **SET-02**      | Crear Perfil de Usuario                             |
| :-------------- | --------------------------------------------------- |
| **Usuarios**    | Usuario.                                            |
| **Descripción** | El sistema debe permitir crear perfiles de usuario. |

| **SET-03**      | Solicitar al usuario que inicie sesión luego de registrarse                                                     |
| :-------------- | --------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                             |
| **Descripción** | El sistema debe volver a solicitar los datos de inicio de sesión al usuario una vez este haya creado su perfil. |

| **SET-04**      | Iniciar Sesión                                          |
| :-------------- | ------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                     |
| **Descripción** | El sistema debe permitir a los usuarios iniciar sesión. |

| **SET-05**      | Cerrar Sesión                                          |
| :-------------- | ------------------------------------------------------ |
| **Usuarios**    | Usuario Registrado.                                    |
| **Descripción** | El sistema debe permitir a los usuarios cerrar sesión. |

| **SET-06**      | Aplicar configuraciones                                                                 |
| :-------------- | --------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                     |
| **Descripción** | El sistema debe permitir al usuario seleccionar una configuración previamente guardada. |

| **SET-07**      | Importar configuraciones de medición                                                                                                     |
| :-------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                      |
| **Descripción** | El sistema debe permitir al usuario importar configuraciones de medición desde el almacenamiento local y guardarlos en la base de datos. |

| **SET-08**      | Exportar configuraciones de medición                                                                                                  |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                   |
| **Descripción** | El sistema debe permitir al usuario exportar las configuraciones de medición guardadas en la base de datos a su almacenamiento local. |

| **SET-09**      | Importar configuraciones de calibración                                                                                                     |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                         |
| **Descripción** | El sistema debe permitir al usuario importar configuraciones de calibración desde el almacenamiento local y guardarlos en la base de datos. |

| **SET-10**      | Exportar configuraciones de calibración                                                                                                  |
| :-------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                      |
| **Descripción** | El sistema debe permitir al usuario exportar las configuraciones de calibración guardadas en la base de datos a su almacenamiento local. |

| **SET-11**      | Importar mediciones                                                                                                     |
| :-------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                     |
| **Descripción** | El sistema debe permitir al usuario importar mediciones desde el almacenamiento local y guardarlos en la base de datos. |

| **SET-12**      | Exportar mediciones                                                                                                  |
| :-------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                  |
| **Descripción** | El sistema debe permitir al usuario exportar las mediciones guardadas en la base de datos a su almacenamiento local. |

| **SET-13**      | Exportar gráficas generadas                                                                     |
| :-------------- | ----------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                             |
| **Descripción** | El sistema debe permitir a los usuarios exportar las gráficas generadas en una carpeta definida |

| **SET-14**      | Visualizar datos guardados                                                                                                         |
| :-------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                |
| **Descripción** | El sistema debe permitir visualizar datos (mediciones realizadas, gráficas y setups) anteriores aunque la placa no esté conectada. |

| **SET-15**      | Mantener la sesión activa en el dispositivo                                                 |
| :-------------- | ------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                         |
| **Descripción** | El sistema debe mantener la sesión del usuario activa aunque se haya cerrado la aplicación. |

### Subsistema 4: Entorno de Ejecución y Plataforma

#### Módulo 1: Compatibilidad del Sistema

| **COM-01**      | Proveer entorno de aplicación de escritorio                                                                                                            |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario Registrado.                                                                                                                                    |
| **Descripción** | El software debe ser diseñado, compilado y distribuido como una aplicación de escritorio orientada a computadoras personales y portátiles (notebooks). |

| **COM-02**      | Garantizar ejecución nativa en Microsoft Windows                                                                                                                                          |
| :-------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                                                                       |
| **Descripción** | El sistema debe garantizar total compatibilidad, estabilidad y funcionalidad de todos sus módulos (especialmente la comunicación de puertos) bajo el sistema operativo Microsoft Windows. |

| **COM-03**      | Proveer soporte secundario para entornos Linux                                                                                                                |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                                           |
| **Descripción** | El sistema debe contemplar en su arquitectura la portabilidad necesaria para poder ser ejecutado en distribuciones de escritorio del sistema operativo Linux. |

| **COM-04**      | Garantizar el funcionamiento sin conexión a internet                                                   |
| :-------------- | ------------------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario Registrado.                                                                                    |
| **Descripción** | El sistema debe ser capaz de funcionar de manera completa aunque no se establezca conexión a internet. |

### Subsistema 5: Persistencia

#### Módulo 1: Almacenamiento y Estructura de Datos

| **PER-01**      | Almacenar setups de medición y calibración en una Base de Datos                                                                             |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                         |
| **Descripción** | El sistema debe guardar todos las configuraciones de calibración y medición establecidas por el usuario en en una base de datos relacional. |

| **PER-02**      | Almacenar mediciones y sus resultados en una Base de Datos                                                                      |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                             |
| **Descripción** | El sistema debe guardar todas las mediciones completadas junto con sus resultados directamente en una base de datos relacional. |

| **PER-03**      | Configurar directorios                                                                                                |
| :-------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                   |
| **Descripción** | El sistema debe permitir al usuario seleccionar un directorio raíz específico para el almacenamiento de sus campañas. |

| **PER-04**      | Generar nomenclatura predeterminada de archivos                                                                                                              |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario Registrado.                                                                                                                                          |
| **Descripción** | El sistema debe asignar automáticamente a cada archivo de salida un nombre basado en la fecha y hora de la medición, utilizando el estándar ISO 8601 básico. |

| **PER-05**      | Renombramiento manual de archivos                                                                             |
| :-------------- | ------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                           |
| **Descripción** | El sistema debe permitir al usuario sobrescribir el nombre automático del archivo antes de su guardado final. |

| **PER-06**      | Estructurar cabeceras de metadatos integrados                                                                                                                                                                                |
| :-------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                                                                                                          |
| **Descripción** | El sistema debe incluir en el archivo final exportado tanto los datos duros de la medición, como una cabecera que contenga el estado exacto de todos los parámetros de configuración utilizados y el texto de observaciones. |

| **PER-07**      | Adjuntar metadatos y observaciones libres sobre mediciones                                                                                                                                              |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado.                                                                                                                                                                                     |
| **Descripción** | El sistema debe proveer un campo de entrada de texto libre para documentar observaciones contextuales sobre el objeto o tejido medido, vinculando este texto al paquete de datos final de una medición. |

| **PER-08**      | Adjuntar metadatos y observaciones libres sobre setups                                                                                                                                                                                           |
| :-------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Usuarios**    | Usuario Registrado.                                                                                                                                                                                                                              |
| **Descripción** | El sistema debe proveer un campo de entrada de texto libre para documentar observaciones contextuales sobre las configuraciones establecidas en un setup (de calibración o medición), vinculando este texto al paquete de datos final del mismo. |



### Nuevos Requerimientos a Integrar

#### Módulo: Automatización de Secuencias (AUT)

| **AUT-01**      | Construir secuencias experimentales automáticas |
| :-------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe proveer un editor visual para construir flujos automáticos (macros) que combinen diferentes métodos de medición de forma consecutiva. |

| **AUT-02**      | Configurar repeticiones e intervalos en secuencias |
| :-------------- | :------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe permitir definir la cantidad de repeticiones de un método y establecer tiempos de pausa (delays) entre mediciones o etapas de la secuencia. |

| **AUT-03**      | Exportar secuencias automáticas |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe permitir al usuario exportar y guardar las secuencias de automatización en archivos dentro de su almacenamiento local. |

| **AUT-04**      | Importar secuencias automáticas |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe permitir al usuario cargar secuencias de automatización previamente configuradas desde su almacenamiento local. |

#### Módulo: Análisis Visual y Gráficos (ANA)

| **ANA-01**      | Renderizar gráficos específicos avanzados |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe generar y visualizar gráficos temporales, diagramas de Bode (módulo/fase vs. frecuencia) y diagramas de Cole-Cole (-Im vs. Re). |

| **ANA-02**      | Proveer herramientas de interacción gráfica |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe permitir realizar zoom interactivo, paneo (desplazamiento libre) y utilizar cursores para consultar coordenadas exactas. |

| **ANA-03**      | Gestionar curvas de medición individuales |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe permitir superponer, ocultar, renombrar y asignar colores o estilos de línea diferentes a múltiples curvas dentro de un mismo gráfico. |

| **ANA-04**      | Visualizar datos en formato tabular |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe presentar los resultados numéricos adquiridos en una tabla estructurada, mostrando variables como frecuencia, módulo, fase, componente real e imaginaria. |

| **ANA-05**      | Manipular datos en tabla interactiva |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe permitir interactuar con la tabla de resultados mediante ordenamiento por columnas, filtrado condicional y la capacidad de copiar celdas al portapapeles. |

| **ANA-06**      | Vincular selección entre tabla y gráfico |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe resaltar automáticamente en la gráfica el punto o la curva que el usuario haya seleccionado en la tabla de datos, y viceversa. |

#### Módulo: Modelos Matemáticos y Estadística (MOD)

| **MOD-01**      | Calcular estadística descriptiva temporal y espectral |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe calcular y mostrar promedios y desviaciones estándar sobre mediciones repetidas en el tiempo o en múltiples espectros de frecuencias. |

| **MOD-02**      | Ajustar modelos físicos de impedancia |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe permitir estimar y ajustar parámetros matemáticos para modelos físicos predefinidos, como Debye o Cole-Cole, sobre los datos adquiridos. |

| **MOD-03**      | Configurar modelos de circuitos equivalentes predefinidos (A Revisar) |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe proveer una lista de circuitos eléctricos equivalentes predefinidos y evaluar matemáticamente la calidad del ajuste (fitting) respecto a la medición real. |

#### Módulo: Adquisición, Sesiones y Control (ADQ)

| **ADQ-01**      | Seleccionar canal de medición y patrones físicos |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe permitir alternar entre los canales DUT1 y DUT2 para realizar mediciones, y elegir entre patrones de calibración internos o el ingreso manual de un valor de resistencia externa. |

| **ADQ-02**      | Detener mediciones en curso |
| :-------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe proveer una opción para solicitar el fin o cancelación segura de una adquisición que ya se encuentra en ejecución. |

| **ADQ-03**      | Mostrar estimación de tiempo de adquisición |
| :-------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe calcular y mostrar de manera dinámica una estimación del tiempo restante para completar la medición o secuencia actual. |

| **ADQ-04**      | Mantener registro de eventos (Logs) |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe registrar y mostrar al usuario los eventos críticos de la sesión, incluyendo inicios de adquisición, interrupciones, errores y finalizaciones exitosas. |

| **ADQ-05**      | Proveer consola de comandos para diagnóstico |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe proveer una interfaz de consola (CLI) que permita al usuario enviar comandos en texto plano directamente a la placa y visualizar sus respuestas crudas para propósitos de diagnóstico. |

| **ADQ-06**      | Alertar sobre calidad de señal y validez de calibración |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe alertar al usuario si detecta saturación en la señal, baja respuesta digital, o si se ha modificado un parámetro que invalida la calibración actual. |

| **ADQ-07**      | Proveer recalibración automática |
| :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe ofrecer o disparar automáticamente una nueva secuencia de calibración cuando se modifiquen parámetros que invaliden la anterior. |

| **ADQ-08**      | Intentar reconexión automática |
| :-------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe ejecutar un mecanismo de contingencia para intentar recuperar automáticamente la comunicación si esta se interrumpe de forma inesperada. |

| **ADQ-09**      | Autoguardar y recuperar sesiones experimentales |
| :-------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe realizar un guardado periódico o temporal del estado de la sesión para evitar pérdida de datos y ofrecer su recuperación tras un fallo de la aplicación. |

| **ADQ-10**      | Importar mediciones de hardware legacy (A Revisar) |
| :-------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe poder interpretar, importar y visualizar datos provenientes de versiones anteriores del instrumento Guanaco y de la placa AD5933EBZ. |

| **ADQ-11**      | Personalizar y modularizar espacios de trabajo (Workspace) |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| **Usuarios**    | Usuario Registrado. |
| **Descripción** | El sistema debe permitir redimensionar, mover y ocultar los paneles visuales, y almacenar dicha configuración como una preferencia persistente del usuario. |