import os
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.api import health
from app.api import auth
from app.api import review
from app.api import stats
from app.api import apps
from app.core.services.ai_predict import predictor
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    print("Loading neassary models and resources...")
    predictor.load_models()
    print("Model Loaded Successfully!")
    
    yield
    
    # --- SHUTDOWN ---
    print("Shutting down...")
    predictor.model = None

# Create the FastAPI app and run with lifespan
app = FastAPI(title="NLP API", lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
]

FRONTEND_URL = os.getenv("FRONTEND_URL")

if FRONTEND_URL:
    # This strips any accidental trailing slashes from your GitHub Secret!
    clean_url = FRONTEND_URL.rstrip("/")
    origins.append(clean_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    # Allows your Vue app to connect
    allow_credentials=True,   # Allows cookies/tokens
    allow_methods=["*"],      # ALLOWS ALL METHODS (This fixes the OPTIONS 405 error!)
    allow_headers=["*"],      # Allows all headers
)

# Include the router
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(review.router, prefix="/reviews", tags=["Reviews"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])
app.include_router(apps.router, prefix="/apps", tags=["Apps"])
    