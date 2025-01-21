from urllib.parse import urlparse
from bs4 import BeautifulSoup

def extract_domain(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc

def clean_form_labels(label_array):
    cleaned_labels = []
    
    for label_html in label_array:
        try:
            soup = BeautifulSoup(label_html, "html.parser")
            
            all_texts = soup.stripped_strings
            
            unique_texts = list(dict.fromkeys(all_texts))
            
            cleaned_label = " ".join(unique_texts)
            
            cleaned_labels.append(cleaned_label)
        except Exception as e:
            print(f"Error processing label: {e}")
            cleaned_labels.append("Error in label")
    
    return cleaned_labels
