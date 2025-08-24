# Refactor & Extend: Simple Tool-Using Agent

**Goal:** Turn a brittle, partially working agent into production-quality code, then extend it with a new tool and real tests.

---
You must **refactor for robustness**, **add one new tool** (translator / unit converter), and **add proper tests**.
---

## Your Tasks (Summary)

1. **Refactor**
2. **Improve**
3. **Add ONE new tool** 
4. **Write tests**
5. **Improve Documentation**

See the assignment brief for full details (shared in the job post).

---

## Quick Start

### Python 3.10+ recommended

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
python main.py "What is 12.5% of 243?"
python main.py "Summarize today's weather in Paris in 3 words"
python main.py "Who is Ada Lovelace?"
python main.py "Add 10 to the average temperature in Paris and London right now."
```

### Test

```bash
pytest -q
```

> Note: The fake LLM sometimes emits malformed JSON to simulate real-world flakiness.

---

## What we expect you to change

- Split responsibilities into modules/classes.
- Add a schema for tool plans; validate inputs and tool names.
- Make tool calls resilient and typed;
- Add one new tool and tests that prove your design is extensible.
- Update this README with an architecture diagram (ASCII ok) and clear instructions.
- You can use Real LLMs or a fake one, but ensure your code is robust against malformed responses.

Good luck & have fun!

## My Updates
#🚀Features
- 🔍 Natural language prompt interpretation via OpenAI (via OpenRouter)
- 🛠️ Built-in tools (Weather, Currency Conversion, Math) in one file
- 🧠 Structured plan generation using LLM
- 🧪 Unit-tested with pytest
- 📦 Easily extensible architecture

# 🏗️ Architecture Diagram

```
+----------------------------+
|        User Prompt         |
+----------------------------+
              ↓
+----------------------------+
|     LLM.generate_plan()    |  ← Interacts with OpenAI via OpenRouter
+----------------------------+
              ↓
+----------------------------+
|   Structured JSON Plan     |  ← Contains ordered tool calls
+----------------------------+
              ↓
+----------------------------+
|     Tool Dispatcher        |  ← Parses plan and routes to tools
+----------------------------+
              ↓
+----------------------------+
|        tools.py            |  ← Contains all tool logic
+----------------------------+
      ↓        ↓        ↓
+--------+ +--------+ +--------+
| Weather| |  Calc  | |   Fx   | ← Tool classes inside tools.py / if knowledge base then llm deals with it.
+--------+ +--------+ +--------+
              ↓
+----------------------------+
|     Final Answer Output    |

```   


# 🔁 Code Flow
- User Input: A natural language prompt is passed to main.py.
- LLM Planning: LLM.generate_plan() sends the prompt to OpenAI and receives a structured JSON plan.
- Tool Dispatching: Each step in the plan is routed to the appropriate class in tools.py.
- Tool Execution: Tools fetch data (e.g., weather, currency rates) or compute results.
- Response Assembly: Final output is constructed and returned to the user.


# 🧩 Tool Details (All in tools.py)
```
| Tool | Description  
| WeatherTool | Fetches weather data for cities |
| CalcTool | Evaluates math expressions |
| FxTool | Converts currency | 
| KbTool | Knowledge Based Tool|
```


# 🧪 Testing
Run all tests using:
python -m pytest tests/test_smoke.py -v 

# 📚 Example Prompt
- Prompt:
"Convert 1000 usd to bdt "


Result from console:
 PS E:\se1-agent-debug-assignment2\se1-agent-debug-assignment> python main.py "Convert 1000 usd to bdt " 
Convert 1000 usd to bdt 
plan Convert 1000 usd to bdt 
AMount: 1000.0
121598.4 BDT

- Another Prompt:
Add 10 to the average temperature in Sylhet and Dhaka right now. "

Result:
(.venv) PS E:\se1-agent-debug-assignment2\se1-agent-debug-assignment> python main.py "Add 10 to the average temperature in Sylhet and Dhaka right now. "<br>
Add 10 to the average temperature in Sylhet and Dhaka right now. <br>
plan Add 10 to the average temperature in Sylhet and Dhaka right now. <br>
Average temperature for Sylhet, Dhaka + 10 is: 37.6°C<br>

- Another Prompt:
"Weather in Sylhet right now. "

Result:
 PS E:\se1-agent-debug-assignment2\se1-agent-debug-assignment> python main.py "Weather in Sylhet right now. "<br>       
Weather in Sylhet right now. <br>
plan Weather in Sylhet right now.<br> 
Sylhet: 26.2°C Condition:Light rain shower



