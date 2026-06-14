from groq import Groq
from config import GROQ_API_KEY

groq_client = Groq(api_key = GROQ_API_KEY)

def generate_answer(question: str, relevant_chunks: list[dict], company_name: str = "the company", conversation_history: list[dict]= None)-> tuple[str, list[dict]]:
  if conversation_history is None:
    conversation_history = []
  seen = set()
  source_files = []
  context_parts = []
  for i, chunk in enumerate(relevant_chunks):
    context_parts.append(f"[Source {i+1}: {chunk['filename']}]\n{chunk['text']}")
    key = f"{chunk['filename']}_page{chunk['pageNumber']}"
    if key not in seen:
        seen.add(key)
        source_files.append({
            "documentId": chunk["documentId"],
            "filename": chunk["filename"],
            "pageNumber": chunk["pageNumber"]
        })
  context = "\n\n".join(context_parts)

  messages = [
        {
            "role": "system",
            "content": f"""You are a helpful customer support assistant for {company_name}.

Your job is to answer customer questions accurately using ONLY the context provided below.

Rules you must follow:
1. Answer ONLY based on the provided context
2. If the answer is not in the context, say exactly: "I don't have information about that in my knowledge base. Please contact our support team directly."
3. Never make up information or use knowledge outside the context
4. Keep answers clear, friendly and concise
5. If the context partially answers the question, give what you know and mention the limitation

Context from {company_name}'s documents:
{context}"""
        }
    ]
  for message in conversation_history:
        messages.append({
            "role": message["role"],
            "content": message["content"]
        })

  messages.append({
        "role": "user",
        "content": question
    })

  response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_tokens=1024,
        temperature=0.1
    )
  answer = response.choices[0].message.content

  return answer, source_files





