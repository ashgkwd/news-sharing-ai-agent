
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.google import Gemini

load_dotenv()


agent = Agent(
    model=Gemini(id="gemini-1.5-flash"),
    markdown=True,
)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story.")
# print(run.content)

# Print the response in the terminal
agent.print_response(
    "Give one week actionable plan for spreading word about open source project")

# For reference, sample output is stored in image at example_gemini.png
