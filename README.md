# EcoReason AI 🌱

## AI Biodiversity Intelligence & Environmental Reasoning Engine

EcoReason AI is an AI-powered environmental intelligence system designed to reason about biodiversity, soil, water, land use, climate and human-impact conditions.

The system combines **structured environmental state, multi-metric reasoning, conversational memory, scientific retrieval, vector search and AI-assisted synthesis** to produce actionable, evidence-grounded recommendations.

The goal is to behave like an **AI environmental scientist rather than a generic chatbot**.

---

## 🎯 Problem

Environmental problems are interconnected.

For example:

```text
Low Soil Organic Carbon
        +
Low Rainfall
        +
Monoculture
        +
Low Species Richness
        ↓
Soil-water stress
        +
Habitat diversity loss
        ↓
Biodiversity pressure
```

A useful environmental intelligence system therefore needs to reason across multiple variables instead of generating a recommendation from a single metric.

EcoReason AI was designed around this principle.

---

# 🏗️ System Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                         USER INPUT                           │
│                                                              │
│          Natural Language / Environmental Information       │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                    INPUT / STATE EXTRACTION                  │
│                                                              │
│  Extract environmental values from the conversation         │
│  and maintain a structured EnvironmentalState                │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                   CONVERSATION MEMORY                        │
│                                                              │
│  EnvironmentalState + conversation history                   │
│  Session-level contextual memory                              │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Required data        │
                    │ available?           │
                    └──────────┬───────────┘
                               │
                     ┌─────────┴─────────┐
                     │                   │
                    NO                  YES
                     │                   │
                     ▼                   ▼
          ┌──────────────────┐   ┌──────────────────────────┐
          │ Clarification    │   │ Environmental State      │
          │ Question         │   │ Pydantic Model           │
          └──────────────────┘   └─────────────┬────────────┘
                                               │
                                               ▼
┌──────────────────────────────────────────────────────────────┐
│                  MULTI-METRIC REASONING                      │
│                                                              │
│  Soil ↔ Water                                               │
│  Land Use ↔ Biodiversity                                    │
│  Deforestation ↔ Habitat Fragmentation                      │
│                                                              │
│  Deterministic environmental risk detection                  │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                  SCIENTIFIC RETRIEVAL                        │
│                                                              │
│     ┌─────────────────────┐     ┌──────────────────────┐    │
│     │ Local FAISS Vector  │     │ Scientific Web       │    │
│     │ Knowledge Base      │     │ Retrieval             │    │
│     └──────────┬──────────┘     └──────────┬───────────┘    │
│                │                           │                │
│                └─────────────┬─────────────┘                │
│                              ▼                              │
│                    Retrieved Evidence                       │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                  RECOMMENDATION ENGINE                       │
│                                                              │
│  What to do                                                 │
│  Why it works                                               │
│  Impacted environmental metrics                             │
│  Expected time horizon                                      │
│  Supporting evidence                                        │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                  FINAL AI RESPONSE                            │
│                                                              │
│       Actionable + Explainable + Evidence-Grounded           │
└──────────────────────────────────────────────────────────────┘
```

---

# 🧠 Design Principle

EcoReason AI is **not an LLM-only system**.

The reasoning pipeline is:

```text
Structured Environmental State
            +
Deterministic Multi-Metric Reasoning
            +
Scientific Knowledge Retrieval
            +
Vector Similarity Search
            +
Scientific Web Retrieval
            +
AI-Assisted Synthesis
```

This separates environmental reasoning from natural-language generation.

The structured reasoning layer identifies environmental relationships and risks, while the retrieval layer provides scientific context and the AI layer helps synthesize the final explanation.

---

# 🌱 Multi-Metric Reasoning

The core reasoning layer connects environmental variables rather than treating them independently.

### Soil + Water

```text
Low Organic Carbon
        +
Limited Rainfall
        ↓
Soil-Water Stress
```

### Land Use + Biodiversity

```text
Monoculture
        +
Low Species Richness
        ↓
Habitat Diversity Loss
```

### Deforestation + Biodiversity

```text
Habitat Loss
        +
Low Species Richness
        ↓
Habitat Fragmentation Pressure
```

This allows the system to reason across several environmental variables simultaneously.

The challenge identifies multi-metric reasoning as a core differentiator and requires relationships such as soil health ↔ biodiversity, water availability ↔ species survival, and land use ↔ habitat fragmentation.

---

# 🔎 Scientific Knowledge System

EcoReason AI includes a retrievable scientific knowledge layer instead of relying only on prompts.

The knowledge layer uses:

* Sentence Transformers
* FAISS
* Scientific environmental documents
* Vector similarity search
* Document metadata

The current knowledge corpus covers:

```text
knowledge/
│
├── agroforestry.txt
├── ipcc_land.txt
├── soil_organic_matter.txt
├── soil_water.txt
│
└── index/
    ├── knowledge.faiss
    └── metadata.json
```

The embedding model currently used is:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Documents are embedded and stored in a FAISS similarity index.

---

# 📚 Knowledge Retrieval Flow

```text
Environmental Risk
        ↓
