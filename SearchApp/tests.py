from django.test import TestCase
from django.conf import settings
import google.generativeai as genai


class APIKeyTest(TestCase):
    def setUp(self):
        self.api_key = settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)

    def test_api_key_is_set(self):
        self.assertIsNotNone(
            self.api_key, "GEMINI_API_KEY is not set in settings")

    def test_generate_keyword(self):

        prompt = "Suggest relevant keywords for product search based on the provided product categories and user's query."
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        self.assertIsNotNone(response.text, "API response is empty")
        self.assertGreater(len(response.text), 0, "API response is empty")

        print("API response:", response.text)
