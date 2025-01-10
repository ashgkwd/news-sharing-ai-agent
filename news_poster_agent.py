import datetime
from typing import Optional

from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.workflow import RunResponse
from pydantic import BaseModel, Field

from aal import Aal

load_dotenv()


class NewsArticle(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    published_at: str = Field(..., description="Date of the article")
    body: Optional[str] = Field(..., alias="body",
                                description="Body of the article. Use title is body is not available")


class SearchResults(BaseModel):
    articles: list[NewsArticle]


today = datetime.datetime.now().strftime("%d %b %Y")
sources = """techradar.com
wired.com
technologyreview.com
nvidianews.nvidia.com
blogs.microsoft.com
nbcnews.com
reuters.com
aboutamazon.com
investopedia.com
techopedia.com
techcrunch.com
venturebeat.com
edition.cnn.com
businesswire.com
wsj.com
bbc.com"""

news_agent = Agent(
    name="News Agent",
    tools=[DuckDuckGo()],
    instructions=["Given a date, search 25 relevant news on 'AI Agent' topic. ",
                  "Pick at least 15 most relevant ones out of those who has 'AI Agent' words in the title and body. ",
                  f"Prefer news from sources: {sources}",
                  "Exclude negative news about violence, not suitable for work, abuse or other safety voilations. ",
                  "Only output url to articles, date of publishing and headings."],
    model=Groq(id="llama-3.3-70b-versatile", response_format={"type": "text"}),
    response_model=SearchResults
)


def fetch_news():
    news_response: RunResponse = news_agent.run(today)
    for a in news_response.content.articles:
        print(a.title)
        print(a.published_at)
        print(a.url)
        print(a.body)
        print(" ")
    return news_response.content.articles


def main():
    articles = fetch_news()
    aal = Aal(login=True)
    aal.share_news(articles)
    # Alternatively, share via email or slack or telegram


if __name__ == "__main__":
    main()
