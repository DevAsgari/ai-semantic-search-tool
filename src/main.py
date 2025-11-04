from embedder import Embedder
from search import SemanticSearch
from nltk.tokenize import sent_tokenize
import nltk

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

file_path = "./data/text.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
    documents = sent_tokenize(content, language="english")

embedder = Embedder()
doc_embeddings = embedder(documents)
search_engine = SemanticSearch(doc_embeddings, documents)

print("🔍 Semantic Search App")
while True:
    query = input("\nEnter query (or 'quit' to exit): ")
    if query.lower() == "quit":
        break

    q_emb = embedder(query)
    results = search_engine.search(q_emb, top_k=3)

    print("\nTop results:")
    for text, score in results:
        print(f"- {text} (score: {score:.2f})")
