import ollama

def generate_response(prompt, context=""):

    full_prompt = f"""
    Use the following context to answer the question.

    Context:
    {context}

    Question:
    {prompt}
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": full_prompt}]
    )

    return response["message"]["content"]