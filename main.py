"""Entry point of the program."""

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/", StaticFiles(directory="public", html=True), name="public")
