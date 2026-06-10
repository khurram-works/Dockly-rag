# from groq import Groq
# from config import GROQ_API_KEY

# # Create Groq client — connects to Groq's API
# # This is like creating an OpenAI client but free
# groq_client = Groq(api_key=GROQ_API_KEY)


# # ─────────────────────────────────────────────
# # generate_answer
# # Takes the customer's question + relevant chunks
# # Builds a prompt and gets an AI answer from Groq
# # ─────────────────────────────────────────────
# def generate_answer(
#     question: str,
#     relevant_chunks: list[dict],
#     company_name: str = "the company",
#     conversation_history: list[dict] = []
# ) -> tuple[str, list[str]]:
#     # Returns: (answer string, list of source filenames)

#     # Step 1: Build the context string from relevant chunks
#     # This is the text we found in Qdrant that's relevant to the question
#     context_parts = []
#     source_files = []

#     for i, chunk in enumerate(relevant_chunks):
#         context_parts.append(f"[Source {i+1}: {chunk['filename']}]\n{chunk['text']}")
#         # Format: "[Source 1: ReturnPolicy.pdf]\nProducts may be returned..."

#         if chunk['filename'] not in source_files:
#             source_files.append(chunk['filename'])
#             # Collect unique filenames for the sources list

#     context = "\n\n".join(context_parts)
#     # Join all context pieces with double newline between them

#     # Step 2: Build the messages array for Groq
#     # Groq uses the same message format as OpenAI:
#     # role: "system" = instructions for the AI
#     # role: "user" = the human's message
#     # role: "assistant" = the AI's previous replies

#     messages = [
#         {
#             "role": "system",
#             "content": f"""You are a helpful customer support assistant for {company_name}.

# Your job is to answer customer questions accurately using ONLY the context provided below.

# Rules you must follow:
# 1. Answer ONLY based on the provided context
# 2. If the answer is not in the context, say exactly: "I don't have information about that in my knowledge base. Please contact our support team directly."
# 3. Never make up information or use knowledge outside the context
# 4. Keep answers clear, friendly and concise
# 5. If the context partially answers the question, give what you know and mention the limitation

# Context from {company_name}'s documents:
# {context}"""
#         }
#     ]

#     # Step 3: Add conversation history for follow-up questions
#     # This lets the AI remember what was said earlier in the conversation
#     for message in conversation_history:
#         messages.append({
#             "role": message["role"],
#             # "user" or "assistant"
#             "content": message["content"]
#         })

#     # Step 4: Add the current question
#     messages.append({
#         "role": "user",
#         "content": question
#     })

#     # Step 5: Call Groq API
#     response = groq_client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         # llama-3.1-8b-instant = fast, free, excellent quality
#         # "instant" means optimized for low latency

#         messages=messages,

#         max_tokens=1024,
#         # Maximum length of the AI's response
#         # 1024 tokens ≈ about 750 words — plenty for support answers

#         temperature=0.1
#         # Temperature controls randomness
#         # 0.0 = completely deterministic (same question = same answer always)
#         # 1.0 = very creative and random
#         # 0.1 = mostly consistent with tiny variation
#         # For customer support, low temperature is better — you want accuracy
#     )

#     # Step 6: Extract the answer text from the response
#     answer = response.choices[0].message.content
#     # choices[0] = the first (and only) response
#     # .message.content = the actual text string

#     return answer, source_files