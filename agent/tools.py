import json
import string
from typing import Any, Dict
from abc import ABC, abstractmethod
import requests
from dotenv import load_dotenv
from typing import Dict
import os

from agent.llm import LLM

def get_weather(city: str, api_key: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    temp = data["main"]["temp"]
    condition = data["weather"][0]["description"]
    return f"{city.title()}: {temp}°C, {condition}"


class ToolError(Exception):
    """Base class for tool-related errors"""
    pass

class Tool(ABC):
    @abstractmethod
    def execute(self, args: Dict) -> Any:
        pass

class CalculatorTool(Tool):
    def execute(self, args: Dict) -> string:
        # if not isinstance(args.get("result"), (str, int, float)):
        #     raise ToolError("Invalid expression format")
        try:
            # expr = str(args["expr"]).replace(" ", "")
            # if any(op in expr for op in "+-*/%"):
            #     return self._evaluate_math(expr)
            return args.get("result")
        except Exception as e:
            raise ToolError(f"Calculation error: {str(e)}")

    def _evaluate_math(self, expr: str) -> float:
        try:
            # Handle percentages with "of" (e.g., "12.5% of 243")
            if "%" in expr:
                expr = expr.replace(" ", "")  # Remove spaces for consistent parsing
                if "%of" in expr:
                    percent, value = expr.split("%of")
                    return (float(percent) / 100) * float(value)
                # Handle cases like "15%of300" or "15% of300"
                elif "%of" in expr.replace("of", "%of"):  # Handle missing space after %
                    expr = expr.replace("of", "%of").replace(" ", "")
                    percent, value = expr.split("%of")
                    return (float(percent) / 100) * float(value)
            
            # Handle basic arithmetic with percentages
            return float(eval(expr.replace("%", "/100*")))
        except ValueError as e:
            raise ToolError(f"Invalid numeric value in expression: {str(e)}")
        except SyntaxError as e:
            raise ToolError(f"Invalid mathematical syntax: {str(e)}")
        except Exception as e:
            raise ToolError(f"Calculation error: {str(e)}")

class WeatherTool(Tool):
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("WEATHER_API_KEY")
        if not self.api_key:
            raise ToolError("Missing WEATHER_API_KEY in environment")

        self._temps = {
            "paris": 18.0,
            "london": 17.0,
            "dhaka": 31.0,
            "amsterdam": 19.5
        }
    
    def execute(self, args: Dict) -> str:
        city = args.get("city")
        cities = args.get("cities")

        if not city and not cities:
            raise ToolError("City or cities must be provided")

        temperatures = []
        conditions = []

        if city:
            cities = [city]

        for city in cities:
            try:
                url = f"http://api.weatherapi.com/v1/current.json?key={self.api_key}&q={city}"
                response = requests.get(url)
                data = response.json()

                if "error" in data:
                    raise ToolError(data["error"].get("message", "Unknown error"))

                temp = data["current"]["temp_c"]
                data_new = data["current"]["condition"]["text"]
                temperatures.append(temp)
                conditions.append(data_new)
            except Exception as e:
                raise ToolError(f"Weather API error for {city}: {str(e)}")

        if not temperatures:
            raise ToolError("No temperature data found for the provided cities")

        if len(temperatures) == 1:
            return f"{cities[0].title()}: {temperatures[0]}°C Condition:{conditions[0]}"

        average_temp = sum(temperatures) / len(temperatures)
        average_temp += 10  # Add 10 to the average temperature

        return f"Average temperature for {', '.join([city.title() for city in cities])} + 10 is: {average_temp}°C"
class KBTool(Tool):
    def __init__(self):
        try:
            with open("data/kb.json", "r") as f:
                self.data = json.load(f)
        except Exception as e:
            self.data = {"entries": []}
            raise ToolError(f"KB initialization error: {str(e)}")
    
    def execute(self, args: Dict) -> str:
        if not isinstance(args.get("q"), str):
            raise ToolError("Query must be a string")
        
        query = args["q"].strip().lower()
        for item in self.data.get("entries", []):
            if query in item.get("name", "").lower():
                return item.get("summary", "")
            else:
                llm = LLM()
                return llm.generate_plan(args.get("q"))
        return "No entry found."

class FxTool(Tool):
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("FX_KEY")
    
    def execute(self, args: Dict) -> str:
        required_fields = ["amount", "from", "to"]
        for field in required_fields:
            if field not in args:
                raise ToolError(f"Missing required field: {field}")
        from_currency = args["from"].upper()
        to_currency= args["to"].upper()
        try:
            url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/latest/{args['from']}"
            response = requests.get(url)
            data = response.json()
            amount = float(args["amount"])
            print("AMount:",amount)
        except:
            raise ToolError("Amount must be a number")
        rate = data["conversion_rates"][to_currency]
        if not rate:
            raise ToolError(f"Unsupported currency pair: {from_currency}/{to_currency}")
        
        converted = round(amount * rate, 2)
        return f"{converted} {to_currency.upper()}"
