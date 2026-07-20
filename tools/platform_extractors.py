"""
File Name: platform_extractors.py
Purpose: Extracts problem content from competitive programming platforms.
"""
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

class BaseExtractor(ABC):
    """
    [Abstract base class for platform-specific extractors]
    """

    def _fetchHtml(self, url: str) -> str:
        """
        [Fetches HTML content from a URL using a headless browser with Cloudflare bypass]
        
        Takes:
        	self (BaseExtractor): The instance of the extractor.
        	url (str): The URL to fetch.
        
        Gives:
        	str: The extracted HTML content.
        """
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            page.goto(url)
            page.wait_for_timeout(3000)
            html = page.content()
            browser.close()
            return html

    def _cleanHtml(self, soup: BeautifulSoup) -> None:
        """
        [Cleans HTML by removing scripts, styles, and inline style attributes]
        
        Takes:
        	self (BaseExtractor): The instance of the extractor.
        	soup (BeautifulSoup): The parsed HTML tree to clean.
        
        Gives:
        	None: Modifies the soup in-place.
        """
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
            
        for tag in soup.find_all(style=True):
            del tag['style']

    @abstractmethod
    def extract(self, url: str) -> str:
        """
        [Extracts raw problem text or HTML from the given URL]
        
        Takes:
        	self (BaseExtractor): The instance of the extractor.
        	url (str): The URL of the problem.
        
        Gives:
        	dict: The extracted data containing at least the 'html' key.
        """
        pass

class CodeforcesExtractor(BaseExtractor):
    """
    [Extractor implementation for Codeforces]
    """

    def extract(self, url: str) -> dict:
        """
        [Extracts problem content from Codeforces]
        
        Takes:
        	self (CodeforcesExtractor): The instance of the extractor.
        	url (str): The Codeforces problem URL.
        
        Gives:
        	dict: Extracted problem content and metadata.
        """
        html = self._fetchHtml(url)
        soup = BeautifulSoup(html, "html.parser")
        self._cleanHtml(soup)
        
        titleNode = soup.select_one(".problem-statement .header .title")
        titleHtml = str(titleNode) if titleNode else ""
        
        statementNode = soup.select_one(".problem-statement")
        if statementNode:
            contentHtml = str(statementNode)
        else:
            contentHtml = str(soup)
            
        import re
        contestMatch = re.search(r"(?:problemset/problem|contest)/(\d+)/([A-Za-z0-9]+)", url)
        contestNumber = contestMatch.group(1) if contestMatch else "unknown_contest"
        questionChar = contestMatch.group(2) if contestMatch else "unknown_question"
            
        finalHtml = "<h2>Title:</h2>\n" + titleHtml + "\n\n<h2>Problem Content:</h2>\n" + contentHtml
        return {
            "html": finalHtml,
            "contestNumber": contestNumber,
            "questionChar": questionChar
        }

class AtcoderExtractor(BaseExtractor):
    """
    [Extractor implementation for AtCoder]
    """

    def extract(self, url: str) -> dict:
        """
        [Extracts problem content from AtCoder]
        
        Takes:
        	self (AtcoderExtractor): The instance of the extractor.
        	url (str): The AtCoder problem URL.
        
        Gives:
        	dict: Extracted problem content.
        """
        html = self._fetchHtml(url)
        soup = BeautifulSoup(html, "html.parser")
        self._cleanHtml(soup)
        
        titleNode = soup.select_one("span.h2")
        titleHtml = str(titleNode) if titleNode else ""
        
        statementNode = soup.select_one("div#task-statement span.lang-en")
        if statementNode:
            contentHtml = str(statementNode)
        else:
            contentHtml = str(soup)
            
        import re
        # Example url: https://atcoder.jp/contests/abc467/tasks/abc467_a
        match = re.search(r"contests/([a-zA-Z]+)(\d+)/tasks/(?:[a-zA-Z0-9]+_)?([a-zA-Z0-9]+)", url)
        contestName = match.group(1).lower() if match else "unknown"
        contestNumber = match.group(2) if match else "0"
        questionChar = match.group(3).upper() if match else "UNKNOWN"
            
        finalHtml = "<h2>Title:</h2>\n" + titleHtml + "\n\n<h2>Problem Content:</h2>\n" + contentHtml
        return {
            "html": finalHtml,
            "contestName": contestName,
            "contestNumber": contestNumber,
            "questionChar": questionChar
        }

