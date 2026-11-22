"""
agents/orchestrator.py — Classifies the user query and dispatches
to the correct specialist agent(s) using LangGraph's Send() API.
"""
from typing import Literal
from pydantic import BaseModel, Field
from langgraph.types import Command

from snackstack.config import llm
from snackstack.logger import setup_logger
from snackstack.state import StackState


logger=setup_logger('snackstack:orchestrator')

class OrchestratorDecision(BaseModel):
    """The orchestrator's routing decision."""
    reasoning:str = Field(description="Brief explanation of why this agent chosen")
    agents: list[Literal["menu_agent"]] = Field(
        description="List of agents to dispatch. Always at least one.",
        min_length=1
    )

routing_llm = llm.with_structured_output(OrchestratorDecision)

def orchestrator_node(state: StackState)->Command[Literal["menu_agent_node"]]:
    """Classify the query and fan out to menu_agent or end."""
    

