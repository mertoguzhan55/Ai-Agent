from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from typing import Dict, List, Optional, Union
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.groq import GroqModel
import random


@dataclass
class CustomAgent():

    def run(self, dep):
        model = GroqModel('llama-3.3-70b-versatile')

        agent = Agent(
            model = model,  
            deps_type = dep,  
            system_prompt=(
                "You're a dice game, you should roll the die and see if the number "
                "you get back matches the user's guess. If so, tell them they're a winner. "
                "Use the player's name in the response."
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


        dice_result = agent.run_sync('My guess is 4', deps = dep)  
        print(dice_result.data)
        #> Congratulations Anne, you guessed correctly! You're a winner!


if __name__ == "__main__":
    pass












