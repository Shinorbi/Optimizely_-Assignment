from .llm import call_llm
from .tools import Tool, ToolError
import abc
import json
from typing import Any, Dict, List, Optional, Union

from .tools import CalculatorTool, WeatherTool, KBTool, FxTool

class ToolRegistry:
    def __init__(self):
        self.tools = {
            "calc": CalculatorTool(),
            "weather": WeatherTool(),
            "kb": KBTool(),
            "fx": FxTool()
        }
    
    def get_tool(self, name: str) -> Optional[Tool]:
        return self.tools.get(name)
    
    def execute_tool(self, tool_name: str, args: Dict) -> Any:
        tool = self.get_tool(tool_name)
        if not tool:
            raise ToolError(f"Unknown tool: {tool_name}")
        
        try:
            return tool.execute(args)
        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"Tool execution error: {str(e)}")

class Agent:
    def __init__(self):
        self.tool_registry = ToolRegistry()
    
    def run(self, query: str) -> str:
        try:
            print("plan", query)
            plan = call_llm(query)
            
            if isinstance(plan, dict) and "tool" in plan:
                tool_name = plan["tool"]
                args = plan.get("args", {})
                result = self.tool_registry.execute_tool(tool_name, args)
                return str(result)
            
            return str(plan)
        except ToolError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"System error: {str(e)}"

# Backward compatibility for existing code
tool_registry = ToolRegistry()
def answer(q: str) -> str:
    return Agent().run(q)
