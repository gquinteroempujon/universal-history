# Manual de Usuario: Universal History

## Índice
1. [Introducción](#introducción)
   - [¿Qué es Universal History?](#qué-es-universal-history)
   - [Conceptos Fundamentales](#conceptos-fundamentales)
   - [Casos de Uso](#casos-de-uso)
2. [Instalación](#instalación)
   - [Requisitos](#requisitos)
   - [Instalación Básica](#instalación-básica)
   - [Opciones de Instalación](#opciones-de-instalación)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
   - [Componentes Principales](#componentes-principales)
   - [Flujo de Datos](#flujo-de-datos)
4. [Primeros Pasos](#primeros-pasos)
   - [Inicialización del Cliente](#inicialización-del-cliente)
   - [Configuración](#configuración)
5. [Trabajando con Registros de Eventos](#trabajando-con-registros-de-eventos)
   - [Creación de Eventos](#creación-de-eventos)
   - [Consulta de Eventos](#consulta-de-eventos)
   - [Búsqueda de Eventos](#búsqueda-de-eventos)
6. [Síntesis de Trayectoria](#síntesis-de-trayectoria)
   - [Creación Manual de Síntesis](#creación-manual-de-síntesis)
   - [Generación Automática de Síntesis](#generación-automática-de-síntesis)
7. [Documento de Estado](#documento-de-estado)
   - [Creación y Actualización](#creación-y-actualización)
   - [Actualización desde Eventos](#actualización-desde-eventos)
   - [Actualización desde Síntesis](#actualización-desde-síntesis)
8. [Catálogos de Dominio](#catálogos-de-dominio)
   - [Definición de Términos](#definición-de-términos)
   - [Definición de Métricas](#definición-de-métricas)
9. [Integración con Modelos de Lenguaje](#integración-con-modelos-de-lenguaje)
   - [Obtención de Contexto para LLMs](#obtención-de-contexto-para-llms)
   - [Optimización del Contexto](#optimización-del-contexto)
10. [Opciones de Almacenamiento](#opciones-de-almacenamiento)
    - [Almacenamiento en Memoria](#almacenamiento-en-memoria)
    - [Almacenamiento en Archivos](#almacenamiento-en-archivos)
    - [Almacenamiento en MongoDB](#almacenamiento-en-mongodb)
11. [Importación y Exportación](#importación-y-exportación)
    - [Exportar una Historia](#exportar-una-historia)
    - [Importar una Historia](#importar-una-historia)
    - [Copiar Historias](#copiar-historias)
12. [Ejemplos Prácticos](#ejemplos-prácticos)
    - [Historia Educativa](#historia-educativa)
    - [Historia Clínica](#historia-clínica)
    - [Historia Laboral](#historia-laboral)
13. [Solución de Problemas](#solución-de-problemas)
    - [Problemas Comunes](#problemas-comunes)
    - [Depuración](#depuración)
14. [Referencias y Recursos](#referencias-y-recursos)
    - [API de Referencia](#api-de-referencia)
    - [Recursos Adicionales](#recursos-adicionales)

## Introducción

### ¿Qué es Universal History?

Universal History es una biblioteca de Python diseñada para crear, mantener, analizar y utilizar registros históricos estructurados de cualquier sujeto a través de múltiples dominios. A diferencia de los sistemas tradicionales de mantenimiento de registros que suelen estar limitados a un solo dominio (como la educación, la salud o el empleo), Universal History proporciona un marco estandarizado que puede aplicarse a cualquier ámbito donde sea valioso mantener un registro histórico detallado.

La biblioteca implementa el estándar de Historia Universal (HU), que define una estructura coherente para registrar eventos, sintetizar trayectorias y mantener una representación actualizada del estado actual de un sujeto, todo ello optimizado para su uso con sistemas de inteligencia artificial modernos.

### Conceptos Fundamentales

El sistema Universal History se basa en cinco componentes fundamentales:

1. **Registro de Evento (RE)**: Es la unidad básica de información que captura un evento, observación o logro específico en la trayectoria del sujeto. Cada RE incluye información detallada sobre el evento, su contexto, fuente y metadatos asociados.

2. **Síntesis de Trayectoria (ST)**: Documento que condensa y analiza la información de múltiples REs en diferentes niveles temporales, proporcionando una visión general del progreso del sujeto en un dominio específico.

3. **Documento de Estado (DE)**: Representación en tiempo real del estado actual del sujeto derivada del análisis de su historia, optimizada específicamente para proporcionar contexto relevante a sistemas de IA como los modelos de lenguaje.

4. **Catálogo de Definiciones de Dominio (CDD)**: Marco semántico que define y estandariza los términos, métricas y categorías utilizadas para interpretar la información en un dominio específico.

5. **Historia Universal (HU)**: Contenedor principal que agrupa todos los componentes anteriores relacionados con un sujeto específico, proporcionando una visión integral y multidimensional de su trayectoria.

### Casos de Uso

La biblioteca Universal History puede aplicarse en numerosos contextos:

- **Educación**: Seguimiento completo del desarrollo académico de estudiantes, capturando no solo calificaciones sino también habilidades, proyectos, actividades extracurriculares y observaciones cualitativas.

- **Salud**: Registro integral del historial médico de pacientes, incluyendo consultas, procedimientos, medicaciones, mediciones de signos vitales y observaciones de profesionales de la salud.

- **Laboral**: Documentación de experiencias laborales, desarrollo de habilidades, evaluaciones de desempeño, proyectos completados y logros profesionales.

- **Deportivo**: Seguimiento del rendimiento deportivo, entrenamientos, competiciones, mediciones físicas y desarrollo de habilidades técnicas y tácticas.

- **Financiero**: Registro de transacciones, inversiones, patrones de gasto e ingreso, y desarrollo de comportamientos financieros.

- **Personal**: Documentación de eventos significativos, relaciones, hitos personales y desarrollo individual.

El valor diferencial de Universal History radica en su capacidad para proporcionar una visión holística que integra información de múltiples dominios, revelando patrones y conexiones que podrían perderse en sistemas aislados.

## Instalación

### Requisitos

Para utilizar Universal History necesitas:

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

Para funcionalidades específicas:
- MongoDB (para almacenamiento en base de datos)
- Librerías adicionales para integración con LLMs

### Instalación Básica

Para instalar la versión básica de Universal History:

```bash
pip install universal-history
```

### Opciones de Instalación

Para instalar con soporte para MongoDB:

```bash
pip install universal-history[mongodb]
```

Para instalar con soporte para integración con modelos de lenguaje:

```bash
pip install universal-history[llm]
```

Para instalar todas las funcionalidades:

```bash
pip install universal-history[all]
```

Para desarrolladores:

```bash
pip install universal-history[dev]
```

## Arquitectura del Sistema

### Componentes Principales

El sistema Universal History está estructurado en varios módulos:

1. **Modelos**: Define las estructuras de datos fundamentales (EventRecord, TrajectorySynthesis, StateDocument, DomainCatalog, UniversalHistory).

2. **Servicios**: Implementa la lógica de negocio para manipular los modelos (EventService, SynthesisService, StateService, HistoryService).

3. **Almacenamiento**: Proporciona implementaciones para diferentes backends de almacenamiento (MemoryHistoryRepository, FileHistoryRepository, MongoDBHistoryRepository).

4. **Utilidades**: Ofrece funciones auxiliares para operaciones comunes como hash, validación y manipulación de fechas.

5. **Cliente**: Integra todos los componentes en una interfaz unificada y fácil de usar (UniversalHistoryClient).

### Flujo de Datos

El flujo típico de datos en Universal History es el siguiente:

1. Los eventos se registran a través del EventService y se almacenan como EventRecords.
2. Periódicamente, el SynthesisService analiza conjuntos de eventos para crear TrajectorySynthesis.
3. El StateService mantiene actualizado el StateDocument basándose en eventos recientes y síntesis.
4. El documento de estado optimizado puede utilizarse como contexto para modelos de lenguaje u otros sistemas de IA.
5. Todo esto está coordinado por el HistoryService y expuesto a través del UniversalHistoryClient.

## Primeros Pasos

### Inicialización del Cliente

Para comenzar a trabajar con Universal History, primero debes importar e inicializar el cliente:

```python
from universal_history import UniversalHistoryClient

# Cliente con almacenamiento en memoria (para pruebas)
client = UniversalHistoryClient()

# Cliente con almacenamiento en archivos
client = UniversalHistoryClient(storage_dir="./data")

# Cliente con almacenamiento en MongoDB
client = UniversalHistoryClient(mongodb_connection="mongodb://localhost:27017/")
```

### Configuración

Puedes personalizar la configuración global de Universal History:

```python
from universal_history import configure

configure({
    "storage_type": "file",
    "storage_dir": "./custom_data_dir",
    "mongodb_connection": "mongodb://localhost:27017/",
    "mongodb_database": "universal_history_db"
})
```

También puedes configurar utilizando variables de entorno:

- `UNIVERSAL_HISTORY_STORAGE_TYPE`: Tipo de almacenamiento ("memory", "file", "mongodb")
- `UNIVERSAL_HISTORY_STORAGE_DIR`: Directorio para almacenamiento de archivos
- `UNIVERSAL_HISTORY_MONGODB_CONNECTION`: Cadena de conexión para MongoDB
- `UNIVERSAL_HISTORY_MONGODB_DATABASE`: Nombre de la base de datos MongoDB

## Trabajando con Registros de Eventos

### Creación de Eventos

Los eventos son la unidad básica de información en Universal History. Para crear un evento:

```python
# Ejemplo de evento educativo
event_result = client.create_event(
    subject_id="estudiante123",
    domain_type="education",
    event_type="exam",
    content="El estudiante obtuvo 85/100 en el examen de Álgebra.",
    content_type="text",
    source_type="institution",
    source_id="escuela001",
    source_name="Escuela Secundaria Springfield",
    creator_id="profesor001",
    creator_name="Sra. Martínez",
    creator_role="Profesora de Matemáticas",
    metrics={"score": 85, "max_score": 100},
    assessments={"performance": "Buena comprensión de conceptos algebraicos pero necesita mejorar en problemas verbales."},
    tags=["matemáticas", "álgebra", "examen"]
)

# Obtener IDs resultantes
hu_id = event_result['hu_id']  # ID de la Historia Universal
re_id = event_result['re_id']  # ID del Registro de Evento
```

Parámetros importantes para la creación de eventos:

- `subject_id`: Identificador único del sujeto (estudiante, paciente, empleado, etc.)
- `domain_type`: Dominio al que pertenece el evento (education, health, work, etc.)
- `event_type`: Tipo específico de evento dentro del dominio
- `content`: Descripción principal del evento
- `source_type`: Tipo de fuente que origina el evento
- `source_id`: Identificador de la fuente
- `source_name`: Nombre de la fuente
- `metrics`: Datos cuantitativos asociados al evento (diccionario)
- `assessments`: Evaluaciones cualitativas asociadas al evento (diccionario)
- `tags`: Etiquetas para categorizar el evento (lista)

### Consulta de Eventos

Para recuperar un evento específico:

```python
event = client.get_event(re_id=re_id, hu_id=hu_id)
```

Para obtener todos los eventos de un dominio específico:

```python
events = client.event_service.get_events_by_domain(
    subject_id="estudiante123",
    domain_type="education"
)
```

### Búsqueda de Eventos

Para buscar eventos con criterios específicos:

```python
# Buscar eventos de examen en educación entre dos fechas
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=90)

events = client.search_events(
    subject_id="estudiante123",
    domain_type="education",
    event_type="exam",
    start_date=start_date,
    end_date=end_date,
    tags=["álgebra"]
)
```

## Síntesis de Trayectoria

### Creación Manual de Síntesis

Las síntesis proporcionan una visión analítica de múltiples eventos a lo largo del tiempo:

```python
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=90)

synthesis_result = client.create_synthesis(
    subject_id="estudiante123",
    domain_type="education",
    summary="El estudiante mostró un fuerte desempeño en Álgebra con una mejora significativa a lo largo del curso.",
    start_date=start_date.isoformat(),
    end_date=end_date.isoformat(),
    source_events=[event1_id, event2_id, event3_id],
    key_insights=[
        "El estudiante demostró habilidades algebraicas sólidas",
        "Mejora significativa en la resolución de problemas verbales",
        "Completó consistentemente las tareas asignadas"
    ],
    significant_events=[
        {
            "re_id": event3_id,
            "description": "Obtuvo 92/100 en el examen final",
            "significance": "Muestra dominio de conceptos algebraicos y mejora significativa"
        }
    ],
    metrics={
        "promedio_puntuacion": {
            "value": 87,
            "trend": "improving",
            "analysis": "Las puntuaciones mejoraron constantemente a lo largo del curso"
        }
    },
    patterns=[
        "Desafíos iniciales con problemas verbales seguidos de una mejora significativa",
        "Rendimiento consistentemente alto en problemas computacionales"
    ],
    recommendations=[
        "Listo para conceptos avanzados de álgebra",
        "Considerar participación en competiciones matemáticas"
    ]
)

st_id = synthesis_result['st_id']  # ID de la Síntesis de Trayectoria
```

### Generación Automática de Síntesis

También puedes generar síntesis automáticamente a partir de eventos:

```python
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=90)

st_id = client.generate_synthesis_from_events(
    subject_id="estudiante123",
    domain_type="education",
    start_date=start_date.isoformat(),
    end_date=end_date.isoformat(),
    level=1  # Nivel de detalle (1 = más detallado, mayor número = más resumido)
)
```

Para generar una síntesis de nivel superior basada en síntesis existentes:

```python
st_id = client.synthesis_service.generate_higher_level_synthesis(
    subject_id="estudiante123",
    domain_type="education",
    source_synthesis_ids=[st_id1, st_id2, st_id3]
)
```

## Documento de Estado

### Creación y Actualización

El documento de estado mantiene una representación actualizada del sujeto:

```python
# Crear un documento de estado
de_id = client.create_state_document("estudiante123")

# Actualizar el estado de un dominio específico
client.update_domain_state(
    subject_id="estudiante123",
    domain_type="education",
    current_status="Actualmente inscrito en 10° grado en la Escuela Secundaria Springfield",
    key_attributes={
        "gpa": 3.8,
        "attendance_rate": 98.5,
        "grade_level": 10
    },
    recent_events=[
        {
            "re_id": event_id1,
            "description": "Obtuvo 92/100 en el examen final de Álgebra"
        },
        {
            "re_id": event_id2,
            "description": "Creó un modelo detallado del sistema solar"
        }
    ],
    significant_events=[
        {
            "re_id": event_id3,
            "description": "Obtuvo el 2° lugar en torneo de ajedrez",
            "significance": "Demuestra pensamiento estratégico y espíritu competitivo"
        }
    ],
    trends={
        "academic_performance": "Fuerte y en mejora en todas las asignaturas",
        "participation": "Activo en actividades académicas y extracurriculares"
    }
)

# Actualizar insights agregados (patrones entre dominios)
client.state_service.update_aggregated_insights(
    subject_id="estudiante123",
    cross_domain_patterns=[
        "Muestra mayor rendimiento académico después de actividades deportivas",
        "Periodos de estrés académico correlacionados con cambios en patrones de sueño"
    ],
    recommended_actions=[
        "Mantener balance entre actividades académicas y físicas",
        "Implementar técnicas de gestión de estrés durante periodos de exámenes"
    ]
)
```

### Actualización desde Eventos

Puedes actualizar automáticamente el estado basándote en eventos recientes:

```python
client.update_state_from_events(
    subject_id="estudiante123",
    domain_type="education",
    limit=10  # Considerar los 10 eventos más recientes
)
```

### Actualización desde Síntesis

También puedes actualizar el estado basándote en una síntesis:

```python
client.state_service.update_state_from_synthesis(
    subject_id="estudiante123",
    st_id=synthesis_id
)
```

## Catálogos de Dominio

### Definición de Términos

Los catálogos de dominio permiten estandarizar la terminología utilizada:

```python
from universal_history.models.domain_catalog import DomainCatalog, Organization

# Crear un catálogo de dominio
catalog = DomainCatalog(
    domain_type="education",
    organization=Organization(
        id="org001",
        name="Ministerio de Educación"
    )
)

# Añadir definiciones de términos
catalog.add_term(
    term_key="competencia_digital",
    definition="Capacidad de utilizar tecnologías digitales de manera segura, crítica y creativa",
    context="Evaluación de habilidades del siglo XXI",
    examples=["Uso efectivo de herramientas de búsqueda", "Creación de contenido digital"]
)

# Guardar el catálogo para un sujeto
client.history_service.get_history_by_subject("estudiante123").add_domain_catalog(catalog)
```

### Definición de Métricas

También puedes definir métricas estándar:

```python
catalog.add_metric(
    metric_key="fluidez_lectora",
    description="Velocidad de lectura en palabras por minuto",
    unit="ppm",
    min_value=0,
    max_value=500,
    interpretation="Valores entre 150-200 ppm indican fluidez adecuada para nivel secundario"
)

catalog.add_classification(
    classification_key="nivel_participacion",
    categories=["bajo", "moderado", "alto", "excepcional"],
    description="Nivel de participación activa del estudiante en actividades de clase"
)
```

## Integración con Modelos de Lenguaje

### Obtención de Contexto para LLMs

Una de las características más poderosas de Universal History es su capacidad para proporcionar contexto optimizado para modelos de lenguaje:

```python
# Obtener contexto optimizado para LLM
context = client.get_llm_context("estudiante123")

# Usar el contexto con un LLM
from langchain import OpenAI, LLMChain
from langchain.prompts import PromptTemplate

prompt_template = """
Historia del estudiante:
{context}

Basándote en esta información, responde la siguiente pregunta:
{question}
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=prompt_template
)

llm = OpenAI(temperature=0)
chain = LLMChain(llm=llm, prompt=prompt)

response = chain.run(
    context=context,
    question="¿Qué áreas matemáticas necesita reforzar este estudiante?"
)

print(response)
```

### Optimización del Contexto

Puedes personalizar el contexto que se proporciona al LLM:

```python
# Actualizar el resumen optimizado para LLM
client.state_service.update_llm_optimized_summary("estudiante123")

# Obtener contexto para dominios específicos
context = client.get_llm_context(
    subject_id="estudiante123",
    domain_types=["education", "sports"]
)
```

## Opciones de Almacenamiento

Universal History ofrece flexibilidad en cuanto a dónde y cómo se almacenan los datos.

### Almacenamiento en Memoria

El almacenamiento en memoria es rápido y útil para pruebas o aplicaciones efímeras:

```python
client = UniversalHistoryClient()  # Por defecto usa almacenamiento en memoria
```

Los datos solo persisten durante la sesión actual y se pierden al reiniciar la aplicación.

### Almacenamiento en Archivos

El almacenamiento en archivos proporciona persistencia sin necesidad de infraestructura adicional:

```python
client = UniversalHistoryClient(storage_dir="./data")
```

Los datos se almacenan en una estructura de directorios:
- `./data/histories/`: Información básica de cada Historia Universal
- `./data/events/`: Registros de Eventos organizados por Historia
- `./data/syntheses/`: Síntesis de Trayectoria
- `./data/states/`: Documentos de Estado
- `./data/catalogs/`: Catálogos de Definiciones de Dominio
- `./data/indexes/`: Índices para búsqueda rápida

### Almacenamiento en MongoDB

Para aplicaciones a mayor escala, el almacenamiento en MongoDB ofrece mejor rendimiento y escalabilidad:

```python
client = UniversalHistoryClient(mongodb_connection="mongodb://localhost:27017/")
```

Requiere una instalación de MongoDB y la dependencia adicional:

```bash
pip install universal-history[mongodb]
```

## Importación y Exportación

### Exportar una Historia

Para exportar una Historia Universal completa:

```python
# Exportar a un diccionario
history_data = client.export_history(
    subject_id="estudiante123",
    include_events=True,
    include_syntheses=True,
    include_state=True,
    include_catalogs=True
)

# Guardar como JSON
import json
with open("historia_estudiante123.json", "w") as f:
    json.dump(history_data, f, default=str)
```

### Importar una Historia

Para importar una Historia Universal:

```python
# Cargar desde un archivo JSON
with open("historia_estudiante123.json", "r") as f:
    history_data = json.load(f)

# Importar la historia
hu_id = client.import_history(history_data)
```

También hay métodos auxiliares para simplificar este proceso:

```python
# Guardar directamente a un archivo
client.save_history_to_file("estudiante123", "historia_estudiante123.json")

# Cargar directamente desde un archivo
hu_id = client.load_history_from_file("historia_estudiante123.json")
```

### Copiar Historias

Para copiar una Historia Universal entre sujetos:

```python
# Copiar historia completa
new_hu_id = client.history_service.copy_history(
    source_subject_id="estudiante123",
    target_subject_id="estudiante124"
)

# Copiar selectivamente
new_hu_id = client.history_service.copy_history(
    source_subject_id="estudiante123",
    target_subject_id="estudiante124",
    include_events=True,
    include_syntheses=False,
    include_state=True,
    include_catalogs=True
)
```

## Ejemplos Prácticos

### Historia Educativa

```python
# Crear un estudiante con eventos educativos
student_id = "estudiante123"

# Eventos de curso de matemáticas
math_exam_1 = client.create_event(
    subject_id=student_id,
    domain_type="education",
    event_type="exam",
    content="El estudiante obtuvo 85/100 en el examen parcial de Álgebra.",
    source_type="institution",
    source_id="escuela001",
    source_name="Escuela Secundaria Springfield",
    creator_id="profesor001",
    creator_name="Sra. Martínez",
    creator_role="Profesora de Matemáticas",
    metrics={"score": 85, "max_score": 100},
    assessments={"performance": "Buena comprensión de conceptos algebraicos pero necesita mejorar en problemas verbales."},
    tags=["matemáticas", "álgebra", "examen"]
)

math_assignment = client.create_event(
    subject_id=student_id,
    domain_type="education",
    event_type="assignment",
    content="El estudiante completó la tarea sobre ecuaciones cuadráticas con puntuación 18/20.",
    source_type="institution",
    source_id="escuela001",
    source_name="Escuela Secundaria Springfield",
    creator_id="profesor001",
    creator_name="Sra. Martínez",
    creator_role="Profesora de Matemáticas",
    metrics={"score": 18, "max_score": 20},
    tags=["matemáticas", "álgebra", "tarea", "ecuaciones cuadráticas"]
)

math_exam_2 = client.create_event(
    subject_id=student_id,
    domain_type="education",
    event_type="exam",
    content="El estudiante obtuvo 92/100 en el examen final de Álgebra.",
    source_type="institution",
    source_id="escuela001",
    source_name="Escuela Secundaria Springfield",
    creator_id="profesor001",
    creator_name="Sra. Martínez",
    creator_role="Profesora de Matemáticas",
    metrics={"score": 92, "max_score": 100},
    assessments={"performance": "Excelente mejora en todas las áreas, especialmente en problemas verbales."},
    tags=["matemáticas", "álgebra", "examen", "final"]
)

# Generar una síntesis para el curso de matemáticas
from datetime import datetime, timedelta

today = datetime.now()
three_months_ago = today - timedelta(days=90)

math_synthesis = client.create_synthesis(
    subject_id=student_id,
    domain_type="education",
    summary="El estudiante mostró un fuerte desempeño en Álgebra con una mejora significativa a lo largo del curso.",
    start_date=three_months_ago.isoformat(),
    end_date=today.isoformat(),
    source_events=[
        math_exam_1['re_id'],
        math_assignment['re_id'],
        math_exam_2['re_id']
    ],
    key_insights=[
        "El estudiante demostró habilidades algebraicas sólidas",
        "Mejora significativa en la resolución de problemas verbales",
        "Completó consistentemente las tareas asignadas"
    ],
    significant_events=[
        {
            "re_id": math_exam_2['re_id'],
            "description": "Obtuvo 92/100 en el examen final",
            "significance": "Muestra dominio de conceptos algebraicos y mejora significativa"
        }
    ],
    metrics={
        "promedio_puntuacion": {
            "value": 87,
            "trend": "improving",
            "analysis": "Las puntuaciones mejoraron constantemente a lo largo del curso"
        }
    },
    patterns=[
        "Desafíos iniciales con problemas verbales seguidos de una mejora significativa",
        "Rendimiento consistentemente alto en problemas computacionales"
    ],
    recommendations=[
        "Listo para conceptos avanzados de álgebra",
        "Considerar participación en competiciones matemáticas"
    ]
)

# Actualizar el estado educativo
client.create_state_document(student_id)
client.update_domain_state(
    subject_id=student_id,
    domain_type="education",
    current_status="Actualmente inscrito en 10° grado en la Escuela Secundaria Springfield",
    key_attributes={
        "gpa": 3.8,
        "attendance_rate": 98.5,
        "grade_level": 10
    },
    recent_events=[
        {
            "re_id": math_exam_2['re_id'],
            "description": "Obtuvo 92/100 en el examen final de Álgebra"
        }
    ],
    significant_events=[
        {
            "re_id": math_exam_2['re_id'],
            "description": "Obtuvo 92/100 en el examen final de Álgebra",
            "significance": "Demuestra excelente progreso y dominio de conceptos algebraicos"
        }
    ],
    trends={
        "academic_performance": "Fuerte y en mejora en todas las asignaturas",
        "participation": "Activo en actividades académicas"
    }
)

# Obtener contexto para un LLM
context = client.get_llm_context(student_id)
print(context)
```

### Historia Clínica

```python
# Crear un paciente con eventos de salud
patient_id = "paciente456"

# Examen físico anual
physical = client.create_event(
    subject_id=patient_id,
    domain_type="health",
    event_type="examination",
    content="Examen físico anual. El paciente se encuentra en buen estado general de salud.",
    source_type="institution",
    source_id="hospital001",
    source_name="Hospital General de la Ciudad",
    creator_id="doctor001",
    creator_name="Dr. García",
    creator_role="Médico de Atención Primaria",
    metrics={
        "weight_kg": 70.5,
        "height_cm": 175,
        "blood_pressure_systolic": 118,
        "blood_pressure_diastolic": 75,
        "heart_rate": 68
    },
    assessments={
        "general_health": "Bueno",
        "recommendations": "Continuar con ejercicio regular y dieta balanceada"
    },
    tags=["examen", "anual", "rutina"]
)

# Análisis de laboratorio
lab_test = client.create_event(
    subject_id=patient_id,
    domain_type="health",
    event_type="lab_test",
    content="Panel sanguíneo completo. Todos los resultados dentro de rangos normales.",
    source_type="institution",
    source_id="lab001",
    source_name="LabMed",
    creator_id="tech001",
    creator_name="Sara Rodríguez",
    creator_role="Técnico de Laboratorio",
    metrics={
        "cholesterol_total": 185,
        "cholesterol_hdl": 55,
        "cholesterol_ldl": 110,
        "glucose": 92
    },
    tags=["laboratorio", "análisis de sangre", "rutina"]
)

# Vacunación
vaccination = client.create_event(
    subject_id=patient_id,
    domain_type="health",
    event_type="vaccination",
    content="Vacunación anual contra la gripe.",
    source_type="institution",
    source_id="clinic001",
    source_name="Clínica Comunitaria de Salud",
    creator_id="nurse001",
    creator_name="Roberto Jiménez",
    creator_role="Enfermero Registrado",
    metrics={
        "vaccine_type": "Influenza Cuadrivalente",
        "lot_number": "FL2023-456"
    },
    tags=["vacunación", "gripe", "preventivo"]
)

# Consulta con especialista
specialist = client.create_event(
    subject_id=patient_id,
    domain_type="health",
    event_type="specialist_visit",
    content="Consulta con dermatólogo para revisión rutinaria de piel. Sin hallazgos preocupantes.",
    source_type="institution",
    source_id="clinic002",
    source_name="Asociados de Dermatología",
    creator_id="doctor002",
    creator_name="Dr. Lee",
    creator_role="Dermatólogo",
    assessments={
        "skin_condition": "Saludable con mínimo daño solar",
        "recommendations": "Continuar usando protector solar diariamente y programar próxima revisión en un año"
    },
    tags=["dermatología", "revisión de piel", "especialista", "preventivo"]
)

# Crear una síntesis de salud
from datetime import datetime, timedelta

today = datetime.now()
one_year_ago = today - timedelta(days=365)

health_synthesis = client.create_synthesis(
    subject_id=patient_id,
    domain_type="health",
    summary="El paciente ha mantenido un buen estado general de salud con atención preventiva constante durante el último año.",
    start_date=one_year_ago.isoformat(),
    end_date=today.isoformat(),
    source_events=[
        physical['re_id'],
        lab_test['re_id'],
        vaccination['re_id'],
        specialist['re_id']
    ],
    key_insights=[
        "El paciente asiste consistentemente a citas preventivas",
        "Todos los indicadores de salud están dentro de rangos normales",
        "El paciente sigue las medidas preventivas recomendadas"
    ],
    significant_events=[
        {
            "re_id": physical['re_id'],
            "description": "Examen físico anual con resultados normales",
            "significance": "Confirma continuidad de buen estado de salud"
        }
    ],
    metrics={
        "health_status": {
            "value": 9.0,
            "trend": "stable",
            "analysis": "El paciente mantiene excelente salud sin cambios significativos"
        }
    },
    patterns=[
        "Adherencia consistente al calendario de atención preventiva",
        "Signos vitales y valores de laboratorio estables a lo largo del tiempo"
    ],
    recommendations=[
        "Continuar con prácticas actuales de mantenimiento de salud",
        "Considerar añadir análisis de vitamina D en próximo panel sanguíneo"
    ]
)

# Actualizar el documento de estado
client.create_state_document(patient_id)
client.update_domain_state(
    subject_id=patient_id,
    domain_type="health",
    current_status="Adulto saludable sin condiciones crónicas",
    key_attributes={
        "weight_kg": 70.5,
        "height_cm": 175,
        "bmi": 23.0,
        "blood_pressure": "118/75"
    },
    recent_events=[
        {
            "re_id": specialist['re_id'],
            "description": "Revisión dermatológica sin preocupaciones"
        },
        {
            "re_id": vaccination['re_id'],
            "description": "Vacunación anual contra la gripe"
        }
    ],
    significant_events=[
        {
            "re_id": physical['re_id'],
            "description": "Examen físico anual",
            "significance": "Confirma buen estado general de salud"
        }
    ],
    trends={
        "overall_health": "Salud excelente estable",
        "preventive_care": "Adherencia consistente al calendario recomendado"
    }
)

# Obtener contexto optimizado para LLM
context = client.get_llm_context(patient_id)
print(context)
```

### Historia Laboral

```python
# Crear un empleado con eventos laborales
employee_id = "empleado789"

# Contratación
hiring = client.create_event(
    subject_id=employee_id,
    domain_type="work",
    event_type="hiring",
    content="Contratado como Desarrollador de Software Junior tras exitoso proceso de entrevista.",
    source_type="institution",
    source_id="empresa001",
    source_name="TechCorp Solutions",
    creator_id="rrhh001",
    creator_name="María Rodríguez",
    creator_role="Gerente de Recursos Humanos",
    metrics={
        "starting_salary": 75000,
        "level": 1
    },
    tags=["contratación", "incorporación", "desarrollo de software"]
)

# Finalización de proyecto
project1 = client.create_event(
    subject_id=employee_id,
    domain_type="work",
    event_type="project_completion",
    content="Completó exitosamente el proyecto de rediseño del portal de clientes antes de lo programado.",
    source_type="institution",
    source_id="empresa001",
    source_name="TechCorp Solutions",
    creator_id="manager001",
    creator_name="David Chen",
    creator_role="Gerente de Desarrollo",
    assessments={
        "code_quality": "Excelente",
        "collaboration": "Muy buena",
        "project_management": "Superó expectativas"
    },
    tags=["proyecto", "desarrollo web", "portal de clientes"]
)

# Evaluación de desempeño
review = client.create_event(
    subject_id=employee_id,
    domain_type="work",
    event_type="performance_review",
    content="Evaluación de desempeño semestral. Superando expectativas en habilidades técnicas y trabajo en equipo.",
    source_type="institution",
    source_id="empresa001",
    source_name="TechCorp Solutions",
    creator_id="manager001",
    creator_name="David Chen",
    creator_role="Gerente de Desarrollo",
    metrics={
        "overall_rating": 4.5,
        "technical_skills": 4.7,
        "teamwork": 4.3,
        "communication": 4.0
    },
    assessments={
        "strengths": "Fuertes habilidades de resolución de problemas y rápida capacidad de aprendizaje",
        "areas_for_improvement": "Podría mejorar prácticas de documentación",
        "overall_assessment": "Miembro valioso del equipo con alto potencial"
    },
    tags=["evaluación", "desempeño", "revisión"]
)

# Capacitación
training = client.create_event(
    subject_id=employee_id,
    domain_type="work",
    event_type="training",
    content="Completó curso de certificación avanzada en React y TypeScript.",
    source_type="institution",
    source_id="training001",
    source_name="TechLearn Academy",
    creator_id="instructor001",
    creator_name="Jason Wright",
    creator_role="Instructor Senior",
    metrics={
        "certification_score": 95,
        "course_duration_hours": 40
    },
    tags=["capacitación", "certificación", "React", "TypeScript"]
)

# Promoción
promotion = client.create_event(
    subject_id=employee_id,
    domain_type="work",
    event_type="promotion",
    content="Promovido a Desarrollador de Software II basado en desempeño sobresaliente.",
    source_type="institution",
    source_id="empresa001",
    source_name="TechCorp Solutions",
    creator_id="rrhh001",
    creator_name="María Rodríguez",
    creator_role="Gerente de Recursos Humanos",
    metrics={
        "new_salary": 90000,
        "new_level": 2
    },
    assessments={
        "promotion_rationale": "Consistentemente superó expectativas en proyectos y demostró liderazgo técnico"
    },
    tags=["promoción", "desarrollo profesional"]
)

# Crear una síntesis laboral
from datetime import datetime, timedelta

today = datetime.now()
one_year_ago = today - timedelta(days=365)

work_synthesis = client.create_synthesis(
    subject_id=employee_id,
    domain_type="work",
    summary="El empleado ha demostrado un crecimiento y desempeño excepcionales durante su primer año de empleo.",
    start_date=one_year_ago.isoformat(),
    end_date=today.isoformat(),
    source_events=[
        hiring['re_id'],
        project1['re_id'],
        review['re_id'],
        training['re_id'],
        promotion['re_id']
    ],
    key_insights=[
        "Rápida progresión de Desarrollador Junior a Desarrollador II",
        "Consistentemente supera expectativas en desempeño técnico",
        "Fuerte inversión en desarrollo de habilidades a través de capacitación",
        "Entregó exitosamente proyectos de alta visibilidad"
    ],
    significant_events=[
        {
            "re_id": promotion['re_id'],
            "description": "Promoción a Desarrollador de Software II",
            "significance": "Reconocimiento de desempeño excepcional y crecimiento"
        }
    ],
    metrics={
        "salary_growth": {
            "value": 20,
            "trend": "increasing",
            "analysis": "20% de incremento en compensación dentro del primer año"
        },
        "performance_rating": {
            "value": 4.5,
            "trend": "stable",
            "analysis": "Calificaciones de desempeño consistentemente altas"
        }
    },
    patterns=[
        "Toma iniciativa para desarrollar nuevas habilidades",
        "Entrega proyectos en tiempo o antes de lo programado",
        "Recibe feedback positivo consistente de miembros del equipo"
    ],
    recommendations=[
        "Considerar para oportunidades de liderazgo técnico",
        "Fomentar mentoría de miembros junior del equipo",
        "Potencial candidato de vía rápida para rol de desarrollador senior"
    ]
)

# Actualizar el documento de estado
client.create_state_document(employee_id)
client.update_domain_state(
    subject_id=employee_id,
    domain_type="work",
    current_status="Desarrollador de Software II en TechCorp Solutions",
    key_attributes={
        "company": "TechCorp Solutions",
        "department": "Desarrollo de Producto",
        "position": "Desarrollador de Software II",
        "tenure_years": 1,
        "salary": 90000
    },
    recent_events=[
        {
            "re_id": promotion['re_id'],
            "description": "Promoción a Desarrollador de Software II"
        },
        {
            "re_id": training['re_id'],
            "description": "Completó certificación de React y TypeScript"
        }
    ],
    significant_events=[
        {
            "re_id": promotion['re_id'],
            "description": "Promoción a Desarrollador de Software II",
            "significance": "Avance rápido reflejando desempeño excepcional"
        }
    ],
    trends={
        "career_trajectory": "Trayectoria de crecimiento acelerado",
        "skill_development": "Aprendizaje proactivo y certificación",
        "performance": "Consistentemente superando expectativas"
    }
)

# Obtener contexto optimizado para LLM
context = client.get_llm_context(employee_id)
print(context)
```

## Solución de Problemas

### Problemas Comunes

**1. Error al instalar MongoDB**

```
ImportError: No module named 'pymongo'
```

**Solución**: Instalar las dependencias de MongoDB:

```bash
pip install universal-history[mongodb]
```

**2. Error al inicializar el cliente con almacenamiento en archivos**

```
ModuleNotFoundError: No module named 'universal_history.storage.file_repository'
```

**Solución**: Verificar que estás utilizando la versión más reciente de la biblioteca:

```bash
pip install --upgrade universal-history
```

**3. Errores de validación al crear eventos**

```
ValueError: Invalid domain type: sport
```

**Solución**: Verificar que estás utilizando valores de dominio válidos (education, health, work, sports, financial, personal, etc.). Ten en cuenta que algunos valores usan singular y otros plural.

**4. Errores al exportar a JSON**

```
TypeError: Object of type datetime is not JSON serializable
```

**Solución**: Utilizar un serializador personalizado:

```python
json.dumps(data, default=str)
```

### Depuración

Para activar el registro de depuración:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("universal_history")
logger.setLevel(logging.DEBUG)
```

Para verificar la integridad de una cadena de eventos:

```python
valid = client.history_service.verify_event_chain(
    subject_id="estudiante123",
    domain_type="education"
)
print(f"Cadena de eventos válida: {valid}")
```

## Referencias y Recursos

### API de Referencia

Para obtener una referencia detallada de la API de Universal History, consulta la documentación en línea en [https://universal-history.readthedocs.io/](https://universal-history.readthedocs.io/)

### Recursos Adicionales

- **Repositorio GitHub**: [https://github.com/yourusername/universal-history](https://github.com/yourusername/universal-history)
- **Estándar HU Completo**: [https://hustandard.org/](https://hustandard.org/) (sitio ficticio)
- **Foro de la Comunidad**: [https://community.universal-history.org/](https://community.universal-history.org/) (sitio ficticio)

---

Este manual está diseñado para ayudarte a aprovechar al máximo la biblioteca Universal History. Si tienes preguntas, sugerencias o encuentras problemas, no dudes en abrir un issue en nuestro repositorio de GitHub o participar en el foro de la comunidad.