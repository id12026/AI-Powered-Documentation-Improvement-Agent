import requests
from bs4 import BeautifulSoup
import textstat
import json
import re
import logging
import os

# Configure logging for backend debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Google Gemini API key (replace with your own)
GEMINI_API_KEY = " "  # Obtain from https://aistudio.google.com/app/apikey

# Output directory
OUTPUT_DIR = "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_article_content(url):
    """Fetch and parse webpage content using BeautifulSoup.
    
    Args:
        url (str): The webpage URL to scrape.
    
    Returns:
        tuple: (extracted_text, error_message). Returns None for text and an error message if fetching fails.
    """
    logger.info(f"Fetching content from URL: {url}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, timeout=30, headers=headers)
        response.raise_for_status()
        logger.info("Successfully fetched webpage")
    except Exception as e:
        logger.error(f"Failed to fetch URL: {str(e)}")
        fallback_text = "This is a sample webpage content. The platform supports various features to enhance user experience. You can configure settings to achieve optimal results. Learn more about our services and tools."
        return fallback_text, f"Error fetching URL: {str(e)}. Using fallback text."
    
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try multiple selectors to find main content
        content = (soup.find('article') or
                   soup.find('main') or
                   soup.find('div', class_=re.compile('content|article|post|body|main', re.I)) or
                   soup.find('section') or
                   soup.find('body'))
        if not content:
            logger.warning("No main content found in HTML")
            return None, "No main content found in HTML structure."
        
        # Remove scripts and styles
        for elem in content.find_all(['script', 'style']):
            elem.decompose()
        
        # Extract text from relevant elements
        text = ' '.join(p.get_text(strip=True) for p in content.find_all(['p', 'li', 'h1', 'h2', 'h3', 'h4', 'span', 'div']) if p.get_text(strip=True))
        text = re.sub(r'\s+', ' ', text).strip()
        
        if not text or len(text.split()) < 10:
            logger.warning("Insufficient meaningful text extracted")
            return None, "Insufficient meaningful text extracted from webpage."
        
        logger.info("Successfully extracted text content")
        return text, None
    except Exception as e:
        logger.error(f"Error parsing HTML: {str(e)}")
        return None, f"Error parsing HTML: {str(e)}."

def query_gemini(text, prompt, model="gemini-1.5-flash"):
    """Query Google Gemini API for text analysis or simplification.
    
    Args:
        text (str): Input text to analyze or simplify.
        prompt (str): Prompt for the Gemini model.
        model (str): Gemini model to use (default: gemini-1.5-flash).
    
    Returns:
        dict or str: API response or error message.
    """
    logger.info("Querying Google Gemini API")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt + "\n\n" + text[:1000]}]}],  # Limit input size
        "generationConfig": {"maxOutputTokens": 500}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        generated_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        logger.info("Successfully received Gemini response")
        return generated_text
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        return {"error": f"Gemini API error: {str(e)}"}

def analyze_readability(text):
    """Analyze text readability using textstat and Gemini for tone.
    
    Args:
        text (str): Text to analyze.
    
    Returns:
        dict: Readability scores, assessment, and suggestions.
    """
    if not text:
        logger.warning("No text provided for readability analysis")
        return {"score": 0, "assessment": "No content to analyze.", "suggestions": []}
    
    logger.info("Analyzing readability")
    flesch_score = textstat.flesch_kincaid_grade(text)
    fog_score = textstat.gunning_fog(text)
    
    assessment = f"Flesch-Kincaid Grade: {flesch_score:.1f}, Gunning Fog: {fog_score:.1f}. "
    suggestions = []
    
    # Use Gemini to assess tone
    prompt = "Analyze the tone of the following text. Is it positive, neutral, or technical? Suggest improvements if the tone is not positive or engaging."
    gemini_result = query_gemini(text, prompt)
    
    if isinstance(gemini_result, str) and "technical" in gemini_result.lower():
        assessment += "The tone may feel technical or neutral. "
        suggestions.append("Use a positive, engaging tone, e.g., 'Easily explore our features'.")
    
    if flesch_score > 8:
        assessment += "The content is complex for a general audience. "
        suggestions.append("Simplify sentences, e.g., replace 'utilize' with 'use'.")
    
    if fog_score > 10:
        assessment += "Long sentences may reduce clarity. "
        suggestions.append("Break sentences longer than 15 words into shorter ones, e.g., 'Use our tools. Improve your results.'")
    
    logger.info("Readability analysis completed")
    return {
        "score": {"flesch_kincaid": flesch_score, "gunning_fog": fog_score},
        "assessment": assessment,
        "suggestions": suggestions
    }

