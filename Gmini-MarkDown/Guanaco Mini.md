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

### Definiciones, siglas y abreviaturas

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
