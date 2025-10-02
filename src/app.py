"""
FastAPI application with RedisSaver checkpointer.
"""

from fastapi import FastAPI
from pathlib import Path
import sys

project_root = Path(__file__).parent
sys.path.append(str(project_root))

from budget_scoping_agent.main import create_budget_search_agent
from src.redis_db.config import redis_client

app = FastAPI(
    title="Budget Search Agent API",
    description="API for interacting with the government budget search agent",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    print("Initializing Budget Search Agent with RedisSaver...")
    
    try:

        redis_client.ping()
        print("Connected to Redis successfully!")
        
        app.agent = create_budget_search_agent()
        print("Agent initialized successfully with persistent storage!")
        
    except Exception as e:
        print(f"Error during startup: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down Budget Search Agent...")

from src.budget_scoping_agent_api.routes.routes import router
app.include_router(router)