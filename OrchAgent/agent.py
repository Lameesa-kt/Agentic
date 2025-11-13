"""
Orchestrator Agent - Simple orchestrator that delegates to DealAgent
"""
try:
    from google.adk import Agent
except ImportError:
    from google.adk.agents import Agent

# Import DealAgent directly
from DealAgent.agent import agent as deal_agent

# Create Orchestrator Agent - directly delegates to DealAgent
agent = Agent(
    model="gemini-2.0-flash",
    name="OrchAgent",
    description="Orchestrator agent that delegates to DealAgent",
    instruction="""You are a simple pass-through agent. When users ask about deals, delegate to Deal_agent sub-agent and return its response exactly as-is. Do NOT modify or change anything.""",
    sub_agents=[deal_agent]
)

# Expose for ADK CLI
root_agent = agent

