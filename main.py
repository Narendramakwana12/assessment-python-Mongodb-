from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes import router

app = FastAPI(title="Employee API", version="1.0.0")

@app.get("/")
def root():
    return RedirectResponse(url="/docs")


app.include_router(router)