Scientific Query
        ↓
Sentence Transformer
        ↓
Vector Embedding
        ↓
FAISS Similarity Search
        ↓
Top Relevant Documents
        ↓
Scientific Context
        ↓
Recommendation / Explanation
```

The system can additionally perform scientific web retrieval from trusted scientific domains to supplement the local knowledge base.

The challenge requires a retrievable knowledge layer using approaches such as RAG, embeddings, vector databases or structured datasets and expects the retrieval process to be clearly demonstrated.

---

# 💬 Conversational Memory

EcoReason AI includes a session-level conversational memory layer implemented through `ConversationMemory`.

The memory maintains:

* Current environmental state
* Previously provided environmental measurements
* Conversation history

Example:

```text
User:
My soil organic carbon is 0.3%.

System:
What is the approximate annual rainfall?

User:
Around 500 mm.

System:
What is the current land use?

User:
Monoculture wheat.
```

The system retains previously supplied information and progressively builds the environmental state.

### Memory architecture

```text
User Message
     ↓
Environmental Values
     ↓
ConversationMemory
     ↓
EnvironmentalState
     +
Conversation History
     ↓
Reasoning
```

### Current scope

Memory is currently **session-level** and is maintained in application state.

It is not a persistent user database.

The challenge requires multi-turn conversation, context awareness and memory handling.

---

# ❓ Clarification System

When required environmental information is missing, the system does not immediately generate a generic recommendation.

Instead, it asks a targeted clarification question.

For example:

```text
User:
Biodiversity is declining on my land.

System:
What is the soil organic carbon (%)?
```

The current analysis requires key environmental information including:

```text
organic_carbon
rainfall_mm
land_use
```

Additional environmental variables can be supplied when available.

---

# 🧩 Environmental State Schema

Environmental information is represented using a validated Pydantic model.

```python
EnvironmentalState(
    ph=None,
    organic_carbon=None,
    moisture=None,
    rainfall_mm=None,
    temperature_c=None,
    land_use=None,
    crop=None,
    species_richness=None,
    habitat_diversity=None,
    pollution=None,
    deforestation=None
)
```

### Environmental dimensions

| Category     | Variables                           |
| ------------ | ----------------------------------- |
| Soil         | pH, organic carbon, moisture        |
| Climate      | rainfall, temperature               |
| Land         | land use, crop                      |
| Biodiversity | species richness, habitat diversity |
| Human impact | pollution, deforestation            |

The challenge specifies these environmental dimensions as part of the knowledge-system requirements.

---

# 🗂️ Structured Knowledge Schema

The project uses structured JSON files to represent environmental relationships and interventions.

## `data/relationships.json`

Stores relationships between environmental variables.

Example:

```json
{
  "id": "REL-001",
  "from": ["organic_carbon", "rainfall_mm"],
  "to": ["moisture"],
  "relationship": "Low soil organic carbon combined with limited rainfall can reduce soil water resilience.",
  "evidence": ["FAO-SOIL-001"]
}
```

## `data/interventions.json`

Stores intervention information.

Example:

```json
{
  "id": "INT-001",
  "action": "Cover crops",
  "targets": ["organic_carbon", "moisture"],
  "mechanism": "Adds vegetation cover and organic matter while supporting soil structure.",
  "horizon": "6–24 months",
  "evidence": ["FAO-SOIL-001"]
}
```

---

# 🌿 Recommendation Engine

Recommendations are generated from detected environmental risks.

Each recommendation is structured around:

```text
Recommendation
      ↓
Why it works
      ↓
Impacted metrics
      ↓
Expected time horizon
      ↓
Scientific evidence
```

Example:

```text
Recommended intervention:
Introduce cover crops and suitable agroforestry practices.

Why it works:
Vegetative cover and organic inputs can improve soil structure,
water retention and soil biological activity.

Impacted metrics:
organic_carbon
moisture
rainfall_mm

Expected time horizon:
6–24 months
```

The challenge requires recommendations to explain what to do, why it works scientifically, which metric is affected, and provide a study/report/model reference.

---

# 🔬 Reasoning Example

### Input

```text
Soil organic carbon: 0.3%
Annual rainfall: 500 mm
Land use: monoculture wheat
Species richness: 12
```

### Reasoning

```text
SOC = 0.3%
      +
Rainfall = 500 mm
      ↓
Soil-water stress

Monoculture
      +
Species richness = 12
      ↓
Habitat diversity loss
```

### Possible interventions

```text
Cover crops
       +
Agroforestry
       +
