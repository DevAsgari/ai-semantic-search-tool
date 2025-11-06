# AI Semantic Search Tool

```text
🔍 AI Semantic Search Tool

Enter query (or 'quit' to exit): AI

Top results:
- The AI revolution is escalating this challenge. (score: 0.61)
- This momentum signals an accelerating shift—AI adoption is not just expanding but becoming a corne... (score: 0.58)
- By prioritizing security alongside AI advancements, businesses can not only stay ahead of the ever-... (score: 0.55)

📝 Summary: The rise of AI, particularly generative AI, presents both opportunities and challenges for security. 
By prioritizing security alongside AI advancements, businesses can stay ahead of the ever-evolving threat landscape.
```

A prototype AI-powered search tool that finds text based on meaning, not just keywords.
Built with **Sentence-BERT**, **FAISS**, and **BART**, it turns text into vector embeddings, finds the passages that are semantically closest to your query, and generates concise summaries.
It's a prototype showing how modern NLP can make search more accurate, flexible, and human-like. 

---

## Project Structure

```text
semantic-search-app/
├── data/                  # Documents for searching (supports .txt, .md, .pdf) 
│
├── src/                   # Source code
│   ├── embedder.py        # Wrapper for Sentence-BERT embeddings
│   ├── search.py          # Semantic search using FAISS
│   ├── generator.py       # BART-based summary generator
│   ├── file_loader.py     # Generic document loader for multiple formats
│   └── main.py            # CLI interface with search and summarization
│
├── requirements.txt       # Python dependencies
└── README.md              # Project description
```

---

## Installation

1. Clone the project:

```bash
git clone https://github.com/<your-repo>/SemanticSearchApp.git
cd SemanticSearchApp
```

2. Set up a virtual environment and install dependencies:

**Using venv:**
```bash
python -m venv venv

# On Windows (PowerShell):
venv\Scripts\Activate.ps1
# On Windows (CMD):
venv\Scripts\activate.bat
# On Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

**Using Conda:**
```bash
conda create -n semantic-search python=3.11
conda activate semantic-search
pip install -r requirements.txt
```

3. Add your documents to the `./data/` folder.
The tool automatically loads all supported files (.txt, .md, .pdf) from the data directory.
The repo comes with sample files you can replace or extend.

## Usage

Run a search from the project root:

```bash
python src/main.py
```

Type a query to get semantically relevant passages with an automatic AI-generated summary.

---

## How the AI Works

This tool uses modern NLP and vector search to retrieve passages based on meaning rather than exact words. Here's how it works under the hood:

### 1. Embeddings (Sentence-BERT)
- Both the text passages and user queries are encoded into vectors using Sentence-BERT.
- These embeddings capture semantic meaning, so that even differently worded texts can be recognized as similar.

### 2. Vector Indexing (FAISS)
- All embeddings are stored in a FAISS index that enables fast and scalable similarity search.
- When a query is submitted, its embedding is compared to the stored ones to find the nearest matches.

### 3. Similarity Scores (cosine similarity)
- Each result includes a **similarity score**, calculated using **cosine similarity** between the query and each passage.
- A score close to **1.0** means high semantic overlap; a score closer to **0.0** means weak or no similarity.
- For example, `(score: 0.89)` means the model finds that result highly relevant to the query's meaning.

## Tech Stack
- **Python 3.11+**
- **Sentence-BERT** (all-mpnet-base-v2 model) for text embeddings
- **FAISS** (IndexFlatIP) for fast vector similarity search
- **NLTK** for sentence tokenization
- **BART** (facebook/bart-large-cnn) for AI summary generation
- **PyPDF2** for PDF text extraction

## Features
- **Semantic search** - Find text based on meaning, not just keywords
- **AI-generated summaries** - Automatic summaries of search results using BART (facebook/bart-large-cnn)
- **Multi-format support** - Automatically loads and indexes .txt, .md, and .pdf files from data directory
- **Plug-and-play** - Just drop files in ./data/ folder and run - no configuration needed

## Language Support
- Uses the **all-mpnet-base-v2** model, which supports English and multiple other languages
- Produces 768-dimensional embeddings (higher quality than the previous all-MiniLM-L6-v2 model)
- Model size: ~420MB (automatically downloaded on first run)

