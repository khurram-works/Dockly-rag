# from typing import Any

# class PromptBuilder:
#     """Build prompts for LLM answer generation."""

#     def build_prompt(
#         self,
#         question: str,
#         context_chunks: list[str],
#         conversation_history: list[dict[str, Any]] = None,
#     ) -> str:
#         context = "\n\n".join([
#             f"Context {i + 1}:\n{chunk}"
#             for i, chunk in enumerate(context_chunks)
#         ])

#         history_text = ""
#         if conversation_history:
#             history_lines = []
#             for message in conversation_history:
#                 role = message.get("role", "user").lower()
#                 content = message.get("content", "")
#                 if role and content:
#                     history_lines.append(f"{role.capitalize()}: {content}")
#             if history_lines:
#                 history_text = "\n\nConversation history:\n" + "\n".join(history_lines)

#         prompt = f"""You are a helpful assistant that answers questions based on the provided context.

# Context:
# {context}

# Question:
# {question}
# {history_text}

# Instructions:
# - Answer the question using ONLY the provided context.
# - If the answer is not in the context, say "I don't have enough information to answer this question."
# - Be concise and accurate.
# - Cite the context you used in the form of document filename and page numbers.
# - Do not fabricate facts.

# Answer:"""

#         return prompt

# What you should be storing in Qdrant's payload:
from typing import Any

class PromptBuilder:
    """Build prompts for LLM answer generation."""

    def build_prompt(
        self,
        question: str,
        # CHANGED: Accept dictionaries holding text and metadata keys
        context_chunks: list[dict[str, Any]],
        conversation_history: list[dict[str, Any]] = None,
    ) -> str:
        
        # CHANGED: Extract content, source file, and page directly into the prompt string
        context_blocks = []
        for i, chunk in enumerate(context_chunks):
            text = chunk.get("text", "").strip()
            source = chunk.get("source", "Unknown Document")
            page = chunk.get("page", "Unknown Page")
            
            block = f"Context {i + 1} [Source: {source}, Page: {page}]:\n{text}"
            context_blocks.append(block)
            
        context = "\n\n".join(context_blocks)

        history_text = ""
        if conversation_history:
            history_lines = []
            for message in conversation_history:
                role = message.get("role", "user").lower()
                content = message.get("content", "")
                if role and content:
                    history_lines.append(f"{role.capitalize()}: {content}")
            if history_lines:
                history_text = "\n\nConversation history:\n" + "\n".join(history_lines)

        prompt = f"""You are a helpful assistant that answers questions based on the provided context.

Context:
{context}

Question:
{question}
{history_text}

Instructions:
- Answer the question using ONLY the provided context.
- If the answer is not in the context, say "I don't have enough information to answer this question."
- Be concise and accurate.
- Cite the context you used by strictly naming the source file and page numbers provided in the brackets.
- Do not fabricate facts or invent citations.

Answer:"""

        return prompt

