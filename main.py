from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
from contextlib import asynccontextmanager

from src.mongodb import MongoDB
from src.routers import collections, reviews, users


# MongoDB instance — routers resolve it lazily via src.routers.deps.get_db,
# so tests can patch("main.db").
db: Optional[MongoDB] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage MongoDB connection lifecycle."""
    global db
    db = MongoDB()
    yield
    db.close()


app = FastAPI(
    title="Nexus Integration API",
    description="API for managing users, collections, and reviews",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for prototype
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(collections.router)
app.include_router(reviews.router)


# ==================== Health Check ====================


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {"message": "Nexus Integration API is running", "status": "healthy"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    try:
        # Test MongoDB connection
        db.list_users()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e),
            },
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
