from dotenv import load_dotenv                      # reads local .env file and puts its values into environment variables
from langchain_openai import ChatOpenAI             # a client object for talking to OpenAI's chat models
from langchain_core.messages import HumanMessage    # a message from the user
from langgraph.graph import MessagesState, StateGraph, START, END   
from langgraph.checkpoint.redis import RedisSaver

load_dotenv()

llm = ChatOpenAI(model="gpt-5-pro", temperature=0)
# temperature=0 means "be as deterministic as possible". the same question gets the same grounded answer

import json
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from app.db.orders import fetch_order_status as db_fetch_order_status

@tool
def fetch_order_status(order_id: int) -> str:
    """Look up an order by its ID and return its item, amount, and status.
    Use this when a customer asks where their order is or what its status is."""
    result = db_fetch_order_status(order_id)
    if result is None:
        return "Order not found."
    return json.dumps(result, default=str)

llm_with_tools = llm.bind_tools([fetch_order_status])

def call_model(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph = StateGraph(MessagesState)
graph.add_node("call_model", call_model)
graph.add_node("tools", ToolNode([fetch_order_status]))
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



if __name__ == "__main__":
    with RedisSaver.from_conn_string("redis://localhost:6379") as checkpointer:
        checkpointer.setup()
        agent = graph.compile(checkpointer=checkpointer)

        config = {"configurable": {"thread_id": "test-3"}}
        result = agent.invoke(
            {"messages": [HumanMessage(content="Where is my order 1?")]},
            config,
        )
        print(get_text(result["messages"][-1]))


    

