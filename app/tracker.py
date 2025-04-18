from collections import defaultdict
from datetime import datetime

class RantTracker:
    def __init__(self):
        self.user_data = defaultdict(list)

    def add_rant_analysis(self, user_id, analysis_results):
        """Add a new rant analysis to the tracker's history."""
        timestamp = datetime.now()
        self.user_data[user_id].append({"timestamp": timestamp, "analysis": analysis_results})

    def generate_progress_report(self, user_id):
        """Generate a progress report for the given user."""
        if user_id not in self.user_data:
            return {"message": "No data found for this user."}
        history = self.user_data[user_id]
        return {"total_rants": len(history), "last_analysis": history[-1]}