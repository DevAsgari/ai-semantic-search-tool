from embedder import Embedder
from search import SemanticSearch
from generator import SummaryGenerator
from file_loader import DocumentLoader
from nltk.tokenize import sent_tokenize
import nltk
import sys

# Download required NLTK data
try:
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)
except Exception as e:
    print(f"⚠️  Warning: Failed to download NLTK data: {e}")
    print("Continuing anyway - may fail if data is not already installed.")

# Load all documents from data directory
try:
    print("Loading documents from data directory...")
    loader = DocumentLoader(data_dir="./data")
    content, files_loaded = loader.load_all_documents()

    print(f"✓ Loaded {len(files_loaded)} file(s):")
    for filename in files_loaded:
        print(f"  • {filename}")

    if not content.strip():
        print(f"❌ Error: All files are empty")
        sys.exit(1)

    print("\nTokenizing documents into sentences...")
    documents = sent_tokenize(content, language="english")
    print(f"✓ Created {len(documents)} searchable text segments")

except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    print("Please ensure the ./data directory exists with at least one .txt, .md, or .pdf file.")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error loading documents: {e}")
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

    print("Loading summary generator (this may take a moment)...")
    summary_generator = SummaryGenerator()
    print("✓ Summary generator ready")

except Exception as e:
    print(f"❌ Error initializing search engine: {e}")
    print("This may be due to network issues downloading the model.")
    print("Please check your internet connection and try again.")
    sys.exit(1)

print("\n🔍 Semantic Search & Summary Tool")
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

        # Generate summary automatically
        passages = [text for text, score in results]
        summary = summary_generator.generate_summary(query, passages)
        print(f"\n📝 Summary: {summary}")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        break
    except Exception as e:
        print(f"❌ Error during search: {e}")
        print("Please try a different query.")
