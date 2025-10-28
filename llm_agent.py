from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

llm = ChatOpenAI(model="gpt-4o-mini")

def draft_purchase_order(item):
    prompt = f"""
    Draft a professional purchase order for the following item:
    SKU: {item['sku']}
    Quantity: {item['reorder_qty']}
    Supplier: {item['supplier']}
    Ship to: {item['ship_address']}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content
