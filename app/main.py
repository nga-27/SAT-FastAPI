from fastapi import FastAPI

from app.libs.test_math import add_numbers
from app.routers import tools

from app.dependencies import metadata_tags

app = FastAPI(
    title="SecuritiesAnalysisTools API",
    description="The FastAPI version of SecuritiesAnalysisTools repo.",
    version="0.0.1",
    openapi_tags=metadata_tags.tags_metadata
)

app.include_router(tools.router)


@app.get("/")
def check_heartbeat():
    return {"hello there": "from SAT-FastAPI"}


@app.get("/{ticker}")
def echo_ticker(ticker: str):
    return {"ticker": ticker}


@app.post("/add_values/{a}/{b}")
def echo_add(a: int, b: int):
    value = add_numbers(a, b)
    return {"value": value}
