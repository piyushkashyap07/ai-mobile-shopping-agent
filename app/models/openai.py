from llama_index.llms.openai import OpenAI
from app.core.config import settings

def openai_model(reasoning: bool = False, temperature: float = 0.7):
  """
  Create OpenAI model instance
  
  Args:
    reasoning: Whether to use reasoning model (future use)
    temperature: Temperature for generation (default 0.7 for conversational)
  
  Returns:
    OpenAI model instance
  """
  # Use gpt-4o for now (gpt-5 doesn't exist yet)
  model = "gpt-4o-mini" if not reasoning else "gpt-4o"
  api_key = settings.OPENAI_API_KEY
  
  if not api_key:
    raise ValueError("OPENAI_API_KEY not set in environment variables")
  
  return OpenAI(
    model=model, 
    temperature=temperature, 
    openai_api_key=api_key, 
    timeout=180
  )