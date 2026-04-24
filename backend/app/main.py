from fastapi import FastAPI

from app.database.session import Base, engine

# 🔥 Import ALL models FIRST (very important)
import app.models.user
import app.models.question
import app.models.answer
import app.models.attempt

# 🔥 Import routers
from app.api.routes.auth import router as auth_router
from app.api.routes import question, admin

# 🔥 Create app
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for now (dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

# 🔥 Create tables
Base.metadata.create_all(bind=engine)

# 🔥 Include routers
app.include_router(auth_router)
app.include_router(question.router)
app.include_router(admin.router)