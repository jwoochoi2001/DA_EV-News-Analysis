import numpy as np, pandas as pd, umap, plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.decomposition import PCA
from sklearn.manifold import trustworthiness
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors
E = np.load('title_embeddings.npy'); d = pd.read_csv('title_embeddings_index.csv')
y = (d['언어'] == 'ko').astype(int).values
P = PCA(2, random_state=0).fit_transform(E)
U = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1, metric='cosine', random_state=0).fit_transform(E)
pd.DataFrame({'언어': d['언어'], '정리_제목': d['정리_제목'], 'umap1': U[:, 0], 'umap2': U[:, 1]}).to_csv('title_umap.csv', index=False, encoding='utf-8-sig')
def knn_purity(X, k=10):
    idx = NearestNeighbors(n_neighbors=k + 1).fit(X).kneighbors(X, return_distance=False)[:, 1:]
    return (y[idx] == y[:, None]).mean()
print('%-8s %12s %12s %12s' % ('', '신뢰도(k=10)', '언어 실루엣', '이웃언어일치'))
print('%-8s %12s %12.3f %12.3f' % ('384차원', '-', silhouette_score(E, y, metric='cosine'), knn_purity(E)))
for n, X in (('PCA', P), ('UMAP', U)):
    print('%-8s %12.3f %12.3f %12.3f' % (n, trustworthiness(E, X, n_neighbors=10, metric='cosine'), silhouette_score(X, y), knn_purity(X)))
fig = make_subplots(rows=1, cols=2, subplot_titles=('PCA', 'UMAP (cosine, n_neighbors=15, min_dist=0.1)'))
for c, X in ((1, P), (2, U)):
    for lang, name, color in (('ko', '한국어', '#2a6fdb'), ('en', '영어', '#e0782b')):
        m = (d['언어'] == lang).values
        t = d.loc[m, '정리_제목'].str.replace(r'(.{40})', r'\1<br>', regex=True)
        fig.add_trace(go.Scatter(x=X[m, 0], y=X[m, 1], mode='markers', name=name, legendgroup=name, showlegend=(c == 1),
            marker=dict(size=9, color=color, opacity=0.75, line=dict(width=0.5, color='white')),
            customdata=np.stack([t, d.loc[m, '매체'] if '매체' in d else d.loc[m, '언어']], axis=1),
            hovertemplate='<b>%{customdata[0]}</b><extra>' + name + '</extra>'), row=1, col=c)
fig.update_layout(title='제목 임베딩 차원축소 비교: PCA vs UMAP', template='plotly_white', height=650,
                  font=dict(family='Malgun Gothic, sans-serif'), hoverlabel=dict(align='left'))
fig.write_html('pca_vs_umap.html', include_plotlyjs=True)
