"""
agents/orchestrator.py — Classifies the user query and dispatches
to the correct specialist agent(s) using LangGraph's Send() API.
"""
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.types import Command,Send
from langgraph.graph import END

from snackstack.config import llm
from snackstack.logger import setup_logger
from snackstack.state import StackState
from snackstack.agents.prompts import ORCHESTRATOR_PROMPT_A 


logger=setup_logger('snackstack:orchestrator')

class OrchestratorDecision(BaseModel):
    """The orchestrator's routing decision."""
    reasoning:str = Field(description="Brief explanation of why this agent chosen")
    agents: list[Literal["menu_agent"]] = Field(
        description="Agent to dispatch. Use an empty list when the query "
            "is not appropriate for SnackStack."
    )

routing_llm = llm.with_structured_output(OrchestratorDecision)

def orchestrator_node(state: StackState)->Command[Literal["menu_agent_node"]]:
    """Classify the query and fan out to menu_agent or end."""

    query = state["user_query"]
    logger.info("Routing query: %s", query[:60])

    # Conversation history is persisted via MemorySaver — just use it
    history = state.get("messages", [])[-6:]

    decision: OrchestratorDecision = routing_llm.invoke([
        SystemMessage(content=ORCHESTRATOR_PROMPT_A),
        *history,
        HumanMessage(content=query),
    ])
    logger.info("Agents: %s | Reason: %s", decision.agents, decision.reasoning)

    if not decision.agents:
        return Command(
            goto=END,
            update={
                "route": [],
                "final_answer": (
                    "I can only help with SnackStack menu and "
                    "food-related questions."
                ),
            },
        )

    # Reset per-turn buffers BEFORE sending to agents
    clean_state = {
        **state,
        "menu_messages": [],
        "order_messages": [],
        "menu_response": "",
        "order_response": "",
    }

    sends = [Send(f"{agent}_node", clean_state) for agent in decision.agents]
    return Command(
        goto=sends, update={
        "route": decision.agents
    })
