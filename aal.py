import os

import requests
from bs4 import BeautifulSoup

# TODO: update Aal class to work as tools with phidata


class Aal:
    def __init__(self, login=False):
        self.base_url = os.getenv("AAL_BASE_URL")
        self.session = requests.Session()
        self.session.headers.update({"Referer": self.base_url})
        self.creds = {
            "email_address": os.getenv("AAL_EMAIL"),
            "password": os.getenv("AAL_PASSWORD")
        }
        if login:
            self.login()

    def csrf_from_url(self, url):
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        csrf_token = soup.find('meta', attrs={'name': 'csrf-token'})['content']
        return csrf_token

    def login(self) -> bool:
        headers = {
            "Content-Type": "application/json",
            "X-CSRF-Token": self.csrf_from_url(f"{self.base_url}/session/new")
        }
        response = self.session.post(
            f"{self.base_url}/session.json", json=self.creds, headers=headers)

        if 200 <= response.status_code < 400:
            print("Login successful", response.status_code)
            return True
        else:
            print("Login failed", response.status_code, response.text)
            return False

    def fetch_existing_news_titles(self, count=50) -> list:
        """Use this method to avoid re-posting a news that's already on the platform"""
        response = self.session.get(
            f"{self.base_url}/news.json?count={count}&only=title")

        if 200 <= response.status_code < 400:
            print("Successfully fetched existing news", response.status_code)
            return [x["title"] for x in response.json()]
        else:
            print("Failed to fetch existing news",
                  response.status_code, response.text)
            return []

    def share_news(self, articles: list) -> bool:
        existing_titles = self.fetch_existing_news_titles()
        headers = {
            "Content-Type": "application/json",
            "X-CSRF-Token": self.csrf_from_url(f"{self.base_url}/news")
        }
        for a in articles:
            if a.title in existing_titles:
                continue
            payload = {
                "news": {
                    "title": a.title,
                    "published_at": a.published_at,
                    "description": a.body,
                    "website": a.url
                }
            }
            response = self.session.post(
                f"{self.base_url}/news.json", json=payload, headers=headers)

            if response.status_code > 299:
                print("Failed to create a news:",
                      response.status_code, response.text)
                return False
            else:
                print("Created a news article with title:",
                      a.title, response.status_code)
        return True
