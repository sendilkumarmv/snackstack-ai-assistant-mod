"""
agents/menu_agent.py — Menu Discovery Agent.

Uses LangGraph conditional edges instead of a manual tool-calling loop.
- menu_agent_node  → calls the LLM, stores response in menu_messages
- menu_tools_node  → executes tool calls, stores results in menu_messages
- should_continue_menu → conditional edge: tool calls? → tools : → synthesizer
"""

from langchain.messages import HumanMessage, SystemMessage

from snackstack.config import llm
from snackstack.logger import setup_logger
from snackstack.state import StackState
from snackstack.tools.menu_tool import menu_tools_list


logger = setup_logger("snackstack.menu_agent")

# tools
menu_llm = llm.bind_tools(menu_tools_list)

# For each tool in menu_tools_llist an entry in dict with 
# key=toolName and value is tool
tool_map = {t.name: t for t in menu_tools_list }


def menu_agent_node(state: StackState):
    """Call the LLM. On first invocation build the initial prompt
    using persisted conversation history; on subsequent invocations
    (after tool results) continue from menu_messages."""

    existing = state.get("menu_messages" or [])

    if not existing:
        # First call - conversation history persisted vi memory saver
        logger.info("Processing menu query...")
        history = state.get("messages", [])[-6:]
        all_message = [
            SystemMessage(),
            *history,
            HumanMessage()
        ]
    else:
        # Subsequent call — tool results already in menu_messages
        logger.info("Menu agent re-invoked after tool results")
        all_message = existing

    response = menu_llm.invoke(all_message)
    all_message = [*all_message, response]

    has_tools = bool(getattr(response, "tool_calls", None))
    logger.info("Tool calls: %s", has_tools)

    update: dict = {"menu_messages": all_message}

    if not has_tools:
        update["menu_response"] = response.content
        update["messages"] = [response]

    return update


def menu_tool_node():
    pass

def should_continue_menu():
    pass