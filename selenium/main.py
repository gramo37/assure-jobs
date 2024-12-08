from fastapi import FastAPI
from pydantic import BaseModel
from utils.driver import automate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    url: str
    path: str
    cookie_string: str

@app.get("/")
async def ping():
    return {"message": "Hello World!"}

@app.post("/automate/")
async def automate_route(item: Item):
    url = item.url
    path = item.path
    cookie_string = item.cookie_string
    try:
        page_html = automate(url, path, cookie_string)
        return {"page_html": page_html}
    except any as e:
        print(e)
        return {"error": "Something went wrong"}
