from snackstack.tools.menu_tool import search_menu_catalog
from snackstack.tools.orders_tool import get_order_status


def run():
    print("testing started...")
    result = search_menu_catalog.invoke("What are dishes made in cheese?")
    print(result)
    order = get_order_status.invoke("ORD-203")
    print(order)
    