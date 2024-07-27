import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from pdfminer.high_level import extract_text

# Ensure necessary NLTK data packages are downloaded
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

def extract_text_from_pdfs(folder_path):
    combined_text = ""
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            try:
                text = extract_text(file_path)
                combined_text += text
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    return combined_text

def process_text(text):
    # Tokenize the text
    words = nltk.word_tokenize(text)
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]
    
    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    
    return ' '.join(lemmatized_words)

def process_pdfs(folder, output_file):
    # Extract text from PDFs
    combined_text = extract_text_from_pdfs(folder)
    
    # Process the text
    processed_text = process_text(combined_text)
    
    # Write the processed text to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(processed_text)
    
    print(f"Processed text saved to {output_file}")

if __name__ == "__main__":
    main()
