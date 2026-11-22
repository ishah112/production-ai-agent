from fastapi import APIRouter, Request
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from agent.graph import get_text

router = APIRouter()

class ChatRequest(BaseModel):
    conversation_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
def chat(request: Request, body: ChatRequest):
    config = {"configurable": {"thread_id": body.conversation_id}}

    result = request.app.state.agent.invoke(
        {"messages": [HumanMessage(content=body.message)]},
        config,
    )

    return {"reply": get_text(result["messages"][-1])}
