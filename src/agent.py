from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from src.tools import search_company, search_competitors, get_mistral_llm
from src.prompts import (RESEARCH_PROMPT, COMPETITORS_PROMPT,
                          ANALYSIS_PROMPT, REPORT_PROMPT)

# ── State ─────────────────────────────────────────────────
class AgentState(TypedDict):
    company: str
    context: str
    research: str
    summary: str
    competitors: List[str]
    analyses: str
    report: str

# ── Nodes ─────────────────────────────────────────────────
def research_company_node(state: AgentState) -> AgentState:
    print(f"Recherche d'informations sur {state['company']}...")
    research = search_company(state["company"], state["context"])
    return {**state, "research": research}


def summarize_company_node(state: AgentState) -> AgentState:
    print("Analyse de l'entreprise...")
    llm = get_mistral_llm()
    prompt = RESEARCH_PROMPT.format(
        company=state["company"],
        research=state["research"]
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {**state, "summary": response.content}


def find_competitors_node(state: AgentState) -> AgentState:
    print("Identification des concurrents...")
    llm = get_mistral_llm()
    prompt = COMPETITORS_PROMPT.format(
        company=state["company"],
        summary=state["summary"]
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    competitors = [c.strip() for c in response.content.split(",")]
    return {**state, "competitors": competitors[:3]}


def analyze_competitors_node(state: AgentState) -> AgentState:
    print(f"Analyse des concurrents: {state['competitors']}...")
    llm = get_mistral_llm()
    all_analyses = []

    for competitor in state["competitors"]:
        competitor_research = search_competitors(
            state["company"], competitor
        )
        prompt = ANALYSIS_PROMPT.format(
            company=state["company"],
            summary=state["summary"],
            competitor=competitor,
            competitor_research=competitor_research
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        all_analyses.append(f"### {competitor}\n{response.content}")

    return {**state, "analyses": "\n\n".join(all_analyses)}


def generate_report_node(state: AgentState) -> AgentState:
    print("Génération du rapport final...")
    llm = get_mistral_llm()
    prompt = REPORT_PROMPT.format(
        company=state["company"],
        summary=state["summary"],
        analyses=state["analyses"]
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {**state, "report": response.content}


# ── Graph ─────────────────────────────────────────────────
def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("research", research_company_node)
    graph.add_node("summarize", summarize_company_node)
    graph.add_node("find_competitors", find_competitors_node)
    graph.add_node("analyze", analyze_competitors_node)
    graph.add_node("report", generate_report_node)

    graph.set_entry_point("research")
    graph.add_edge("research", "summarize")
    graph.add_edge("summarize", "find_competitors")
    graph.add_edge("find_competitors", "analyze")
    graph.add_edge("analyze", "report")
    graph.add_edge("report", END)

    return graph.compile()