def analyze_structure(url, text):
    """Analyze webpage structure using BeautifulSoup.
    
    Args:
        url (str): Webpage URL.
        text (str): Extracted text (unused here, kept for compatibility).
    
    Returns:
        dict: Structure assessment and suggestions.
    """
    logger.info(f"Analyzing structure for URL: {url}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, timeout=30, headers=headers)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch URL for structure analysis: {str(e)}")
        return {
            "assessment": f"Error analyzing structure: {str(e)}.",
            "suggestions": []
        }
    
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        headings = len(soup.find_all(['h1', 'h2', 'h3', 'h4']))
        paragraphs = len(soup.find_all('p'))
        lists = len(soup.find_all(['ul', 'ol']))
        
        assessment = f"Page has {headings} headings, {paragraphs} paragraphs, and {lists} lists. "
        suggestions = []
        
        if headings < 1:
            assessment += "Lack of headings makes navigation difficult. "
            suggestions.append("Add at least one heading, e.g., 'Introduction' or 'How It Works'.")
        
        if paragraphs > 15 and lists == 0:
            assessment += "Dense paragraphs without lists may overwhelm readers. "
            suggestions.append("Use lists to break up content, e.g., list steps or features.")
        
        logger.info("Structure analysis completed")
        return {
            "assessment": assessment,
            "suggestions": suggestions
        }
    except Exception as e:
        logger.error(f"Error analyzing structure: {str(e)}")
        return {
            "assessment": f"Error analyzing structure: {str(e)}",
            "suggestions": []
        }

def analyze_completeness(text):
    """Analyze content completeness.
    
    Args:
        text (str): Text to analyze.
    
    Returns:
        dict: Completeness assessment and suggestions.
    """
    logger.info("Analyzing completeness")
    assessment = "The content provides an overview. "
    suggestions = []
    
    if len(text.split()) < 100:
        assessment += "The content is too brief for comprehensive coverage. "
        suggestions.append("Expand with details, e.g., add examples or FAQs.")
    
    if "example" not in text.lower() and len(text.split()) < 500:
        assessment += "Lack of examples may limit understanding. "
        suggestions.append("Include practical examples, e.g., 'Here’s how to use this feature.'")
    
    logger.info("Completeness analysis completed")
    return {
        "assessment": assessment,
        "suggestions": suggestions
    }

def analyze_style(text):
    """Analyze content style using Gemini for tone.
    
    Args:
        text (str): Text to analyze.
    
    Returns:
        dict: Style assessment and suggestions.
    """
    logger.info("Analyzing style")
    assessment = "The tone is generally clear. "
    suggestions = []
    
    sentences = text.split('.')
    longest_sentence = max(sentences, key=len, default="")
    if len(longest_sentence) > 40:
        assessment += "Some sentences are too long, reducing readability. "
        suggestions.append(f"Shorten long sentences, e.g., split '{longest_sentence.strip()[:40]}...' into shorter parts.")
    
    if any(word in text.lower() for word in ['leverage', 'utilize', 'optimize', 'synergize']):
        assessment += "Jargon may confuse readers. "
        suggestions.append("Replace jargon with simple terms, e.g., 'use' instead of 'leverage'.")
    
    # Use Gemini to check engagement
    prompt = "Evaluate if the following text is engaging and uses second-person pronouns (e.g., 'you'). Suggest improvements if it lacks engagement or uses third-person pronouns."
    gemini_result = query_gemini(text, prompt)
    
    if isinstance(gemini_result, str) and "lacks engagement" in gemini_result.lower():
        assessment += "The tone lacks engagement. "
        suggestions.append("Use second-person pronouns, e.g., 'You can explore features' instead of 'Users can explore features.'")
    
    logger.info("Style analysis completed")
    return {
        "assessment": assessment,
        "suggestions": suggestions
    }

def analyze_documentation(url):
    """Analyze a webpage's content and generate a report.
    
    Args:
        url (str): Webpage URL to analyze.
    
    Returns:
        dict: Analysis report with readability, structure, completeness, and style.
    """
    logger.info(f"Starting analysis for URL: {url}")
    text, error = fetch_article_content(url)
    
    if error:
        report = {
            "url": url,
            "error": error,
            "analysis": {
                "readability": analyze_readability(text or ""),
                "structure": analyze_structure(url, text or ""),
                "completeness": analyze_completeness(text or ""),
                "style": analyze_style(text or "")
            }
        }
    else:
        report = {
            "url": url,
            "analysis": {
                "readability": analyze_readability(text),
                "structure": analyze_structure(url, text),
                "completeness": analyze_completeness(text),
                "style": analyze_style(text)
            }
        }
    
    if save_report(report, os.path.join(OUTPUT_DIR, "analysis_report.json")):
        logger.info("Analysis report saved successfully")
    else:
        logger.error("Failed to save analysis report")
    
    return report

def save_report(report, filename):
    """Save the analysis report to a JSON file.
    
    Args:
        report (dict): Analysis report to save.
        filename (str): Output file path.
    
    Returns:
        bool: True if saved successfully, False otherwise.
    """
    logger.info(f"Saving report to {filename}")
    try:
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Error saving report: {str(e)}")
        return False
