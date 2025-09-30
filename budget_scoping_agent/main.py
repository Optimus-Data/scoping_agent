"""
Main entry point for the Budget Search Agent.

This module centralizes the execution of the budget search workflow,
providing a clean interface for testing and running the agent.
"""

from dotenv import load_dotenv
load_dotenv()

from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage
from budget_scoping_agent.core.config.scope_research import deep_researcher_builder

# ===== FACTORY =====
def create_budget_search_agent():
    """
    Create and compile the budget search agent with in-memory checkpointer.

    Returns:
        Compiled budget search agent graph
    """
    checkpointer = InMemorySaver()
    return deep_researcher_builder.compile(checkpointer=checkpointer)

# ===== WORKFLOW RUNNER =====
def run_budget_search_workflow(agent, user_message: str, thread_id: str = "1"):
    """
    Run the budget search workflow with a user message.
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
