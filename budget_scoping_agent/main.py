"""
Main entry point for the Budget Search Agent.

This module centralizes the execution of the budget search workflow,
providing a clean interface for testing and running the agent.
"""

from dotenv import load_dotenv
load_dotenv()

from langgraph.checkpoint.redis import RedisSaver
from langchain_core.messages import HumanMessage
from budget_scoping_agent.core.config.scope_research import deep_researcher_builder
from src.redis_db.config import REDIS_URL

# ===== FACTORY =====
def create_budget_search_agent():
    """
    Create and compile the budget search agent with Redis checkpointer.

    Returns:
        Compiled budget search agent graph with persistent state
    """
    checkpointer = RedisSaver(REDIS_URL)  
    return deep_researcher_builder.compile(checkpointer=checkpointer)

# ===== WORKFLOW RUNNER =====
def run_budget_search_workflow(agent, user_message: str, thread_id: str = "1"):
    """
    Run the budget search workflow with a user message.
    
    The checkpointer automatically manages conversation history.
    """
    thread = {"configurable": {"thread_id": thread_id}}

    result = agent.invoke(
        {"messages": [HumanMessage(content=user_message)]},
        config=thread
    )

    return result

# ===== BACKWARD COMPATIBILITY =====
create_research_agent = create_budget_search_agent
run_research_workflow = run_budget_search_workflow