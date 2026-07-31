# ANÁLISIS LATAM — Comparación regional de tesis + datasets

**Fecha:** 2026-07-30
**Propósito:** Comparar el corpus UNA con tesis similares en Uruguay, Chile, Argentina, Brasil para validar gaps.

---

## 🇺🇾 Uruguay — Grupo PLN UdelaR (FUERTÍSIMO)

**URL:** fing.edu.uy/inco/grupos/pln/
**Director:** Dra. Aiala Rosá
**Co-director:** Dr. Luis Chiruzzo

### Equipo (12 personas)
- **Dra. Aiala Rosá** (responsable)
- **Dr. Luis Chiruzzo** (corresponsable)
- **Dr. Guillermo Moncecchi**
- **MSc. JuanJo Prada**
- **MSc. Diego Garat**
- **MSc. Santiago Góngora**
- Estudiantes posgrado: Soledad Álvarez, Karina Cardozo, Gonzalo Herrera, etc.
- 8 estudiantes de grado

### Líneas de investigación
- **Subjetividad: análisis de sentimiento, detección de humor, detección de discurso de odio**
- Búsqueda de Respuestas, RAG
- **PLN aplicado a la enseñanza de lenguas**
- Co-creatividad Humano-Computadora
- **IA para Inclusión y Accesibilidad**
- LLMs aplicados a dominios específicos
- Análisis de textos periodísticos
- **Trabajan en Guaraní actualmente** ← clave para V5

### Relevancia para P3/V5
- Han publicado Guaraní sentiment analysis
- Co-supervisor natural para V5 (Guaraní PLN)
- **Email**: pln@fing.edu.uy

---

## 🇪🇸 España — Universidad de Granada (Tesis Guaraní/Jopara existente)

### Tesis doctoral UGR 2022 — **CRUCIAL para P3/V5**
- **Título**: "Machine Learning approaches for Topic and Sentiment Analysis in multilingual opinions and low-resource languages: From English to Guarani"
- **Autor**: Marvin Matías Agüero Torales
- **Director**: Antonio Gabriel López Herrera (UGR)
- **Fecha**: 2022-02-04
- **URL**: digibug.ugr.es/handle/10481/72863

### Lo que cubre
- ✅ Sentiment analysis en **Guaraní**
- ✅ Sentiment analysis en **Jopara** (code-switching)
- ✅ Topic modeling en español
- ✅ Polarity classification
- ✅ Emotion recognition
- ✅ Humor detection
- ✅ Offensive/toxic language identification
- ✅ Code-switching handling

### Publicación derivada (Cognitive Computation, Springer, 2023)
"Multidimensional Affective Analysis for Low-resource Languages: A Use Case with Guarani-Spanish Code-switching Language"
- URL: link.springer.com/article/10.1007/s12559-023-10165-0
- Co-autores: Agüero-Torales, López-Herrera, Vilares

---

## 📊 DATASETS PÚBLICOS EN HUGGINGFACE (ENCONTRADOS)

**Marvin M. Agüero-Torales** subió todo a HuggingFace:

| Dataset | URL | P-relevance |
|---|---|---|
| **gn-emotion-recognition** | huggingface.co/datasets/mmaguero/gn-emotion-recognition | **P3 DIRECTO** |
| **gn-humor-detection** | huggingface.co/datasets/mmaguero/gn-humor-detection | V5 |
| **gn-offensive-language-identification** | huggingface.co/datasets/mmaguero/gn-offensive-language-identification | V5 |

**GitHub repo:** github.com/mmaguero/guarani-multi-affective-analysis

### Lo que faltaba para P3 (gap específico)
- ❌ **Salud mental específicamente** (depresión, ansiedad, suicidal ideation)
- ❌ **Validación con datos paraguayos reales** (Telegram/WhatsApp)
- ❌ **Aplicación a español paraguayo cotidiano** (no solo Guarani/Jopara formal)
- ❌ **Contexto clínico real** (no solo Twitter social)

