import streamlit as st

from conversation import ConversationMemory
from reasoning import assess
from recommender import recommend
from rag import ScientificRetriever


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="EcoReason AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(circle at top left, #123c2b 0%, transparent 35%),
            radial-gradient(circle at bottom right, #0d3326 0%, transparent 35%),
            #06120e;
        color: #ecf8f1;
    }

    [data-testid="stSidebar"] {
        background: #071812;
        border-right: 1px solid #1d4435;
    }

    .hero {
        padding: 12px 0 18px 0;
    }

    .hero-title {
        font-size: 2.7rem;
        font-weight: 800;
        color: #e3ffed;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        color: #8fb5a3;
        font-size: 1rem;
        margin-top: -4px;
    }

    .state-card {
        background: rgba(14, 40, 29, 0.88);
        border: 1px solid #28523f;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 12px;
    }

    .state-value {
        font-size: 1.35rem;
        font-weight: 750;
        color: #d8ffe6;
    }

    .state-label {
        color: #82a996;
        font-size: 0.78rem;
        margin-top: 3px;
    }

    .waiting-card {
        background: rgba(18, 45, 34, 0.75);
        border: 1px solid #28523f;
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
    }

    .risk-card {
        background: rgba(72, 43, 28, 0.50);
        border: 1px solid #87583f;
        border-radius: 15px;
        padding: 18px;
        margin: 12px 0;
    }

    .recommendation-card {
        background: linear-gradient(
            135deg,
            rgba(18, 69, 49, 0.95),
            rgba(11, 42, 32, 0.95)
        );
        border: 1px solid #39805f;
        border-radius: 17px;
        padding: 20px;
        margin: 14px 0;
    }

    .evidence-card {
        background: rgba(12, 32, 24, 0.85);
        border: 1px solid #234b3a;
        border-radius: 14px;
        padding: 16px;
        margin: 10px 0;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 750;
        color: #dfffea;
        margin: 20px 0 10px 0;
    }

    .chat-user {
        background: #173d2d;
        border: 1px solid #285b43;
        border-radius: 16px 16px 4px 16px;
        padding: 14px 17px;
        margin: 10px 0 10px 15%;
    }

    .chat-ai {
        background: #10291f;
        border: 1px solid #28523f;
        border-radius: 16px 16px 16px 4px;
        padding: 15px 18px;
        margin: 10px 15% 10px 0;
    }

    .chat-name {
        font-size: 0.78rem;
        font-weight: 700;
        color: #8fc9a8;
        margin-bottom: 5px;
    }

    .small-muted {
        color: #769788;
        font-size: 0.82rem;
    }

    .footer {
        text-align: center;
        color: #567969;
        padding: 35px 0 15px 0;
    }

    div.stButton > button {
        border-radius: 11px;
        min-height: 44px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "retriever" not in st.session_state:
    st.session_state.retriever = None


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🌿 EcoReason AI</div>
        <div class="hero-subtitle">
            Biodiversity Intelligence Engine · Conversational environmental reasoning
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown("## 🌍 Environmental State")

    state = st.session_state.memory.state

    def display_state(label, value, unit=""):
        if value is None:
            shown = "—"
        else:
            shown = f"{value}{unit}"

        st.markdown(
            f"""
            <div class="state-card">
                <div class="state-value">{shown}</div>
                <div class="state-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    display_state(
        "Soil organic carbon",
        state.organic_carbon,
        "%" if state.organic_carbon is not None else "",
    )

    display_state(
        "Annual rainfall",
        state.rainfall_mm,
        " mm" if state.rainfall_mm is not None else "",
    )

    display_state(
        "Land use",
        state.land_use.title() if state.land_use else None,
    )

    display_state(
        "Species richness",
        state.species_richness,
    )

    display_state(
        "Temperature",
        state.temperature_c,
        " °C" if state.temperature_c is not None else "",
    )

    st.markdown("---")

    missing = st.session_state.memory.missing()

    if missing:
        st.markdown("### 🔎 Information needed")

        for field in missing:
            st.markdown(
                f'<div class="small-muted">• {field.replace("_", " ").title()}</div>',
                unsafe_allow_html=True,
            )

    else:
        st.success("Environmental profile is ready for analysis.")

    st.markdown("---")

    if st.button("↻ Start New Conversation", use_container_width=True):

        st.session_state.memory = ConversationMemory()
        st.session_state.messages = []
        st.session_state.analysis = None
        st.rerun()


# ---------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">💬 Environmental Conversation</div>',
    unsafe_allow_html=True,
)


for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="chat-user">
                <div class="chat-name">👤 You</div>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            f"""
            <div class="chat-ai">
                <div class="chat-name">🌿 EcoReason AI</div>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

user_input = st.chat_input(
    "Describe your ecosystem or provide an environmental measurement..."
)


# ---------------------------------------------------------
# PROCESS MESSAGE
# ---------------------------------------------------------

if user_input:

    text = user_input.strip()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": text,
        }
    )

    lower = text.lower()

    # -----------------------------------------------------
    # Lightweight environmental value extraction
    # -----------------------------------------------------

    import re

    extracted = {}

    # Soil organic carbon
    soc_match = re.search(
        r"(?:organic carbon|soil carbon|soc)[^\d]*(\d+(?:\.\d+)?)",
        lower,
    )

    if soc_match:
        extracted["organic_carbon"] = float(soc_match.group(1))

    # Rainfall
    rainfall_match = re.search(
        r"(?:rainfall|annual rainfall|precipitation)[^\d]*(\d+(?:\.\d+)?)",
        lower,
    )

    if rainfall_match:
        extracted["rainfall_mm"] = float(rainfall_match.group(1))

    # Species richness
    species_match = re.search(
        r"(?:species richness|species)[^\d]*(\d+)",
        lower,
    )

    if species_match:
        extracted["species_richness"] = int(species_match.group(1))

    # Temperature
    temperature_match = re.search(
        r"(?:temperature|temp)[^\d]*(\d+(?:\.\d+)?)",
        lower,
    )

    if temperature_match:
        extracted["temperature_c"] = float(temperature_match.group(1))

    # Land use
    land_use_options = [
        "monoculture",
        "mixed cropping",
        "agroforestry",
        "grassland",
        "forest",
    ]

    for option in land_use_options:
        if option in lower:
            extracted["land_use"] = option
            break

    # -----------------------------------------------------
    # Update environmental memory
    # -----------------------------------------------------

    if extracted:
        st.session_state.memory.update(**extracted)


    # -----------------------------------------------------
    # Check clarification
    # -----------------------------------------------------

    clarification = st.session_state.memory.clarification()

    if clarification:

        ai_message = clarification

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": ai_message,
            }
        )

        st.rerun()


    # -----------------------------------------------------
    # Full analysis
    # -----------------------------------------------------

    with st.spinner(
        "🌿 Connecting environmental variables and scientific evidence..."
    ):

        memory = st.session_state.memory

        risks = assess(memory.state)

        evidence = []

        # Create retriever only when analysis is actually needed
        if st.session_state.retriever is None:
            st.session_state.retriever = ScientificRetriever()

        retriever = st.session_state.retriever

        for risk in risks:

            try:

                result = retriever.retrieve_for_risk(risk)

                evidence.append(
                    {
                        "risk": risk["id"],
                        "research": result["research"],
                        "vector_results": result["vector_results"],
                        "sources": [
                            {
                                "title": source.title,
                                "url": source.url,
                            }
                            for source in result["sources"]
                        ],
                    }
                )

            except Exception as error:

                evidence.append(
                    {
                        "risk": risk["id"],
                        "research": (
                            "Online scientific retrieval is temporarily "
                            f"unavailable: {error}"
                        ),
                        "vector_results": [],
                        "sources": [],
                    }
                )

        recommendations = recommend(
            risks,
            evidence,
        )

        st.session_state.analysis = {
            "risks": risks,
            "recommendations": recommendations,
            "evidence": evidence,
        }


    # -----------------------------------------------------
    # Generate conversational response
    # -----------------------------------------------------

    if not risks:

        ai_message = (
            "I have enough environmental information, but I did not detect "
            "one of the ecological risk patterns currently defined in my "
            "reasoning system. You can provide additional information such "
            "as soil moisture, temperature, deforestation, or biodiversity "
            "indicators for a broader assessment."
        )

    else:

        risk_names = [
            risk["id"].replace("_", " ").title()
            for risk in risks
        ]

        recommendation_names = [
            recommendation["action"]
            for recommendation in recommendations
        ]

        ai_message = (
            f"I analyzed the relationships between your environmental "
            f"variables and detected **{len(risks)} connected ecological "
            f"risk pattern(s)**: {', '.join(risk_names)}.\n\n"
            f"Recommended actions include: "
            f"{'; '.join(recommendation_names)}.\n\n"
            "I have also retrieved supporting scientific knowledge "
            "from the local biodiversity knowledge base."
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_message,
        }
    )

    st.rerun()


