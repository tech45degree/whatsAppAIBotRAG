from dotenv import load_dotenv
from langchain_community.llms import Ollama

load_dotenv()



class AIResponse:
    def __init__(self, userResponse, source_knowledge):
        self.userResponse = userResponse
        self.source_knowledge = source_knowledge

    def generatePrompt(self):
        try:
            aug_prompt = f"""
            You are a chatbot that is trained to answer for user response.
            You are given the following context:
            {self.source_knowledge}
            You are asked to generate short and accurate answer to the following question using above context.
            question:
            {self.userResponse}
            strictly do not hallucinate. only use the above context to generate an answer.
            """
            return aug_prompt

        except Exception as e:
            raise e

    def generateResponse(self):
        try:
            prompt = self.generatePrompt()
            llm = Ollama(model='orca-mini')
            model_response = llm.invoke(prompt)
            return model_response

        except Exception as e:
            raise e