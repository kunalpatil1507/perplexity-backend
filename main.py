import asyncio
from fastapi import FastAPI, WebSocket
from pydantic_models.chat_body import ChatBody
from services.search_service import SearchService
from services.sort_source_service import SortSourceService
from services.llm_service import LLMService

app = FastAPI()

search_service = SearchService()
sort_source_service = SortSourceService()
llm_service = LLMService()

@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        query = data.get("query")

        search_results = search_service.web_search(query)
        sorted_results = sort_source_service.sort_sources(query, search_results)
        await websocket.send_json({"type": "search_result", "data": sorted_results})

        for chunk in llm_service.generate_response(query, sorted_results):
            await websocket.send_json({"type": "content", "data": chunk})

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

@app.post("/chat")
def chat_endpoint(body: ChatBody):
    search_results = search_service.web_search(body.query)
    sorted_results = sort_source_service.sort_sources(body.query, search_results)
    response = "".join(llm_service.generate_response(body.query, sorted_results))
    return {"response": response}
