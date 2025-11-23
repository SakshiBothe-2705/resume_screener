# AI-Based Resume Screening System 🚀

An intelligent tool that uses Natural Language Processing (NLP) and Machine Learning (TF-IDF) to rank resumes based on their relevance to a job description.

## 🌟 Features
- **AI Ranking**: Automatically ranks candidates based on semantic relevance.
- **Multi-Format Support**: Accepts PDF, DOCX, and TXT files.
- **Premium UI**: Modern, dark-themed interface with drag-and-drop support.
- **Instant Analysis**: Get results in seconds.

## 🛠️ Prerequisites
Make sure you have **Python 3.8+** installed on your system.

## 📦 Installation

1.  **Clone the Repository** (if you haven't already):
    ```bash
    git clone https://github.com/SakshiBothe-2705/resume_screener.git
    cd resume_screener
    ```

2.  **Install Dependencies**:
    Run the following command to install the required Python libraries:
    ```bash
    pip install flask scikit-learn nltk pandas pdfminer.six python-docx
    ```

## 🚀 How to Run

1.  **Start the Application**:
    ```bash
    python app.py
    ```

2.  **Open in Browser**:
    Go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📖 How to Use
1.  **Paste Job Description**: Copy the job requirements into the "Job Description" box.
2.  **Upload Resumes**: Drag and drop multiple resume files (PDF/DOCX) into the upload area.
3.  **Click Analyze**: The system will process the files and display a ranked list of candidates with match percentages.

## 📂 Project Structure
- `app.py`: Main Flask application server.
- `utils/processor.py`: Core AI logic (Text extraction, TF-IDF, Cosine Similarity).
- `static/`: CSS styles and JavaScript logic.
- `templates/`: HTML files.
- `uploads/`: Temporary storage for uploaded files.

## 📜 License
This project is for educational purposes.
