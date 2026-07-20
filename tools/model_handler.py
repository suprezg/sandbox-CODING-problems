"""
File Name: model_handler.py
Purpose: Analyzes problem content using Gemini API and saves to markdown.
"""
import os
import json
import re
import datetime
import logging
from google import genai
from pydantic import BaseModel

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_DIRECTORY = os.path.join(PROJECT_ROOT, "core")
DATA_DIRECTORY = os.path.join(PROJECT_ROOT, "data")

MODEL_MAPPING = {
    "Gemini 3.5 Flash": "gemini-3.5-flash",
    "Gemini 3 Flash": "gemini-3.0-flash",
    "Gemma 4 31B": "gemma-4-31b",
    "Gemini 2.5 Flash": "gemini-2.5-flash",
    "Gemini 3.1 Flash Lite": "gemini-3.1-flash-lite",
    "Gemini 2.5 Flash Lite": "gemini-2.5-flash-lite"
}

MODEL_PRIORITY = [
    "Gemini 3.5 Flash",
    "Gemini 3 Flash",
    "Gemma 4 31B",
    "Gemini 2.5 Flash",
    "Gemini 3.1 Flash Lite",
    "Gemini 2.5 Flash Lite"
]

class ProblemAnalysis(BaseModel):
    """
    [Data structure representing the problem and its markdown content]
    """
    title: str
    markdownContent: str

class ModelManager:
    """
    [Manages the state and pooling of AI models]
    """
    def __init__(self, stateFile="models_state.json"):
        os.makedirs(DATA_DIRECTORY, exist_ok=True)
        self.stateFile = os.path.join(DATA_DIRECTORY, stateFile)
        self.state = self.loadState()

    def loadState(self):
        """
        [Loads the model states from the JSON file]
        
        Takes:
        	self (ModelManager): The instance of the manager.
        
        Gives:
        	dict: The state dictionary.
        """
        if os.path.exists(self.stateFile):
            with open(self.stateFile, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            state = {model: {"exhausted": False, "exhausted_date": None} for model in MODEL_PRIORITY}
            self.saveState(state)
            return state

    def saveState(self, state):
        """
        [Saves the state dictionary to the JSON file]
        
        Takes:
        	self (ModelManager): The instance of the manager.
        	state (dict): The state to save.
        
        Gives:
        	None: Does not return anything.
        """
        with open(self.stateFile, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)

    def getBestModel(self):
        """
        [Gets the best available model based on priority and exhaustion state]
        
        Takes:
        	self (ModelManager): The instance of the manager.
        
        Gives:
        	tuple: A tuple containing modelName and apiModeName, or (None, None) if all exhausted.
        """
        today = datetime.date.today().isoformat()
        
        for model in self.state:
            if self.state[model]["exhausted"] and self.state[model]["exhausted_date"] != today:
                self.state[model]["exhausted"] = False
                self.state[model]["exhausted_date"] = None
        self.saveState(self.state)

        for model in MODEL_PRIORITY:
            if not self.state[model].get("exhausted", False):
                return model, MODEL_MAPPING[model]
        
        return None, None

    def markExhausted(self, modelName):
        """
        [Marks a specific model as exhausted for the day]
        
        Takes:
        	self (ModelManager): The instance of the manager.
        	modelName (str): The name of the model.
        
        Gives:
        	None: Does not return anything.
        """
        today = datetime.date.today().isoformat()
        self.state[modelName]["exhausted"] = True
        self.state[modelName]["exhausted_date"] = today
        self.saveState(self.state)

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
    modelManager = ModelManager()
    
    prompt = (
        "You are an expert competitive programming assistant. I will provide you with the HTML of a problem statement.\n"
        "Your task is to analyze it, extract and format the problem into a comprehensive Markdown document.\n\n"
        "Important Guidelines:\n"
        "1. Start your response EXACTLY with this line:\n"
        "Title: <Problem Title>\n\n"
        "2. After that line, provide the full Markdown content for the problem. Use the following headers:\n"
        "   # <Problem Title>\n"
        "   ## Statement\n"
        "   ## Constraints\n"
        "   ## Input and Output Format\n"
        "   ### Input\n"
        "   ### Output\n"
        "   ## Input and Output Instances\n"
        "3. Make the main problem statement description bigger, more detailed, and comprehensive.\n"
        "4. Ensure the constraints are comprehensive, covering all bounds and conditions explicitly.\n"
        "5. Under the 'Input and Output Instances' heading, provide each input instance first, followed immediately by its corresponding output instance, and then a small explanation of why that output was produced. If there are fewer than 3 input/output instances in the HTML, you MUST generate and provide 1-2 more logical examples following the exact same format.\n"
        "6. Do not wrap the output in a JSON block. Return plain Markdown as requested.\n\n"
        f"Problem HTML:\n{problemHtml}"
    )
    
    response = None
    while True:
        modelName, apiModeName = modelManager.getBestModel()
        if not modelName:
            print("All models limits have been depleted. Try next day.")
            raise Exception("All models limits have been depleted. Try next day.")
            
        logging.info("Trying model: " + modelName)
        
        try:
            response = client.models.generate_content(
                model=apiModeName,
                contents=prompt
            )
            break
        except Exception as e:
            errorString = str(e).lower()
            if "429" in errorString or "quota" in errorString or "exhausted" in errorString:
                logging.warning("Model " + modelName + " exhausted its limits. Marking as depleted.")
                modelManager.markExhausted(modelName)
            else:
                raise
    
    text = response.text.strip()
    
    titleMatch = re.search(r"Title:\s*(.+)", text, re.IGNORECASE)
    
    title = titleMatch.group(1).strip() if titleMatch else "unknown_problem"
    
    markdownContent = re.sub(r"^(Title:.*?\n+)", "", text, flags=re.IGNORECASE | re.MULTILINE)
    if markdownContent.startswith("```markdown"):
        markdownContent = markdownContent[11:]
    if markdownContent.startswith("```"):
        markdownContent = markdownContent[3:]
    if markdownContent.endswith("```"):
        markdownContent = markdownContent[:-3]
    markdownContent = markdownContent.strip()
    
    return ProblemAnalysis(title=title, markdownContent=markdownContent)



