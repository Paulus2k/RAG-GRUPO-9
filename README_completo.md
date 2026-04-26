# 🎓 Asistente Académico RAG

Sistema de Retrieval-Augmented Generation (RAG) que responde preguntas usando únicamente el material del curso de Inteligencia Artificial, citando siempre las fuentes utilizadas.

**Universidad Mariano Gálvez — Curso de Inteligencia Artificial**
**Equipo:** Juan (Backend + RAG) · Pablo (Frontend) · Kimberly (Datos + Evaluación)

---

## 📦 Repositorios del proyecto

| Parte | Repositorio |
|---|---|
| Backend + RAG | https://github.com/Paulus2k/RAG-GRUPO-9 |
| Frontend | https://github.com/Paulus2k/RAG-GRUPO-9 |
| Datos + Evaluación | https://github.com/Paulus2k/RAG-GRUPO-9 |

---

## 🏗️ Arquitectura general

```
Usuario → Frontend (Streamlit) → Backend (FastAPI + ngrok) → ChromaDB + Ollama
                                         ↑
                              40 documentos .txt (Kimberly)
```

---

## ⚙️ Requisitos previos

Instalar antes de empezar:

- Python 3.11 (importante: NO usar 3.14)
- PostgreSQL
- Git
- ngrok — cuenta gratuita en https://ngrok.com
- Ollama — descargar en https://ollama.com/download

---

## 🔽 PARTE 1 — Instalar y encender el Backend (Juan)

### Paso 1 — Instalar Ollama y descargar el modelo

1. Descarga e instala Ollama desde **https://ollama.com/download**
2. Abre una terminal y corre:

```bash
ollama pull llama3.1
```

⚠️ El modelo pesa varios GB, espera a que descargue completamente.

3. Verifica que funciona:

```bash
ollama run llama3.1
```

Escribe cualquier cosa, si responde es que funciona. Cierra con `/bye`.

---

### Paso 2 — Clonar el repositorio del backend

```bash
git clone https://github.com/Paulus2k/RAG-GRUPO-9.git
cd RAG-GRUPO-9
```

---

### Paso 3 — Crear entorno virtual

```bash
python -m venv .venv
```

Activarlo en Windows:

```bash
.venv\Scripts\activate
```

Deberías ver `(.venv)` al inicio de la terminal.

---

### Paso 4 — Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### Paso 5 — Configurar variables de entorno

1. Busca el archivo `.env.example` en la carpeta del proyecto
2. Crea una copia llamada `.env`
3. Asegúrate que tenga esto:

```
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.1
DATABASE_URL=postgresql://postgres:TU_CONTRASEÑA@localhost:5432/backend_rag
```

---

### Paso 6 — Configurar PostgreSQL

1. Abre pgAdmin o tu cliente de PostgreSQL
2. Crea una base de datos llamada `backend_rag`
3. Importa el archivo SQL:

```bash
psql -U postgres -d backend_rag -f sql/documentos_actualizados.sql
```

---

### Paso 7 — Encender el backend (3 terminales)

**Terminal 1 — Indexar documentos (solo la primera vez)**

```bash
.venv\Scripts\activate
python -m scripts.index_sql_file_documents
```

Espera a que termine completamente antes de continuar.

**Terminal 2 — Encender la API**

```bash
.venv\Scripts\activate
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```

Deberías ver:
```
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Terminal 3 — Crear link público con ngrok**

```bash
ngrok http 8000
```

Copia el link que aparece en **Forwarding**, por ejemplo:
```
https://abc123.ngrok-free.dev
```

**Verificar que el backend funciona:**

Abre el navegador y entra a:
```
https://TU_LINK.ngrok-free.dev/health
```

Debe responder:
```json
{"status": "ok", "collection_count": 72}
```

---

## 🔽 PARTE 2 — Instalar y encender el Frontend (Pablo)

### Paso 1 — Clonar el repositorio del frontend

```bash
git clone https://github.com/InteligenciaIA/frontend.git
cd frontend
```

---

### Paso 2 — Instalar dependencias

```bash
pip install streamlit requests
```

---

### Paso 3 — Actualizar el link del backend

Abre el archivo `app.py` y busca esta línea:

```python
BACKEND_URL = "https://unpasteurized-metronomically-konnor.ngrok-free.dev"
```

Reemplaza el link con el que generó ngrok en la Parte 1.

---

### Paso 4 — Encender el frontend

```bash
python -m streamlit run app.py
```

Se abre automáticamente en el navegador en `http://localhost:8501`

---

## ✅ Verificar que todo funciona

1. El backend responde en `/health` con `collection_count: 72`
2. El frontend se abre en el navegador
3. Escribe una pregunta sobre el material del curso
4. El chatbot responde con texto, fragmentos y fuentes

---

## ❗ Problemas comunes

| Error | Solución |
|---|---|
| `ollama: command not found` | Reinstala Ollama y reinicia la terminal |
| `pip install` falla con error de Rust | Usa Python 3.11 en lugar de 3.14 |
| `collection_count: 0` | Corre el script de indexación del Paso 7 |
| El chatbot dice "no tengo evidencia" | Verifica que el backend está encendido con ngrok |
| ngrok no abre | Verifica que tienes cuenta en ngrok.com |
| Error de PostgreSQL | Verifica que el servicio de PostgreSQL está corriendo |
