from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import sys
import json
import asyncio
from pathlib import Path

# Add parent directory to path
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

# Import agent and tools
from DealAgent.agent import agent, query_sales_agent, get_deal_by_customer_id, add_deal

# Try to import Message types for ADK
try:
    from google.adk import UserMessage
except ImportError:
    try:
        from google.adk.messages import UserMessage
    except ImportError:
        UserMessage = None

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class CustomerIdRequest(BaseModel):
    customer_id: int

class DealDataRequest(BaseModel):
    deal_data: dict

@app.get("/")
async def root():
    return {
        "message": "DealAgent FastAPI is running",
        "endpoints": {
            "POST /query": "Query sales agent",
            "GET /deal/{customer_id}": "Get deal by customer ID",
            "POST /deal": "Add new deal"
        }
    }

@app.post("/query")
async def handle_query(request: QueryRequest):
    """Query the DealAgent. Returns JSON response."""
    try:
        # Create message object for ADK agent
        if UserMessage:
            message = UserMessage(content=request.query)
        else:
            message = request.query
        
        # Run the agent and collect response
        response_text = ""
        async for event in agent.run_async(message):
            if hasattr(event, 'content'):
                response_text += str(event.content)
            elif hasattr(event, 'text'):
                response_text += str(event.text)
            elif isinstance(event, str):
                response_text += event
        
        # Try to parse as JSON
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # If not JSON, wrap it
            result = {"status": "error", "response": response_text}
        
        return Response(
            content=json.dumps(result, ensure_ascii=False),
            media_type="application/json"
        )
    except Exception as e:
        error_result = {"status": "error", "response": f"Error: {str(e)}"}
        return Response(
            content=json.dumps(error_result, ensure_ascii=False),
            media_type="application/json",
            status_code=500
        )

@app.get("/deal/{customer_id}")
async def get_deal(customer_id: int):
    """Get deal by customer ID. Returns JSON response."""
    result = get_deal_by_customer_id(customer_id)
    return Response(
        content=json.dumps(result, ensure_ascii=False),
        media_type="application/json"
    )

@app.post("/deal")
async def create_deal(request: DealDataRequest):
    """Add a new deal. Returns JSON response."""
    result = add_deal(request.deal_data)
    return Response(
        content=json.dumps(result, ensure_ascii=False),
        media_type="application/json"
    )

if __name__ == "__main__":
    uvicorn.run(
        "DealAgent.fastapi_server:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )

