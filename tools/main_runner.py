"""
File Name: main_runner.py
Purpose: Main execution script for the problem fetcher program.
"""
import argparse
import logging
from platform_extractors import ExtractorFactory
from model_handler import analyzeProblem, saveProblemFiles

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
        extractor = ExtractorFactory.createExtractor(args.site)
        rawText = extractor.extract(args.link)
        
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
