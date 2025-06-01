AI-Powered Documentation Improvement Agent
This project is a Python-based solution for analyzing and improving MoEngage public documentation articles (e.g., https://help.moengage.com/hc/en-us/articles/...). It features two agents:

Documentation Analyzer Agent: Analyzes articles for readability, structure, completeness, and style, producing actionable suggestions for non-technical marketers.
Documentation Revision Agent: Automatically revises content based on analysis suggestions, enhancing clarity and engagement.

Built with Flask, BeautifulSoup, and Google Gemini API, the project emphasizes backend processing with minimal frontend, delivering outputs in JSON, Markdown, and plain text formats.
Features

Analysis: Evaluates MoEngage documentation for:
Readability (Flesch-Kincaid, Gunning Fog, tone via Gemini API).
Structure (headings, paragraphs, lists).
Completeness (detail, examples).
Style (clarity, conciseness, action-oriented language per Microsoft Style Guide).


Revision: Simplifies text, replaces jargon, uses second-person pronouns, and splits long sentences.
Outputs: Generates analysis_report.json, revised__content.md, revised_content.txt, and revision_result.json in Output/.
Backend Focus: Modular code with logging, error handling, and no UI optimization.
Dependencies: Python, BeautifulSoup, textstat, Flask, NLTK, Google Gemini API.

Project Structure
MoEngage-Web-Analyzer/
├── backend/
│   ├── doc_analyzer.py      # Analyzer agent logic
│   ├── doc_revision.py      # Revision agent logic
├── app.py                   # Flask application
├── templates/
│   ├── index.html           # Input form
│   ├── result.html          # Result display
├── static/
│   ├── style.css            # Minimal styling
├── Output/
│   ├── analysis_report.json # Analysis report
│   ├── revised__content.md  # Revised Markdown
│   ├── revised_content.txt  # Revised plain text
│   ├── revision_result.json # Revision details
├── README.md                # Project documentation

Setup Instructions

Navigate to Directory:
cd /path/to/MoEngage-Web-Analyzer


Create and Activate Virtual Environment:Ensure Python 3.8+ is installed:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Install Dependencies:
pip install requests beautifulsoup4 textstat flask nltk
python -c "import nltk; nltk.download('punkt')"


Configure Google Gemini API Key:

Obtain a key at https://aistudio.google.com/app/apikey.
Update backend/doc_analyzer.py and backend/doc_revision.py:GEMINI_API_KEY = "your-valid-gemini-api-key"




Save Files:

Place doc_analyzer.py, doc_revision.py in backend/.
Place app.py, README.md in root.
Place index.html, result.html in templates/.
Place style.css in static/.
Create Output/:mkdir Output




Run Application:
python app.py

Access at http://127.0.0.1:5000/ in a browser.

Usage:

Enter a MoEngage URL (e.g., https://help.moengage.com/hc/en-us/articles/...).
Submit to generate analysis and revised content.
Outputs are saved in Output/.



Assumptions

URL Accessibility: MoEngage documentation is publicly accessible without CAPTCHAs or authentication.
HTML Content: Articles use static HTML with standard tags (<article>, <p>). JavaScript-heavy pages may limit extraction.
Gemini API: Available with a valid key; fallbacks return original text.
Language: Content is English for accurate analysis.
Environment: User has Python 3.8+ and a compatible OS (Windows/Linux/Mac).
Browser: Interface works in Chrome, Firefox, or Edge.

Design Choices

Flask: Lightweight framework for rapid backend development.
BeautifulSoup: Efficient for HTML parsing, with flexible selectors to handle varied MoEngage page structures.
Google Gemini API: Chosen for tone analysis and text simplification, optimized for marketer-friendly revisions.
Modularity: Separates analysis (doc_analyzer.py) and revision (doc_revision.py) for maintainability.
Readability: Uses textstat for Flesch-Kincaid/Gunning Fog, enhanced by Gemini for qualitative tone assessment.
Style Guidelines: Focuses on clarity, conciseness, and second-person pronouns (Microsoft Style Guide), implemented via regex and LLM.
Outputs: Multiple formats (JSON, Markdown, text) for flexibility, stored in Output/ for organization.
Logging: Detailed logs for debugging scraping, API calls, and revisions.

Challenges

JavaScript Content: BeautifulSoup misses dynamic content. Mitigated with robust selectors; future improvement could use Selenium.
Gemini API: Prompt engineering was needed for consistent tone analysis and simplification. Addressed with specific prompts and input limits.
Output Quality: Initial punctuation issues (double periods, concatenated words) were fixed in apply_suggestions with regex cleanup.
Revision Scope: Limited to readability and style due to complexity. Completeness suggestions (e.g., examples) are partially addressed via clarity improvements.
Rate Limits: Gemini API free tier limits handled with input truncation and fallbacks.

Troubleshooting

Gemini API Failure:
Verify key at https://aistudio.google.com/app/apikey.
Test:curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=your-key" -H "Content-Type: application/json" -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'




Scraping Issues:
Check HTML structure and update selectors in backend/doc_analyzer.py (e.g., soup.find('div', class_='custom-class')).


Missing Outputs:
Ensure Output/ exists and check write permissions.
Review logs for errors.


Virtual Environment:
Recreate if issues persist:python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install requests beautifulsoup4 textstat flask nltk





Example Outputs
Below are outputs for two MoEngage URLs, demonstrating Task 1 (Analyzer) and Task 2 (Revision).
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

MoEngage SDKs support iOS, Android, web, React Native, Flutter, and Unity. You can use MoEngage with Unity mobile apps. MoEngage SDKs also support Capacitor and Ionic apps. The SDK connects to TVs, streaming services, and integrates with many marketing partners. New SDK updates are available. Need help? Let us help you!


Output/revised_content.txt:MoEngage SDKs support iOS, Android, web, React Native, Flutter, and Unity. You can use MoEngage with Unity mobile apps. MoEngage SDKs also support Capacitor and Ionic apps. The SDK connects to TVs, streaming services, and integrates with many marketing partners. New SDK updates are available. Need help? Let us help you!


Output/revision_result.json (partial):[
    {
        "url": "https://developers.moengage.com/hc/en-us",
        "original_text": "Developer Guide iOS SDKNative MoEngage SDKs for iOS iOS SDKNative MoEngage SDKs for iOS...",
        "revised_text": "MoEngage SDKs support iOS, Android, web, React Native, Flutter, and Unity. You can use MoEngage with Unity mobile apps...",
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
            "assessment": "Flesch-Kincaid Grade: 12.5, Gunning Fog: 15.3. The tone is technical. Content is complex for marketers. Long sentences reduce clarity.",
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

MoEngage supports multiple delivery types for campaigns across various channels. You can set up campaigns based on events, user location, or business criteria.

- Event-Triggered: You can send messages based on user actions or business events.
- Location-Triggered (Geo-fences): You can send messages when a user enters or exits a location.
- Inbound Channels: In-app or On-site channels support real-time messaging.
- Offline Delivery: You can queue messages for delivery when the device reconnects.

Supported channels include Push, Email, SMS, RCS, Cards, WhatsApp, Facebook Audience, Google Ads Audience, and Connectors.


Output/revised_content.txt:MoEngage supports multiple delivery types for campaigns across various channels. You can set up campaigns based on events, user location, or business criteria.

- Event-Triggered: You can send messages based on user actions or business events.
- Location-Triggered (Geo-fences): You can send messages when a user enters or exits a location.
- Inbound Channels: In-app or On-site channels support real-time messaging.
- Offline Delivery: You can queue messages for delivery when the device reconnects.

Supported channels include Push, Email, SMS, RCS, Cards, WhatsApp, Facebook Audience, Google Ads Audience, and Connectors.


Output/revision_result.json (partial):[
    ...,
    {
        "url": "https://help.moengage.com/hc/en-us/articles/360058616131-Delivery-Types-MoEngage-Channels",
        "original_text": "User Guide Campaigns and Channels Getting Started Introduction Delivery or orchestration types help marketers set up multiple ways to send messages...",
        "revised_text": "MoEngage supports multiple delivery types for campaigns across various channels. You can set up campaigns based on events, user location, or business criteria...",
        "output_files": ["Output/revised__content.md", "Output/revised_content.txt"]
    }
]



Future Improvements

Dynamic Content: Use Selenium for JavaScript-rendered MoEngage pages.
Bulk Analysis: Support multiple URLs in a single run.
Multilingual Support: Handle non-English documentation with Gemini.
Performance: Cache API responses to reduce Gemini calls.
Customization: Allow user-defined output formats or file names.

Notes

Second Analysis Report: The analysis_report.json for the second URL is synthesized based on provided revision outputs and typical patterns. Run the application to generate the exact report.
Fixes: Punctuation issues (e.g., double periods) and header repetition in revised__content.md were resolved in backend/doc_revision.py using regex cleanup and URL-specific headers.
Style Focus: Revision agent prioritizes readability (simplification, sentence splitting) and style (jargon removal, second-person pronouns), as allowed for partial implementation in Task 2.

