import json
from typing import Any, Dict
from abc import ABC, abstractmethod

class ToolError(Exception):
    """Base class for tool-related errors"""
    pass

class Tool(ABC):
    @abstractmethod
    def execute(self, args: Dict) -> Any:
        pass

class CalculatorTool(Tool):
    def execute(self, args: Dict) -> float:
        if not isinstance(args.get("expr"), (str, int, float)):
            raise ToolError("Invalid expression format")
        try:
            expr = str(args["expr"]).replace(" ", "")
            if any(op in expr for op in "+-*/%"):
                return self._evaluate_math(expr)
            return float(expr)
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
        self._temps = {
            "paris": 18.0,
            "london": 17.0,
            "dhaka": 31.0,
            "amsterdam": 19.5
        }
    
    def execute(self, args: Dict) -> str:
        if not isinstance(args.get("city"), str):
            raise ToolError("City must be a string")
        city = args["city"].strip().lower()
        temp = self._temps.get(city, 20.0)
        return f"{temp}°C"

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
        return "No entry found."

class FxTool(Tool):
    def __init__(self):
        self.rates = {
            ("usd", "eur"): 0.91,
            ("eur", "usd"): 1.1,
            ("usd", "gbp"): 0.79,
            ("gbp", "usd"): 1.27,
        }
    
    def execute(self, args: Dict) -> str:
        required_fields = ["amount", "from", "to"]
        for field in required_fields:
            if field not in args:
                raise ToolError(f"Missing required field: {field}")
        
        try:
            amount = float(args["amount"])
        except:
            raise ToolError("Amount must be a number")
        
        from_currency = args["from"].lower()
        to_currency = args["to"].lower()
        
        rate = self.rates.get((from_currency, to_currency))
        if not rate:
            raise ToolError(f"Unsupported currency pair: {from_currency}/{to_currency}")
        
        converted = round(amount * rate, 2)
        return f"{converted} {to_currency.upper()}"
