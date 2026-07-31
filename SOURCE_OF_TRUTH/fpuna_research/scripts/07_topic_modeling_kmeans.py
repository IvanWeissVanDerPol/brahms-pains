"""Topic modeling on 765 UNA theses using TF-IDF + K-means."""
import json
from pathlib import Path
from collections import defaultdict, Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Load corpus
data = json.loads(Path("/root/psycology/SOURCE_OF_TRUTH/fpuna_research/opac_una_full_from_saved.json").read_text())
recs = data["records"] if "records" in data else data

# Extract titles with metadata
titles = []
metadata = []
for r in recs:
    title = r.get("title", "").strip()
    if not title:
        continue
    titles.append(title)
    metadata.append({
        "bibnum": r.get("bibnum"),
        "year": r.get("year"),
        "branch": r.get("branch_text", ""),
        "is_thesis": r.get("is_thesis", False),
        "authors": r.get("authors", []),
        "orientadores": r.get("orientadores", []),
    })

print(f"Loaded {len(titles)} titles with text")

# Spanish stopwords + custom
STOPWORDS = set("""
a ante bajo cabe con contra de desde durante en entre hacia hasta mediante
para por segun sin sobre tras y o u pero sino mas muy ya no si es son fue
ser estar tener hacer haber ir ver dar saber querer poder ese esta estos
estas ese eso esa eso ese ser sido son era estoy estas ese esta el la los
las un una unos unas del al lo le se sus tu mi yo me ya nos como mas
todo tambien muy fue han hay si solo sin embargo
""".split())

def clean(s):
    s = s.lower()
    s = re.sub(r'[^\wáéíóúñü\s]', ' ', s)
    return ' '.join(w for w in s.split() if w not in STOPWORDS and len(w) > 2)

cleaned = [clean(t) for t in titles]

# TF-IDF
vec = TfidfVectorizer(min_df=2, max_df=0.6, ngram_range=(1,2), max_features=2000)
X = vec.fit_transform(cleaned)
print(f"TF-IDF matrix: {X.shape}")

# K-means — 20 clusters
K = 20
km = KMeans(n_clusters=K, random_state=42, n_init=10)
labels = km.fit_predict(X)

# Cluster → top terms
terms = vec.get_feature_names_out()
print("\n=== TOPIC CLUSTERS (K=20) ===")
cluster_topics = {}
for k in range(K):
    center = km.cluster_centers_[k]
    top_idx = center.argsort()[-10:][::-1]
    top_words = [terms[i] for i in top_idx]
    cluster_topics[k] = top_words

    cluster_recs = [metadata[i] for i in range(len(metadata)) if labels[i] == k]
    years = [m["year"] for m in cluster_recs if m["year"]]
    yr_counts = Counter(years)
    last_year = max([int(y) for y in years]) if years else None

    print(f"\nCluster {k} ({len(cluster_recs)} recs, last_year: {last_year}):")
    print(f"  Terms: {' | '.join(top_words[:7])}")
    if years:
        print(f"  Year range: {min(years)}-{max(years)}")
        recent = dict(sorted(yr_counts.items())[-5:])
        print(f"  Recent years: {recent}")

# Gap analysis
print("\n=== GAP CLUSTERS (last_year < 2020) ===")
gaps = []
for k in range(K):
    cluster_recs = [metadata[i] for i in range(len(metadata)) if labels[i] == k]
    years = [int(m["year"]) for m in cluster_recs if m["year"]]
    if not years:
        continue
    last_year = max(years)
    if last_year < 2020:
        gaps.append((k, cluster_topics[k], last_year, len(cluster_recs)))
        print(f"  GAP: Cluster {k}, last={last_year}, {len(cluster_recs)} recs, terms={cluster_topics[k][:5]}")

# Save results
out = []
for i, (title, meta, lbl) in enumerate(zip(titles, metadata, labels)):
    out.append({
        "bibnum": meta["bibnum"],
        "title": title,
        "year": meta["year"],
        "cluster": int(lbl),
        "cluster_terms": cluster_topics[lbl][:7],
        "branch": meta["branch"][:50] if meta["branch"] else "",
        "is_thesis": meta["is_thesis"],
    })

Path("/root/psycology/SOURCE_OF_TRUTH/fpuna_research/clustering_kmeans_k20.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
Path("/root/psycology/SOURCE_OF_TRUTH/fpuna_research/cluster_topics.json").write_text(
    json.dumps({k: v for k, v in cluster_topics.items()}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"\n✅ Saved clustering → clustering_kmeans_k20.json + cluster_topics.json")
