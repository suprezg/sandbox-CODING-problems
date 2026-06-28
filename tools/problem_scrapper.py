"""
File Name: problem_scrapper.py
Purpose: Scrapes problem content from competitive programming platforms and uses Gemini API to categorize and format it.
"""
import argparse
import logging
import os
import re
from abc import ABC, abstractmethod
from typing import Literal

from google import genai
from google.genai import types
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

SUPPORTED_SITES = ["Atcoder", "Codeforces", "Leetcode", "Adventofcode", "Codechef"]
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_DIRECTORY = os.path.join(PROJECT_ROOT, "core")
GEMINI_MODEL_NAME = "gemini-2.5-flash"


class ProblemAnalysis(BaseModel):
    """
    [Data structure representing the categorized problem and its markdown content]
    """
    category: str
    title: str
    markdownContent: str


class BaseScraper(ABC):
    """
    [Abstract base class for platform-specific scrapers]
    """

    @abstractmethod
    def extract(self, url: str) -> str:
        """
        [Extracts raw problem text or HTML from the given URL]
        
        Takes:
        	self (BaseScraper): The instance of the scraper.
        	url (str): The URL of the problem.
        
        Gives:
        	str: The raw problem text or HTML.
        """
        pass


class CodeforcesScraper(BaseScraper):
    """
    [Scraper implementation for Codeforces]
    """

    def extract(self, url: str) -> str:
        """
        [Extracts problem content from Codeforces]
        
        Takes:
        	self (CodeforcesScraper): The instance of the scraper.
        	url (str): The Codeforces problem URL.
        
        Gives:
        	str: Extracted problem content.
        """
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        titleNode = soup.select_one(".problem-statement .header .title")
        titleHtml = str(titleNode) if titleNode else ""
        
        statementNode = soup.select_one(".problem-statement")
        if statementNode:
            contentHtml = str(statementNode)
        else:
            contentHtml = str(soup)
            
        return "<h2>Title:</h2>\n" + titleHtml + "\n\n<h2>Problem Content:</h2>\n" + contentHtml


class AtcoderScraper(BaseScraper):
    """
    [Scraper implementation for AtCoder]
    """

    def extract(self, url: str) -> str:
        """
        [Extracts problem content from AtCoder]
        
        Takes:
        	self (AtcoderScraper): The instance of the scraper.
        	url (str): The AtCoder problem URL.
        
        Gives:
        	str: Extracted problem content.
        """
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        titleNode = soup.select_one("span.h2")
        titleHtml = str(titleNode) if titleNode else ""
        
        statementNode = soup.select_one("div#task-statement span.lang-en")
        if statementNode:
            contentHtml = str(statementNode)
        else:
            contentHtml = str(soup)
            
        return "<h2>Title:</h2>\n" + titleHtml + "\n\n<h2>Problem Content:</h2>\n" + contentHtml


