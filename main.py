import asyncio
import os
import sys
from google.antigravity import Agent, LocalAgentConfig
from flask import Flask, jsonify, request

app = Flask(__name__)

GEMINI_API_KEY = sys.argv[1].split(',')

print(GEMINI_API_KEY)

@app.route("/api/chat", methods=["GET"])
async def get_all_books():
  script_dir = os.path.dirname(os.path.abspath(__file__))
  skill_path = os.path.abspath(
      os.path.join(script_dir, "../skills")
  )
  
  config = LocalAgentConfig(
    model="gemini-3.1-flash-lite",
    api_key=GEMINI_API_KEY, 
    skills_paths=[skill_path]
  )
  
  async with Agent(config) as my_agent:
    # Ask the agent what skills it has.
    prompt = "What available skills do you have?"
    print(f"  User: {prompt}")

    response = await my_agent.chat(prompt)

    # Await the full aggregated text response.
    response_text = await response.text()
    print(f"  Agent: {response_text}")

if __name__ == "__main__":
    asyncio.run(app.run(debug=True, port=8080))
    
