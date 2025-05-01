#  YouTube Video Summarizer

**YouTube Video Summarizer** is a Python-based tool that extracts transcripts from YouTube videos and generates concise summaries. It's perfect for understanding long videos like lectures, interviews, and tutorials without watching them fully.

---

##  Features

-  Automatic transcript extraction from YouTube videos  
-  AI-powered summarization of key content  
-  Command-line interface (CLI)  
-  Modular and clean codebase  

---

## 🛠️ Installation

1. **Clone the repository**  
```bash
git clone https://github.com/shhivaansh/Youtube-Video-Summarizer.git
cd Youtube-Video-Summarizer
```

2. **(Optional) Create a virtual environment**  
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install the required packages**  
```bash
pip install -r requirements.txt
```

---

## 📈 Usage

1. Run the script:
```bash
streamlit run transcript.py
```

2. When prompted, paste the YouTube video URL.

The tool will:
- Extract the transcript
- Summarize it using natural language processing
- Print the summary on screen

---

## 📂 Project Structure

```
Youtube-Video-Summarizer/
├── transcript.py          # Main script for summarizing YouTube videos
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 📚 Dependencies

- `youtube_transcript_api` – to fetch transcripts from YouTube
- `env` – for gemini pro API key

Install all dependencies with:
```bash
pip install -r requirements.txt
```


---

## 📧 Contact

Made by [shhivaansh](https://github.com/shhivaansh). 
