from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from typing import Dict, List, Optional, Union
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.groq import GroqModel
import random
import requests


@dataclass
class CustomAgent():

    def __post_init__(self):
        self.model = GroqModel('llama-3.3-70b-versatile')

    def run(self, dep):

        agent = Agent(
            model = self.model,  
            deps_type = dep,  
            system_prompt=(
                "You are an AI assistant integrated with various website APIs, designed to assist users in retrieving and processing data from different online platforms. Your primary function is to understand user queries, determine the appropriate API endpoints, and fetch the relevant information efficiently. You can interact with e-commerce, social media, finance, weather, and other website APIs to provide real-time and accurate responses. Ensure that the data is well-structured, relevant, and easy to understand for the user."
            ),
        )

        @agent.tool_plain  
        def roll_die() -> str:
            """Roll a six-sided die and return the result."""
            return str(random.randint(1, 6))

        @agent.tool  
        def get_player_name(ctx: RunContext[str]) -> str:
            """Get the player's name"""
            return ctx.deps
        
        @agent.tool
        def get_name_from_database(ctx: RunContext) -> str:
            """Read names from database.txt and return a name related to Turkish."""
            try:
                with open('database/database.txt', 'r', encoding='utf-8') as file:
                    names = file.read().splitlines()
                if names:
                    return random.choice(names)
                else:
                    return "Unknown"
            except FileNotFoundError:
                return "Unknown"
            
        @agent.tool
        def get_product_categories_from_trendyol(self):
            """
            Retrieves the list of product categories from the Trendyol API and returns the name of the first category.

            This function sends a GET request to the Trendyol product categories endpoint 
            and retrieves the available product categories in JSON format. If the request 
            is successful, it extracts and returns the name of the first category in the response. 
            Otherwise, it prints an error message with the HTTP status code.

            """
            url = "https://apigw.trendyol.com/integration/product/product-categories"

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
            else:
                print(f"Hata! HTTP Durum Kodu: {response.status_code}")
            return data["categories"][0]["name"]
        
        @agent.tool
        def get_product_categories_from_sahibinden(self):
            pass


        prompt = input("Haydi sor sor!\n")
        dice_result = agent.run_sync(str(prompt), deps = dep)  
        print(dice_result.data)
        # bana trendyoldaki kategorileri söyler misin?


if __name__ == "__main__":
    pass












