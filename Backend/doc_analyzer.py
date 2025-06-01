import requests
from bs4 import BeautifulSoup
import textstat
import json
import re
from urllib.parse import urlparse


# API keys (replace with your own)
SCRAPER_API_KEY = "3764d739eadaaf472e73dca934041437"  # Replace with valid key from https://www.scraperapi.com/
HUGGINGFACE_API_KEY = "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"  # Replace with valid key from https://huggingface.co/

def fetch_article_content(url):
    """Fetch content from any webpage using ScraperAPI or direct requests."""
    # Try ScraperAPI
    scraper_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={url}"
    try:
        response = requests.get(scraper_url, timeout=30)
        response.raise_for_status()
    except Exception as e:
        # Fallback to direct requests
        try:
            response = requests.get(url, timeout=30, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
            response.raise_for_status()
        except Exception as e2:
            # Fallback content
            fallback_text = "This is a sample webpage content. The platform supports various features to enhance user experience. Users can configure settings to achieve optimal results. Learn more about our services and tools."
            return fallback_text, f"Error fetching URL: ScraperAPI failed ({str(e)}). Direct request failed ({str(e2)}). Using fallback text."
    
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Flexible selectors for any webpage
        content = (soup.find('article') or
                   soup.find('main') or
                   soup.find('div', class_=re.compile('content|article|post|body|main', re.I)) or
                   soup.find('section') or
                   soup.find('body'))
        if not content:
            return None, "No main content found in HTML structure."
        
        # Extract text from common elements, excluding scripts and styles
        for elem in content.find_all(['script', 'style']):
            elem.decompose()
        text = ' '.join(p.get_text(strip=True) for p in content.find_all(['p', 'li', 'h1', 'h2', 'h3', 'h4', 'span', 'div']) if p.get_text(strip=True))
        text = re.sub(r'\s+', ' ', text).strip()
        
        if not text or len(text.split()) < 10:
            return None, "Insufficient meaningful text extracted from webpage."
        return text, None
    except Exception as e:
        return None, f"Error parsing HTML: {str(e)}."

def query_huggingface(text, task="text-classification", model="distilbert-base-uncased"):
    """Query Hugging Face Inference API for text analysis."""
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": text[:512],  # Truncate to avoid API limits
        "parameters": {"return_all_scores": True}
    }
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model}",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Hugging Face API error: {str(e)}"}

def analyze_readability(text):
    """Analyze readability for a general audience."""
    if not text:
        return {"score": 0, "assessment": "No content to analyze.", "suggestions": []}
    
    flesch_score = textstat.flesch_kincaid_grade(text)
    fog_score = textstat.gunning_fog(text)
    
    assessment = f"Flesch-Kincaid Grade: {flesch_score:.1f}, Gunning Fog: {fog_score:.1f}. "
    suggestions = []
    
    hf_result = query_huggingface(text)
    if "error" not in hf_result:
        positive_score = next((item['score'] for item in hf_result if item['label'] == 'POSITIVE'), 0)
        if positive_score < 0.5:
            assessment += "The tone may feel technical or neutral. "
            suggestions.append("Use a positive, engaging tone, e.g., 'Easily explore our features'.")
    
    if flesch_score > 8:
        assessment += "The content is complex for a general audience. "
        suggestions.append("Simplify sentences, e.g., replace 'utilize' with 'use'.")
    
    if fog_score > 10:
        assessment += "Long sentences may reduce clarity. "
        suggestions.append("Break sentences longer than 15 words into shorter ones, e.g., 'Use our tools. Improve your results.'")
    
    return {
        "score": {"flesch_kincaid": flesch_score, "gunning_fog": fog_score},
        "assessment": assessment,
        "suggestions": suggestions
    }

def analyze_structure(url, text):
    """Analyze webpage structure and flow."""
    scraper_url = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={url}"
    try:
        response = requests.get(scraper_url, timeout=30)
        response.raise_for_status()
    except Exception as e:
        # Fallback to direct requests
        try:
            response = requests.get(url, timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
        except Exception as e2:
            return {
                "assessment": f"Error analyzing structure: ScraperAPI failed ({str(e)}). Direct request failed ({str(e2)}).",
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
        
        return {
            "assessment": assessment,
            "suggestions": suggestions
        }
    except Exception as e:
        return {
            "assessment": f"Error analyzing structure: {str(e)}",
            "suggestions": []
        }

def analyze_completeness(text):
    """Analyze content completeness."""
    assessment = "The content provides an overview. "
    suggestions = []
    
    if len(text.split()) < 100:
        assessment += "The content is too brief for comprehensive coverage. "
        suggestions.append("Expand with details, e.g., add examples or FAQs.")
    
    if "example" not in text.lower() and len(text.split()) < 500:
        assessment += "Lack of examples may limit understanding. "
        suggestions.append("Include practical examples, e.g., 'Here’s how to use this feature.'")
    
    return {
        "assessment": assessment,
        "suggestions": suggestions
    }

def analyze_style(text):
    """Analyze content style."""
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
    
    hf_result = query_huggingface(text)
    if "error" not in hf_result:
        positive_score = next((item['score'] for item in hf_result if item['label'] == 'POSITIVE'), 0)
        if positive_score < 0.5:
            assessment += "The tone lacks engagement. "
            suggestions.append("Use second-person pronouns, e.g., 'You can explore features' instead of 'Users can explore features.'")
    
    return {
        "assessment": assessment,
        "suggestions": suggestions
    }

def analyze_documentation(url):
    """Analyze a webpage's content."""
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
    
    save_report(report, "report.json")
    return report

def save_report(report, filename):
    """Save the analysis report to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving report: {str(e)}")
        return False