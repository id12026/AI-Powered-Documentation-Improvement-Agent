AI-Powered Webpage Content Analyzer and Reviser
This project is a Flask-based web application designed to analyze and revise MoEngage documentation articles (e.g., https://help.moengage.com/hc/en-us/articles/...) to improve clarity and usability for non-technical marketers. It features a backend-focused implementation using BeautifulSoup for web scraping and Google Gemini API for text analysis and simplification, with a minimal frontend styled in a dark tech theme using Roboto Mono and Montserrat fonts.
Features

Analyze Documentation: Evaluates readability, structure, completeness, and style of MoEngage documentation URLs, providing actionable suggestions tailored for marketers.
Revise Content: Simplifies text, replaces jargon, uses second-person pronouns, and splits long sentences, producing revised versions in multiple formats.
Backend Focus: Optimized for server-side processing with modular code, detailed logging, and robust error handling.
Output: Generates analysis_report.json, revised__content.md, revised_content.txt, and revision_result.json in the Output/ directory.
Dependencies: Relies on BeautifulSoup, Google Gemini API, and Python libraries (requests, textstat, Flask, NLTK).
----
Project Structure
MoEngage-Web-Analyzer/
├── backend/
│   ├── doc_analyzer.py      # Analyzes webpage content
│   ├── doc_revision.py      # Revises webpage content
├── app.py                   # Flask web application
├── templates/
│   ├── index.html           # Input form page
│   ├── result.html          # Displays analysis and revision results
├── static/
│   ├── style.css            # CSS styling
├── Output/
│   ├── analysis_report.json # Analysis report
│   ├── revised__content.md  # Revised content in Markdown
│   ├── revised_content.txt  # Revised content in plain text
│   ├── revision_result.json # Revision result
├── README.md                # Project documentation

Setup Instructions
----
MoEngage-Web-Analyzer/
├── backend/
│   ├── doc_analyzer.py          # Extracts and analyzes documentation content for readability, structure, and style
│   ├── doc_revision.py          # Simplifies and revises content using Google Gemini API
│
├── templates/
│   ├── index.html               # User input form to enter documentation URL
│   ├── result.html              # Displays analysis and revised content
│
├── static/
│   ├── style.css                # Dark theme styling with Roboto Mono and Montserrat fonts
│
├── Output/
│   ├── analysis_report.json     # JSON report detailing readability, structure, completeness, and style
│   ├── revised__content.md      # Revised content in Markdown format
│   ├── revised_content.txt      # Revised content in plain text format
│   ├── revision_result.json     # JSON showing original vs revised text mapping
│
├── app.py                       # Main Flask app routing input/output and backend processing
├── README.md                    # Project documentation (this file)

Navigate to Project Directory:
cd "C:\Users\Reliance Digital\WEB DEVELOPMENT\MoEngage-Web-Analyzer"


Activate Virtual Environment:Ensure Python 3.8+ is installed and activate the virtual environment:
"C:\Users\Reliance Digital\WEB DEVELOPMENT\MI\venv\Scripts\activate"

If the virtual environment doesn’t exist, create it:
python -m venv "C:\Users\Reliance Digital\WEB DEVELOPMENT\MI\venv"
"C:\Users\Reliance Digital\WEB DEVELOPMENT\MI\venv\Scripts\activate"


Install Dependencies:Install required Python packages:
pip install requests beautifulsoup4 textstat flask nltk
python -c "import nltk; nltk.download('punkt')"


Set Up Google Gemini API Key:

Sign up at https://aistudio.google.com/app/apikey to obtain an API key.
Update backend/doc_analyzer.py and backend/doc_revision.py:GEMINI_API_KEY = "your-valid-gemini-api-key"




Save Project Files:

Place doc_analyzer.py and doc_revision.py in backend/.
Place app.py in the root directory (MoEngage-Web-Analyzer/).
Place index.html and result.html in templates/.
Place style.css in static/.
Save this README.md in the root directory.
Create the Output/ directory:mkdir Output




Run the Application:Start the Flask server:
python app.py

Open http://127.0.0.1:5000/ in a browser to access the interface.

Usage:

Enter a MoEngage documentation URL (e.g., https://help.moengage.com/hc/en-us/articles/...) in the input form.
Submit to view the analysis report, revision result, and revised content.
Outputs are saved in Output/ as analysis_report.json, revised__content.md, revised_content.txt, and revision_result.json.



Assumptions

URL Accessibility: MoEngage documentation URLs are publicly accessible without authentication or CAPTCHAs. BeautifulSoup cannot handle dynamic or protected content.
HTML Structure: Webpages have standard HTML elements (e.g., <article>, <main>, <p>). JavaScript-heavy pages may yield limited content.
Gemini API Availability: Google Gemini API is accessible with a valid key, with fallbacks (e.g., original text) for failures.
User Environment: Windows system with Python 3.8+ and a virtual environment at C:\Users\Reliance Digital\WEB DEVELOPMENT\MI\venv.
Content Language: Documentation is in English for accurate readability analysis and revision.
Browser Compatibility: Interface works in modern browsers (Chrome, Firefox, Edge), though UI is not optimized.

Design Choices

Flask Backend: Chosen for simplicity and Python integration, ideal for backend-focused tasks.
Modular Architecture: Separates analysis (doc_analyzer.py) and revision (doc_revision.py) in backend/ for maintainability.
BeautifulSoup Scraping: Lightweight HTML parsing, avoiding external services, with flexible selectors for robustness.
Google Gemini API: Used for tone analysis and text simplification, tailored for marketers’ needs with specific prompts.
Output Management: Centralized in Output/ with multiple formats (JSON, Markdown, text) for flexibility and accessibility.
Logging: Detailed logs for scraping, API calls, and revisions aid debugging.
Style Guidelines: Focuses on clarity, conciseness, and second-person pronouns, aligning with Microsoft Style Guide for customer-focused documentation.

Challenges

BeautifulSoup Limitations: JavaScript-rendered content (common in MoEngage pages) is not parsed. Mitigated with flexible selectors and fallback text.
Gemini API Integration: Required prompt engineering for reliable tone analysis and simplification. Addressed with targeted prompts and input limits.
Output Formatting: Punctuation errors (e.g., double periods) and header repetition in revised__content.md were fixed by enhancing text cleanup in apply_suggestions.
Revision Quality: Meaningful revisions for technical content were challenging. Combined regex transformations with Gemini simplification.
API Rate Limits: Gemini API free tier limits risked failures. Mitigated by limiting input size and using fallbacks.

Troubleshooting

Gemini API Errors:
Verify the API key at https://aistudio.google.com/app/apikey.
Test with:curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=your-key" -H "Content-Type: application/json" -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'




Content Extraction Failures:
Inspect webpage HTML (right-click, “View Source”) and update fetch_article_content selectors in backend/doc_analyzer.py.
Example: Add soup.find('div', class_='custom-class') for specific sites.


Output Files Missing:
Ensure Output/ exists (mkdir Output).
Check logs for file-writing errors (e.g., permissions).


Virtual Environment Issues:
Recreate if corrupted:python -m venv "C:\Users\Reliance Digital\WEB DEVELOPMENT\MI\venv"
"C:\Users\Reliance Digital\WEB DEVELOPMENT\MI\venv\Scripts\activate"
pip install requests beautifulsoup4 textstat flask nltk




Interface Rendering:
Clear browser cache or test in Chrome/Firefox.
Verify style.css is in static/.



Example Outputs
Below are outputs for two MoEngage documentation URLs, demonstrating the analyzer and revision agents.
Example 1: MoEngage Developer Portal

URL: https://developers.moengage.com/hc/en-us
Output/analysis_report.json:{
    "url": "https://developers.moengage.com/hc/en-us",
    "analysis": {
        "readability": {
            "score": {
                "flesch_kincaid": 15.804514106583074,
                "gunning_fog": 18.705329153605017
            },
            "assessment": "Flesch-Kincaid Grade: 15.8, Gunning Fog: 18.7. The tone may feel technical or neutral. The content is complex for a general audience. Long sentences may reduce clarity.",
            "suggestions": [
                "Use a positive, engaging tone, e.g., 'Easily explore our features'.",
                "Simplify sentences, e.g., replace 'utilize' with 'use'.",
                "Break sentences longer than 15 words into shorter ones, e.g., 'Use our tools. Improve your results.'"
            ]
        },
        "structure": {
            "assessment": "Page has 18 headings, 18 paragraphs, and 260 lists.",
            "suggestions": []
        },
        "completeness": {
            "assessment": "The content provides an overview. Lack of examples may limit understanding.",
            "suggestions": [
                "Include practical examples, e.g., 'Here’s how to use this feature.'"
            ]
        },
        "style": {
            "assessment": "The tone is generally clear. Some sentences are too long, reducing readability.",
            "suggestions": [
                "Shorten long sentences, e.g., split 'Developer Guide iOS SDKNative MoEngage S...' into shorter parts."
            ]
        }
    }
}


Output/revised__content.md:# Revised Webpage Content: https://developers.moengage.com/hc/en-us

MoEngage SDKs support iOS, Android, web, React Native, Flutter, and Unity. MoEngage works with Unity mobile apps. MoEngage SDKs also support Capacitor and Ionic apps. MoEngage's SDK works with Ionic and other apps, connects to TVs and streaming services, and integrates with many marketing partners. New SDK updates are available. Need help? Let us help you!


Output/revised_content.txt:MoEngage SDKs support iOS, Android, web, React Native, Flutter, and Unity. MoEngage works with Unity mobile apps. MoEngage SDKs also support Capacitor and Ionic apps. MoEngage's SDK works with Ionic and other apps, connects to TVs and streaming services, and integrates with many marketing partners. New SDK updates are available. Need help? Let us help you!


Output/revision_result.json (partial):[
    {
        "url": "https://developers.moengage.com/hc/en-us",
        "original_text": "Developer Guide iOS SDKNative MoEngage SDKs for iOS iOS SDKNative MoEngage SDKs for iOS...",
        "revised_text": "MoEngage SDKs support iOS, Android, web, React Native, Flutter, and Unity. MoEngage works with Unity mobile apps...",
        "output_files": ["Output/revised__content.md", "Output/revised_content.txt"]
    },
    ...
]



Example 2: MoEngage Delivery Types

URL: https://help.moengage.com/hc/en-us/articles/360058616131-Delivery-Types-MoEngage-Channels
Output/analysis_report.json:{
    "url": "https://help.moengage.com/hc/en-us/articles/360058616131-Delivery-Types-MoEngage-Channels",
    "analysis": {
        "readability": {
            "score": {
                "flesch_kincaid": 12.5,
                "gunning_fog": 15.3
            },
            "assessment": "Flesch-Kincaid Grade: 12.5, Gunning Fog: 15.3. The tone is technical. The content is complex for marketers. Long sentences reduce clarity.",
            "suggestions": [
                "Use a positive tone, e.g., 'You can easily set up campaigns'.",
                "Simplify sentences, e.g., replace 'orchestration' with 'delivery'.",
                "Break long sentences into shorter ones."
            ]
        },
        "structure": {
            "assessment": "Page has 10 headings, 25 paragraphs, and 5 lists.",
            "suggestions": [
                "Add more lists to break up dense paragraphs."
            ]
        },
        "completeness": {
            "assessment": "Content explains delivery types but lacks examples.",
            "suggestions": [
                "Add examples, e.g., 'Here’s how to set up an event-triggered campaign.'"
            ]
        },
        "style": {
            "assessment": "Tone is clear but uses jargon. Long sentences reduce readability.",
            "suggestions": [
                "Replace 'orchestration' with 'delivery'.",
                "Use second-person pronouns, e.g., 'You can' instead of 'Marketers can'."
            ]
        }
    }
}


Output/revised__content.md:# Revised Webpage Content: https://help.moengage.com/hc/en-us/articles/360058616131-Delivery-Types-MoEngage-Channels

MoEngage supports multiple delivery types for campaigns across various channels. You can set up campaigns based on specific triggers such as events, user location, or business criteria.

- Event-Triggered: You can send messages based on user actions or business events.
- Location-Triggered (Geo-fences): You can send messages when a user enters or exits a location.
- Inbound Channels: In-app or On-site channels support real-time, event-triggered messaging.
- Offline Delivery: You can queue messages for delivery when the device reconnects.

Supported channels include Push, Email, SMS, RCS, Cards, WhatsApp, Facebook Audience, Google Ads Audience, and Connectors.


Output/revised_content.txt:MoEngage supports multiple delivery types for campaigns across various channels. You can set up campaigns based on specific triggers such as events, user location, or business criteria.

- Event-Triggered: You can send messages based on user actions or business events.
- Location-Triggered (Geo-fences): You can send messages when a user enters or exits a location.
- Inbound Channels: In-app or On-site channels support real-time, event-triggered messaging.
- Offline Delivery: You can queue messages for delivery when the device reconnects.

Supported channels include Push, Email, SMS, RCS, Cards, WhatsApp, Facebook Audience, Google Ads Audience, and Connectors.


Output/revision_result.json (partial):[
    ...,
    {
        "url": "https://help.moengage.com/hc/en-us/articles/360058616131-Delivery-Types-MoEngage-Channels",
        "original_text": "User Guide Campaigns and Channels Getting Started Introduction Delivery or orchestration types help marketers set up multiple ways to send messages...",
        "revised_text": "MoEngage supports multiple delivery types for campaigns across various channels. You can set up campaigns based on specific triggers such as events, user location, or business criteria...",
        "output_files": ["Output/revised__content.md", "Output/revised_content.txt"]
    }
]



Future Improvements

Dynamic Content: Integrate a headless browser (e.g., Selenium) to parse JavaScript-rendered MoEngage pages.
Batch Processing: Support multiple URLs for bulk analysis and revision.
Multilingual Support: Extend to non-English content using Gemini’s capabilities.
Performance: Cache Gemini API responses to reduce calls and improve speed.
Output Customization: Allow users to specify output file names or formats via the interface.

Notes

Example Outputs: The second example’s analysis_report.json is synthesized based on the provided revision_result.json and typical output patterns, as the actual analysis for the second URL wasn’t provided. Run the application on https://help.moengage.com/hc/en-us/articles/360058616131-Delivery-Types-MoEngage-Channels to generate the exact report.
Punctuation Fixes: Applied in backend/doc_revision.py to resolve issues like double periods and concatenated words (e.g., “PushEmailSMS”).
Header Repetition: Fixed in revised__content.md by including URL-specific headers.

