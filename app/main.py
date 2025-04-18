from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.analyzer import AdvancedRantAnalyzer
from app.tracker import RantTracker

# Initialize FastAPI app
app = FastAPI(title="Advanced Rant Analyzer API", version="1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Advanced Rant Analyzer API"}

@app.post("/analyze")
def analyze():
    return {"message": "This is the analyze endpoint"}
    
# Initialize the analyzer and tracker
analyzer = AdvancedRantAnalyzer()
tracker = RantTracker()

# Input data model for the API
class RantInput(BaseModel):
    text: str
    user_id: str = "anonymous"

@app.post("/analyze")
def analyze_rant(rant_input: RantInput):
    """Analyze a rant and return detailed insights."""
    try:
        # Analyze the rant
        analysis_results = analyzer.analyze(rant_input.text, rant_input.user_id)

        # Track the rant if user ID is provided
        if rant_input.user_id != "anonymous":
            tracker.add_rant_analysis(rant_input.user_id, analysis_results)

        # Generate response
        response = analyzer.generate_response(analysis_results)

        return {"analysis": analysis_results, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing rant: {str(e)}")

@app.get("/progress/{user_id}")
def get_progress_report(user_id: str):
    """Get the progress report for a user."""
    try:
        return tracker.generate_progress_report(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating progress report: {str(e)}")