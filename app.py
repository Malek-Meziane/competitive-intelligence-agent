import streamlit as st
from src.agent import build_agent

st.set_page_config(
    page_title="Competitive Intelligence Agent",
    page_icon="🔍",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    /* Header */
    .ci-header {
        background: #0C447C;
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    .ci-header h1 {
        font-size: 28px;
        font-weight: 600;
        margin: 0 0 6px;
        color: white;
    }
    .ci-header p {
        font-size: 14px;
        color: #B5D4F4;
        margin: 0;
    }

    /* Section titles */
    .ci-section-title {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #0C447C;
        border-bottom: 2px solid #0C447C;
        padding-bottom: 6px;
        margin-bottom: 1rem;
        display: inline-block;
    }

    /* Summary box */
    .ci-summary {
        background: #E6F1FB;
        border-left: 3px solid #0C447C;
        padding: 1rem 1.25rem;
        border-radius: 0 8px 8px 0;
        font-size: 14px;
        color: #0C447C;
        line-height: 1.7;
        margin-bottom: 1.5rem;
    }

    /* Competitor cards */
    .ci-competitor-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-bottom: 1.5rem;
    }
    .ci-competitor-card {
        border: 0.5px solid #B5D4F4;
        border-radius: 8px;
        padding: 1rem;
        background: white;
    }
    .ci-competitor-name {
        font-size: 15px;
        font-weight: 600;
        color: #0C447C;
        margin-bottom: 4px;
    }
    .ci-competitor-tag {
        font-size: 11px;
        background: #E6F1FB;
        color: #0C447C;
        padding: 2px 8px;
        border-radius: 99px;
        display: inline-block;
    }

    /* Report sections */
    .ci-report h2 {
        font-size: 16px;
        font-weight: 600;
        color: #0C447C;
        margin: 1.5rem 0 0.5rem;
        padding-bottom: 4px;
        border-bottom: 0.5px solid #B5D4F4;
    }

    /* Badges */
    .ci-badge {
        display: inline-block;
        font-size: 11px;
        padding: 3px 10px;
        border-radius: 99px;
        border: 0.5px solid #B5D4F4;
        color: #185FA5;
        background: #E6F1FB;
        margin-right: 6px;
    }

    /* Metrics */
    [data-testid="metric-container"] {
        background: #F5F9FD;
        border: 0.5px solid #B5D4F4;
        border-radius: 8px;
        padding: 1rem;
    }

    /* Button override */
    .stButton > button {
        background: #0C447C;
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
    }
    .stButton > button:hover {
        background: #185FA5;
        color: white;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────
st.markdown("""
<div class="ci-header">
    <h1>Competitive Intelligence Agent</h1>
    <p>Analyse automatique du positionnement concurrentiel — LangGraph + Mistral AI + Tavily</p>
</div>
""", unsafe_allow_html=True)

# ── Input section ─────────────────────────────────────────
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    company = st.text_input(
        "Entreprise à analyser",
        placeholder="ex: Ekimetrics, McKinsey, Dataiku..."
    )
with col2:
    context = st.text_input(
        "Secteur / contexte",
        value="data AI consulting",
        placeholder="ex: data science consulting France"
    )
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    run_button = st.button(
        "Analyser →",
        disabled=not company,
        use_container_width=True
    )

st.divider()

# ── Idle state ────────────────────────────────────────────
if not run_button:
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0; color: #888;">
        <div style="font-size: 48px; margin-bottom: 1rem;">🔍</div>
        <div style="font-size: 16px; font-weight: 500; margin-bottom: 8px; color: #0C447C;">
            Comment ça marche
        </div>
        <div style="font-size: 14px; max-width: 500px; margin: 0 auto; line-height: 1.8;">
            1. <b>Recherche</b> — Tavily cherche des infos réelles sur l'entreprise<br>
            2. <b>Analyse</b> — Mistral résume le positionnement<br>
            3. <b>Concurrents</b> — Mistral identifie 3 concurrents directs<br>
            4. <b>Comparaison</b> — Tavily + Mistral comparent chaque concurrent<br>
            5. <b>Rapport</b> — Rapport de veille structuré généré automatiquement
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Agent ─────────────────────────────────────────────────
@st.cache_resource
def get_agent():
    return build_agent()

agent = get_agent()

with st.spinner(f"Analyse de {company} en cours — environ 60 secondes..."):
    try:
        result = agent.invoke({
            "company": company,
            "context": context,
            "research": "",
            "summary": "",
            "competitors": [],
            "analyses": "",
            "report": ""
        })
    except Exception as e:
        st.error(f"Erreur : {str(e)}")
        st.stop()

# ── Metrics ───────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Entreprise analysée", result["company"])
col2.metric("Concurrents identifiés", len(result["competitors"]))
col3.metric("Statut", "✅ Complété")

st.divider()

# ── Summary ───────────────────────────────────────────────
st.markdown('<div class="ci-section-title">Résumé de l\'entreprise</div>', unsafe_allow_html=True)
st.markdown(f'<div class="ci-summary">{result["summary"]}</div>', unsafe_allow_html=True)

# ── Competitors ───────────────────────────────────────────
st.markdown('<div class="ci-section-title">Concurrents identifiés</div>', unsafe_allow_html=True)

competitor_cols = st.columns(len(result["competitors"]))
for i, competitor in enumerate(result["competitors"]):
    with competitor_cols[i]:
        st.markdown(f"""
        <div class="ci-competitor-card">
            <div class="ci-competitor-name">{competitor}</div>
            <span class="ci-competitor-tag">concurrent direct</span>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── Full report ───────────────────────────────────────────
st.markdown('<div class="ci-section-title">Rapport de veille complet</div>', unsafe_allow_html=True)
st.markdown(result["report"])

st.divider()

# ── Footer ────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    <span class="ci-badge">LangGraph</span>
    <span class="ci-badge">Mistral AI</span>
    <span class="ci-badge">Tavily</span>
    <span class="ci-badge">Sources web publiques</span>
    """, unsafe_allow_html=True)

with col2:
    st.download_button(
        label="⬇ Télécharger le rapport",
        data=result["report"],
        file_name=f"rapport_veille_{company.lower().replace(' ', '_')}.md",
        mime="text/markdown",
        use_container_width=True
    )