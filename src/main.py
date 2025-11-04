from embedder import Embedder
from search import SemanticSearch
from nltk.tokenize import sent_tokenize
import nltk
import sys
import os

# Download required NLTK data
try:
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)
except Exception as e:
    print(f"⚠️  Warning: Failed to download NLTK data: {e}")
    print("Continuing anyway - may fail if data is not already installed.")

file_path = "./data/text.md"

# Load and tokenize text corpus
try:
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        print(f"Please ensure the file exists or update the file_path variable.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        print(f"❌ Error: File is empty: {file_path}")
        sys.exit(1)

    documents = sent_tokenize(content, language="english")
    print(f"✓ Loaded {len(documents)} documents from {file_path}")

except UnicodeDecodeError:
    print(f"❌ Error: Failed to decode {file_path} as UTF-8")
    print("Try converting the file to UTF-8 encoding or update the encoding parameter.")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error loading file: {e}")
    sys.exit(1)

# Initialize embedder and search engine
try:
    print("Loading embedding model (this may take a moment on first run)...")
    embedder = Embedder()
    print("✓ Model loaded successfully")

    print("Creating document embeddings...")
    doc_embeddings = embedder(documents)
    print("✓ Embeddings created")

    print("Building search index...")
    search_engine = SemanticSearch(doc_embeddings, documents)
    print("✓ Search engine ready")

except Exception as e:
    print(f"❌ Error initializing search engine: {e}")
    print("This may be due to network issues downloading the model.")
    print("Please check your internet connection and try again.")
    sys.exit(1)

print("\n🔍 Semantic Search App")
print("=" * 50)

while True:
    try:
        query = input("\nEnter query (or 'quit' to exit): ")
        if query.lower() == "quit":
            print("Goodbye!")
            break

        if not query.strip():
            print("⚠️  Please enter a valid query")
            continue

        q_emb = embedder(query)
        results = search_engine.search(q_emb, top_k=3)

        print("\nTop results:")
        for text, score in results:
            print(f"- {text[:100]}{'...' if len(text) > 100 else ''} (score: {score:.2f})")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        break
    except Exception as e:
        print(f"❌ Error during search: {e}")
        print("Please try a different query.")
