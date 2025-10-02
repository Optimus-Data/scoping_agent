"""
Service layer for budget search agent.
Estado da conversa gerenciado automaticamente pelo LangGraph RedisSaver.
Redis customizado usado apenas para auditoria/histórico externo.
"""

import uuid
from datetime import datetime
from budget_scoping_agent.main import run_budget_search_workflow
from src.redis_db.db_operations import save_thread_interaction, get_thread_interactions

async def run_budget_search_service(agent, message: str, thread_id: str = None):
    """
    Run budget search workflow.
    
    O histórico da conversa é gerenciado automaticamente pelo RedisSaver do LangGraph.
    Não é necessário carregar mensagens anteriores manualmente.
    """
    thread_id = thread_id or str(uuid.uuid4())
    
    result = run_budget_search_workflow(agent, message, thread_id)
    
    messages = []
    for msg in result.get("messages", []):
        messages.append({
            "type": msg.__class__.__name__,
            "content": getattr(msg, "content", str(msg)),
        })

    response = {
        "thread_id": thread_id,
        "messages": messages,
        "search_query": result.get("search_query"),
        "topic_of_interest": result.get("topic_of_interest"),
        "reference_year": result.get("reference_year"),
        "timestamp": datetime.now().isoformat(),
    }

    await save_thread_interaction(thread_id, response)
    
    return response

async def get_thread_service(thread_id: str):
    """
    Retrieve thread history from custom Redis storage (audit trail).
    """
    data = await get_thread_interactions(thread_id)
    if not data:
        return {"thread_id": thread_id, "status": "not found"}
    return data

async def generate_thread_id_service():
    """
    Generate a new unique thread ID.
    """
    thread_id = str(uuid.uuid4())
    return {"thread_id": thread_id}