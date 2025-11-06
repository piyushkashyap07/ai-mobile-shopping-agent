"""
Mobile Shopping Agent - Creates the FunctionAgent for mobile phone shopping
"""
import logging

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.llms import LLM

from app.tools.mobile_shopping_tools import create_mobile_shopping_tools
from app.prompts.mobile_shopping_prompt import get_mobile_shopping_agent_prompt

logger = logging.getLogger(__name__)


def create_mobile_shopping_agent(llm: LLM) -> FunctionAgent:
    """
    Create a FunctionAgent for mobile phone shopping
    
    Args:
        llm: The LLM instance to use (should be OpenAI)
    
    Returns:
        FunctionAgent configured for mobile shopping
    """
    logger.info("Creating mobile shopping agent...")
    
    # Get all mobile shopping tools (CSV database only)
    tools = create_mobile_shopping_tools()
    logger.info(f"Created {len(tools)} mobile shopping tools")
    
    # Get the system prompt
    system_prompt = get_mobile_shopping_agent_prompt()
    
    # Create the agent
    agent = FunctionAgent(
        tools=tools,
        llm=llm,
        system_prompt=system_prompt,
        verbose=True
    )
    
    logger.info("Mobile shopping agent created successfully")
    return agent
