import uuid
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
from src.redis_db.db_operations import save_thread_interaction, get_thread_interactions
from budget_scoping_agent.main import run_budget_search_workflow

async def run_budget_search_service(agent, message: str, thread_id: str = None):
    thread_id = thread_id or str(uuid.uuid4())
    
    # Se thread_id foi fornecido, tenta recuperar conversa anterior do Redis
    previous_messages = []
    if thread_id:
        previous_data = await get_thread_interactions(thread_id)
        if previous_data and "messages" in previous_data:
            # Reconstrói as mensagens anteriores
            for msg in previous_data["messages"]:
                if msg["type"] == "HumanMessage":
                    previous_messages.append(HumanMessage(content=msg["content"]))
                elif msg["type"] == "AIMessage":
                    previous_messages.append(AIMessage(content=msg["content"]))
    
    # Adiciona a nova mensagem do usuário
    all_messages = previous_messages + [HumanMessage(content=message)]
    
    # Executa o workflow com todas as mensagens (anteriores + nova)
    result = run_budget_search_workflow(agent, message, thread_id)
    
    # Se havia mensagens anteriores, adiciona elas ao resultado para salvar o histórico completo
    if previous_messages:
        # Combina mensagens anteriores com as novas do resultado
        all_result_messages = previous_messages + result.get("messages", [])
        result["messages"] = all_result_messages
    
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
    data = await get_thread_interactions(thread_id)
    if not data:
        return {"thread_id": thread_id, "status": "not found"}
    return data

async def generate_thread_id_service():
    thread_id = str(uuid.uuid4())
    return {"thread_id": thread_id}