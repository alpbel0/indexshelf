from fastapi import FastAPI

app = FastAPI(title="IndexShelf Data Health", version="0.1.0")


@app.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "live"}


@app.get("/health/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}
