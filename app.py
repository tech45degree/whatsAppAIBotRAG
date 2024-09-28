from src.routes import router as pinecone_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "AI Service",
        "description": "",
    }
]

app = FastAPI(openapi_tags=tags_metadata,
              title="AI Service", description="This service is to integrate  AI services.", version="0.1",
              contact={
                  "name": "Byte Transition"
              })


@app.get("/")
async def root():
    return {"message": "Welcome to the AI Integration System"}


app.include_router(pinecone_router)

origins = [
    "http://localhost",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)