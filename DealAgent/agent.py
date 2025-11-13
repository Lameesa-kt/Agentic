import os
import httpx
from typing import Any, Dict

try:
    # Preferred in newer versions
    from google.adk import Agent  # type: ignore
except Exception:
    # Fallback for older package layouts
    from google.adk.agents import Agent  # type: ignore

# Sales Agent FastAPI URL
SALES_AGENT_URL = os.getenv("SALES_AGENT_API_URL", "http://127.0.0.1:8000")

# Deal Server URL (Node.js Express server)
DEAL_SERVER_URL = os.getenv("DEAL_SERVER_URL", "http://127.0.0.1:3000")

# DealAgent FastAPI URL
DEAL_AGENT_API_URL = os.getenv("DEAL_AGENT_API_URL", "http://127.0.0.1:8001")


def query_sales_agent(query: str) -> Dict[str, Any]:
    """
    Query the Sales Agent with a natural language question.
    
    This tool calls the Sales Agent's FastAPI /query endpoint to get answers
    about customers, discounts, rebates, or any sales-related queries.
    
    Args:
        query: Natural language query (e.g., "Show me customer info for CompanyABC" or "Get customer ID for CompanyABC")
    
    Returns:
        Dictionary with response from the sales agent
    """
    try:
        # Preferred: match Sales Agent fastapi_server.py (GET /search?search=...)
        response = httpx.get(
            f"{SALES_AGENT_URL}/search",
            params={"search": query},
            timeout=30.0
        )
        if response.status_code == 404:
            # Fallback: try legacy POST /query if available
            fallback = httpx.post(
                f"{SALES_AGENT_URL}/query",
                json={"query": query},
                timeout=30.0
            )
            fallback.raise_for_status()
            return fallback.json()
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {
            "status": "error",
            "response": f"HTTP {e.response.status_code}: {e.response.text}"
        }
    except httpx.RequestError as e:
        return {
            "status": "error",
            "response": f"Request failed: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "response": f"Error: {str(e)}"
        }


def get_deal_by_customer_id(customer_id: int) -> Dict[str, Any]:
    """
    Get deal data by customer ID from the Deal Server.
    
    This tool calls the Deal Server's /api/getdeal/customer/:customer_id endpoint
    to retrieve deal information (bid details, accounts, terms, etc.) for a given customer.
    
    Args:
        customer_id: The customer ID (integer, e.g., 1, 2, 3)
    
    Returns:
        Dictionary with deal data including bidHead, bidAcct, etc.
    """
    try:
        response = httpx.get(
            f"{DEAL_SERVER_URL}/api/getdeal/customer/{customer_id}",
            timeout=10.0
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {
            "status": "error",
            "error": f"HTTP {e.response.status_code}: {e.response.text}",
            "customer_id": customer_id
        }
    except httpx.RequestError as e:
        return {
            "status": "error",
            "error": f"Request failed: {str(e)}",
            "customer_id": customer_id
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error: {str(e)}",
            "customer_id": customer_id
        }


def add_deal(deal_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add a new deal to the Deal Server by saving it to the data folder.
    
    This tool calls the Deal Server's POST /api/adddeal endpoint to save a deal JSON.
    The server will extract bidNum and save it as bidNum.json in the data folder.
    
    Args:
        deal_data: A dictionary containing the complete deal JSON structure.
    
    Returns:
        Dictionary with status and message indicating success or error.
        On success: {"message": "Deal saved successfully", "file": "bidNum.json"}
        On error: {"status": "error", "error": "error message"}
    """
    try:
        response = httpx.post(
            f"{DEAL_SERVER_URL}/api/adddeal",
            json=deal_data,
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {
            "status": "error",
            "error": f"HTTP {e.response.status_code}: {e.response.text}"
        }
    except httpx.RequestError as e:
        return {
            "status": "error",
            "error": f"Request failed: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error: {str(e)}"
        }


def query_deal_agent_fastapi(query: str) -> Dict[str, Any]:
    """
    Query DealAgent via FastAPI endpoint.
    
    This tool connects to DealAgent's FastAPI server to process queries.
    Useful for delegating complex queries or when direct agent access is needed.
    
    Args:
        query: Natural language query (e.g., "Find CompanyABC's deal")
    
    Returns:
        Dictionary with response from DealAgent FastAPI
    """
    try:
        response = httpx.post(
            f"{DEAL_AGENT_API_URL}/query",
            json={"query": query},
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return {
            "status": "error",
            "response": f"HTTP {e.response.status_code}: {e.response.text}"
        }
    except httpx.RequestError as e:
        return {
            "status": "error",
            "response": f"Request failed: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "response": f"Error: {str(e)}"
        }


# Define the Agent explicitly as requested
agent = Agent(
    model="gemini-2.0-flash",
    name='Deal_agent',
    description="A simple deal agent with data and 1 database tool",
    instruction=
"""SIMPLE RULES:
1. When user asks for a deal: Call query_sales_agent("Get customer ID for [company]"), then call get_deal_by_customer_id(customer_id)
2. The get_deal_by_customer_id tool returns the EXACT JSON from json1.json, json2.json, or json3.json
3. Return the tool response EXACTLY as-is, wrapped in: {"status": "success", "customer_id": X, "company_name": "...", "deal": <TOOL_RESPONSE>}
4. DO NOT modify, change, or create any fields - use the tool response exactly
5. DO NOT create fields like "deal_id", "description", "stage", "value" - they don't exist
6. The JSON files have: {"bidStart": {"bidHead": {...}, "bidAcct": [...]}} - return this EXACT structure

Tools:
- query_sales_agent(query): Get customer ID
- get_deal_by_customer_id(customer_id): Returns EXACT JSON from data folder - use it exactly
- add_deal(deal_data): Save new deal

Example:
User: "Find CompanyABC's deal"
1. query_sales_agent("Get customer ID for CompanyABC") → customer_id = 1
2. get_deal_by_customer_id(1) → returns: {"bidStart": {"bidHead": {...}, "bidAcct": [...]}}
3. Return: {"status": "success", "customer_id": 1, "company_name": "CompanyABC", "deal": <EXACT_TOOL_RESPONSE>}

CRITICAL: Copy the tool response EXACTLY - no changes, no new fields, no simplification.
""",
    tools=[query_sales_agent, get_deal_by_customer_id, add_deal, query_deal_agent_fastapi]
)

# Expose a separate root_agent that points to the Agent instance
root_agent = agent
