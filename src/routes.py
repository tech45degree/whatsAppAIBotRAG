from fastapi import APIRouter
from starlette import status

from dto.request_dto import requestDTO
from dto.pinecone_dto import pineconeDTO
from src import RAG_ai, pinecone_db

router = APIRouter()


@router.post("/video/", status_code=status.HTTP_200_OK, tags=["Upload Video"])
async def upload_video(videoRequestDTO: requestDTO):
    pinecone_DB = pinecone_db.vectorDB()
    pinecone_DB.upload_embeddings(videoRequestDTO.video_link)


@router.post("/query", status_code=status.HTTP_200_OK, tags=["Query Video"])
async def RagChat(data: pineconeDTO):
    User_message = data.userMessage
    pinecone_DB = pinecone_db.vectorDB()

    source_knowledge, video_link = pinecone_DB.handle_query(User_message)

    # get model response
    model = RAG_ai.AIResponse(User_message, source_knowledge)
    model_response = model.generateResponse()
    print(model_response)

    response = f"{model_response} video_link = {video_link}"

    return response
