"""
agents/menu_agent.py — Menu Discovery Agent.

Uses LangGraph conditional edges instead of a manual tool-calling loop.
- menu_agent_node  → calls the LLM, stores response in menu_messages
- menu_tools_node  → executes tool calls, stores results in menu_messages
- should_continue_menu → conditional edge: tool calls? → tools : → synthesizer
"""

from snackstack.config import llm
from snackstack.logger import setup_logger
from snackstack.state import StackState
from snackstack.tools.menu_tool import menu_tools_list


logger = setup_logger("snackstack.menu_agent")

# tools
menu_llm = llm.bind_tools(menu_tools_list)



def menu_agent_node(state: StackState):
    """Call the LLM. On first invocation build the initial prompt
    using persisted conversation history; on subsequent invocations
    (after tool results) continue from menu_messages."""





def menu_tool_node():
    pass

def should_continue_menu():
    pass