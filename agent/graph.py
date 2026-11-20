from dotenv import load_dotenv                      # reads local .env file and puts its values into environment variables
from langchain_openai import ChatOpenAI             # a client object for talking to OpenAI's chat models
from langchain_core.messages import HumanMessage    # a message from the user
from langgraph.graph import MessagesState, StateGraph, START, END   

load_dotenv()

llm = ChatOpenAI(model="gpt-5-pro", temperature=0)
# temperature=0 means "be as deterministic as possible". the same question gets the same grounded answer

# node - one step in the graph
def call_model(state: MessagesState):   
    # state["messages"] — the conversation so far, as a list of message objects.
    # llm.invoke(...) — sends that whole list to OpenAI and gets back one reply, an AIMessage object
    #  {"messages": [...]} is basically appending LLM response to existing messages
    return {"messages": [llm.invoke(state["messages"])]}
    

graph = StateGraph(MessagesState)   # Creates the graph blueprint and tells it what state shape to use. 
graph.add_node("call_model", call_model) # Registers function in the graph under the name "call_model"
graph.add_edge(START, "call_model") # When the graph starts, go to Node call_model first
graph.add_edge("call_model", END) # After call_model finishes, stop.
# the whole flow is: START → call_model → END. One LLM call. No loop yet 
agent = graph.compile() # Turns the blueprint into a runnable agent.

if __name__ == "__main__":
    result = agent.invoke({"messages": [HumanMessage(content="What is 2 + 2?")]})
    print(result["messages"][-1].content)   # [-1] is the last item, AI's reply
