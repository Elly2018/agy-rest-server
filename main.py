import asyncio
import os
import sys
from google.antigravity import Agent, LocalAgentConfig

GEMINI_API_KEY = sys.argv[1]

print(GEMINI_API_KEY)

async def main() -> None:
    # Let's get a little meta: We are loading the real 'google-antigravity-sdk' skill
    # that teaches this agent how to build with the very SDK it is running on! 🧠
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_path = os.path.abspath(
        os.path.join(script_dir, "../skills")
    )

    print(f"  Loading skills from: {skill_path}")

    # Configure the agent with the skills path.
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
    asyncio.run(main())
