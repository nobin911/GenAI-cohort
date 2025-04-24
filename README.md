# Md file for weather_cursor.py file

# 🧠 AI Assistant with Tool-Use Capabilities (Weather + System Commands)

This is a simple interactive AI assistant built using OpenAI's SDK and Gemini models. It follows a **Plan-Action-Observe** reasoning pattern to solve user queries using **tool calls**. The assistant can:
- 🌤️ Get real-time weather data for any city using `wttr.in`
- 🖥️ Run system commands on a Windows machine

---

## ✨ Features

- Uses Google's Gemini model through OpenAI-compatible API.
- Follows a structured step-by-step reasoning process (Plan → Action → Observe → Output).
- Supports two tools:
  - `get_weather`: Get weather for any city.
  - `run_command`: Execute system shell commands (Windows only).

---

## ⚙️ How It Works

1. **User inputs a question.**
2. AI plans the steps needed to answer the question.
3. It selects a tool based on the plan and calls it.
4. It observes the result of the tool's output.
5. Finally, it responds to the user with the resolved query.

---

## 🛠 Available Tools

| Tool         | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| `get_weather`| Takes a city name and returns the current weather. Uses `wttr.in` API.     |
| `run_command`| Takes a shell command and runs it on a Windows OS. Returns the command output. |

---

## 🧪 Example Interaction

**User:** What is the weather of New York?  
**Output:**
```json
{"step":"plan","content":"The user is interested in weather data of New York"}
{"step":"plan","content":"From the available tools I should call get_weather"}
{"step":"action","function":"get_weather","input":"New York"}
{"step":"observe","output":"☀️ +15°C"}
{"step":"output","content":"The current weather of New York seems to be ☀️ +15°C."}
