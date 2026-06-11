from contextlib import asynccontextmanager
import os
from typing import Any
from dotenv import load_dotenv
import uvicorn

from fastapi import FastAPI
from kagglesdk.kaggle_client import KaggleClient
from kagglesdk.competitions.types.competition_api_service import (
    ApiCompetition,
    ApiGetCompetitionRequest,
    ApiListCompetitionPagesRequest,
    ApiListCompetitionPagesResponse,
    ApiListCompetitionsRequest,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()

    kaggle_api_token = os.getenv("KAGGLE_API_TOKEN")
    if not kaggle_api_token:
        raise RuntimeError("KAGGLE_API_TOKEN environment variable is not set")

    app.state.kaggle_api_client = KaggleClient(
        api_token=kaggle_api_token
    ).competitions.competition_api_client
    yield


app = FastAPI(
    title="Kaggle Competition API",
    description="REST API for reading Kaggle competition information",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/competitions")
def get_competitions() -> dict[str, Any]:
    competitions_request = ApiListCompetitionsRequest()
    competitions = app.state.kaggle_api_client.list_competitions(competitions_request)

    return competitions.to_dict()


@app.get("/competitions/{competition_name}")
def get_competition(competition_name: str) -> dict[str, Any]:
    competition_request = ApiGetCompetitionRequest()
    competition_request.competition_name = competition_name

    competition: ApiCompetition = app.state.kaggle_api_client.get_competition(
        competition_request
    )

    pages_request = ApiListCompetitionPagesRequest()
    pages_request.competition_name = competition_name
    pages: ApiListCompetitionPagesResponse = (
        app.state.kaggle_api_client.list_competition_pages(pages_request)
    )

    response: dict[str, Any] = competition.to_dict()
    response["pages"] = pages.to_dict().get("pages", [])

    return response


def main() -> None:
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("UVICORN_RELOAD", "false").lower() == "true",
    )


if __name__ == "__main__":
    main()