Intercropping
```

The system then retrieves relevant scientific material before producing the final explanation.

---

# 📊 Output Structure

The application is designed to produce structured environmental recommendations containing:

```text
Recommendation
Impacted metrics
Scientific mechanism
Expected time horizon
Supporting evidence
```

A confidence score is not currently required by the implementation because the challenge describes confidence as optional.

---

# 🛠️ Technology Stack

| Layer                | Technology                  |
| -------------------- | --------------------------- |
| Language             | Python 3.11                 |
| Interface            | Streamlit                   |
| Data validation      | Pydantic                    |
| LLM / synthesis      | OpenAI API                  |
| Embeddings           | Sentence Transformers       |
| Vector database      | FAISS                       |
| Scientific retrieval | OpenAI web search           |
| Memory               | Custom `ConversationMemory` |
| Structured knowledge | JSON                        |
| Testing              | Pytest                      |
| Version control      | Git / GitHub                |
| CI                   | GitHub Actions              |
| Containerization     | Docker                      |

---

# 📁 Project Structure

```text
EcoReason-AI/
│
├── app.py
├── models.py
├── conversation.py
├── reasoning.py
├── rag.py
├── rag_faiss.py
├── recommender.py
├── build_index.py
│
├── data/
│   ├── relationships.json
│   └── interventions.json
│
├── knowledge/
│   ├── agroforestry.txt
│   ├── ipcc_land.txt
│   ├── soil_organic_matter.txt
│   ├── soil_water.txt
│   └── index/
│       ├── knowledge.faiss
│       └── metadata.json
│
├── tests/
│   └── test_reasoning.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Local Setup

## 1. Clone

```bash
git clone https://github.com/shitizkumar/EcoReason-AI.git
cd EcoReason-AI
```

## 2. Create Python environment

Windows:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## 4. Configure API key

Create `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Never commit `.env`.

## 5. Build the FAISS index

```powershell
python build_index.py
```

## 6. Run the application

```powershell
python -m streamlit run app.py
```

The application will be available on the local Streamlit server.

---

# 🧪 Testing

Run the automated tests:

```powershell
python -m pytest -q
```

Current core reasoning tests cover:

* Multi-metric soil/water risk detection
* Normal environmental conditions
* Deforestation/habitat fragmentation reasoning

Example result:

```text
3 passed
```

---

# 🔄 CI/CD

EcoReason AI uses GitHub Actions for automated testing.

The current CI pipeline:

```text
Git Push / Pull Request
          │
          ▼
┌──────────────────────┐
│ Checkout Repository  │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Python 3.11          │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Install Test         │
│ Dependencies         │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Verify Environment   │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Run Pytest           │
└──────────┬───────────┘
           ▼
       ✅ CI Pass
```

The workflow is defined in:

```text
.github/workflows/ci.yml
```

The CI pipeline currently runs successfully on the `main` branch.

---

# 🐳 Docker

The application is containerized using Docker.

### Build

```bash
docker build -t ecoreason-ai .
```

### Run

```bash
docker run --env-file .env -p 8501:8501 ecoreason-ai
```

The application listens on:

```text
http://localhost:8501
```

The Docker image provides a reproducible runtime environment independent of the local Python installation.

### Docker exclusions

The `.dockerignore` prevents sensitive and unnecessary files from entering the image:

```text
.env
.venv/
.git/
.github/
__pycache__/
.pytest_cache/
```

---

# 🔐 Security

API credentials are supplied through environment variables.

Sensitive files are excluded from Git:

```text
.env
.venv/
__pycache__/
*.pyc
```

No API key should be committed to the repository.

---

# 🎯 Challenge Alignment

| Challenge Area              | EcoReason AI Implementation                                |
| --------------------------- | ---------------------------------------------------------- |
| Knowledge system            | FAISS + scientific documents + structured JSON             |
| Soil health                 | SOC, moisture, pH state representation                     |
| Land use                    | Structured environmental state                             |
| Biodiversity                | Species richness, habitat diversity                        |
| Climate                     | Rainfall, temperature                                      |
| Human impact                | Pollution, deforestation                                   |
| Conversational intelligence | Session-level `ConversationMemory`                         |
| Clarification               | Missing-field questioning                                  |
| Multi-metric reasoning      | Soil ↔ water, land ↔ biodiversity, deforestation ↔ habitat |
| Scientific grounding        | Local scientific retrieval + web retrieval                 |
| Recommendations             | Structured intervention engine                             |
| Impacted metrics            | Included in recommendations                                |
| Time horizon                | Included in recommendations                                |
| Testing                     | Pytest                                                     |
| CI/CD                       | GitHub Actions                                             |
| Containerization            | Docker                                                     |

The project is designed around the challenge's requirement for a knowledge-grounded reasoning system rather than a generic LLM-only chatbot.

---

# 🚧 Current Scope & Future Improvements

Potential extensions include:

* Persistent conversational memory
* Structured JSON input interface
* Geographic coordinates and spatial reasoning
* Larger scientific document corpus
* Additional biodiversity datasets
* Time-series environmental analysis
* More detailed evidence-to-recommendation mapping
* Confidence estimation
* Production vector database
* Cloud deployment
* Automated Docker image publishing

These are extensions beyond the current core implementation.

---

# 👨‍💻 Author

**Shitiz Kumar**

AI Engineer focused on:

* Artificial Intelligence
* Machine Learning
* Generative AI
* Retrieval-Augmented Generation
* AI Engineering
* Environmental AI

GitHub:

https://github.com/shitizkumar

---

# 📄 License

This project was developed as an engineering challenge project for demonstration and evaluation purposes.
