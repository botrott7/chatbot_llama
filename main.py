import os

from llama_cpp import Llama
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from fastapi import HTTPException
from logs.logi import logger

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIRECTORY, "model/model-q8_01.gguf")
LLM = Llama(model_path=MODEL_PATH, n_ctx=1024)


@app.get('/')
async def main_menu(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logger.error(f'Ошибка: {str(e)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")


class Question(BaseModel):
    question: str


@app.post("/messageAI")
async def message_AI(question: Question):
    try:
        if not question.question:
            raise HTTPException(status_code=400, detail="Question field is empty")
        logger.debug(f'Получен ВОПРОС: {question}')
        output = LLM(question.question, max_tokens=2024, echo=False)
        # result = re.search(r'(?<=bot\s)(.*)', output).group(1)
        result = output["choices"][0]["text"].strip()
        logger.debug(f'Получен ОТВЕТ: {result[:100]}')
        return {"result": result}
    except Exception as e:
        logger.error(f'Ошибка: {str(e)}')
        raise HTTPException(status_code=500, detail="Internal Server Error")