class LeetcodeScraper(BaseScraper):
    """
    [Scraper implementation for LeetCode]
    """

    def extract(self, url: str) -> str:
        """
        [Extracts problem content from LeetCode using GraphQL]
        
        Takes:
        	self (LeetcodeScraper): The instance of the scraper.
        	url (str): The LeetCode problem URL.
        
        Gives:
        	str: Extracted problem content.
        """
        titleSlug = url.rstrip("/").split("/")[-1]
        apiUrl = "https://leetcode.com/graphql"
        query = '''
        query questionContent($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                title
                content
            }
        }
        '''
        response = requests.post(apiUrl, json={"query": query, "variables": {"titleSlug": titleSlug}}, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        data = response.json()
        
        if "data" in data and data["data"].get("question"):
            question = data["data"]["question"]
            title = str(question.get("title", ""))
            contentHtml = str(question.get("content", ""))
            return "<h2>Title:</h2>\n<p>" + title + "</p>\n\n<h2>Problem Content:</h2>\n" + contentHtml
        
        return ""


class CodechefScraper(BaseScraper):
    """
    [Scraper implementation for CodeChef]
    """

    def extract(self, url: str) -> str:
        """
        [Extracts problem content from CodeChef using API]
        
        Takes:
        	self (CodechefScraper): The instance of the scraper.
        	url (str): The CodeChef problem URL.
        
        Gives:
        	str: Extracted problem content.
        """
        problemCode = url.rstrip("/").split("/")[-1]
        apiUrl = "https://www.codechef.com/api/contests/PRACTICE/problems/" + problemCode
        response = requests.get(apiUrl, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        data = response.json()
        
        if "body" in data:
            title = str(data.get("problem_name", ""))
            contentHtml = str(data["body"])
            return "<h2>Title:</h2>\n<p>" + title + "</p>\n\n<h2>Problem Content:</h2>\n" + contentHtml
        
        return str(data)


class AdventofcodeScraper(BaseScraper):
    """
    [Scraper implementation for Advent of Code]
    """

    def extract(self, url: str) -> str:
        """
        [Extracts problem content from Advent of Code]
        
        Takes:
        	self (AdventofcodeScraper): The instance of the scraper.
        	url (str): The Advent of Code problem URL.
        
        Gives:
        	str: Extracted problem content.
        """
        headers = {"User-Agent": "Mozilla/5.0"}
        sessionCookie = os.environ.get("AOC_SESSION")
        if sessionCookie:
            headers["Cookie"] = "session=" + sessionCookie
            
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        titleNode = soup.select_one("article.day-desc h2")
        titleHtml = str(titleNode) if titleNode else ""
        
        articles = soup.select("article.day-desc")
        
        if articles:
            contentHtml = "\n".join([str(article) for article in articles])
        else:
            contentHtml = str(soup)
            
        return "<h2>Title:</h2>\n" + titleHtml + "\n\n<h2>Problem Content:</h2>\n" + contentHtml


class ScraperFactory:
    """
    [Factory to instantiate correct scraper]
    """

    @staticmethod
    def createScraper(siteName: str) -> BaseScraper:
        """
        [Creates a scraper instance based on site name]
        
        Takes:
        	siteName (str): Name of the programming platform.
        
        Gives:
        	BaseScraper: A scraper instance for the platform.
        """
        normalizedName = siteName.lower()
        if normalizedName == "codeforces":
            return CodeforcesScraper()
        elif normalizedName == "atcoder":
            return AtcoderScraper()
        elif normalizedName == "leetcode":
            return LeetcodeScraper()
        elif normalizedName == "codechef":
            return CodechefScraper()
        elif normalizedName == "adventofcode":
            return AdventofcodeScraper()
        else:
            raise ValueError("Unsupported site: " + siteName)


def toSnakeCase(title: str) -> str:
    """
    [Generates a snake_case string from a title]
    
    Takes:
    	title (str): The original title.
    
    Gives:
    	str: The snake_case version of the title.
    """
    cleaned = re.sub(r"[^a-zA-Z0-9\s-]", "", title)
    return re.sub(r"\s+", "_", cleaned.strip()).lower()


def analyzeProblem(problemHtml: str) -> ProblemAnalysis:
    """
    [Analyzes problem HTML using Gemini]
    
    Takes:
    	problemHtml (str): Raw problem HTML.
    
    Gives:
    	ProblemAnalysis: Structured analysis result.
    """
    apiKey = os.environ.get("GEMINI_API_KEY")
    if not apiKey:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")
        
    client = genai.Client(api_key=apiKey)
    
    prompt = (
        "You are an expert competitive programming assistant. I will provide you with the HTML of a problem statement.\n"
        "Your task is to analyze it, determine its optimal expected time complexity class out of: "
        "sublinear, linear, polynomial, exponential. "
        "Extract and format the problem into a comprehensive Markdown document.\n\n"
        "Important Guidelines:\n"
        "1. Start your response EXACTLY with these two lines:\n"
        "Category: <complexity_class>\n"
        "Title: <Problem Title>\n\n"
        "2. After those two lines, provide the full Markdown content for the problem. Use the following headers:\n"
        "   # <Problem Title>\n"
        "   ## Statement\n"
        "   ## Constraints\n"
        "   ## Input and Output Instances\n"
        "3. Make the main problem statement description bigger, more detailed, and comprehensive.\n"
        "4. Ensure the constraints are comprehensive, covering all bounds and conditions explicitly.\n"
        "5. Under the 'Input and Output Instances' heading, provide each input instance first, followed immediately by its corresponding output instance, and then a small explanation of why that output was produced. If there are fewer than 3 input/output instances in the HTML, you MUST generate and provide 1-2 more logical examples following the exact same format.\n"
        "6. Do not wrap the output in a JSON block. Return plain Markdown as requested.\n\n"
        f"Problem HTML:\n{problemHtml}"
    )
             
    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=prompt
    )
    
    text = response.text.strip()
    
    categoryMatch = re.search(r"Category:\s*(sublinear|linear|polynomial|exponential)", text, re.IGNORECASE)
    titleMatch = re.search(r"Title:\s*(.+)", text, re.IGNORECASE)
    
    category = categoryMatch.group(1).lower() if categoryMatch else "linear"
    title = titleMatch.group(1).strip() if titleMatch else "unknown_problem"
    
    markdownContent = re.sub(r"^(Category:.*?\nTitle:.*?\n+)", "", text, flags=re.IGNORECASE | re.MULTILINE)
    if markdownContent.startswith("```markdown"):
        markdownContent = markdownContent[11:]
    if markdownContent.startswith("```"):
        markdownContent = markdownContent[3:]
    if markdownContent.endswith("```"):
        markdownContent = markdownContent[:-3]
    markdownContent = markdownContent.strip()
    
    return ProblemAnalysis(category=category, title=title, markdownContent=markdownContent)


def saveProblemFiles(analysisResult: ProblemAnalysis) -> None:
    """
    [Saves the problem data into standard markdown format]
    
    Takes:
    	analysisResult (ProblemAnalysis): The structured problem data.
    
    Gives:
    	None: Does not return anything.
    """
    problemSlug = toSnakeCase(analysisResult.title)
    targetDir = os.path.join(CORE_DIRECTORY, analysisResult.category, problemSlug)
    os.makedirs(targetDir, exist_ok=True)
    
    problemPath = os.path.join(targetDir, "problem.md")
    with open(problemPath, "w", encoding="utf-8") as f:
        f.write(analysisResult.markdownContent)
        
    solutionContent = "# [Naive / Better / Optimal] Solution\n\n" + \
                      "## Idea\n\n" + \
                      "## Pseudocode\n\n" + \
                      "## Analysis\n\n" + \
                      "## Pros and Cons\n"
                      
    solutionPath = os.path.join(targetDir, "solution.md")
    with open(solutionPath, "w", encoding="utf-8") as f:
        f.write(solutionContent)
        
    logging.info("Successfully saved problem to: " + targetDir)


def main() -> None:
    """
    [Main execution function for the scrapper program]
    
    Takes:
    	None: No arguments.
    
    Gives:
    	None: Does not return anything.
    """
    parser = argparse.ArgumentParser(description="Competitive Programming Problem Scrapper")
    parser.add_argument("-s", "--site", type=str, required=True, choices=SUPPORTED_SITES, help="Site name")
    parser.add_argument("-l", "--link", type=str, required=True, help="Problem link")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        
    try:
        logging.info("Starting extraction for " + args.site + ": " + args.link)
        scraper = ScraperFactory.createScraper(args.site)
        rawText = scraper.extract(args.link)
        
        logging.debug("Extracted raw text length: " + str(len(rawText)))
        
        logging.info("Analyzing problem content via Gemini...")
        analysis = analyzeProblem(rawText)
        
        logging.info("Categorized as: " + analysis.category)
        
        saveProblemFiles(analysis)
        
    except Exception as e:
        logging.error("An error occurred: " + str(e))
        if args.verbose:
            logging.exception("Detailed traceback:")


if __name__ == "__main__":
    main()
