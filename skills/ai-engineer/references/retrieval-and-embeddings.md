# Retrieval and embeddings (answering from documents)

When to read this: a chatbot or assistant must answer from the owner's documents (FAQ, policies, manuals), or someone asks about vector databases and embeddings.

## 1. The shape
Retrieval-augmented generation keeps the knowledge outside the model: find the relevant passages, give them to the model, answer only from them [S-RAG-1]. Each stage can fail on its own: indexing, retrieval, ranking, generation [S-RAG-2]. Evaluate retrieval and answers separately.

## 2. Start with keyword search
- For small collections (tens to a few thousand pages) a keyword ranking such as BM25 is a strong, cheap baseline that embeddings do not always beat on new domains [S-RAG-4]. SQLite's built-in full-text search ranks with BM25 and needs no service [S-RAG-10].
- Add embeddings when users ask with words that do not appear in the documents (synonyms, other languages). Dense retrieval can win on some tasks [S-RAG-3], but no single embedding model wins everywhere; test on your own questions [S-RAG-5].
- Merging keyword and vector rankings with reciprocal rank fusion is simple and robust [S-RAG-7]. Adding short context to each chunk and reranking are further steps; the published gains are the vendor's own figures [S-RAG-6].
- Storage: a local index (Faiss) [S-RAG-8] or vectors inside Postgres with SQL filters (pgvector) [S-RAG-9] before a separate vector service.

## 3. Documents are versioned facts
- Keep a date or version per document; when two documents disagree (an old and a new returns policy), index only the current one or rank it first and tell the owner about the conflict. Never let the model pick.
- Record the source file of every chunk so answers can cite it.
- Documents are untrusted text: a page may contain instructions for the assistant. Do not index or pass instructions as instructions; flag such passages to the owner and test them (`security-and-injection.md`).

## 4. Answering
- Answer only from the retrieved passages; cite the file; if nothing relevant was retrieved (score below a threshold), say "I don't know" and give the contact path [S-LLM-6].
- Put the best passages first and keep the count small; models use the start and end of a long context better than the middle [S-EVL-11].

## 5. Stdlib keyword retriever (good enough for small FAQs and tests)
```python
import math, re, collections
from pathlib import Path
TOK = re.compile(r"[a-z0-9]+")
def tokens(s): return TOK.findall(s.lower())
class BM25:
    def __init__(self, docs: dict[str, str], k1=1.5, b=0.75):
        self.docs = {k: tokens(v) for k, v in docs.items()}; self.k1, self.b = k1, b
        self.avg = sum(map(len, self.docs.values())) / max(1, len(self.docs))
        self.df = collections.Counter(t for d in self.docs.values() for t in set(d))
    def score(self, q, d):
        tf = collections.Counter(d); n = len(self.docs); s = 0.0
        for t in tokens(q):
            if t not in tf: continue
            idf = math.log(1 + (n - self.df[t] + 0.5) / (self.df[t] + 0.5))
            s += idf * tf[t] * (self.k1 + 1) / (tf[t] + self.k1 * (1 - self.b + self.b * len(d) / self.avg))
        return s
    def top(self, q, k=3, min_score=1.0):
        ranked = sorted(((self.score(q, d), name) for name, d in self.docs.items()), reverse=True)
        return [(name, s) for s, name in ranked[:k] if s >= min_score]
```
Tune `min_score` on the eval set's "not found" questions. Roman Urdu and English mixed questions need a few synonyms or an embedding step; measure, do not assume.

## 6. Evaluate
- Retrieval: for each eval question, is the right file in the top k?
- Answer: faithful to the passages, relevant to the question, cites the source; reference-free metrics exist but have caveats, so spot-check by hand [S-EVL-9].
- Cases: normal, paraphrased, other language, not answerable, conflicting documents, attack passage.

## 7. Failure modes
Stuffing the whole knowledge base into every prompt; chunks that cut a rule in half; old documents still indexed; answers without citations; a confident answer when retrieval found nothing; hallucinated details beyond the passages [S-EVL-10].