# ---------------------------------------------------------
# ANALYSIS RESULTS
# ---------------------------------------------------------

analysis = st.session_state.analysis

if analysis:

    risks = analysis["risks"]
    recommendations = analysis["recommendations"]
    evidence = analysis["evidence"]


    # -----------------------------------------------------
    # Risks
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">⚠️ Detected Ecological Risks</div>',
        unsafe_allow_html=True,
    )

    if not risks:

        st.info("No predefined ecological risk pattern was detected.")

    else:

        for risk in risks:

            st.markdown(
                f"""
                <div class="risk-card">
                    <h4>⚠️ {risk["id"].replace("_", " ").title()}</h4>
                    <p>{risk["reason"]}</p>
                    <div class="small-muted">
                        Connected metrics:
                        {", ".join(risk["metrics"])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


   # ---------------------------------------------------------
# ANALYSIS RESULTS
# ---------------------------------------------------------

analysis = st.session_state.analysis

if analysis:

    risks = analysis["risks"]
    recommendations = analysis["recommendations"]
    evidence = analysis["evidence"]

    # -----------------------------------------------------
    # Risks
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">⚠️ Detected Ecological Risks</div>',
        unsafe_allow_html=True,
    )

    if not risks:

        st.info("No predefined ecological risk pattern was detected.")

    else:

        for risk in risks:

            st.markdown(
                f"""
                <div class="risk-card">
                    <h4>⚠️ {risk["id"].replace("_", " ").title()}</h4>
                    <p>{risk["reason"]}</p>
                    <div class="small-muted">
                        Connected metrics:
                        {", ".join(risk["metrics"])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # -----------------------------------------------------
    # Recommendations
    # -----------------------------------------------------

    if recommendations:

        st.markdown(
            '<div class="section-title">🌱 Recommended Interventions</div>',
            unsafe_allow_html=True,
        )

        for recommendation in recommendations:

            st.markdown(
                f"### 🌿 {recommendation['action']}"
            )

            st.markdown(
                f"**Why it works:**  \n"
                f"{recommendation['mechanism']}"
            )

            st.markdown(
                f"**Impacted metrics:**  \n"
                f"{', '.join(recommendation['metrics'])}"
            )

            st.markdown(
                f"**Expected time horizon:**  \n"
                f"{recommendation['horizon']}"
            )

            st.divider()

    # -----------------------------------------------------
    # Scientific Evidence
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🔬 Scientific Evidence</div>',
        unsafe_allow_html=True,
    )

    for item in evidence:

        with st.expander(
            f'📚 {item["risk"].replace("_", " ").title()} — Retrieved Evidence'
        ):

            vector_results = item.get("vector_results", [])

            if vector_results:

                st.markdown("### 🧠 Local Knowledge Base")

                for vector in vector_results:

                    st.markdown(
                        f"""
                        <div class="evidence-card">

                            <strong>{vector["id"]}</strong>

                            <br>

                            <span class="small-muted">
                                Semantic similarity: {vector["score"]}
                            </span>

                            <p>
                                {vector["text"][:900]}
                            </p>

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            else:

                st.info(
                    "No local FAISS evidence was returned for this analysis."
                )

            sources = item.get("sources", [])

            if sources:

                st.markdown("### 🌐 Scientific Sources")

                for source in sources:

                    st.markdown(
                        f'- [{source["title"]}]({source["url"]})'
                    )

            st.markdown("### 📝 Research Synthesis")

            st.write(
                item.get(
                    "research",
                    "No research synthesis available.",
                )
            )


# ---------------------------------------------------------
# SYSTEM PIPELINE
# ---------------------------------------------------------

with st.expander("⚙️ How EcoReason AI Works"):

    st.code(
        """
User
  ↓
Conversational Input
  ↓
Environmental State
  ↓
Conversation Memory
  ↓
Multi-Metric Reasoning
  ↓
Ecological Risk Detection
  ↓
FAISS Knowledge Retrieval
  ↓
Scientific Evidence
  ↓
Evidence-Backed Recommendation
        """,
        language="text",
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        🌿 EcoReason AI · Biodiversity Intelligence Engine<br>
        Soil · Water · Land Use · Climate · Biodiversity
    </div>
    """,
    unsafe_allow_html=True,
)