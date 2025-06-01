# 🧩 AI-Powered Documentation Improvement Agent

This project provides an AI-powered tool that analyzes and rewrites MoEngage documentation, making it clearer and easier to understand—especially for marketers without a technical background.

---
The system has two main components:


## 🔍 Task 1: Documentation Analyzer Agent

### 🔸 What It Does:

* **Analyzer**: Reviews MoEngage help articles for:

  * **Readability** – Uses Flesch-Kincaid, Gunning Fog, and Gemini API tone analysis.
  * **Structure** – Checks clarity of headings, lists, and paragraph flow.
  * **Completeness** – Identifies missing explanations or lack of examples.
  * **Style** – Assesses clarity, tone, and friendliness per Microsoft Style Guide.


---

## ✏️ Task 2: Documentation Revision Agent

* **Reviser**: Uses those insights from task 1 to generate improvement suggestions.
### 🔸 What It Does:

* **Rewrites Content**:

  * Simplifies complex language.
  * Uses second-person ("you") for a conversational tone.
  * Breaks down long or technical sentences.

* **Saves Output Files** in `/Output/`:

  * `analysis_report.json`
  * `revised_content.md`
  * `revised_content.txt`
  * `revision_result.json`

---

## 🚀 Features

🚀 Features
* **AI-Powered Analysis** : Evaluates MoEngage documentation for readability, structure, completeness, and style using traditional metrics and the Gemini LLM.
* **Smart Content Revision** : Rewrites documentation to be simpler, clearer, and more personal—ideal for non-technical marketers.
* **Multi-Format Output** : Saves revised content and analysis reports in Markdown, plain text, and JSON formats for easy sharing and review.
* **LLM Integration**: Uses Google Gemini 1.5 Flash for tone analysis, rewriting, and content optimization.
* **Clean and Modular Backend** : Built with Flask and Python, with a clear separation of concerns for easier maintenance and expansion.
* **User-Friendly Web Interface** :
Minimalist UI that lets users paste a URL, submit, and get results—no technical skills required.
* **Robust Logging and Error Handling** : Provides detailed logs to help with debugging and transparency of API responses and processing steps.

---

---

## 📁 Project Structure

```
MoEngage-Web-Analyzer/
├── backend/
│   ├── doc_analyzer.py         # Web content analyzer
│   ├── doc_revision.py         # Text simplifier and reviser
├── app.py                      # Flask app
├── templates/
│   ├── index.html              # User input page
│   ├── result.html             # Analysis and revision results
├── static/
│   ├── style.css               # Dark-themed styles
├── Output/                     # Output files
├── README.md                   # Project documentation
```

---

## ⚙️ Setup Instructions


---

## 🚀 How to Set It Up

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/MoEngage-Doc-Improver.git
cd MoEngage
```

###2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate 

```

### 3. Install Dependencies

```bash
pip install requests beautifulsoup4 textstat flask nltk
python -c "import nltk; nltk.download('punkt')"
```

### 4. Set Up Gemini API Key

* Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey)
* In `backend/doc_analyzer.py` and `backend/doc_revision.py`, replace:

```python
GEMINI_API_KEY = "your-valid-gemini-api-key"
```

---

## ▶️ Run the Application

```bash
python app.py
```

Then visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---


