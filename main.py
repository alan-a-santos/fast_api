from fastapi import FastAPI
from api_router import api_router as router  # ou altere o nome no outro arquivo

app = FastAPI(title="api_santander")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
