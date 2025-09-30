"""
State Definitions and Pydantic Schemas for Budget Search Scoping.
This defines the state objects and structured schemas used for the budget search agent scoping workflow,
including state management and output schemas.
"""

import operator
from typing_extensions import Optional, Annotated, List, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


# ===== STATE DEFINITIONS =====
class AgentInputState(MessagesState):
    """Input state for the full agent - only contains messages from user input."""
    pass


class AgentState(MessagesState):
    """
    Main state for the budget search system.
    Extends MessagesState with additional fields for budget search coordination.

    Note: Some fields are duplicated across different state classes for proper
    state management between subgraphs and the main workflow.
    """

    search_query: Optional[str]
    topic_of_interest: Optional[str]
    reference_year: Optional[str]
    supervisor_messages: Annotated[Sequence[BaseMessage], add_messages]
    raw_notes: Annotated[list[str], operator.add] = []
    notes: Annotated[list[str], operator.add] = []
    final_report: str


# ===== STRUCTURED OUTPUT SCHEMAS =====
class ClarifyWithUser(BaseModel):
    """Schema for user clarification decision and questions."""

    need_clarification: bool = Field(
        description="Whether the user needs to be asked a clarifying question to provide topic and/or year.",
    )
    question: str = Field(
        description="A question to ask the user to clarify the budget search topic and/or reference year",
    )
    verification: str = Field(
        description="Verification message that we have both topic and year and will start the budget search.",
    )


class BudgetSearchQuery(BaseModel):
    """Schema for structured budget search query generation."""

    topic_of_interest: str = Field(
        description="The specific budget topic/theme extracted from user's request (e.g., hospitais, educação, segurança)",
    )
    reference_year: str = Field(
        description="The specific year for budget data extracted from user's request (e.g., 2024, 2025)",
    )
    search_query: str = Field(
        description="The formatted search query in the format '[topic] [year]' that will be used for budget search",
    )