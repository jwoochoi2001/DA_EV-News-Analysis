"""임베딩 유사도로 기사 검색. 사용: python search.py "전기차 충전 비용" [개수]"""
import sys, numpy as np, pandas as pd
from sentence_transformers import SentenceTransformer

query = sys.argv[1] if len(sys.argv) > 1 else '전기차 충전 비용'
k = int(sys.argv[2]) if len(sys.argv) > 2 else 10
E = np.load('title_embeddings.npy'); d = pd.read_csv('title_embeddings_index.csv')
m = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', device='cpu')
s = E @ m.encode([query], normalize_embeddings=True)[0]
for r, i in enumerate(np.argsort(-s)[:k], 1):
    print(f'{r:>2} {s[i]:.3f} [{d.at[i, "언어"]}] {d.at[i, "정리_제목"]} | {d.at[i, "매체"]}')
