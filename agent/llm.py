import json
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
import os

class LLM:
    """LLM that uses OpenAI API to generate plans based on input prompts"""
    
    def __init__(self):
        """Initialize the OpenAI client"""
        load_dotenv()
        self.client = OpenAI( base_url="https://openrouter.ai/api/v1",api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_plan(self, prompt: str) -> Dict[str, Any]:
        """
        Generate a structured plan based on the input prompt.
        Returns a dictionary with either a tool call or a direct answer.
        """
        system_prompt = """You are an AI assistant that helps determine which tool to use for a given query.
        Available tools:
        - weather: Get weather information for a city
        - calc: Perform mathematical calculations
        - fx: Convert between currencies
        
        For each query, respond with a JSON object containing either:
        1. "tool" and "args" for the appropriate tool, or
        2. "answer" with a direct response if no tool is needed
        4. only given format give me not anything if tools available
        5. for curreny use from and to in args
        6. For currency conversion, if in prompt currency is all lower then also  use: {"tool": "fx", "args": {"from": "bdt", "to": "gbp", "amount": 100}}
        7. If two cities then do what it done to prompt
        8.For math args do calculation too
        9. For Math in args a result section should be add where result will be added.
        10. If the user asks to add 10 to the average temperature of multiple cities, use the weather tool with a list of cities.
        11. If propmt is contain a name or thing then find out what is this and summarize that.
        
        Example format:
        {"tool": "weather", "args": {"city": "paris"}}
        or
        {"tool": "weather", "args": {"cities": ["paris", "london"]}}
        or
        {"answer": "The capital of France is Paris"}"""
        
        # Call OpenAI API
        completion = self.client.chat.completions.create(
            model="openai/gpt-4o",
            temperature=0,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse the response
        try:
            content = completion.choices[0].message.content.strip()
            response = json.loads(content)
            if isinstance(response, list):
                for step in response:
                    print("Tool:", step.get("tool"), "Args:", step.get("args"))
                return response
            else:
                return response

            # print("llm response:",response)
            # return response
        except (AttributeError, json.JSONDecodeError) as e:
            # Fallback response if there's an error
            return {"answer": f"I'm having trouble processing that request: {str(e)}"}

# Backward compatibility for existing code
llm = LLM()

def call_llm(prompt: str) -> Dict[str, Any]:
    """Legacy interface for compatibility"""
    return llm.generate_plan(prompt)
