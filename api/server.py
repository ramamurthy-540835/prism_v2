from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="PRISM v2 OS Kernel", version="0.1.0")
app.include_router(router)
