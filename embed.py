import numpy as np, pandas as pd
from sentence_transformers import SentenceTransformer
M = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
d = pd.read_csv('ev_news_review.csv', dtype=str, keep_default_na=False)
model = SentenceTransformer(M, device='cpu')
E = model.encode(d['정리_제목'].tolist(), batch_size=32, normalize_embeddings=True, show_progress_bar=False)
np.save('title_embeddings.npy', E)
d[['언어', '정리_제목', '매체', '발행일', '링크']].to_csv('title_embeddings_index.csv', index=False, encoding='utf-8-sig')
print(E.shape, E.dtype, 'max_seq_length', model.max_seq_length)
ko = np.where(d['언어'] == 'ko')[0]; en = np.where(d['언어'] == 'en')[0]
S = E[ko] @ E[en].T
print('ko-en 유사도 평균 %.3f 최대 %.3f' % (S.mean(), S.max()))
print('ko-ko 평균 %.3f / en-en 평균 %.3f' % ((E[ko] @ E[ko].T)[np.triu_indices(len(ko), 1)].mean(), (E[en] @ E[en].T)[np.triu_indices(len(en), 1)].mean()))
idx = np.dstack(np.unravel_index(np.argsort(-S.ravel()), S.shape))[0]
seen_k, seen_e, n = set(), set(), 0
for i, j in idx:
    if i in seen_k or j in seen_e: continue
    seen_k.add(i); seen_e.add(j); n += 1
    print('%.3f | %s | %s' % (S[i, j], d.at[ko[i], '정리_제목'], d.at[en[j], '정리_제목']))
    if n == 8: break
