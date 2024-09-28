from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import YoutubeLoader
from pinecone import Pinecone
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from src import langfunc
import os

load_dotenv()

pinecone_client = Pinecone()


class vectorDB:
    def __init__(self):
        self.MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.index_name = os.getenv("PINECONE_INDEX_NAME")

    def data_preprocess(self, video_link):
        print(f"Processing {video_link}")
        try:
            loader = YoutubeLoader.from_youtube_url(video_link, add_video_info=True)
            transcription = loader.load()

            text = ''

            if (len(transcription) > 0):
                text = transcription[0].page_content
            else:
                downloadPath = langfunc.download_youtube_video(video_link, "./download")
                if downloadPath is not None:
                    transcription = langfunc.transcribe_video(downloadPath)
                    text = transcription['text']

            language = langfunc.detect_language(text)
            if(language != "en"):
                statsCode, text = langfunc.translate_text(text,"en")



            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,  # Define the size of each chunk
                chunk_overlap=50  # Define the overlap between chunks
            )
            print("=============================")
            print(text)
            # Split the text
            chunks = text_splitter.split_text(text)

            return chunks

        except Exception as e:
            raise e

    def upload_embeddings(self, video_link):
        try:
            # self.init_pinecone()
            docs = self.data_preprocess(video_link)
            index = pinecone_client.Index(self.index_name)
            embeddings = self.MODEL.encode(docs)
            metadata, ids = langfunc.prepare_data(docs, video_link)
            upsert_data = [
                (id, embedding.tolist(), meta)
                for id, embedding, meta in zip(ids, embeddings, metadata)
            ]
            index.upsert(vectors=upsert_data)
            print(index.describe_index_stats())
        except Exception as e:
            raise e

    def handle_query(self, query):
        try:
            index = pinecone_client.Index(self.index_name)
            query_embedding = self.MODEL.encode([query])[0]
            retrived_text = index.query(vector=query_embedding.tolist(), top_k=3, include_metadata=True)
            output = [match['metadata']['text'] for match in retrived_text["matches"]]
            videoUrl = retrived_text['matches'][0]['metadata']['video']
            return "\n".join(output), videoUrl
        except Exception as e:
            raise e
