# Laboratorio de Desarrollo de Software

## Curso 2026

**Alegre, Elias Nahuel
Hegemann, Albaro Tobias
Vasquez Mamani, Juan Pablo
Vargas Da Silva, Eliam Joaquin**

## ÍNDICE

- **INTRODUCCIÓN**
- **ESPECIFICACIÓN DE REQUERIMIENTOS**
	- Introducción y ámbito del sistema
		- Definiciones, siglas y abreviaturas
		- Referencias
	- Descripción General
		- Funciones del producto
		- Características de los usuarios
		- Restricciones
	- Requisitos específicos
		- Subsistema 1: Comunicación e Interacción con el Hardware
			- Modulo 1: Conectividad y Estado
			- Modulo 2: Calibración del Dispositivo
		- Subsistema 2: Configuración y Toma de Mediciones
			- Modulo 1: Tipos y Estrategias de Medición
		- Subsistema 3: Configuración y Gestión de Perfiles (Setups)
			- Modulo 1: Perfiles de Usuario y Gestión de Setups de Medición
		- Subsistema 4: Entorno de Ejecución y Plataforma
			- Modulo 1: Compatibilidad del Sistema
		- Subsistema 5: Persistencia
			- Modulo 1: Almacenamiento y Estructura de Datos
- **CRONOGRAMA DE TRABAJO**
	- Visión general
	- Cronograma por requerimientos
- **METODOLOGÍA DE DESARROLLO**
	- Resumen de la metodología elegida
- **HERRAMIENTAS UTILIZADAS**
- **ANÁLISIS Y DISEÑO**
	- Análisis
	- Diseño
- **SOBRE LAS ITERACIONES**
- **SOBRE LOS ENTREGABLES**
	- Aplicaciones y plataformas que forman parte del sistema
	- Requerimientos técnicos para la isntalación
- **PRESENTACIÓN VISUAL PARA APROBAR EL FINAL**

## INTRODUCCIÓN
El proyecto tiene como propósito el desarrollo integral de una plataforma de software y una interfaz gráfica de usuario (GUI) para el hardware "Guanaco Mini” (GMini) desarrollado por el Laboratorio de Electrónica Aplicada y Biomedicina (LEAB) del Instituto de Desarrollo Económico e Innovación de la Universidad Nacional de Tierra del Fuego AeiAS. El cliente interesado en el desarrollo de este software es el Doctor en Ciencias Biológicas e Ingeniero Biomédico Antonio Héctor Dell’osa, el cual en este contexto es miembro del LEAB, autor de la tesis “Espectroscopía de Impedancia para la Detección Rápida de Lesiones Óseas” sobre la cual este proyecto está basado y líder del proyecto GMini. Nuestro contacto con él es mediante su correo electrónico institucional [ahdellosa@untdf.edu.ar](mailto:ahdellosa@untdf.edu.ar) .

Dicho dispositivo está diseñado para proveer una interfaz capaz de realizar mediciones de espectroscopía de impedancia eléctrica y bioimpedancia.

El GMini ofrece un alto potencial para aplicaciones en investigaciones científicas y académicas. Desde el punto de vista médico y tecnológico, la bioimpedancia resulta interesante porque permite obtener información sobre un tejido utilizando corrientes eléctricas de pequeña amplitud, sin recurrir necesariamente a técnicas de diagnóstico más complejas, costosas o que utilicen radiación ionizante.

Además, los equipos de medición pueden ser relativamente pequeños y de bajo costo, por lo que existe interés en desarrollar sistemas portátiles capaces de realizar mediciones fuera de grandes centros médicos.

Sin embargo, medir la impedancia es solamente una parte del problema. Una medición puede contener una gran cantidad de datos: diferentes frecuencias, módulo de impedancia, fase, componente real, componente imaginaria y mediciones repetidas sobre diferentes personas o condiciones.

Desde nuestra formación en Sistemas, el problema resulta especialmente interesante en la etapa posterior a la adquisición de los datos: almacenamiento, organización, procesamiento, visualización e identificación automática de patrones que puedan relacionarse con diferentes estados del tejido.

