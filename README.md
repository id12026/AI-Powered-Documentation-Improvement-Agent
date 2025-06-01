---

# AI-Powered Webpage Content Analyzer and Reviser

A **Flask-based web application** that analyzes and revises MoEngage documentation to improve **clarity**, **readability**, and **usability** for **non-technical marketers**. It leverages **BeautifulSoup** for web scraping and **Google Gemini API** for AI-powered text simplification. Features a minimalistic, dark-themed frontend styled with **Roboto Mono** and **Montserrat** fonts.

---

## 🚀 Features

* **Analyze Documentation**
  Evaluates MoEngage documentation for readability, structure, completeness, and style, providing actionable suggestions tailored for marketers.

* **Revise Content**
  Simplifies text, removes jargon, uses second-person pronouns, and breaks long sentences. Outputs are saved in Markdown, plain text, and JSON formats.

* **Backend-Focused**
  Modular and optimized server-side architecture with detailed logging and robust error handling.

* **Clean Output**
  Generates the following files in the `Output/` directory:

  * `analysis_report.json`
  * `revised__content.md`
  * `revised_content.txt`
  * `revision_result.json`

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

## 🧪 Usage

1. Enter a MoEngage documentation URL (e.g., `https://help.moengage.com/hc/en-us/articles/...`)
2. Submit the form.
3. View the analysis, revised content, and download output files.

---

## 🧠 Assumptions

* URLs are publicly accessible (no login, CAPTCHA).
* Documentation uses standard HTML structure.
* English language is used for content.
* Valid Google Gemini API key is configured.
* Modern browser used (Chrome, Firefox, Edge).

---

## 🎨 Design Choices

* **Modular Code**: Separation of logic for maintainability.
* **Google Gemini API**: For AI-based readability improvements.
* **Dark Theme UI**: Designed with a tech-centric aesthetic.
* **Logging**: Detailed logs for debugging and auditing.

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

## 🧾 Outputs



## 🌟 Future Improvements

* ✅ Support JavaScript-rendered content via Selenium or Playwright
* ✅ Batch processing for multiple URLs
* ✅ Multilingual support
* ✅ Customizable output filenames
* ✅ Gemini API response caching

---


## 📬 Contact

For queries or contributions, please open an [issue](https://github.com/your-repo/issues) or submit a [pull request](https://github.com/your-repo/pulls).


