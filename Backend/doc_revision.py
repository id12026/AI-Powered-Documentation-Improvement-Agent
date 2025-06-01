import requests
import json
import nltk
import re
import os
import logging
from backend.doc_analyzer import fetch_article_content

# Configure logging for backend debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Download NLTK data
nltk.download('punkt', quiet=True)

# Google Gemini API key (replace with your own)
GEMINI_API_KEY = " "  # Obtain from https://aistudio.google.com/app/apikey

# Output directory
OUTPUT_DIR = "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def query_gemini(text, prompt, model="gemini-1.5-flash"):
    """Query Google Gemini API for text simplification.
    
    Args:
        text (str): Input text to simplify.
        prompt (str): Prompt for the Gemini model.
        model (str): Gemini model to use.
    
    Returns:
        str: Simplified text or original text on error.
    """
    logger.info("Querying Google Gemini API for simplification")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt + "\n\n" + text[:1000]}]}],
        "generationConfig": {"maxOutputTokens": max(20, len(text.split()) // 2)}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        simplified_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", text)
        logger.info("Successfully simplified text")
        return simplified_text
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        return text  # Fallback to original text

def simplify_sentence(sentence):
    """Simplify a sentence using Google Gemini API.
    
    Args:
        sentence (str): Sentence to simplify.
    
    Returns:
        str: Simplified sentence or original if unchanged.
    """
    logger.info("Simplifying sentence")
    if len(sentence.split()) > 10:
        prompt = "Simplify the following sentence to make it clear and concise, using simple words and short phrases."
        simplified = query_gemini(sentence, prompt)
        return simplified if simplified != sentence else sentence
    return sentence

def replace_jargon(text):
    """Replace technical jargon with simpler terms.
    
    Args:
        text (str): Input text.
    
    Returns:
        str: Text with jargon replaced.
    """
    logger.info("Replacing jargon")
    jargon_dict = {
        r'\bleverage\b': 'use',
        r'\butilize\b': 'use',
        r'\boptimize\b': 'improve',
        r'\bconfigure\b': 'set up',
        r'\bimplement\b': 'apply',
        r'\bsynergize\b': 'work together',
        r'\borchestration\b': 'management'
    }
    for jargon, replacement in jargon_dict.items():
        text = re.sub(jargon, replacement, text, flags=re.IGNORECASE)
    return text

def convert_to_second_person(text):
    """Convert third-person pronouns to second-person.
    
    Args:
        text (str): Input text.
    
    Returns:
        str: Text with second-person pronouns.
    """
    logger.info("Converting to second-person")
    replacements = {
        r'\busers can\b': 'you can',
        r'\bthe user\b': 'you',
        r'\buser should\b': 'you should',
        r'\busers should\b': 'you should',
        r'\busers\b': 'you',
        r'\bpeople can\b': 'you can',
        r'\bindividuals\b': 'you'
    }
    for old, new in replacements.items():
        text = re.sub(old, new, text, flags=re.IGNORECASE)
    return text

def split_long_sentences(text):
    """Split sentences longer than 10 words into shorter ones.
    
    Args:
        text (str): Input text.
    
    Returns:
        str: Text with long sentences split.
    """
    logger.info("Splitting long sentences")
    sentences = nltk.sent_tokenize(text)
    revised_sentences = []
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 10:
            chunks = [' '.join(words[i:i+8]) for i in range(0, len(words), 8)]
            revised_sentences.extend(chunks)
        else:
            revised_sentences.append(sentence)
    return '. '.join(s for s in revised_sentences if s.strip())

def apply_suggestions(original_text, suggestions):
    """Apply readability and style suggestions to text.
    
    Args:
        original_text (str): Original text to revise.
        suggestions (dict): Analysis suggestions from report.
    
    Returns:
        str: Revised text.
    """
    if not original_text:
        logger.warning("No text provided for revision")
        return "No content to revise."
    
    logger.info("Applying revision suggestions")
    revised_text = original_text
    
    # Apply all relevant suggestions
    for suggestion in suggestions.get('readability', {}).get('suggestions', []) + suggestions.get('style', {}).get('suggestions', []):
        if 'simplify sentences' in suggestion.lower() or 'replace jargon' in suggestion.lower():
            revised_text = replace_jargon(revised_text)
        if 'break sentences' in suggestion.lower() or 'shorten' in suggestion.lower():
            revised_text = split_long_sentences(revised_text)
        if 'second-person' in suggestion.lower():
            revised_text = convert_to_second_person(revised_text)
        if 'shorten' in suggestion.lower() or 'simplify' in suggestion.lower():
            sentences = nltk.sent_tokenize(revised_text)
            revised_text = '. '.join(simplify_sentence(s) for s in sentences if s.strip())
    
    # Clean up punctuation
    revised_text = re.sub(r'\.\.+', '.', revised_text)
    revised_text = re.sub(r'\s+\.', '.', revised_text)
    revised_text = revised_text.strip('. ')
    
    logger.info("Revision completed")
    return revised_text

def revise_documentation(url, report_file):
    """Revise a webpage's content based on analysis report.
    
    Args:
        url (str): Webpage URL.
        report_file (str): Path to analysis report JSON.
    
    Returns:
        dict: Revision results with original and revised text.
    """
    logger.info(f"Starting revision for URL: {url}")
    original_text, error = fetch_article_content(url)
    if error:
        logger.warning(f"Content fetching error: {error}")
    
    try:
        with open(report_file, 'r') as f:
            report = json.load(f)
    except Exception as e:
        logger.error(f"Error reading report: {str(e)}")
        # Fallback suggestions
        report = {
            "analysis": {
                "readability": {
                    "suggestions": [
                        "Simplify sentences, e.g., replace 'utilize' with 'use'.",
                        "Break sentences longer than 15 words into shorter ones."
                    ]
                },
                "style": {
                    "suggestions": [
                        "Use second-person pronouns, e.g., 'You can' instead of 'Users can'.",
                        "Replace jargon with simpler terms.",
                        "Shorten complex sentences."
                    ]
                }
            }
        }
    
    suggestions = report.get('analysis', {})
    revised_text = apply_suggestions(original_text, suggestions)
    
    # Save revised content as Markdown
    md_output = os.path.join(OUTPUT_DIR, "revised__content.md")
    txt_output = os.path.join(OUTPUT_DIR, "revised_content.txt")
    try:
        with open(md_output, 'w') as f:
            f.write("# Revised Webpage Content\n\n")
            f.write(revised_text)
        logger.info(f"Revised Markdown saved to {md_output}")
        
        with open(txt_output, 'w') as f:
            f.write(revised_text)
        logger.info(f"Revised text saved to {txt_output}")
    except Exception as e:
        logger.error(f"Error saving output files: {str(e)}")
        return {"url": url, "error": f"Error saving output files: {str(e)}", "revised_text": revised_text}
    
    return {
        "url": url,
        "original_text": original_text,
        "revised_text": revised_text,
        "output_files": [md_output, txt_output]
    }