Actualmente, la comunicación a bajo nivel con la placa GMini está resuelta y documentada, sin embargo, carece de una plataforma que permita a los usuarios no especializados utilizarla. La solución provisional existente, que parte de una implementación anterior, presenta múltiples problemas estructurales, errores de ejecución y limitaciones operativas, como la incapacidad de realizar muestreos continuos prolongados (sólo es posible ser utilizada para realizar mediciones por sus propios desarrolladores o usuarios entrenados específicamente). Por lo tanto, el desarrollo de una interfaz para el nuevo dispositivo es fundamental para explotar todas las capacidades del hardware, permitiendo su uso en entornos de campo y laboratorio sin requerir que el operador posea conocimientos técnicos en electrónica o programación a bajo nivel. Esta solución permitiría que los 5 dispositivos que actualmente se encuentran sin uso puedan ser puestos en común a partir del producto de software que se propone.

El objetivo principal de nuestro proyecto es desarrollar una aplicación que controle las distintas instrucciones de la placa (de las que disponemos una lista de comandos), mejore y agregue nuevas funcionalidades, implemente las claves para la calidad de software como la robustez, mantenibilidad, usabilidad y portabilidad.

Por otro lado, la bioimpedancia se ha utilizado o investigado en distintos problemas médicos. Algunas de sus aplicaciones más conocidas son la estimación de la composición corporal, como porcentaje de grasa, masa muscular y cantidad de agua corporal, y el seguimiento de cambios en la distribución de líquidos.

También existen aplicaciones e investigaciones relacionadas con:

- detección y seguimiento de edemas o acumulaciones de líquido;
    
- evaluación del estado de tejidos musculares;
    
- análisis de cambios asociados con lesiones o alteraciones de tejidos;
    
- estudio de diferencias entre tejidos sanos y patológicos;
    
- monitoreo cardiovascular mediante técnicas como la cardiografía por impedancia;
    
- evaluación de tejidos pulmonares mediante Tomografía por Impedancia Eléctrica;
    
- investigación de alteraciones producidas por lesiones óseas, inflamación u otros cambios estructurales.

Es importante aclarar que no todas estas aplicaciones tienen el mismo grado de desarrollo clínico. Algunas están ampliamente utilizadas, mientras que otras continúan siendo objeto de investigación. Desde nuestra perspectiva, una dificultad importante aparece cuando las mediciones generan grandes cantidades de datos que deben ser interpretados.

Por ejemplo, para cada paciente pueden obtenerse decenas o cientos de valores correspondientes a diferentes frecuencias. Si además se realizan mediciones sobre diferentes zonas del cuerpo, condiciones o momentos, el volumen de información aumenta rápidamente.

El problema que nos interesa abordar puede formularse entonces de la siguiente manera:

**¿Cómo desarrollar herramientas computacionales que permitan organizar, procesar, visualizar y analizar mediciones de espectroscopía de bioimpedancia, facilitando la identificación de diferencias o patrones que puedan estar asociados con cambios en los tejidos biológicos?**

Este problema involucra aspectos propios de nuestra formación, como procesamiento de datos, programación, construcción de bases de datos, visualización de información, análisis estadístico y eventualmente utilización de algoritmos de aprendizaje automático.

Por lo tanto, nuestro objetivo no sería realizar directamente un diagnóstico médico, sino desarrollar herramientas computacionales que ayuden a transformar las mediciones eléctricas en información interpretable, que posteriormente pueda ser analizada y validada por especialistas del área biomédica.

## ESPECIFICACIÓN DE REQUERIMIENTOS

### Introducción y ámbito del sistema

El Sistema GMini GUI es una aplicación de escritorio integrada directamente con el firmware del microcontrolador ESP32 mediante comunicación bidireccional por puerto serial o Bluetooth.

Su principal objetivo es permitir a los usuarios realizar funciones como:

- Tomar mediciones de espectroscopía por bioimpedancia e impedancia eléctrica con una frecuencia o un espectro de frecuencias.
    
- Configurar los intervalos en los que se toman las mediciones.
    
- Visualizar los datos desde la misma aplicación.
    
