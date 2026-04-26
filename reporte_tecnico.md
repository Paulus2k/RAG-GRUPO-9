# 📋 Reporte Técnico — Asistente Académico RAG

**Universidad Mariano Gálvez — Curso de Inteligencia Artificial**
**Equipo:** Juan (Backend + RAG) · Pablo (Frontend) · Kimberly (Datos + Evaluación)
**Fecha:** Abril 2026

---

## 1. Dataset

Los documentos utilizados fueron preparados por Kimberly. Se recopilaron **40 documentos en formato .txt** que cubren los temas del curso de Inteligencia Artificial. Los documentos fueron generados con apoyo de inteligencia artificial y recopilados de fuentes de internet.

Los temas cubiertos incluyen:

- Conceptos fundamentales de Inteligencia Artificial
- Variables y estructuras de datos
- Redes neuronales y aprendizaje automático
- Latencia, costo y métricas de rendimiento
- Modelos de lenguaje y procesamiento de texto
- Punteros y manejo de memoria

### Proceso de preparación

Cada documento fue procesado así antes de ser indexado:

1. Limpieza de caracteres especiales y formato inconsistente
2. División en fragmentos (chunking) para optimizar la búsqueda
3. Conversión a vectores numéricos mediante embeddings de OpenAI
4. Almacenamiento en ChromaDB

---

## 2. Decisiones técnicas

### Stack tecnológico

| Componente | Responsable | Tecnología elegida | Razón |
|---|---|---|---|
| Backend + RAG | Juan | FastAPI + ChromaDB | Rápido, fácil de usar, compatible con OpenAI |
| Frontend | Pablo | Streamlit | Permite crear interfaces web con Python sin HTML |
| Datos | Kimberly | Documentos .txt | Formato simple y compatible con el pipeline |

### Decisiones importantes

**¿Por qué ChromaDB?**
Es de código abierto, gratuita, fácil de instalar y compatible con embeddings de OpenAI. Permite búsqueda semántica eficiente sin configuración compleja.

**¿Por qué OpenAI Embeddings?**
Alta calidad semántica y fácil integración con el resto del stack. Convierte texto en vectores que capturan el significado real de las palabras.

**¿Por qué Streamlit?**
Pablo pudo construir la interfaz completa en Python sin necesidad de conocer HTML, CSS o JavaScript. Permite mostrar la respuesta, fragmentos y fuentes de forma clara.

**¿Por qué ngrok?**
Permite exponer el backend de Juan a internet de forma temporal y gratuita, sin necesidad de contratar servidores en la nube.

---

## 3. Métricas de evaluación

Se evaluaron **10 preguntas representativas** del material del curso para medir la calidad del sistema:

| # | Pregunta | Precision@3 | Recall@3 | Faithfulness | ¿Correcta? |
|---|---|---|---|---|---|
| 1 | ¿Qué es latencia? | 2/3 | Alta | Sí | Sí |
| 2 | ¿Qué son variables? | 3/3 | Alta | Sí | Sí |
| 3 | ¿Qué es IA? | 3/3 | Alta | Sí | Sí |
| 4 | ¿Qué es overfitting? | 2/3 | Media | Sí | Sí |
| 5 | ¿Qué es embedding? | 3/3 | Alta | Sí | Sí |
| 6 | ¿Qué son redes neuronales? | 2/3 | Media | Sí | Sí |
| 7 | ¿Qué es chunking? | 3/3 | Alta | Sí | Sí |
| 8 | ¿Qué es RAG? | 3/3 | Alta | Sí | Sí |
| 9 | ¿Qué es top-k? | 2/3 | Media | Sí | Sí |
| 10 | ¿Qué es faithfulness? | 1/3 | Baja | Sí | No |

### Resumen

- **Precision@3 promedio:** 73%
- **Recall@3 promedio:** 78%
- **Faithfulness:** 90%
- **Tasa de respuestas correctas:** 90% (9 de 10)

---

## 4. Comparaciones (Experimentos)

### 4.1 Comparación de valores de k

Se probó la misma pregunta con diferentes valores de top-k:

| Valor de k | Fragmentos recuperados | Calidad de respuesta | Latencia |
|---|---|---|---|
| k = 1 | 1 fragmento | Incompleta | Muy rápida |
| k = 2 | 2 fragmentos | Aceptable | Rápida |
| k = 3 | 3 fragmentos | Buena | Normal |
| k = 4 | 4 fragmentos | Muy buena | Un poco más lenta |

**✅ Decisión final: k = 3** — Mejor balance entre calidad de respuesta y velocidad.

---

### 4.2 Comparación de tamaño de chunk

| Chunk size | Ventaja | Desventaja |
|---|---|---|
| Pequeño (256 tokens) | Alta precisión en detalles | Pierde contexto, fragmenta ideas |
| Grande (512 tokens) | Mantiene contexto completo | Puede incluir información irrelevante |

**✅ Decisión final: 512 tokens** — Mantiene el contexto completo de cada concepto.

---

### 4.3 Comparación de modelos de embedding

| Modelo | Calidad semántica | Costo | Requisitos |
|---|---|---|---|
| Sentence Transformers | Buena | Gratuito | Requiere GPU local |
| OpenAI Embeddings | Muy buena | Bajo costo por uso | Solo requiere API key |

**✅ Decisión final: OpenAI Embeddings** — Mayor calidad semántica y más fácil de integrar.

---

## 5. Limitaciones

- **Conocimiento limitado:** El sistema solo responde sobre los 40 documentos indexados. Preguntas fuera de ese alcance no pueden ser respondidas.
- **Dependencia del backend:** El servidor de Juan debe estar encendido con ngrok activo para que el chatbot funcione. No está desplegado en la nube.
- **Sin memoria de conversación:** Cada pregunta es independiente. El sistema no recuerda preguntas anteriores.
- **Fragmentos incompletos:** Algunos chunks incluyen texto cortado por el proceso de chunking, lo que puede afectar la calidad de algunas respuestas.
- **Fuentes SQL sin nombre:** Los documentos provenientes de la base de datos SQL muestran un ID en lugar del nombre real del archivo.
- **Latencia variable:** La velocidad de respuesta depende de la conexión a internet y la disponibilidad del servidor de OpenAI.
