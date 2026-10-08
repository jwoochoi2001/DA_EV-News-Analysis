import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
from top_words import d, ko_nouns, en_words
FONT = r'C:\Windows\Fonts\malgun.ttf'
plt.rcParams['font.family'] = 'Malgun Gothic'; plt.rcParams['axes.unicode_minus'] = False
data = {}
for lang, f in (('ko', ko_nouns), ('en', en_words)):
    tot, doc = Counter(), Counter()
    for t in d[d['언어'] == lang]['제목']:
        ws = f(t); tot.update(ws); doc.update(set(ws))
    data[lang] = (tot, doc)
fig, axes = plt.subplots(1, 2, figsize=(14, 7))
for ax, (lang, name, color) in zip(axes, (('ko', '한국어 명사', '#2a6fdb'), ('en', '영어 단어', '#e0782b'))):
    tot, doc = data[lang]
    top = sorted(doc, key=lambda w: (-doc[w], -tot[w], w))[:20][::-1]
    ax.barh(top, [doc[w] for w in top], color=color)
    for i, w in enumerate(top): ax.text(doc[w] + 0.5, i, f'{doc[w]} ({tot[w]})', va='center', fontsize=9)
    ax.set_title(f'{name} 상위 20 (기사 수, 괄호=총 횟수)'); ax.set_xlim(0, max(doc[w] for w in top) * 1.18)
    ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout(); plt.savefig('top_words_bar.png', dpi=150); plt.close()
for lang in ('ko', 'en'):
    tot = data[lang][0]
    wc = WordCloud(font_path=FONT, width=1200, height=700, background_color='white', max_words=80,
                   colormap='viridis' if lang == 'ko' else 'plasma', random_state=1).generate_from_frequencies(dict(tot))
    wc.to_file(f'wordcloud_{lang}.png')
