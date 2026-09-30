from config import settings

print("API key loaded:", bool(settings.gemini_api_key))
print("API key starts with:", settings.gemini_api_key[:8])
print("Model:", settings.gemini_model)