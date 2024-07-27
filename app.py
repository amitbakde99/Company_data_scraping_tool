from flask import Flask, request, send_file, redirect, url_for
import os
from scraper_v7 import scrape_website, scrape_careers_section
from HTML_content_extractor_and_combiner import process_html_files_in_directory
from Document_combiner_and_extractor_v3 import extract_text_from_pdfs, process_text

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h1>Company Data Scraping Tool</h1>
        <form action="/scrape" method="post">
            <label for="url">Company URL:</label>
            <input type="text" id="url" name="url" required>
            <button type="submit">Scrape</button>
        </form>
    '''

@app.route('/scrape', methods=['POST'])
def scrape():
    company_url = request.form['url'].strip()

    if not company_url:
        return "URL is required.", 400

    # Create output directory
    parsed_url = urlparse(company_url)
    company_name = parsed_url.netloc.replace('www.', '').replace('.com', '').replace('.org', '')
    output_folder = f'{company_name}_scraped_data'

    # Create main directory
    create_folder(output_folder)

    # Scrape website
    scrape_website(company_url, output_folder, common_tabs=['#main-nav', '.footer', 'header', 'footer'])
    
    # Scrape Careers section
    scrape_careers_section(company_url)

    # Process PDFs
    pdf_folder = os.path.join(output_folder, 'documents')
    if os.path.exists(pdf_folder):
        combined_text = extract_text_from_pdfs(pdf_folder)
        processed_text = process_text(combined_text)
        with open(os.path.join(output_folder, 'documents.txt'), 'w', encoding='utf-8') as file:
            file.write(processed_text)

    # Process HTML
    html_folder = os.path.join(output_folder, 'htmls')
    if os.path.exists(html_folder):
        html_output_file = os.path.join(output_folder, 'all_html.txt')
        process_html_files_in_directory(html_folder, html_output_file)
        
        # Process Careers HTML
        careers_html_folder = os.path.join(output_folder, f"{company_name}_careers_scraped_data", 'links')
        if os.path.exists(careers_html_folder):
            careers_output_file = os.path.join(output_folder, 'careers.txt')
            process_html_files_in_directory(careers_html_folder, careers_output_file)

    return redirect(url_for('download', filename=f'{company_name}_scraped_data'))

@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(filename, 'documents.txt')
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found.", 404

def create_folder(folder_path):
    """Creates a folder if it doesn't exist."""
    os.makedirs(folder_path, exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True)
