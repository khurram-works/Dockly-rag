# processing/generation/answer_generator.py
from groq import Groq 
from processing.generation.prompt_builder import PromptBuilder
import os
from typing import List 
from core.config.settings import settings 

class AnswerGenerator:
    def __init__(self) -> None:
        self._client = Groq(api_key=settings.groq_api_key) 
        self._prompt_builder = PromptBuilder()
    
    def generate(
        self,
        question: str,
        context_chunks: List[str],  # List is now properly imported
        conversation_history: List[dict],
    ) -> str:
        """Generate an answer using the LLM."""
        
        prompt = self._prompt_builder.build_prompt(
            question=question,
            context_chunks=context_chunks,
            conversation_history=conversation_history,
        )
        
        response = self._client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1024,
        )
        
        return response.choices[0].message.content