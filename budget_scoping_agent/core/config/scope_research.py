"""
User Clarification and Budget Search Query Generation.

This module implements the scoping phase of the budget search workflow, where we:
1. Assess if the user's request contains both topic of interest and reference year
2. Generate a structured search query for budget data

The workflow uses structured output to make deterministic decisions about whether
sufficient context exists to proceed with budget search.
"""

from datetime import datetime
from typing_extensions import Literal

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, get_buffer_string
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

from budget_scoping_agent.core.prompts.scoping import (
    clarify_with_user_instructions,
    transform_messages_into_research_topic_prompt,
)
from budget_scoping_agent.core.config.state_and_schemas import (
    AgentState,
    ClarifyWithUser,
    BudgetSearchQuery,
    AgentInputState,
)


# ===== UTILITY FUNCTIONS =====
def get_today_str() -> str:
    """Get current date in a human-readable format."""
    return datetime.now().strftime("%a %b %-d, %Y")


# ===== CONFIGURATION =====
model = init_chat_model(model="openai:gpt-4o", temperature=0.0)


# ===== WORKFLOW NODES =====
def clarify_with_user(
    state: AgentState,
) -> Command[Literal["write_budget_search_query", "__end__"]]:
    """
    Determine if the user's request contains both topic of interest and reference year.

    Uses structured output to make deterministic decisions and avoid hallucination.
    Routes to either budget search query generation or ends with a clarification question.
    """
    structured_output_model = model.with_structured_output(ClarifyWithUser)

    response = structured_output_model.invoke(
        [
            HumanMessage(
                content=clarify_with_user_instructions.format(
                    messages=get_buffer_string(messages=state["messages"]),
                    date=get_today_str(),
                )
            )
        ]
    )

    if response.need_clarification:
        return Command(
            goto=END,
            update={"messages": [AIMessage(content=response.question)]},
        )
    else:
        return Command(
            goto="write_budget_search_query",
            update={"messages": [AIMessage(content=response.verification)]},
        )


def write_budget_search_query(state: AgentState):
    """
    Transform the conversation history into a structured budget search query.

    Uses structured output to ensure the query follows the required format:
    topic + year (e.g., "hospitais 2025")
    """
    structured_output_model = model.with_structured_output(BudgetSearchQuery)

    response = structured_output_model.invoke(
        [
            HumanMessage(
                content=transform_messages_into_research_topic_prompt.format(
                    messages=get_buffer_string(state.get("messages", [])),
                    date=get_today_str(),
                )
            )
        ]
    )

    return {
        "search_query": response.search_query,
        "topic_of_interest": response.topic_of_interest,
        "reference_year": response.reference_year,
        "supervisor_messages": [HumanMessage(content=f"Budget search query: {response.search_query}")],
    }


# ===== GRAPH CONSTRUCTION =====
deep_researcher_builder = StateGraph(AgentState, input_schema=AgentInputState)

deep_researcher_builder.add_node("clarify_with_user", clarify_with_user)
deep_researcher_builder.add_node("write_budget_search_query", write_budget_search_query)

deep_researcher_builder.add_edge(START, "clarify_with_user")
deep_researcher_builder.add_edge("write_budget_search_query", END)