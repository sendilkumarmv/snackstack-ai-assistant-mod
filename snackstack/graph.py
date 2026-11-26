"""
graph.py — Build and compile the SnackStack LangGraph StateGraph.

Graph topology (conditional edges shown as dashed):
    START → orchestrator ─ ─ ─ ┬─ menu_agent_node ─ ─ ─ menu_tools_node ─┐
                                │       ↑________________________ ________┘
                                │       └─ ─ ─ ─ → synthesizer_node → END
                                │
                                └─ order_agent_node ─ ─ ─ order_tools_node ─┐
                                        ↑___________________________________┘
                                        └─ ─ ─ ─ → synthesizer_node → END

    Orchestrator dispatches agents conditionally via Send().
    Each agent uses a conditional edge to route to its tools node
    or directly to the synthesizer.

HITL:
    order_agent_node uses interrupt() to pause execution when the user
    query is missing an order ID / tracking ID / email.  The caller
    resumes with Command(resume=<user_input>).
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from snackstack.logger import setup_logger
from snackstack.state import StackState
from snackstack.agents import (
    orchestrator_node,
    menu_agent_node,
    menu_tools_node,
    should_continue_menu,
    synthesizer_node
)


logger = setup_logger("SnackStack.graph")

def build_graph():
    """Construct, compile, and return the SnackStack graph."""

    graph_builder = StateGraph(StackState)

    # Add all nodes
    graph_builder.add_node("orchestrator", orchestrator_node)
    graph_builder.add_node("menu_agent_node", menu_agent_node)
    graph_builder.add_node("menu_tools_node", menu_tools_node)
    graph_builder.add_node("synthesizer_node", synthesizer_node)

    # Add edges
    graph_builder.add_edge(START, "orchestrator")

    graph_builder.add_conditional_edges(
        "menu_agent_node",
        should_continue_menu,
        {"menu_tools_node": "menu_tools_node", "synthesizer_node": "synthesizer_node"}
    )
    graph_builder.add_edge("menu_tools_node", "menu_agent_node")

    graph_builder.add_edge("synthesizer_node", END)


    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)

    logger.info("SnackStack graph compiled")
    return graph