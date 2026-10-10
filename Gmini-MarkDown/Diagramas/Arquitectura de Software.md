## HERRAMIENTAS UTILIZADAS
### Diagramas de Arquitectura de Software
#### Diagrama de Contexto
```mermaid
C4Context

title Diagrama de Contexto para el Sistema GMini GUI
Person(user, "Usuario registrado")

System(GMini-GUI, "Sistema Guanaco Mini", "Permite a los usuarios interactuar con el dispositivo Guanaco Mini.")

System_Ext(ESP32, "Placa GMini", "Dispositivo de Hardware que realiza mediciones de impedancia y bioimpedancia eléctrica.")

Rel(user, GMini-GUI, "Calibra el dispositivo y realiza mediciones")
Rel(GMini-GUI, ESP32, "Envía comandos de control al dispositivo y recolecta las respuestas")
```

#### Diagrama de Contenedores

```mermaid
C4Container

title Diagrama de Contenedores para el Sistema GMini GUI

Enterprise_Boundary(LEAB, "Entorno de Laboratorio") {

Person(user, "Usuario registrado")

System_Boundary(sys_gmini, "Sistema Guanaco Mini"){

Container(app, "Aplicación de Escritorio", "Python3 + PyQt6" ,"Provee la interfaz gráfica de usuario y la lógica de negocio para interactuar con el Hardware.")

ContainerDb(sqlite, "Base de Datos del Sistema", "SQLite3", "Base de Datos relacional donde se almacenan mediciones y setups de configuración.")

}

System_Ext(ESP32, "Placa GMini", "Dispositivo medidor de impedancia.")

}

Rel(user, app, "Calibra el dispositivo y realiza mediciones")
Rel(app, sqlite, "Persiste datos generados")
Rel(app, ESP32, "Envía comandos de control al dispositivo y recolecta las respuestas")
```
#### Diagrama de Componentes

```mermaid
C4Component
UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
title Diagrama de Componentes para el Sistema GMini GUI

Person(user, "Usuario registrado")

System_Boundary(GMini-GUI, "Sistema Guanaco Mini") {

Container_Boundary(app, "Aplicación de Escritorio"){

Component(UI, "Interfaz Gráfica", "PyQt6", "Maneja la interacción visual.")
    
Component(sesion, "Autenticación y Sesión", "Python 3", "Mantiene la sesión activa.")

Component(mediciones, "Mediciones y Config", "Python 3", "Orquesta las mediciones.")

Component(comunicacion, "Comunicación y HW", "Python 3", "Maneja el puerto serial/Bluetooth.")
    
Component(persistencia, "Persistencia", "Python 3", "Centraliza el acceso a datos.")
}

System_Boundary(externos, "Infraestructura Externa") {
ContainerDb(sqlite, "Base de Datos", "SQLite3", "Almacenamiento local.")
}

}

System_Ext(ESP32, "Placa GMini", "Dispositivo medidor de impedancia.")

Rel(user, UI, "Opera sistema")

Rel(UI, sesion, "Valida acceso")
Rel(UI, mediciones, "Inicia proceso")
Rel(UI, comunicacion, "Ajusta puerto")
Rel(UI, persistencia, "Exporta/Importa")

Rel(mediciones, comunicacion, "Delega comandos")
Rel(sesion, persistencia, "Consulta usuario")
Rel(mediciones, persistencia, "Guarda resultados")

Rel(comunicacion, ESP32, "I/O Hardware")
Rel(persistencia, sqlite, "Lee / Escribe")
```
