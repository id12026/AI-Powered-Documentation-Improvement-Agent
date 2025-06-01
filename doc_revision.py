import requests
import json
import nltk
import re
from urllib.parse import urlparse
from doc_analyzer import fetch_article_content

# Download NLTK data
nltk.download('punkt')

# API keys (replace with your own)
HUGGINGFACE_API_KEY = "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"

def query_huggingface(text, task="summarization", model="facebook/bart-large-cnn"):
    """Query Hugging Face Inference API for text simplification."""
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": text[:512],
        "parameters": {"max_length": max(20, len(text.split()) // 2), "min_length": max(10, len(text.split()) // 4)}
    }
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model}",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()[0]['summary_text']
    except Exception as e:
        return text  # Fallback to original text

def simplify_sentence(sentence):
    """Simplify a sentence using Hugging Face BART model."""
    if len(sentence.split()) > 10:
        simplified = query_huggingface(sentence)
        return simplified if simplified != sentence else sentence
    return sentence

def replace_jargon(text):
    """Replace jargon with simpler terms."""
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
    """Convert third-person to second-person pronouns."""
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
    """Split sentences longer than 10 words into shorter ones."""
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
    """Apply readability and style suggestions."""
    if not original_text:
        return "No content to revise."
    
    revised_text = original_text

    # Apply all suggestions
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
    
    return revised_text

def revise_documentation(url, report_file):
    """Revise a webpage's content."""
    original_text, error = fetch_article_content(url)
    if error:
        print(f"Warning: {error}")
    
    try:
        with open(report_file, 'r') as f:
            report = json.load(f)
    except Exception as e:
        # Fallback suggestions
        print(f"Warning: {str(e)}. Using default suggestions.")
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

    output_filename = f"revised_{urlparse(url).path.replace('/', '_') or 'page'}.md"
    try:
        with open(output_filename, 'w') as f:
            f.write("# Revised Webpage Content\n\n")
            f.write(revised_text)
    except Exception as e:
        return {"url": url, "error": f"Error saving Markdown file: {str(e)}", "revised_text": revised_text}

    return {
        "url": url,
        "original_text": original_text,
        "revised_text": revised_text,
        "output_file": output_filename
    }