- Visualizar y exportar configuraciones en distintos formatos.
    
- Organizar los datos en una carpeta definida.
    
- Realizar muestreos continuos.
    
- Realizar labores de calibración del dispositivo.
    
- Exportar datos.

Al reemplazar la actual comunicación mediante comandos a bajo nivel por esta interfaz gráfica, se elimina la barrera técnica, permitiendo explotar todo el potencial de la placa Guanaco Mini.
El proyecto está dirigido tanto para usuarios técnicos, investigadores y miembros de laboratorios con pocos o nulos conocimientos de programación en cualquiera de sus niveles. Entre los usuarios que harán uso del sistema se deben diferenciar entre aquellos con un rol de experto y aquellos con un uso limitado de las funciones o de operador. Los usuarios expertos serán los encargados de realizar la debida calibración del equipo, estableciendo los distintos parámetros necesarios para realizar las mediciones y los rangos de frecuencia. Por otro lado, los usuarios operadores podrán realizar las mediciones previamente parametrizadas,de manera sencilla.

#### Definiciones, siglas y abreviaturas

- **Bioimpedancia**: Resistencia que oponen los tejidos biológicos (células, fluidos, bacterias, etc.) al paso de una corriente eléctrica alterna.
    
- **CSV (Comma-Separated Values)**: Formato de archivo de texto estructurado que representa datos tabulares separados por comas, ampliamente utilizado para la exportación y análisis de datos científicos.
    
- **EIS (Electrical Impedance Spectroscopy)**: Técnica de análisis no destructiva que consiste en aplicar una señal eléctrica alterna (voltaje o corriente de pequeña amplitud) a un material o tejido biológico a través de un rango de distintas frecuencias, con el fin de medir su impedancia (oposición al paso de la corriente).
    
- **ESP32**: Microcontrolador de bajo costo y consumo de energía que cuenta con tecnología Wi-Fi y Bluetooth de modo dual integrada, utilizado como núcleo de procesamiento del hardware original.
    
- **Espectroscopía (Barrido espectral / Sweep)**:Forma de medición que consiste en realizar una medición de impedancia o bioimpedancia en un determinado intervalo de frecuencias.
    
- **Firmware**: Software de bajo nivel que está integrado de forma permanente o semipermanente en el hardware (en este caso, el código desarrollado por el laboratorio que se ejecuta directamente sobre el ESP32).
    
- **GMini (Guanaco Mini)**: Dispositivo de hardware desarrollado por el laboratorio cliente, diseñado para realizar mediciones de espectroscopía.
    
- **GUI (Graphical User Interface)**: Interfaz Gráfica de Usuario. Entorno visual del software que permite a los operadores interactuar con el sistema y el hardware subyacente mediante elementos gráficos y ventanas, en lugar de comandos de texto.
    
- **ISO 8601**: Estándar internacional para la representación de fechas y horas, utilizado como formato básico para generar la nomenclatura predeterminada de los archivos guardados.
    
- **JSON (JavaScript Object Notation)**: Formato de texto ligero para el intercambio de datos, fácil de leer y escribir tanto para humanos como para máquinas.
    
- **LEAB (Laboratorio de Electrónica Aplicada y Biomedicina)**: Laboratorio perteneciente al Instituto de Desarrollo Económico e Innovación de la Universidad Nacional de Tierra del Fuego. Actúa como creador del hardware y cliente principal del proyecto de software.
    
- **Metadatos**: Información adicional (estado de los parámetros de configuración y observaciones libres) que se adjunta en las cabeceras de los archivos locales junto con los datos crudos de la medición.
    
- **Monofrecuencia**: Forma de medición que consiste en realizar la medición de impedancia o bioimpedancia a una frecuencia fija, también llamado del inglés “single frequency”.
    
- **Muestreo Continuo**: Proceso de recolección de datos y mediciones de manera ininterrumpida o periódica durante un rango de tiempo prolongado, gestionado automáticamente por el software.
    
- **Multifrecuencia**: Forma de medición que implica realizar mediciones a diferentes frecuencias fijas (diferentes mediciones monofrecuencia) que pueden tener o no intervalos equidistantes o no en el campo de la frecuencia.
    
