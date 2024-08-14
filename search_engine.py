from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.writing import AsyncWriter
import os
import streamlit as st

# Function to index files
def index_files(ix, directory):
    writer = AsyncWriter(ix)
    total_files = sum(len(files) for _, _, files in os.walk(directory))
    processed_files = 0

    # Use st.progress to create a progress bar
    progress_bar = st.progress(0)

    for root, dirs, files in os.walk(directory):
        for file in files:
            # Index only specific file types (e.g., .txt)
            if file.endswith(('.txt', '.docx', '.pdf')):
                try:
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        # Limit reading to the first few kilobytes if needed
                        content = f.read(10000)  # Read only first 10KB
                        writer.add_document(title=file, content=content)
                except Exception as e:
                    print(f"Error indexing file {file}: {str(e)}")
            
            # Update progress
            processed_files += 1
            progress_bar.progress(processed_files / total_files)

    writer.commit()  # Commit changes to the index

# Function to search for files
def search_files(ix, query_str):
    results_list = []
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        for result in results:
            results_list.append(dict(result))
    return results_list
