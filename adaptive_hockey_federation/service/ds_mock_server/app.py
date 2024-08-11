import asyncio
import json

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel


working = False
DELAY = 5 * 60 * 60  # in seconds

app = FastAPI()


@app.get("/")
def main():
    page = "<hml><body><h1>Hockey Game Video Processing</h1></body></html>"
    return HTMLResponse(page)


@app.get("/status")
def status():
    return JSONResponse(content={"status": "OK", "version": 1.0})


@app.get("/version")
def version():
    return {"version": 1.0}


class RequestData(BaseModel):
    """Модель для проверки корректности запроса."""

    game_id: int
    game_link: str
    token: str
    player_ids: list[list[int]]
    player_numbers: list[list[int]]
    team_ids: list[int]


@app.post("/process")
async def process(request_data: RequestData):
    await asyncio.sleep(DELAY)
    with open("test_response.json", "r") as file:
        response = json.load(file)
    return JSONResponse(content=response)


@app.post("/clean")
def clean():
    return JSONResponse(
        content={"Removed": "OK", "Objects": 0, "Size": "0 Mb"},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
