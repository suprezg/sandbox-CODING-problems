"""
File Name: directory_manager.py
Purpose: Manages creating directories and saving markdown files based on platform rules.
"""
import os
from abc import ABC, abstractmethod

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class BaseDirManager(ABC):
    """
    [Abstract base class for directory managers]
    """
    @abstractmethod
    def save(self, extractedData: dict, markdownContent: str) -> None:
        """
        [Saves the problem data into standard markdown format at proper locations]
        
        Takes:
        	extractedData (dict): Data extracted from platform.
        	markdownContent (str): The structured problem data in markdown.
        
        Gives:
        	None: Does not return anything.
        """
        pass

class CodeforcesDirManager(BaseDirManager):
    """
    [Directory Manager for Codeforces]
    """
    def save(self, extractedData: dict, markdownContent: str) -> None:
        """
        [Saves the Codeforces problem data following the sharding strategy]
        
        Takes:
        	extractedData (dict): Codeforces specific extracted data.
        	markdownContent (str): The structured problem data in markdown.
        
        Gives:
        	None: Does not return anything.
        """
        cfDir = os.path.join(PROJECT_ROOT, "codeforces")
        os.makedirs(cfDir, exist_ok=True)
        
        contestStr = extractedData.get("contestNumber", "0")
        questionChar = extractedData.get("questionChar", "unknown")
        
        try:
            contestNum = int(contestStr)
        except ValueError:
            contestNum = 0
            
        start = ((contestNum - 1) // 500) * 500 + 1 if contestNum > 0 else 0
        if start == 1:
            rangeStr = "000-500"
        elif start == 0:
            rangeStr = "unknown_range"
        else:
            rangeStr = f"{start}-{start+499}"
            
        rangeDir = os.path.join(cfDir, rangeStr)
        os.makedirs(rangeDir, exist_ok=True)
        
        contestDir = os.path.join(rangeDir, str(contestNum))
        os.makedirs(contestDir, exist_ok=True)
        
        questionDir = os.path.join(contestDir, questionChar)
        os.makedirs(questionDir, exist_ok=True)
        
        problemPath = os.path.join(questionDir, "problem.md")
        with open(problemPath, "w", encoding="utf-8") as f:
            f.write(markdownContent)
            
        solutionPath = os.path.join(questionDir, "solution.md")
        if not os.path.exists(solutionPath):
            solutionContent = "# [Naive / Better / Optimal] Solution\n\n## Idea\n\n## Pseudocode\n\n### Solver\n\n### Verifier\n\n## Analysis\n\n### Time Complexity\n\n### Space Complexity\n\n## Pros and Cons\n"
            with open(solutionPath, "w", encoding="utf-8") as f:
                f.write(solutionContent)
        
        import logging
        logging.info("Successfully saved Codeforces problem to: " + questionDir)


class AtcoderDirManager(BaseDirManager):
    """
    [Directory Manager for AtCoder]
    """
    def save(self, extractedData: dict, markdownContent: str) -> None:
        """
        [Saves the AtCoder problem data]
        
        Takes:
        	extractedData (dict): AtCoder specific extracted data.
        	markdownContent (str): The structured problem data in markdown.
        
        Gives:
        	None: Does not return anything.
        """
        atDir = os.path.join(PROJECT_ROOT, "atcoder")
        os.makedirs(atDir, exist_ok=True)
        
        contestName = extractedData.get("contestName", "unknown")
        contestStr = extractedData.get("contestNumber", "0")
        questionChar = extractedData.get("questionChar", "UNKNOWN")
        
        contestNameDir = os.path.join(atDir, contestName.upper())
        os.makedirs(contestNameDir, exist_ok=True)
        
        try:
            contestNum = int(contestStr)
        except ValueError:
            contestNum = 0
            
        interval = 50
        if contestName.lower() in ["agc", "awc"]:
            interval = 10
            
        start = (contestNum // interval) * interval
        end = start + interval
        rangeStr = f"{start}-{end}"
        
        rangeDir = os.path.join(contestNameDir, rangeStr)
        os.makedirs(rangeDir, exist_ok=True)
        
        contestNumDir = os.path.join(rangeDir, str(contestNum))
        os.makedirs(contestNumDir, exist_ok=True)
        
        questionDir = os.path.join(contestNumDir, questionChar)
        os.makedirs(questionDir, exist_ok=True)
        
        problemPath = os.path.join(questionDir, "problem.md")
        with open(problemPath, "w", encoding="utf-8") as f:
            f.write(markdownContent)
            
        solutionPath = os.path.join(questionDir, "solution.md")
        if not os.path.exists(solutionPath):
            solutionContent = "# [Naive / Better / Optimal] Solution\n\n## Idea\n\n## Pseudocode\n\n### Solver\n\n### Verifier\n\n## Analysis\n\n### Time Complexity\n\n### Space Complexity\n\n## Pros and Cons\n"
            with open(solutionPath, "w", encoding="utf-8") as f:
                f.write(solutionContent)
                
        import logging
        logging.info("Successfully saved AtCoder problem to: " + questionDir)


class LeetcodeDirManager(BaseDirManager):
    """
    [Directory Manager for LeetCode]
    """
    def save(self, extractedData: dict, markdownContent: str) -> None:
        """
        [Saves the LeetCode problem data]
        
        Takes:
        	extractedData (dict): LeetCode specific extracted data.
        	markdownContent (str): The structured problem data in markdown.
        
        Gives:
        	None: Does not return anything.
        """
        lcDir = os.path.join(PROJECT_ROOT, "leetcode")
        os.makedirs(lcDir, exist_ok=True)
        
        questionIdStr = extractedData.get("questionId", "0")
        try:
            questionId = int(questionIdStr)
        except ValueError:
            questionId = 0
            
        start = ((questionId - 1) // 500) * 500 + 1 if questionId > 0 else 0
        if start == 1:
            rangeStr = "0-500"
        elif start == 0:
            rangeStr = "unknown_range"
        else:
            rangeStr = f"{start}-{start+499}"
            
        rangeDir = os.path.join(lcDir, rangeStr)
        os.makedirs(rangeDir, exist_ok=True)
        
        questionDir = os.path.join(rangeDir, str(questionId))
        os.makedirs(questionDir, exist_ok=True)
        
        problemPath = os.path.join(questionDir, "problem.md")
        with open(problemPath, "w", encoding="utf-8") as f:
            f.write(markdownContent)
            
        solutionPath = os.path.join(questionDir, "solution.md")
        if not os.path.exists(solutionPath):
            solutionContent = "# [Naive / Better / Optimal] Solution\n\n## Idea\n\n## Pseudocode\n\n### Solver\n\n### Verifier\n\n## Analysis\n\n### Time Complexity\n\n### Space Complexity\n\n## Pros and Cons\n"
            with open(solutionPath, "w", encoding="utf-8") as f:
                f.write(solutionContent)
                
        import logging
        logging.info("Successfully saved LeetCode problem to: " + questionDir)


class CodechefDirManager(BaseDirManager):
    """
    [Directory Manager for CodeChef]
    """
    def save(self, extractedData: dict, markdownContent: str) -> None:
        """
        [Saves the CodeChef problem data]
        
        Takes:
        	extractedData (dict): CodeChef specific extracted data.
        	markdownContent (str): The structured problem data in markdown.
        
        Gives:
        	None: Does not return anything.
        """
        ccDir = os.path.join(PROJECT_ROOT, "codechef")
        os.makedirs(ccDir, exist_ok=True)
        
        questionCode = extractedData.get("questionCode", "UNKNOWN")
        difficultyStr = extractedData.get("questionDifficulty", "0")
        
        try:
            difficulty = int(difficultyStr)
        except ValueError:
            difficulty = 0
            
        start = ((difficulty - 1) // 500) * 500 + 1 if difficulty > 0 else 0
        if start == 1:
            rangeStr = "0-500"
        elif start == 0:
            rangeStr = "unknown_range"
        else:
            rangeStr = f"{start}-{start+499}"
            
        rangeDir = os.path.join(ccDir, rangeStr)
        os.makedirs(rangeDir, exist_ok=True)
        
        dirName = f"{difficulty}_{questionCode}"
        questionDir = os.path.join(rangeDir, dirName)
        os.makedirs(questionDir, exist_ok=True)
        
        problemPath = os.path.join(questionDir, "problem.md")
        with open(problemPath, "w", encoding="utf-8") as f:
            f.write(markdownContent)
            
        solutionPath = os.path.join(questionDir, "solution.md")
        if not os.path.exists(solutionPath):
            solutionContent = "# [Naive / Better / Optimal] Solution\n\n## Idea\n\n## Pseudocode\n\n### Solver\n\n### Verifier\n\n## Analysis\n\n### Time Complexity\n\n### Space Complexity\n\n## Pros and Cons\n"
            with open(solutionPath, "w", encoding="utf-8") as f:
                f.write(solutionContent)
                
        import logging
        logging.info("Successfully saved CodeChef problem to: " + questionDir)


class AdventofcodeDirManager(BaseDirManager):
    """
    [Directory Manager for Advent of Code]
    """
    def save(self, extractedData: dict, markdownContent: str) -> None:
        """
        [Saves the Advent of Code problem data]
        
        Takes:
        	extractedData (dict): Advent of Code specific extracted data.
        	markdownContent (str): The structured problem data in markdown.
        
        Gives:
        	None: Does not return anything.
        """
        aocDir = os.path.join(PROJECT_ROOT, "adventofcode")
        os.makedirs(aocDir, exist_ok=True)
        
        yearStr = extractedData.get("year", "0")
        dayStr = extractedData.get("day", "0")
        
        try:
            year = int(yearStr)
        except ValueError:
            year = 0
            
        try:
            day = int(dayStr)
        except ValueError:
            day = 0
            
        startYear = ((year - 1) // 5) * 5 + 1 if year > 0 else 0
        if startYear == 0:
            rangeStr = "unknown_range"
        else:
            rangeStr = f"{startYear}-{startYear+4}"
            
        rangeDir = os.path.join(aocDir, rangeStr)
        os.makedirs(rangeDir, exist_ok=True)
        
        dirName = f"{year}-{day}"
        questionDir = os.path.join(rangeDir, dirName)
        os.makedirs(questionDir, exist_ok=True)
        
        problemPath = os.path.join(questionDir, "problem.md")
        with open(problemPath, "w", encoding="utf-8") as f:
            f.write(markdownContent)
            
        solutionPath = os.path.join(questionDir, "solution.md")
        if not os.path.exists(solutionPath):
            solutionContent = "# [Naive / Better / Optimal] Solution\n\n## Idea\n\n## Pseudocode\n\n### Solver\n\n### Verifier\n\n## Analysis\n\n### Time Complexity\n\n### Space Complexity\n\n## Pros and Cons\n"
            with open(solutionPath, "w", encoding="utf-8") as f:
                f.write(solutionContent)
                
        import logging
        logging.info("Successfully saved Advent of Code problem to: " + questionDir)


class DirManagerFactory:
    """
    [Factory to instantiate correct directory manager]
    """
    @staticmethod
    def createDirManager(siteName: str) -> BaseDirManager:
        """
        [Creates a directory manager instance based on site name]
        
        Takes:
        	siteName (str): Name of the programming platform.
        
        Gives:
        	BaseDirManager: A directory manager instance for the platform.
        """
        normalizedName = siteName.lower()
        if normalizedName == "codeforces":
            return CodeforcesDirManager()
        elif normalizedName == "atcoder":
            return AtcoderDirManager()
        elif normalizedName == "leetcode":
            return LeetcodeDirManager()
        elif normalizedName == "codechef":
            return CodechefDirManager()
        elif normalizedName == "adventofcode":
            return AdventofcodeDirManager()
        else:
            raise ValueError("Unsupported site: " + siteName)
