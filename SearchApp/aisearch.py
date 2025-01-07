import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_keyword(text: str, product_category_list: str) -> str:

    prompt = (
        f"Based on the provided product categories{product_category_list}: '{text}', "
        f"and the user's query: '{text}', suggest relevant keywords for product search.  "
        "Ensure the keywords align with available product categories and names."
        "example : the text is 'i want a phone' , the output should be any available related product to phone from {product_category_list} "
        "your response should always only one or multiple keywords. the keywords must be from {product_category_list}"
        "try to relate the '{text}' with any of the '{product_category_list}' however you can. there is nothing irrelevant."
        "you will generate one keyword. DO NOT GENERATE ANY EXTRA TEXT ALONG WITH THE KEYWORDS, the keywords must be from {product_category_list}"
        "the input can be in any language but the Response must be in English"
    )

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text
