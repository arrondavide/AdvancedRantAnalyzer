# Advanced Rant Analyzer

This project is a FastAPI-based application designed to analyze user "rants" or text inputs, detect emotions, analyze sentiment, and provide personalized insights and coping strategies.

## Features
- **Sentiment Analysis**: Detects sentiments using VADER and RoBERTa.
- **Emotion Detection**: Uses pre-trained models to classify emotions.
- **Response Generation**: Provides human-like responses to input text.
- **Tracking and Reporting**: Tracks user input over time and generates progress reports.

## Project Structure
```
rant-analyzer/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── analyzer.py          # AdvancedRantAnalyzer implementation
│   ├── tracker.py           # RantTracker implementation
│   ├── utils.py             # Shared utility functions
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── .devcontainer/           # Setup for GitHub Codespaces
│   ├── devcontainer.json
│   ├── Dockerfile
└── README.md                # Documentation
```

## Getting Started

### Prerequisites
- Python 3.9+
- Docker (optional but recommended)
- GitHub Codespaces (optional)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/rant-analyzer.git
   cd rant-analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

4. Access the Swagger UI:
   Open `http://localhost:8000/docs` in your browser.

## Deployment

### Using Docker
1. Build the Docker image:
   ```bash
   docker build -t rant-analyzer .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 rant-analyzer
   ```

### Using GitHub Codespaces
1. Launch a new Codespace from the repository.
2. Codespaces will automatically install dependencies and set up the environment.
3. Run the application as described above.