- **Multiplexado (Canales / Llaves)**: Sistema de llaves (“switchs”) o conmutación que permite seleccionar diferentes canales en forma secuencial o fija.
    
- **Puerto Serial / Comunicación Serial**: Interfaz de transferencia de datos en la que la información se envía bit a bit de forma secuencial. Se utilizará (vía cable USB) como uno de los medios de comunicación principal entre la PC y el dispositivo.
    
- **Setups (Configuraciones de medición)**: Conjunto de parámetros técnicos (tipo, rango, canales) definidos y guardados localmente por un usuario experto, que pueden ser exportados, o bien importados y aplicados por un usuario operador.

#### Referencias

- **Espressif Systems**: ESP32 Technical Reference Manual. Espressif Systems, Shanghái (2023). Disponible en: [https://documentation.espressif.com/esp32_datasheet_en.html?q=ESP32](https://www.espressif.com/en/support/documents/technical-documents)
    
- **Python Software Foundation**: Python 3 Reference Manual. Disponible en: [https://docs.python.org/3/](https://docs.python.org/3/)
    
- **IEEE Computer Society**: IEEE Recommended Practice for Software Requirements Specifications (IEEE Std 830-1998). IEEE, Nueva York (1998).
    
- **Laboratorio de Electrónica Aplicada y Biomedicina (LEAB)**: Dispositivo de medición de bioimpedancia Guanaco Mini V2.0 [Rev3]. Universidad Nacional de Tierra del Fuego, A.I.A.S. (2026).
    
- **The pandas development team**: pandas-dev/pandas: Pandas. Zenodo. Disponible en: [https://pandas.pydata.org/](https://pandas.pydata.org/)
    
- **Hunter, J. D.: Matplotlib**: A 2D graphics environment. Computing in Science & Engineering, 9(3), 90-95 (2007).

## Descripción General

#### Funciones del Producto

**Subsistema de Comunicación e Interacción con el Hardware**
Este subsistema agrupa las funciones encargadas de establecer y mantener el enlace de datos bidireccional entre la computadora y la placa ESP32, garantizando una transferencia estable.

- Establecer conexión con el entorno de escritorio mediante conexión alámbrica.
    
- Establecer conexión con el entorno de escritorio mediante conexión inalámbrica.

**Subsistema de Configuración y Toma de Mediciones**
Este subsistema es el encargado de agrupar aquellas funciones que permiten a los usuarios monitorear, parametrizar, calibrar y realizar mediciones de manera controlada, pudiendo determinar aspectos como rangos de frecuencia o estrategias de medición.

- Calibrar el dispositivo.
    
- Tomar mediciones de espectroscopía por bioimpedancia e impedancia eléctrica.
    
- Seleccionar una frecuencia o un espectro de frecuencias para realizar las mediciones.
    
- Configurar los intervalos en los que se toman las mediciones.
    
- Visualizar los datos desde la misma aplicación.
    
- Contraponer datos para realizar comparaciones.
    
- Realizar procesamiento de datos.
  
**Subsistema de Configuración y Gestión de Perfiles (Setups)**
Este subsistema es el encargado de habilitar los distintos modos de uso (Experto y Operador) para garantizar la separación de responsabilidades, así como de gestionar la creación, guardado e importación de las configuraciones de medición.  
  

**Subsistema de Entorno de Ejecución y Plataforma**
Este subsistema es el encargado de garantizar la disponibilidad del proyecto en sistemas operativos Microsoft Windows y ofrecer soporte secundario en kernels de Linux.
  
**Subsistema Persistencia**
Este subsistema centraliza las operaciones de persistencia del sistema, garantizando que tanto los datos estructurados como las gráficas generadas se almacenen de manera ordenada y estandarizada para su posterior análisis científico.
- Exportar datos.
    
- Importar datos.
    
- Organizar los datos en una carpeta definida.

#### Características de los usuarios
Los principales usuarios de la plataforma serán los miembros del LEAB, los cuales serán piezas fundamentales a lo largo del desarrollo del proyecto. Para poder brindarles a estos mismos una herramienta que sea capaz de adecuarse a cada perfil, se contemplarán los siguientes roles de usuario:

**Usuarios Expertos**: Este perfil de usuario se caracteriza por un mayor nivel técnico en cuanto a uso intensivo del dispositivo, análisis de los datos, parametrización y calibración del mismo. Los usuarios con este rol deben poder dejar preparado el entorno del sistema para que los usuarios con una menor experiencia puedan realizar mediciones sin dificultad. Esta distinción está pensada para líderes de laboratorios, jefes de proyectos de investigación, técnicos con amplia experiencia en EIS, entre otros.
  
**Usuarios Operadores**: Este perfil de usuario está diseñado para aquellos usuarios menos experimentados, los cuales deban realizar tareas sencillas sin enfocarse en los aspectos más complejos del sistema. Aquellos usuarios que pertenezcan a este rol solo podrán realizar mediciones previamente parametrizadas por los expertos.

#### Restricciones
  
El software no puede modificar el comportamiento interno del dispositivo, debe limitarse a realizar la lista de comandos y eventos ya programadas y documentadas por el LEAB.

El software está destinado para ser utilizado únicamente en la placa ESP32.

El sistema contempla únicamente dos vías de comunicación con la placa. Bluetooth y puerto serial.

El uso de funciones del software está limitado por perfiles y limitado por roles.
  
El sistema debe ser multiplataforma y capaz de funcionar entre distintos tipos de sistemas operativos 

El sistema no busca realizar un diagnóstico médico.

## Requisitos específicos
### Subsistema 1: Comunicación e Interacción con el Hardware
#### Módulo 1: Conectividad y Estado

| CON-01      | Establecer conexión Alámbrica con el hardware                                                                          |
| :---------- | :--------------------------------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                                                                 |
| Descripción | **El sistema debe permitir establecer y gestionar la comunicación con la placa ESP32, soportando conexión alámbrica.** |

| CON-02      | **Establecer conexión inalámbrica con el hardware**                                                                      |
| :---------- | :----------------------------------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                                                                   |
| Descripción | **El sistema debe permitir establecer y gestionar la comunicación con la placa ESP32, soportando conexión inalámbrica.** |

| CON-03      | Notificar visualmente el estado activo de conexión                                                                         |
| :---------- | :------------------------------------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                                                                     |
| Descripción | **El sistema debe informar al usuario mediante indicadores visuales en la interfaz gráfica el estado activo de conexión.** |

| CON-04      | **Notificar visualmente el estado Inactivo de conexión**                                                                     |
| :---------- | :--------------------------------------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                                                                       |
| Descripción | **El sistema debe informar al usuario mediante indicadores visuales en la interfaz gráfica el estado inactivo de conexión.** |

| CON-05      | **Notificar visualmente el estado error de conexión**                                                                                                                  |
| :---------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                                                                                                                 |
| Descripción | **El sistema debe informar al usuario mediante indicadores visuales en la interfaz gráfica el estado de error de la comunicación con el dispositivo en todo momento.** |

| CON-06      | **Traducir comandos de control**                                                              |
| :---------- | :-------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                                        |
| Descripción | **El sistema debe permitir utilizar los comandos de la placa mediante una interfaz gráfica.** |

| CON-07      | Persistir últimos datos generados ante un error                                                                                                   |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| Usuarios    | **Usuario experto, Usuario operador.**                                                                                                            |
| Descripción | **El sistema debe guardar automáticamente los últimos datos recolectados ante una pérdida repentina de señal durante el proceso de adquisición.** |

#### **Módulo 2: Calibración del Dispositivo**
| CAL-01      | **Configurar la calibración electrónica del equipo**                                            |
| :---------- | :---------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto**                                                                             |
| Descripción | **El sistema debe permitir parametrizar la secuencia de comandos de calibración del hardware.** |

| CAL-02      | **Ejecutar calibración electrónica del equipo**                                            |
| :---------- | :----------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                                     |
| Descripción | **El sistema debe permitir iniciar la secuencia de comandos de calibración del hardware.** |

| CAL-03      | **Bloquear ejecución por descalibración**                                                                                                                                                                             |
| :---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                                                                                                                                                                |
| Descripción | **El sistema debe impedir el inicio de nuevas mediciones si detecta que los parámetros críticos del hardware (ganancia, voltaje o resistencia) han sido modificados sin registrar una calibración válida posterior.** |
### Subsistema 2: Configuración y Toma de Mediciones

| MED-01      | **Configurar medición de una frecuencia  (Monofrecuencia)**                                                                         |
| :---------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto.**                                                                                                                |
| Descripción | **El sistema debe permitir elegir los parámetros de medición para  mediciones continuas a una única frecuencia fija seleccionada.** |

| MED-02      | **Ejecutar medición de una frecuencia (Monofrecuencia)**                                             |
| :---------- | :--------------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                                               |
| Descripción | **El sistema debe permitir ejecutar mediciones continuas a una única frecuencia fija seleccionada.** |

| MED-03      | **Configurar medición por espectroscopía (Barrido espectral)**                                                                                                                                      |
| :---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto.**                                                                                                                                                                                |
| Descripción | **El sistema debe permitir elegir los parámetros de medición para realizar una medición secuencial a intervalos fijos de frecuencias establecidas en el espectro frecuencial (sweep) determinado.** |

| MED-04      | **Ejecutar medición por espectroscopía (Barrido espectral)**                                                                                                 |
| :---------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                                                                                                       |
| Descripción | **El sistema debe permitir ejecutar una medición secuencial a intervalos fijos de frecuencias establecidas en el espectro frecuencial (sweep) determinado.** |

| MED-05      | **Configurar medición de multifrecuencia**                                                                               |
| :---------- | :----------------------------------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto.**                                                                                                     |
| Descripción | **El sistema debe permitir elegir los parámetros de medición para una cantidad de frecuencias discretas y específicas.** |

| MED-06      | **Ejecutar medición multifrecuencia**                                                                                         |
| :---------- | :---------------------------------------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                                                                        |
| Descripción | **El sistema permite ejecutar una cantidad de mediciones a las mismas frecuencias discretas y especificadas por el usuario.** |

| MED-07      | **Mostrar progreso de la medición**                                                                                                                     |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Usuarios    | **Usuario experto, Usuario operador.**                                                                                                                  |
| Descripción | **El sistema debe proporcionar una indicación visual en pantalla que informe al usuario que un proceso de medición se encuentra actualmente en curso.** |

| MED-08      | **Ejecutar mediciones en bucle**                                                               |
| :---------- | :--------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                                         |
| Descripción | **El sistema debe permitir ejecutar mediciones continuas del mismo tipo a través del tiempo.** |

| MED-09      | **Seleccionar canales de multiplexado (Llaves/Electrodos)**                                                                     |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------ |
| Usuarios    | **Usuario experto.**                                                                                                            |
| Descripción | **El sistema debe permitir seleccionar qué canal de electrodos o impedancia interna se utilizará para la toma de la medición.** |

| MED-10      | **Calcular estadísticos descriptivos básicos**                                                                                |
| :---------- | :---------------------------------------------------------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                                                                        |
| Descripción | **El sistema debe ser capaz de calcular estadísticos descriptivos a partir de los datos crudos obtenidos en las mediciones.** |

| MED-11      | **Presentar estadísticos descriptivos básicos**                               |
| :---------- | :---------------------------------------------------------------------------- |
| Usuarios    | **Usuario experto, Usuario operador.**                                        |
| Descripción | **El sistema debe ser capaz de presentar métricas estadísticas automáticas.** |
#### Módulo 1: Tipos y Estrategias de Medición

### Subsistema 3: Configuración y Gestión de Perfiles (Setups)

#### Módulo 1: Perfiles de Usuario y Gestión de Setups de Medición

### Subsistema 4: Entorno de Ejecución y Plataforma

#### Módulo 1: Compatibilidad del Sistema

### Subsistema 5: Persistencia

#### Módulo 1: Almacenamiento y Estructura de Datos