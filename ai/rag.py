import os
from typing import Dict
from .embeddings import get_embedding
from .vector_store import VectorStore
from openai import OpenAI

def retrieve_context(query: str, top_k: int, session_id: str, user_id: str) -> List[Dict]:
    vector_store = VectorStore()
    query_embedding = get_embedding([query])[0]
    filters = {"session_id": session_id, "user_id": user_id}
    matches = vector_store.search(query_embedding, top_k, **filters)
    return matches

def answer_question(query: str, session_id: str, user_id: str) -> Dict[str, str]:
    matches = retrieve_context(query, top_k=5, session_id=session_id, user_id=user_id)
    context = "\n".join(match["metadata"]["chunk_text"] for match in matches)

    # Build the prompt
    prompt = f"Answer the following question based on the context:\n\nContext:\n{context}\n\nQuestion:\n{query}"

    # Call the runtime LLM
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    openai_client = OpenAI(api_key=openai_api_key)
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
    )

    # Extract the answer and sources
    answer = response["choices"][0]["message"]["content"]
    sources = [match["metadata"]["source"] for match in matches]

    return {"answer": answer, "sources": sources}