## 🧪 How to Use
Paste a MoEngage article URL (e.g., https://help.moengage.com/hc/en-us/articles/...).

Click Submit.

The tool:

Analyzes the doc.

Rewrites it.

Saves the results in the /Output/ folder.

---

## 📂 Output Files

All generated files are saved in the `Output/` folder in the repository.

| File Name                 | Purpose                                                            |
|---------------------------|--------------------------------------------------------------------|
| `analysis_report.json`    | Readability, structure, completeness, and style scores with tips   |
| `revised_content.md`      | Simplified and marketer-friendly version in Markdown format        |
| `revised_content.txt`     | Plain text version of the revised content                          |
| `revision_result.json`    | Detailed change log: original vs. revised text, tracked by section |

> 📁 You can view all output files inside the `/Output/` directory after running the tool.

---

## 📸 Screenshots 

![WhatsApp Image 2025-05-31 at 20 05 47_02f4b87e](https://github.com/user-attachments/assets/a1968019-dd4e-4be4-b757-45c0e98e52cf)

![WhatsApp Image 2025-05-31 at 20 04 19_055af265](https://github.com/user-attachments/assets/4bad552e-1db4-45aa-a010-ef5bdc1c9f73)
![image](https://github.com/user-attachments/assets/bee89230-45f8-4fd5-815c-2ad774201f2d)

![WhatsApp Image 2025-05-31 at 20 05 03_f918f5b4](https://github.com/user-attachments/assets/6f81c51a-814f-449f-b08c-665bb4145abc)

![WhatsApp Image 2025-05-31 at 20 05 36_71dde27a](https://github.com/user-attachments/assets/82cd50c2-bf9e-4a89-9427-a0de1bb18c5a)

---

## ⚙️ Built With

* **Backend**: Python, Flask
* **Web Scraping**: BeautifulSoup
* **AI/LLM**: Google Gemini 1.5 Flash (via Gemini API)
* **Text Analysis**: NLTK, `textstat`
* **Frontend**: HTML, CSS (dark-themed UI)
* **Output Formats**: Markdown, plain text, JSON

---

## 🧠 Assumptions

* URLs are publicly accessible (no login, CAPTCHA).
* MoEngage documentation is consistent.
* Documentation uses standard HTML structure.
* Valid Google Gemini API key is configured.
* Output revisions are saved/displayed for user.
* Users are non-technical marketers looking for clearer, simpler content.
* Modern browser used (Chrome, Firefox, Edge).

---

## 🎨 Design Choices

* Used a modular Python backend to separate analysis, revision, and routing logic.
* Chose Flask for simplicity and quick setup of the web interface.
* Integrated Google Gemini 1.5 Flash for high-quality rewriting and tone adjustments.
* Followed the Microsoft Style Guide to guide tone and writing style
* Applied regex cleanup for output formatting (e.g., removing double punctuation, repeated headers)
* Designed a minimal, dark-themed UI to reduce visual clutter and align with tech users
* Focused on server-side processing for better control, performance, and logging

---

## 🧰 Troubleshooting

### Gemini API Errors

* Test using:

```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=your-key" -H "Content-Type: application/json" -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'
```

### Output Files Missing

* Ensure `Output/` directory exists:

```bash
mkdir Output
```

* Check permissions and logs.

### Content Not Extracted Properly

* Inspect the HTML and update selectors in `fetch_article_content()`.

---


## ⚠️ Challenges Faced
*  HTML Variability: MoEngage articles use inconsistent HTML, making clean text extraction tricky.

*  Output Formatting: Needed regex cleanup to fix double periods and repeated headers in revised content.

*  Technical Content Revision: Simplifying complex docs was challenging—used a mix of custom rules and Gemini API for clarity.

*  Multi-format Saving: Outputting clean content in Markdown, TXT, and JSON required careful handling.

*  User-Friendliness: Focused on keeping the tool simple and intuitive for non-technical users.
---

## 🌟 Future Improvements

* ✅ Enable batch processing so users can analyze multiple MoEngage URLs at once.
* ✅ Add multilingual support to handle documentation in languages other than English.
* ✅ Allow users to customize output filenames or organize results by date or source.
* ✅ Improve the UI with progress indicators and better usability for non-technical users.
* ✅ Add support for switching between different LLMs like OpenAI, Gemini, or open-source models.

---

## ✍️ Author & Contact
Feel free to reach out or contribute!

## 📬 Mohitha Bandi - 22WU0105037 - Data Science
## 📧 mohitha.bandi_2026@woxsen.edu.in
## 🌐 LinkedIn : www.linkedin.com/in/mohitha-bandi-6b563826b
## 🌐 GitHub : https://github.com/id12026




