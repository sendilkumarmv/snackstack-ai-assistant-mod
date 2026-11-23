from snackstack.state import StackState
from snackstack.tools.menu_tool import search_menu_catalog
from snackstack.tools.orders_tool import get_order_status
from snackstack.agents.orchestrator import orchestrator_node

from langchain_core.messages import HumanMessage


def run():
    print("testing started...")
    result = search_menu_catalog.invoke("What are dishes made in cheese?")
    print(result)
    order = get_order_status.invoke("ORD-203")
    print(order)

def test_orchestrator():
    state: StackState = {
        "messages": [HumanMessage(content="Hello")],
        "user_query": "Recommend something vegetarian",
        "route": [],
        "menu_messages": [],
        "order_messages": [],
        "menu_response": "",
        "order_response": "",
        "final_answer": "",
    }
    command = orchestrator_node(state)
    print(command)
    print("Route:", command.update['route'])
    print("Goto:", command.goto)

    state["user_query"] = "How is the weather in Bangalore"
    command = orchestrator_node(state)
    print(command)
    print("Route:", command.update['route'])
    print("Goto:", command.goto)