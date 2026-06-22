from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from datetime import datetime
from contextlib import asynccontextmanager
from database.config import get_db
from backend.routes.auth import router as auth_router
from backend.routes.documents import router as documents_router
from ai.routes import router as ai_router

# Initialize FastAPI app
app = FastAPI(
    title="Aakaar Project",
    description="AI-powered web application for document processing and querying.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    get_db()  # Corrected to use 'get_db' instead of 'init_db'
    yield
    # Shutdown logic
    pass

app.router.lifespan_context = lifespan

# Mount routers
app.include_router(auth_router, prefix="/api/auth")
app.include_router(documents_router, prefix="/api/documents")
app.include_router(ai_router, prefix="/api/ai")

# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}