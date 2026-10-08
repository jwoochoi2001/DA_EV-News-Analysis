import numpy as np, pandas as pd, plotly.graph_objects as go
from sklearn.decomposition import PCA
E = np.load('title_embeddings.npy'); d = pd.read_csv('title_embeddings_index.csv')
p = PCA(n_components=2, random_state=0); X = p.fit_transform(E)
r = p.explained_variance_ratio_
print('설명 분산', r, r.sum())
d['PC1'], d['PC2'] = X[:, 0], X[:, 1]
d[['언어', '정리_제목', '매체', 'PC1', 'PC2']].to_csv('title_pca.csv', index=False, encoding='utf-8-sig')
fig = go.Figure()
for lang, name, color in (('ko', '한국어', '#2a6fdb'), ('en', '영어', '#e0782b')):
    s = d[d['언어'] == lang]
    fig.add_trace(go.Scatter(x=s['PC1'], y=s['PC2'], mode='markers', name=f'{name} ({len(s)}건)',
        marker=dict(size=9, color=color, opacity=0.75, line=dict(width=0.5, color='white')),
        customdata=np.stack([s['정리_제목'].str.replace(r'(.{40})', r'\1<br>', regex=True), s['매체']], axis=1),
        hovertemplate='<b>%{customdata[0]}</b><br>%{customdata[1]}<br>PC1 %{x:.3f}, PC2 %{y:.3f}<extra>' + name + '</extra>'))
fig.update_layout(title=f'제목 임베딩 PCA 2차원 (설명 분산 PC1 {r[0]:.1%} + PC2 {r[1]:.1%} = {r.sum():.1%})',
    xaxis_title=f'PC1 ({r[0]:.1%})', yaxis_title=f'PC2 ({r[1]:.1%})', template='plotly_white',
    font=dict(family='Malgun Gothic, Apple SD Gothic Neo, sans-serif'), hoverlabel=dict(align='left'), height=700)
fig.write_html('title_pca.html', include_plotlyjs=True)
