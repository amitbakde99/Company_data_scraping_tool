import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib
from urllib3.exceptions import InsecureRequestWarning
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Suppress SSL certificate warnings (use with caution)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def create_folder(folder_path):
    """Creates a folder if it doesn't exist."""
    os.makedirs(folder_path, exist_ok=True)

def get_unique_filename(url):
    """Generates a unique filename based on URL hash."""
    parsed_url = urlparse(url)
    file_name = hashlib.md5(url.encode()).hexdigest()
    return file_name + ".html"

def get_document_filename(url):
    """Extracts the filename from the URL for documents."""
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)

def save_content(content, folder_path, filename):
    """Saves content (text or binary) to a file."""
    with open(os.path.join(folder_path, filename), 'wb') as f:
        f.write(content)

def scrape_website(url, folder_path, visited=set(), depth=0, max_depth=3, common_tabs=None):
    """Recursively scrapes a website up to max_depth."""
    if depth > max_depth or url in visited:
        return

    visited.add(url)

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        if common_tabs:
            for tab in common_tabs:
                for elem in soup.select(tab):
                    elem.decompose()

        # Save HTML content excluding header, footer, and common tabs
        html_folder = os.path.join(folder_path, 'htmls')
        create_folder(html_folder)
        filtered_content = soup.prettify('utf-8')
        save_content(filtered_content, html_folder, get_unique_filename(url))

        # Save documents
        doc_folder = os.path.join(folder_path, 'documents')
        create_folder(doc_folder)
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(url, href)
            if urlparse(full_url).netloc == urlparse(url).netloc:
                if full_url.endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx')):
                    save_content(requests.get(full_url, verify=False).content, doc_folder, get_document_filename(full_url))
                else:
                    scrape_website(full_url, folder_path, visited, depth + 1, max_depth, common_tabs)
                    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")

def safe_filename(text):
    # Replace characters not allowed in Windows filenames
    return ''.join(c for c in text if c.isalnum() or c in [' ', '_', '-', '.'])

def scrape_careers_section(company_url, output_folder):
    # Parse the company URL
    parsed_url = urlparse(company_url)
    company_name = parsed_url.netloc.replace('www.', '').replace('.com', '').replace('.org', '')  # Extract company name

    # Create main directory for scraped data
    main_dir = os.path.join(output_folder, f"{company_name}_careers_scraped_data")
    create_folder(main_dir)

    # Subdirectories for links and documents
    links_dir = os.path.join(main_dir, 'links')
    create_folder(links_dir)

    documents_dir = os.path.join(main_dir, 'documents')
    create_folder(documents_dir)

    # Retry mechanism setup
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    # Fetch HTML content
    try:
        response = session.get(company_url, timeout=30, allow_redirects=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find link to Careers section
            careers_link = None
            header_careers_link = soup.find('a', string='Careers')
            footer_careers_link = soup.find('a', string='Careers')  # Adjust if different in actual site structure

            if header_careers_link:
                careers_link = header_careers_link.get('href')
            elif footer_careers_link:
                careers_link = footer_careers_link.get('href')

            if careers_link:
                # Convert relative URL to absolute URL
                careers_url = urljoin(company_url, careers_link)
                careers_response = session.get(careers_url, timeout=30, allow_redirects=False)
                if careers_response.status_code == 200:
                    careers_soup = BeautifulSoup(careers_response.content, 'html.parser')

                    # Example: Find all links in the 'Careers' section
                    links = careers_soup.find_all('a', href=True)
                    for link in links:
                        link_url = urljoin(careers_url, link['href'])  # Convert relative link to absolute
                        # Check if link is HTTP/HTTPS
                        if link_url.startswith('http://') or link_url.startswith('https://'):
                            # Save each link as an HTML file
                            filename = safe_filename(link_url.split('/')[-1].replace('.html', '')) + '.html'
                            with open(os.path.join(links_dir, filename), 'w', encoding='utf-8') as f:
                                f.write(session.get(link_url, timeout=30, allow_redirects=False).text)

                    # Example: Find all downloadable documents (PDFs)
                    documents = careers_soup.find_all('a', {'class': 'document'}, href=True)
                    for doc in documents:
                        doc_url = urljoin(careers_url, doc['href'])  # Convert relative link to absolute
                        # Check if link is HTTP/HTTPS
                        if doc_url.startswith('http://') or doc_url.startswith('https://'):
                            # Download and save documents
                            doc_filename = safe_filename(doc_url.split('/')[-1])
                            with open(os.path.join(documents_dir, doc_filename), 'wb') as f:
                                f.write(session.get(doc_url, timeout=30, allow_redirects=False).content)
                else:
                    print(f"Failed to retrieve Careers page: {careers_response.status_code}")

            else:
                print("Careers link not found.")

        else:
            print(f"Failed to retrieve page: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")

if __name__ == '__main__':
    company_url = input("Enter the company website URL: ")
    parsed_url = urlparse(company_url)
    domain = parsed_url.netloc.split('.')[1] if 'www' in parsed_url.netloc else parsed_url.netloc.split('.')[0]
    output_folder = f'{domain}_scraped_data'
    common_tabs = ['#main-nav', '.footer', 'header', 'footer']

    create_folder(output_folder)
    scrape_website(company_url, output_folder, common_tabs=common_tabs)
    scrape_careers_section(company_url, output_folder)