---

## 🎯 Implicaciones para nuestras propuestas

### P3 Jopara MH — viabilidad confirmada
1. **Datasets existen** (mmaguero) — se pueden usar como base
2. **Precedente académico existe** (Agüero-Torales, Cognitive Computation 2023)
3. **Gap específico**: salud mental (depresión, ansiedad) no está cubierto
4. **Contribución nueva**: aplicación a datos paraguayos reales + extensión a salud mental
5. **Co-supervisor natural**: Grupo PLN UdelaR (Aiala Rosá) o Agüero-Torales mismo

### V5 Guaraní PLN — extensión natural
1. **Precedente directo** en UGR + UdelaR
2. **Datasets ya están** (mmaguero)
3. **Gap**: aplicación a educación rural, preservación cultural, accesibilidad
4. **Riesgo**: Alto (depende de hablantes + datos + funding)

---

## 🇦🇷 Argentina — Estado de tesis similares
- Sin evidencia directa de tesis Guaraní en universidades argentinas
- SÍ hay grupos PLN en FaMAF (Córdoba), UNS, UBA

## 🇨🇱 Chile — Recursos
- Grupo PLN en Universidad de Chile (Magíster en Inteligencia Artificial — MIA)
- Tesis en español chileno
- Cero en Guaraní (lógico, no es zona geográfica)

## 🇧🇷 Brasil — Recursos relevantes
- **CONNIE experiment** (cluster 7) — tesis que aparece en corpus UNA
- INPE (donde se formó Stalder) — cosmología + GPU sim
- Sin tesis específicas Guaraní (Brasil no habla Guaraní paraguayo)

---

## 📊 Resumen comparativo

| País | Grupo PLN activo | Tesis Guaraní | Datasets públicos | Co-supervisor potencial |
|---|---|---|---|---|
| 🇵🇾 Paraguay UNA | No (Von Lücken solo) | 1 (2014 Jopara) | No | Sí (YA conocido) |
| 🇺🇾 Uruguay UdelaR | **Sí (fuerte)** | Sí (en curso) | En HuggingFace | **pln@fing.edu.uy** |
| 🇪🇸 España UGR | Sí | **Sí (Agüero-Torales 2022)** | **Sí (HuggingFace)** | Sí (Agüero-Torales) |
| 🇦🇷 Argentina | Sí (FaMAF, UNS) | No | — | Potencial |
| 🇨🇱 Chile | Sí | No | — | No |
| 🇧🇷 Brasil | Sí | No | — | Ya conocido (Stalder) |

---

## 🚦 Decisión sugerida

### P3 (Jopara salud mental) tiene ahora:
- ✅ **Datasets pre-existentes** (no partimos de cero)
- ✅ **Precedente publicado** (Cognitive Computation Springer 2023)
- ✅ **Co-supervisor internacional** (mmaguero, Aiala Rosá)
- ✅ **Gap específico**: salud mental no cubierto
- ✅ **Datos propios** (psycology repo Telegram/WhatsApp)

### V5 (Guaraní PLN general) tiene:
- ✅ Datasets
- ✅ Precedente
- ⚠️ Riesgo: depende de datos + hablantes

### V6 (Educación LLM tutor) — explorar Chile:
- Magister en IA en Chile (UC)
- Becas Chile + Paraguay

---

## 📝 Lista para considerar

1. **Leer tesis Agüero-Torales completa** (PDF UGR)
2. **Descargar datasets mmaguero** (gn-emotion-recognition especialmente)
3. **Comparar extensión a español paraguayo**
4. **Explorar Magister en IA Chile** (posibilidad co-tesis)
5. **Considerar co-supervisión con Aiala Rosá** (UdelaR) si V5

### Archivos nuevos para guardar
- `latam_comparison.json` — universidades LATAM con grupos PLN
- `mmaguero_datasets.json` — datasets Guaraní/Jopara públicos
- `uguarani_thesis.json` — tesis UGR completa referencia