class LeetcodeExtractor(BaseExtractor):
    """
    [Extractor implementation for LeetCode]
    """

    def extract(self, url: str) -> dict:
        """
        [Extracts problem content from LeetCode using HTML extraction]
        
        Takes:
        	self (LeetcodeExtractor): The instance of the extractor.
        	url (str): The LeetCode problem URL.
        
        Gives:
        	dict: Extracted problem content.
        """
        html = self._fetchHtml(url)
        soup = BeautifulSoup(html, "html.parser")
        self._cleanHtml(soup)
        
        titleNode = soup.select_one("div.text-title-large")
        if not titleNode:
            titleNode = soup.select_one("title")
            
        titleText = titleNode.text.strip() if titleNode else ""
        titleHtml = str(titleNode) if titleNode else ""
        
        import re
        match = re.match(r"^(\d+)\.", titleText)
        questionId = match.group(1) if match else "0"
        
        statementNode = soup.select_one("div[data-track-load='description_content']")
        if statementNode:
            contentHtml = str(statementNode)
        else:
            contentHtml = str(soup.find("body") or soup)
            
        finalHtml = "<h2>Title:</h2>\n" + titleHtml + "\n\n<h2>Problem Content:</h2>\n" + contentHtml
        return {
            "html": finalHtml,
            "questionId": questionId
        }

class CodechefExtractor(BaseExtractor):
    """
    [Extractor implementation for CodeChef]
    """

    def extract(self, url: str) -> dict:
        """
        [Extracts problem content from CodeChef using HTML extraction]
        
        Takes:
        	self (CodechefExtractor): The instance of the extractor.
        	url (str): The CodeChef problem URL.
        
        Gives:
        	dict: Extracted problem content.
        """
        html = self._fetchHtml(url)
        soup = BeautifulSoup(html, "html.parser")
        self._cleanHtml(soup)
        
        statementNode = soup.select_one("#problem-statement")
        if statementNode:
            titleNode = statementNode.select_one("h3.notranslate")
            titleHtml = str(titleNode) if titleNode else ""
            contentHtml = str(statementNode)
        else:
            titleHtml = ""
            contentHtml = str(soup)
            
        import re
        match = re.search(r"problems/([a-zA-Z0-9_]+)", url)
        questionCode = match.group(1) if match else "UNKNOWN"
        
        questionDifficulty = "0"
        diffSpan = soup.find(string=re.compile(r"Difficulty:", re.IGNORECASE))
        if diffSpan and diffSpan.parent:
            sibling = diffSpan.parent.find_next_sibling("span")
            if sibling:
                questionDifficulty = sibling.text.strip()
                
        finalHtml = "<h2>Title:</h2>\n" + titleHtml + "\n\n<h2>Problem Content:</h2>\n" + contentHtml
        return {
            "html": finalHtml,
            "questionCode": questionCode,
            "questionDifficulty": questionDifficulty
        }

class AdventofcodeExtractor(BaseExtractor):
    """
    [Extractor implementation for Advent of Code]
    """

    def extract(self, url: str) -> dict:
        """
        [Extracts problem content from Advent of Code]
        
        Takes:
        	self (AdventofcodeExtractor): The instance of the extractor.
        	url (str): The Advent of Code problem URL.
        
        Gives:
        	dict: Extracted problem content.
        """
        html = self._fetchHtml(url)
        soup = BeautifulSoup(html, "html.parser")
        self._cleanHtml(soup)
        
        titleNode = soup.select_one("article.day-desc h2")
        titleHtml = str(titleNode) if titleNode else ""
        
        articles = soup.select("article.day-desc")
        
        if articles:
            contentHtml = "\n".join([str(article) for article in articles])
        else:
            contentHtml = str(soup)
            
        import re
        match = re.search(r"adventofcode\.com/(\d+)/day/(\d+)", url)
        year = match.group(1) if match else "0"
        day = match.group(2) if match else "0"
            
        finalHtml = "<h2>Title:</h2>\n" + titleHtml + "\n\n<h2>Problem Content:</h2>\n" + contentHtml
        return {
            "html": finalHtml,
            "year": year,
            "day": day
        }

class ExtractorFactory:
    """
    [Factory to instantiate correct extractor]
    """

    @staticmethod
    def createExtractor(siteName: str) -> BaseExtractor:
        """
        [Creates an extractor instance based on site name]
        
        Takes:
        	siteName (str): Name of the programming platform.
        
        Gives:
        	BaseExtractor: An extractor instance for the platform.
        """
        normalizedName = siteName.lower()
        if normalizedName == "codeforces":
            return CodeforcesExtractor()
        elif normalizedName == "atcoder":
            return AtcoderExtractor()
        elif normalizedName == "leetcode":
            return LeetcodeExtractor()
        elif normalizedName == "codechef":
            return CodechefExtractor()
        elif normalizedName == "adventofcode":
            return AdventofcodeExtractor()
        else:
            raise ValueError("Unsupported site: " + siteName)
