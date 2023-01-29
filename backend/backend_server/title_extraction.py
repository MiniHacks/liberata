import requests
import os
import openai

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except:
    import sys
    print("Could not find OPENAI_API_KEY -- check your env vars, and if you're having trouble, ask Ritik for help", file=sys.stderr)
    raise


def extract_book_titles(text_block: str) -> list[str]:
    result = openai.Completion.create(
        model = "text-davinci-003",
        prompt = "Identify the book titles that are in the following block of text. Do not provide book titles that are not mentioned in the text. Separate titles with commas.\n"
                 "Text block: \n"
                 f"{text_block}\n"
                 "Book titles:",
        temperature = 0.7,
        max_tokens = 256
    )

    titles: str = result["choices"][0]["text"]
    return [t.strip() for t in titles.strip().split(",")]
