import os
import json
import pandas as pd
from pypdf import PdfReader

def load_all_documents(folder_path):
    """
    Load all documents from folder
    Supports: .txt, .pdf, .csv, .json
    Returns: dict of {filename: content_text}
    """
    documents = {}
    
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    files = os.listdir(folder_path)
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        try:
            # Get file extension
            _, ext = os.path.splitext(file)
            ext = ext.lower()
            
            print(f"📄 Loading: {file}")
            
            if ext == '.txt':
                content = load_txt(file_path)
            elif ext == '.pdf':
                content = load_pdf(file_path)
            elif ext == '.csv':
                content = load_csv(file_path)
            elif ext == '.json':
                content = load_json(file_path)
            else:
                print(f"   ⚠️  Skipping unknown format: {ext}")
                continue
            
            documents[file] = content
            print(f"   ✅ Success ({len(content)} chars)")
            
        except Exception as e:
            print(f"   ❌ Error loading {file}: {e}")
    
    return documents


def load_txt(file_path):
    """Load text file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_pdf(file_path):
    """
    Load PDF file using pypdf
    Extract text from all pages
    """
    reader = PdfReader(file_path)
    text_parts = []
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        text_parts.append(f"=== Page {i+1} ===\n{text}")
    
    return "\n\n".join(text_parts)


def load_csv(file_path):
    """
    Load CSV and convert to readable narrative
    Makes it easier for LLM to understand
    """
    df = pd.read_csv(file_path)
    
    # Create readable narrative
    lines = [f"CSV File: {os.path.basename(file_path)}"]
    lines.append(f"Total Records: {len(df)}")
    lines.append(f"Columns: {', '.join(df.columns)}")
    lines.append("\n=== DATA ===")
    
    # Convert each row to readable format
    for idx, row in df.iterrows():
        row_text = f"\nRecord {idx + 1}:"
        for col in df.columns:
            row_text += f"\n  - {col}: {row[col]}"
        lines.append(row_text)
    
    return "\n".join(lines)


def load_json(file_path):
    """
    Load JSON and convert to readable format
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convert to readable string
    lines = [f"JSON File: {os.path.basename(file_path)}"]
    lines.append("\n=== CONTENT ===")
    
    # Pretty format JSON
    readable = json.dumps(data, indent=2)
    lines.append(readable)
    
    return "\n".join(lines)
