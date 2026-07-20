"""
File Name: main_runner.py
Purpose: Main execution script for the problem fetcher program.
"""
import argparse
import logging
import re
from platform_extractors import ExtractorFactory
from model_handler import analyzeProblem
from directory_manager import DirManagerFactory

SUPPORTED_SITES = ["Atcoder", "Codeforces", "Leetcode", "Adventofcode", "Codechef"]

def main() -> None:
    """
    [Main execution function for the program]
    
    Takes:
    	None: No arguments.
    
    Gives:
    	None: Does not return anything.
    """
    parser = argparse.ArgumentParser(description="Competitive Programming Problem Fetcher")
    parser.add_argument("-l", "--link", type=str, required=True, help="Problem link")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        
    try:
        siteMatch = re.search(r"https?://(?:www\.)?([a-zA-Z0-9-]+)\.(?:com|jp)", args.link)
        if not siteMatch:
            raise ValueError("Could not extract site name from link: " + args.link)
        
        siteName = siteMatch.group(1).lower()
        logging.info("Starting extraction for " + siteName + ": " + args.link)
        
        extractor = ExtractorFactory.createExtractor(siteName)
        extractedData = extractor.extract(args.link)
        rawText = extractedData["html"]
        
        logging.debug("Extracted raw text length: " + str(len(rawText)))
        
        logging.info("Analyzing problem content via Gemini...")
        analysis = analyzeProblem(rawText)
        
        dirManager = DirManagerFactory.createDirManager(siteName)
        dirManager.save(extractedData, analysis.markdownContent)
        
    except Exception as e:
        logging.error("An error occurred: " + str(e))
        if args.verbose:
            logging.exception("Detailed traceback:")


if __name__ == "__main__":
    main()
