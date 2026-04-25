# 🏗️ Diagrama de Arquitectura — Asistente Académico RAG

## Diagrama

```mermaid
flowchart TD
    K["👩‍💻 Kimberly\nDatos + Evaluación"]
    D["📄 40 documentos .txt\nGenerados y recopilados"]
    J["👨‍💻 Juan\nBackend + RAG"]
    API["⚙️ FastAPI"]
    CH["Chunking\ndividir documentos"]
    EM["Embeddings\nOpenAI"]
    DB["ChromaDB\nbase vectorial"]
    RET["Retriever\ntop-k"]
    LLM["🤖 LLM\ngenera respuesta"]
    FE["🖥️ Frontend\nStreamlit UI"]
    U["👤 Usuario"]
    EV["📊 Evaluación\nPrecision, Recall, Faithfulness"]

    K --> D
    D -->|"ingesta"| API
    J --> API
    API --> CH --> EM --> DB --> RET --> LLM
    LLM -->|"respuesta + fragmentos + fuentes"| FE
    RET -->|"ngrok"| FE
    U -->|"pregunta"| FE
    FE -->|"muestra resultado"| U
    D --> EV

    style K fill:#1a7a6e,color:#fff
    style D fill:#1a7a6e,color:#fff
    style EV fill:#1a7a6e,color:#fff
    style J fill:#5b3fa6,color:#fff
    style API fill:#5b3fa6,color:#fff
    style CH fill:#3a2a7a,color:#fff
    style EM fill:#3a2a7a,color:#fff
    style DB fill:#3a2a7a,color:#fff
    style RET fill:#3a2a7a,color:#fff
    style LLM fill:#5b3fa6,color:#fff
    style FE fill:#b8860b,color:#fff
    style U fill:#444,color:#fff
```

---

## Descripción de componentes

### 🟢 Kimberly — Datos + Evaluación
Encargada de recopilar y preparar los **40 documentos .txt** que alimentan el sistema. Los documentos fueron generados con apoyo de IA y recopilados de fuentes del curso. También es responsable de medir la calidad del sistema con métricas de **Precision@k**, **Recall@k** y **Faithfulness**.

### 🟣 Juan — Backend + RAG
Construyó el cerebro del sistema usando **FastAPI**. El pipeline funciona así:
- **Chunking**: divide los documentos en fragmentos manejables
- **Embeddings (OpenAI)**: convierte cada fragmento en un vector numérico
- **ChromaDB**: almacena los vectores para búsqueda rápida
- **Retriever (top-k)**: busca los fragmentos más relevantes para cada pregunta
- **LLM**: genera una respuesta basada únicamente en los fragmentos recuperados

### 🟡 Pablo — Interfaz de usuario
Construyó la interfaz con **Streamlit**. El usuario escribe una pregunta y el sistema muestra:
- La respuesta generada por el LLM
- Los fragmentos de texto utilizados
- Las fuentes de donde proviene la información
- Un mensaje de "no tengo evidencia" si no hay información suficiente

La comunicación entre el frontend y el backend se hace a través de **ngrok**, que expone el servidor de Juan a internet de forma segura.
