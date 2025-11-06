from app.models.openai import openai_model

# Only export OpenAI model (Gemini not used in mobile shopping agent)
__all__ = ["openai_model"]