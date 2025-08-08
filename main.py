from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from controllers import auth_controller
from controllers import plant_controller
from controllers import diagnose_controller
from controllers import discussion_controller
from fastapi.middleware.cors import CORSMiddleware
from controllers import ai_controller

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield             

app = FastAPI(lifespan=lifespan)
app.include_router(auth_controller.router, prefix="/auth")
app.include_router(plant_controller.router, prefix="/plants", tags=["plants"])
app.include_router(diagnose_controller.router, prefix="/diagnose", tags=["diagnose"])
app.include_router(ai_controller.router, prefix="/ai", tags=["ai"])
app.include_router(discussion_controller.router, prefix="/discussions", tags=["discussions"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)