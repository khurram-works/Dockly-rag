# processing/generation/prompt_builder.py
from typing import List

class PromptBuilder:
    """Build prompts for LLM answer generation."""
    
    def build_prompt(
        self,
        question: str,
        context_chunks: List[str],
        conversation_history: List[dict],
    ) -> str:
        """Build a prompt for the LLM."""
        
        context = "\n\n".join([
            f"Context {i+1}:\n{chunk}"
            for i, chunk in enumerate(context_chunks)
        ])
        
        prompt = f"""You are a helpful assistant that answers questions based on the provided context.

Context:
{context}

Question: {question}

Instructions:
- Answer the question using ONLY the provided context
- If the answer is not in the context, say "I don't have enough information to answer this question"
- Be concise and accurate
- Cite the context you used

Answer:"""
        
        return prompt