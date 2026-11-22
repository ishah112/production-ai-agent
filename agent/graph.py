from dotenv import load_dotenv                      # reads local .env file and puts its values into environment variables
from langchain_openai import ChatOpenAI             # a client object for talking to OpenAI's chat models
from langchain_core.messages import HumanMessage    # a message from the user
from langgraph.graph import MessagesState, StateGraph, START, END   
from langgraph.checkpoint.redis import RedisSaver

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# temperature=0 means "be as deterministic as possible". the same question gets the same grounded answer

import json
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from app.db.orders import fetch_order_status as db_fetch_order, process_refund as db_process_refund

@tool
def fetch_order_status(order_id: int) -> str:
    """Look up an order by its ID and return its item, amount, and status.
    Use this when a customer asks where their order is or what its status is."""
    result = db_fetch_order(order_id)
    if result is None:
        return "Order not found."
    return json.dumps(result, default=str)

@tool
def process_refund(order_id: int) -> str:
    """Process a full refund for an order.
    ONLY call this when the customer explicitly asks for a refund.
    Do NOT call it if they only ask about status, mention a problem,
    or say they are unhappy — ask them to confirm first."""
    result = db_process_refund(order_id)
    if result is None:
        return "Order Not found"
    
    return json.dumps(result, default=str)

llm_with_tools = llm.bind_tools([fetch_order_status, process_refund])

def call_model(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph = StateGraph(MessagesState)
graph.add_node("call_model", call_model)
graph.add_node("tools", ToolNode([fetch_order_status, process_refund]))
graph.add_edge(START, "call_model")
# If yes → returns tools -> it calls fetch_order_status
# If no -> return END
graph.add_conditional_edges("call_model", tools_condition)
graph.add_edge("tools", "call_model")

def get_text(message):
    if isinstance(message.content, str):
        return message.content
    return " ".join(
        block.get("text", "")
        for block in message.content
        if block.get("type") == "text"
    )

def build_agent():
    checkpointer_ctx = RedisSaver.from_conn_string("redis://localhost:6379")
    checkpointer = checkpointer_ctx.__enter__()
    checkpointer.setup()
    agent = graph.compile(checkpointer=checkpointer)
    return agent, checkpointer_ctx


if __name__ == "__main__":
    agent, checkpointer_ctx = build_agent()
    config = {"configurable": {"thread_id": "test-5"}}
    try:
        result = agent.invoke(
            {"messages": [HumanMessage(content="Refund my order 3")]},
            config,
        )
        print(get_text(result["messages"][-1]))
    finally:
        checkpointer_ctx.__exit__(None, None, None)
