Arquitectura en FastAPI

models/ vs schemas/: En Django, un solo modelo suele hacer el trabajo de base de datos y validación. En FastAPI se dividen estrictamente. models/ dicta cómo se crean las tablas SQL. schemas/ usa Pydantic para validar estrictamente qué campos JSON entran por el POST y qué campos salen en el GET.

routers/ (Capa de Presentación Web): Aquí solo van los decoradores (@app.post("/medir")). El router recibe la petición web, delega el trabajo pesado a otra capa y devuelve la respuesta. No debe contener lógica matemática ni accesos a base de datos.

services/ (Capa de Dominio): Aquí vive el núcleo algorítmico. Por ejemplo, toda la estructura abstracta (Measure, SingleFreq, MeasureService) viviría en esta carpeta. Son clases de Python puro que no saben ni les importa que están funcionando dentro de una API web.

Los tests se dividirían en:

test_services/ (Pruebas Unitarias): Para ejecutar los cálculos matemáticos y verificar con assert que el resultado es el correcto.

test_routers/ (Pruebas de Integración): Se usa una herramienta de FastAPI llamada TestClient. Sirve para simular peticiones web (GET, POST). En lugar de probar la matemática, se prueba si se envía un JSON mal formado (por ejemplo, sin el eje "x"), la API responda correctamente con un error HTTP 400 Bad Request.
