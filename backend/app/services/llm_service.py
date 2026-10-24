import os

import ollama

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

OLLAMA_UNAVAILABLE_MESSAGE = (
    "The local language model is not available right now. "
    "Please make sure Ollama is running (try `ollama serve`) and that the "
    f"'{OLLAMA_MODEL}' model is installed (try `ollama pull {OLLAMA_MODEL}`), "
    "then send your message again."
)


def generate_response(prompt, context=""):

    full_prompt = f"""
    Use the following context to answer the question.

    Context:
    {context}

    Question:
    {prompt}
    """

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": full_prompt}]
        )
    except Exception:
        # Ollama not running / model missing / connection refused:
        # return a clear, actionable message instead of crashing the API.
        return OLLAMA_UNAVAILABLE_MESSAGE

    try:
        return response["message"]["content"]
    except (KeyError, TypeError):
        return OLLAMA_UNAVAILABLE_MESSAGE
