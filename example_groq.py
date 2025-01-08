from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq

load_dotenv()

agent = Agent(
    name="marketing",
    model=Groq(id="llama-3.3-70b-versatile"),
    markdown=True,
)

agent.print_response("Make a short plan to learn making AI Agents."
                     "Consider hands on experience, in-depth topics to explore and frameworks")
