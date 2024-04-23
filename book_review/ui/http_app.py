from fastapi import FastAPI

app = FastAPI()


@app.get("/ping", response_model=str)
def ping() -> str:
    return "pong"
