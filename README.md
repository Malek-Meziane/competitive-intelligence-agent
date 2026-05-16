# Competitive Intelligence Agent

An autonomous AI agent that automatically generates competitive intelligence 
reports for any company using LangGraph, Mistral AI and Tavily.

## What it does

Enter any company name → the agent:
1. Searches real-time web information (Tavily)
2. Summarises the company positioning (Mistral AI)
3. Identifies 3 direct competitors (Mistral AI)
4. Researches and compares each competitor (Tavily + Mistral)
5. Generates a structured strategic report (Mistral AI)

## Tech stack
LangGraph     → multi-step agent orchestration
Mistral AI    → analysis and report generation (European LLM)
Tavily        → real-time web search
Streamlit     → clean corporate interface
Python        → end-to-end pipeline

## Setup

```bash
git clone https://github.com/Malek-Meziane/competitive-intelligence-agent.git
cd competitive-intelligence-agent
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

Create a `.env` file:
MISTRAL_API_KEY=your_key
TAVILY_API_KEY=your_key

Run:
```bash
streamlit run app.py
```

## Why Mistral AI

Mistral is a French LLM — relevant for European data sovereignty constraints 
that many enterprise clients face. A deliberate choice over OpenAI for this project.

## What I'd add next
- PDF export of the generated report
- Historical comparison (track competitor evolution over time)
- Multi-language support
- Slack/email delivery of reports
