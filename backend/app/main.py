from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import init_db
from .routes import auth, items, users
import os
import time
from sqlalchemy.exc import OperationalError

app = FastAPI(title="Campus Digital Lost & Found", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mount static files - FIXED PATH
# Get the absolute path to the static directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Create the static directory if it doesn't exist
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Initialize database
@app.on_event("startup")
def on_startup():
    init_db()
    



# Include routers
app.include_router(auth.router)
app.include_router(items.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Campus Digital Lost & Found API"}


async def on_startup():
    max_retries = 30
    for attempt in range(max_retries):
        try:
            init_db()
            print("Database initialized successfully!")
            break
        except OperationalError:
            print(f"Database not ready, retrying... ({attempt + 1}/{max_retries})")
            time.sleep(2)
    else:
        print("Failed to initialize database after multiple attempts")

app.add_event_handler("startup", on_startup)