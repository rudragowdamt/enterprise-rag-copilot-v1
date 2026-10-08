from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.documents import load_corpus

root = Path(__file__).resolve().parents[1] / "data" / "knowledge"
docs = load_corpus(root)
print(f"Documents: {len(docs)}")
for d in docs:
    print(f"- [{d.doc_type:12}] {d.title} | system={d.system} | env={d.environment}")
