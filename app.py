from flask import Flask, render_template, request
import json
from doc_analyzer import analyze_documentation
from doc_revision import revise_documentation

app = Flask(__name__)

@app.route('/')
def index():
    """Render the input form."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze and revise the provided URL."""
    url = request.form.get('url')
    if not url:
        return render_template('result.html', error="No URL provided.", analysis_report=None, revision_result=None, revised_text=None)
    
    try:
        # Ensure URL has a scheme
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Run Task 1: Analyze documentation
        analysis_report = analyze_documentation(url)
        
        # Run Task 2: Revise documentation
        revision_result = revise_documentation(url, "report.json")
        
        # Read revised Markdown file
        revised_text = None
        if 'output_file' in revision_result:
            try:
                with open(revision_result['output_file'], 'r') as f:
                    revised_text = f.read()
            except Exception as e:
                revised_text = f"Error reading revised file: {str(e)}"
        
        return render_template(
            'result.html',
            analysis_report=json.dumps(analysis_report, indent=4),
            revision_result=json.dumps(revision_result, indent=4),
            revised_text=revised_text,
            error=None
        )
    except Exception as e:
        return render_template(
            'result.html',
            error=f"Error processing URL: {str(e)}. Ensure API keys are valid and the URL is accessible.",
            analysis_report=None,
            revision_result=None,
            revised_text=None
        )

if __name__ == '__main__':
    app.run(debug=True)