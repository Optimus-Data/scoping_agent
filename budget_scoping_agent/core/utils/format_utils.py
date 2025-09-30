"""Utility functions for formatting and displaying messages."""

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


def format_messages(messages):
    """
    Format and display messages in a readable format.

    Args:
        messages: List of BaseMessage objects
    """
    if not messages:
        print("No messages to display.")
        return

    print("=" * 50)
    print("CONVERSATION HISTORY")
    print("=" * 50)

    for i, message in enumerate(messages, 1):
        message_type = get_message_type(message)
        content = message.content if hasattr(message, 'content') else str(message)

        print(f"\n[{i}] {message_type}:")
        print("-" * 30)
        print(content)
        print()


def get_message_type(message: BaseMessage) -> str:
    """
    Get the display name for a message type.

    Args:
        message: Message object

    Returns:
        String representation of message type
    """
    if isinstance(message, HumanMessage):
        return "USER"
    elif isinstance(message, AIMessage):
        return "ASSISTANT"
    else:
        return message.__class__.__name__.upper()


def print_workflow_status(step: str, status: str = "RUNNING"):
    """
    Print workflow step status.

    Args:
        step: Name of the workflow step
        status: Status of the step (RUNNING, COMPLETED, ERROR)
    """
    print(f"[{status}] {step}")


def print_budget_search_query(search_query: str, topic: str = None, year: str = None):
    """
    Format and print budget search query details.

    Args:
        search_query: The formatted search query
        topic: The topic of interest (optional)
        year: The reference year (optional)
    """
    print("\n" + "=" * 50)
    print("BUDGET SEARCH QUERY")
    print("=" * 50)
    print(f"Query: {search_query}")
    if topic:
        print(f"Topic: {topic}")
    if year:
        print(f"Year: {year}")
    print("=" * 50 + "\n")


def print_search_query(search_query: str):
    """
    Format and print search query (backward compatibility).

    Args:
        search_query: The search query text
    """
    print_budget_search_query(search_query)


print_research_brief = print_budget_search_query