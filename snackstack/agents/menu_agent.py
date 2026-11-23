"""
agents/menu_agent.py — Menu Discovery Agent.

Uses LangGraph conditional edges instead of a manual tool-calling loop.
- menu_agent_node  → calls the LLM, stores response in menu_messages
- menu_tools_node  → executes tool calls, stores results in menu_messages
- should_continue_menu → conditional edge: tool calls? → tools : → synthesizer
"""

