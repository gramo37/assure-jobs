from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from simpletransformers.question_answering import QuestionAnsweringModel
import time
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

# Load environment variables
MODEL_NAME = os.getenv("MODEL_NAME", "distilbert-base-cased-distilled-squad")  # Default value if not set
MODEL_TYPE = os.getenv("MODEL_TYPE", "distilbert")  # Default value if not set
USE_CUDA = os.getenv("USE_CUDA", "False").lower() == "true"  # Convert string to boolean

print("-------------------------Loading ENV variables-------------------------")
print("Model Name", MODEL_NAME)
print("Model Type", MODEL_TYPE)
print("USE CUDA", USE_CUDA)

class Question(BaseModel):
    question: str
    id: str

class QARequest(BaseModel):
    context: str
    questions: List[Question]

class QAResponse(BaseModel):
    id: str
    question: str
    answer: str

# Load the pre-trained QA model globally
model = QuestionAnsweringModel(
    model_type=MODEL_TYPE, 
    model_name=MODEL_NAME, 
    use_cuda=USE_CUDA  # Set to True if you have a GPU
)

# Sample Request
# {
#     "context": "I am a DevOps Engineer with 7 years of experience in automating infrastructure, managing cloud environments, and ensuring the smooth delivery of software. I specialize in tools like Docker, Kubernetes, Terraform, and Jenkins to set up and manage CI/CD pipelines. I am proficient in scripting with Bash and Python to automate repetitive tasks and manage configurations. I have worked extensively with AWS, Google Cloud, and Azure for deploying and managing cloud resources. My expertise includes monitoring and logging using tools such as Prometheus, Grafana, and ELK stack. I have a strong background in configuring high availability systems and optimizing deployments to reduce downtime. Notable projects include automating the deployment process for a large-scale e-commerce platform, setting up container orchestration for a SaaS product, and implementing a disaster recovery plan for a financial services company. I am passionate about improving processes and advocating for DevOps culture within organizations.",
#     "questions": [
#         {"question": "What tools do you use for container orchestration?", "id": "1"},
#         {"question": "What scripting languages are you proficient in?", "id": "2"},
#         {"question": "Can you describe your experience with CI/CD pipelines?", "id": "3"},
#         {"question": "What are your preferred monitoring tools?", "id": "4"},
#         {"question": "Have you worked on disaster recovery plans? If yes, can you elaborate?", "id": "5"},
#         {"question": "What cloud platforms have you worked with?", "id": "6"},
#         {"question": "How do you ensure high availability in deployments?", "id": "7"},
#         {"question": "What is your approach to reducing downtime?", "id": "8"},
#         {"question": "What are some of the major DevOps projects you have led?", "id": "9"},
#         {"question": "How do you promote DevOps culture within teams?", "id": "10"}
#     ]
# }

@app.post("/predict")
async def predict_qa(request: QARequest):
    try:
        if not request.context.strip():
            raise HTTPException(status_code=400, detail="Context cannot be empty.")
        if not request.questions:
            raise HTTPException(status_code=400, detail="Questions list cannot be empty.")

        qa_input = [{"context": request.context, "qas": [{"question": q.question, "id": q.id} for q in request.questions]}]
        
        print("Model Input:", qa_input)
        
        start_time = time.time()
        
        answers, _ = model.predict(qa_input)
        
        end_time = time.time()
        duration = end_time - start_time

        print("Model Output:", answers)
        result = [{'id': int(item['id']), 'answer': item['answer'][0]} for item in answers]
        
        return {"result": result, "duration": duration}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Value error occurred: {str(e)}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
