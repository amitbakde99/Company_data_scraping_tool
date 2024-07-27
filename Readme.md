# Company Data Scraping Tool

A Flask-based web application for scraping company data, including PDFs, HTML content, and careers section, and processing this data into downloadable text files.

## Features

- **Scrape Data**: Extracts PDFs, HTML content, and career section data from the provided company URL.
- **Process Data**: Converts extracted PDFs and HTML content into processed text files.
- **Downloadable Reports**: Provides downloadable text files containing processed data.

## Setup and Installation

### Prerequisites

- Python 3.x
- Flask
- BeautifulSoup4
- Requests
- pdfminer.six
- nltk

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/company-data-scraping-tool.git
    cd company-data-scraping-tool
    ```

2. **Install required packages:**

    ```bash
    pip install -r requirements.txt
    ```

    Create a `requirements.txt` file with the following content:

    ```text
    Flask==2.3.2
    beautifulsoup4==4.12.2
    requests==2.31.0
    pdfminer.six==20221105
    nltk==3.8.1
    ```

3. **Run the Flask application:**

    ```bash
    python app.py
    ```

4. **Open your browser and navigate to** `http://127.0.0.1:5000/` to access the application.

## Usage

1. Enter the company URL in the provided input field on the homepage.
2. Click the "Scrape" button to start the scraping and processing of data.
3. Once completed, download the generated text files from the provided download links.

## File Structure

- `app.py`: Main Flask application file.
- `scraper_v7.py`: Contains functions for scraping websites and careers sections.
- `HTML_content_extractor_and_combiner.py`: Contains functions for processing HTML content.
- `Document_combiner_and_extractor_v3.py`: Contains functions for processing PDFs.
- `requirements.txt`: List of required Python packages.
- `README.md`: This file.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask for the web framework.
- BeautifulSoup4 for HTML parsing.
- Requests for HTTP requests.
- pdfminer.six for PDF text extraction.
- NLTK for natural language processing.

