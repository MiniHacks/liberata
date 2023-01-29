import requests
import os
import openai
import tiktoken

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except:
    import sys
    print("Could not find OPENAI_API_KEY -- check your env vars, and if you're having trouble, ask Ritik for help", file=sys.stderr)
    raise

TOKEN_LIMIT = 3500
enc = tiktoken.get_encoding("gpt2")
async def extract_book_titles(text_block: str) -> list[str]:
    tokens = enc.encode(text_block)
    print(type(tokens))
    i = 0
    ret = []
    while i < len(tokens):
        result = await openai.Completion.acreate(
            model = "text-davinci-003",
            prompt = "Identify the book titles that are in the following block of text. Do not provide book titles that are not mentioned in the text. Do not include author names. Only repeat text verbatim. Separate titles with commas.\n"
                    "Text block: \n"
                    f"{enc.decode(tokens[i:i+3500])}\n"
                    "Book titles:",
            temperature = 0.7,
            max_tokens = 300
        )

        titles: str = result["choices"][0]["text"]
        ret.extend(t.strip() for t in titles.strip().split(","))
        i += TOKEN_LIMIT
    return ret
