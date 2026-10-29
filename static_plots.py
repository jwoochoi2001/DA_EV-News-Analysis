import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from fonts import setup_matplotlib; setup_matplotlib()
p = pd.read_csv('title_pca.csv'); u = pd.read_csv('title_umap.csv')
fig, ax = plt.subplots(1, 2, figsize=(14, 6))
for a, df, x, y, t in ((ax[0], p, 'PC1', 'PC2', 'PCA (설명 분산 PC1 15.1% + PC2 7.5% = 22.6%)'), (ax[1], u, 'umap1', 'umap2', 'UMAP (cosine, n_neighbors=15, min_dist=0.1)')):
    for l, n, c in (('ko', '한국어 (98)', '#2a6fdb'), ('en', '영어 (100)', '#e0782b')):
        s = df[df['언어'] == l]; a.scatter(s[x], s[y], s=28, c=c, alpha=0.75, label=n, edgecolor='white', linewidth=0.4)
    a.set_title(t); a.legend(); a.spines[['top', 'right']].set_visible(False)
plt.tight_layout(); plt.savefig('pca_vs_umap.png', dpi=130)
