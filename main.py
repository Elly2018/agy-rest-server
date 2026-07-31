import asyncio
import os
import sys
from google.antigravity import Agent, LocalAgentConfig
from flask import Flask, jsonify, request
from waitress import serve

app = Flask(__name__)

GEMINI_API_KEY = [key.strip() for key in sys.argv[1].split(',') if key.strip()]
GEMINI_API_KEY_COUNTER = 0
PORT=8080

SYSTEM_INSTRUCTION = """
You are an expert AI software triage agent.
The user will provide an error message or log stacktrace.
The user will provide an file components .
Analyze the issue and respond ONLY with a valid JSON object matching this schema:
{
  "category": "Which buganizer component match with error type",
  "error_type": "What kinda of error is this base on stacktrace and testing title",
  "error_summary": "Brief explanation of what went wrong",
  "root_cause": "Detailed technical root cause",
  "code_snippet": "Corrected code block or command if applicable (or null)"
}
Do NOT include markdown formatting, code fences (like ```json), or conversational text outside the JSON object.
If any of the input is missing, return all the data fullfilled with blank text.
"""

@app.route("/api/triage", methods=["POST"])
def get_all_books():
  global GEMINI_API_KEY_COUNTER
  
  payload = request.get_json(silent=True) or {}
  component_data = payload.get("components")
  test_title = payload.get("test_title")
  stacktrace_data = payload.get("stacktrace")
  
  current_key = GEMINI_API_KEY[GEMINI_API_KEY_COUNTER]
  GEMINI_API_KEY_COUNTER = (GEMINI_API_KEY_COUNTER + 1) % len(GEMINI_API_KEY)
  
  script_dir = os.path.dirname(os.path.abspath(__file__))
  skill_path = os.path.abspath(
      os.path.join(script_dir, "../skills")
  )
  
  config = LocalAgentConfig(
    model="gemini-3.1-flash-lite",
    api_key=current_key, 
    skills_paths=[skill_path],
    enable_google_search=True,
    system_instructions=SYSTEM_INSTRUCTION
  )
  
  async def run_agent():
    async with Agent(config) as my_agent:
      prompt = "Here is the component data:"
      prompt += "\n"
      prompt += component_data
      prompt += "\n"
      prompt += "Here is the test case title:"
      prompt += test_title
      prompt += "\n"
      prompt += "Here is the stacktrace:"
      prompt += stacktrace_data
      
      print(f"  User: {prompt}")

      response = await my_agent.chat(prompt)

      # Await the full aggregated text response.
      response_text = await response.text()
      print(f"  Agent: {response_text}")
      
  try:
      agent_reply = asyncio.run(run_agent())
      return jsonify({
          "success": True,
          "response": agent_reply
      }), 200
  except Exception as e:
      return jsonify({
          "success": False,
          "error": str(e)
      }), 500

if __name__ == "__main__":
    print("Server start: ", PORT)
    asyncio.run(serve(app, host="0.0.0.0", port=PORT))
    
