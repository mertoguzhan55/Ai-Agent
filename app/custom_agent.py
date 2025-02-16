from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from typing import Dict, List, Optional, Union
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.groq import GroqModel
import random


@dataclass
class CustomAgent():

    def __post_init__(self):
        self.model = GroqModel('llama-3.3-70b-versatile')

    def run(self, dep):

        agent = Agent(
            model = self.model,  
            deps_type = dep,  
            system_prompt=(
                "You're a dice game, you should roll the die and see if the number "
                "you get back matches the user's guess. If so, tell them they're a winner. "
                "Use the player's name in the response. To use user name, you should read database and find name related to turkish name."
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


        dice_result = agent.run_sync('My guess is 4', deps = dep)  
        print(dice_result.data)
        #> Congratulations Anne, you guessed correctly! You're a winner!


if __name__ == "__main__":
    pass












