from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel

from . import tasks


app = FastAPI()


class RequestData(BaseModel):
    """Модель для проверки корректности запроса."""

    game_id: int
    game_link: str
    token: str
    player_ids: list[list[int]]
    player_numbers: list[list[int]]
    team_ids: list[int]


@app.get("/")
def main():
    """Имитация старта DS сервера."""
    page = "<hml><body><h1>Hockey Game Video Processing</h1></body></html>"
    return HTMLResponse(page)


@app.get("/status")
def status() -> JSONResponse:
    """Проверка статуса DS сервера."""
    return JSONResponse(content={"status": "OK", "version": 1.0})


@app.get("/version")
def version() -> JSONResponse:
    """Запрос версии DS сервера."""
    return JSONResponse(
        content={"version": 1.0},
    )


@app.post("/process")
async def process(request_data: RequestData) -> JSONResponse:
    """Имитация распознавания видео."""
    task = tasks.mock_ds_process.apply_async(
        kwargs={
            "data": dict(request_data),
        },
    )
    response = task.get()
    return JSONResponse(content=response)


@app.post("/clean")
def clean() -> JSONResponse:
    """Имитация очистки DS сервера."""
    return JSONResponse(
        content={"Removed": "OK", "Objects": 0, "Size": "0 Mb"},
    )
