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

@app.route("/api/chat", methods=["GET"])
def get_all_books():
  global GEMINI_API_KEY_COUNTER
  current_key = GEMINI_API_KEY[GEMINI_API_KEY_COUNTER]
  GEMINI_API_KEY_COUNTER = (GEMINI_API_KEY_COUNTER + 1) % len(GEMINI_API_KEY)
  
  script_dir = os.path.dirname(os.path.abspath(__file__))
  skill_path = os.path.abspath(
      os.path.join(script_dir, "../skills")
  )
  
  config = LocalAgentConfig(
    model="gemini-3.1-flash-lite",
    api_key=current_key, 
    skills_paths=[skill_path]
  )
  
  async def run_agent():
    async with Agent(config) as my_agent:
      # Ask the agent what skills it has.
      prompt = "What available skills do you have?"
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
    
