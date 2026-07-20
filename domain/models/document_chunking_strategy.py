from dataclasses import dataclass


@dataclass(slots=True)
class DocumentChunkingStrategy:
    max_characters: int = 1500

    new_after_n_chars: int = 1000

    combine_text_under_n_chars: int = 1000

    multipage_sections: bool = True

    include_orig_elements: bool = True