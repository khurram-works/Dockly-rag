# from groq import Groq
# from processing.generation.prompt_builder import PromptBuilder
# from typing import Any
# from core.config.settings import settings


# class AnswerGenerator:
#     def __init__(self) -> None:
#         self._client = Groq(api_key=settings.groq_api_key)
#         self._prompt_builder = PromptBuilder()

#     def generate(
#         self,
#         question: str,
#         context_chunks: list[str],
#         conversation_history: list[dict[str, Any]],
#     ) -> str:
#         prompt = self._prompt_builder.build_prompt(
#             question=question,
#             context_chunks=context_chunks,
#             conversation_history=conversation_history,
#         )

#         response = self._client.chat.completions.create(
#             model=settings.groq_model_name,
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are an AI assistant that answers user questions using only the supplied context. "
#                         "Cite specific documents and page numbers when referencing sources."
#                     ),
#                 },
#                 {"role": "user", "content": prompt},
#             ],
#             temperature=0.1,
#             max_tokens=1024,
#         )

#         return response.choices[0].message.content


import logging
from typing import Any
from groq import Groq
from core.config.settings import settings
from processing.generation.prompt_builder import PromptBuilder

logger = logging.getLogger(__name__)

class AnswerGenerator:
    def __init__(self) -> None:
        self._client = Groq(api_key=settings.groq_api_key)
        self._prompt_builder = PromptBuilder()

    def generate(
        self,
        question: str,
        # CHANGED: Accept dictionaries containing text AND metadata for citations
        context_chunks: list[dict[str, Any]], 
        conversation_history: list[dict[str, Any]],
    ) -> str:
        # Construct the prompt inside your custom prompt_builder
        prompt = self._prompt_builder.build_prompt(
            question=question,
            context_chunks=context_chunks,
            conversation_history=conversation_history,
        )

        try:
            response = self._client.chat.completions.create(
                model=settings.groq_model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant that answers user questions using only the supplied context. "
                            "Every chunk contains a 'source' and 'page' key. Use this metadata to cite specific "
                            "documents and page numbers when referencing sources. If the context does not "
                            "contain the answer, state that you do not know."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=1024,
            )
            
            # DEFENSIVE: Ensure valid payload choices exist before parsing
            if not response.choices:
                logger.error("Groq API returned an empty choices list.")
                return "I am sorry, I could not generate an answer at this moment."
                
            content = response.choices[0].message.content
            return content if content else "No response generated."

        except Exception as e:
            logger.error(f"Failed to generate completion from Groq API: {str(e)}")
            return "An internal error occurred while processing your request."
