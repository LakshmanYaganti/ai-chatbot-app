from fastapi import APIRouter
from app.models.chat_model import ChatRequest, ChatResponse
from app.services.rag_service import retrieve_context
from app.services.llm_service import generate_response

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):

    context = retrieve_context(request.message)

    response = generate_response(request.message, context)

    return ChatResponse(response=response)
