from flask import Flask, render_template, request
import json
import os
import logging
from backend.doc_analyzer import analyze_documentation
from backend.doc_revision import revise_documentation

# Configure logging for Flask app
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Output directory
OUTPUT_DIR = "Output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/')
def index():
    """Render the input form.
    
    Returns:
        str: Rendered index.html template.
    """
    logger.info("Rendering index page")
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze and revise the provided URL.
    
    Returns:
        str: Rendered result.html template with analysis and revision data.
    """
    logger.info("Processing analyze request")
    url = request.form.get('url')
    if not url:
        logger.warning("No URL provided in request")
        return render_template('result.html', error="No URL provided.", analysis_report=None, revision_result=None, revised_text=None)
    
    try:
        # Ensure URL has a scheme
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            logger.info(f"Added https scheme to URL: {url}")
        
        # Run Task 1: Analyze documentation
        logger.info("Starting documentation analysis")
        analysis_report = analyze_documentation(url)
        
        # Run Task 2: Revise documentation
        logger.info("Starting documentation revision")
        revision_result = revise_documentation(url, os.path.join(OUTPUT_DIR, "analysis_report.json"))
        
        # Save revision result as JSON
        revision_json_path = os.path.join(OUTPUT_DIR, "revision_result.json")
        try:
            with open(revision_json_path, 'w') as f:
                json.dump(revision_result, f, indent=4)
            logger.info(f"Revision result saved to {revision_json_path}")
        except Exception as e:
            logger.error(f"Error saving revision result: {str(e)}")
        
        # Read revised Markdown file
        revised_text = None
        md_output = os.path.join(OUTPUT_DIR, "revised__content.md")
        try:
            with open(md_output, 'r') as f:
                revised_text = f.read()
            logger.info(f"Successfully read revised file: {md_output}")
        except Exception as e:
            logger.error(f"Error reading revised file: {str(e)}")
            revised_text = f"Error reading revised file: {str(e)}"
        
        logger.info("Rendering result page")
        return render_template(
            'result.html',
            analysis_report=json.dumps(analysis_report, indent=4),
            revision_result=json.dumps(revision_result, indent=4),
            revised_text=revised_text,
            error=None
        )
    except Exception as e:
        logger.error(f"Error processing URL: {str(e)}")
        return render_template(
            'result.html',
            error=f"Error processing URL: {str(e)}. Ensure the URL is accessible.",
            analysis_report=None,
            revision_result=None,
            revised_text=None
        )

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True)
