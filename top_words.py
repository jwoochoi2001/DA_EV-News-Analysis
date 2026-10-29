import re, pandas as pd
from collections import Counter
from normalize import normalize, _kiwi
try:
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as SW
    SW = set(SW)
except ImportError:
    SW = set("a an the and or but if of in on at to for from by with as is are was were be been being it its this that these those has have had not no than then so such into over about after before more most new will can may how why what who which up out via per also just you your our their his her he she they we i s t".split())
SW |= {'s', 't', 'says', 'say'}
d = pd.read_csv('ev_news_norm.csv', dtype=str, keep_default_na=False)
def ko_nouns(t):
    return [x.form for x in _kiwi.tokenize(normalize(t, 'ko')) if x.tag in ('NNG', 'NNP') and len(x.form) > 1]
def en_words(t):
    return [w for w in re.findall(r"[a-z][a-z_'’-]*[a-z]|[a-z]", normalize(t.lower(), 'en')) if w not in SW]
def main():
    for lang, f in (('ko', ko_nouns), ('en', en_words)):
        tot, doc = Counter(), Counter()
        for t in d[d['언어'] == lang]['제목']:
            ws = f(t); tot.update(ws); doc.update(set(ws))
        rows = sorted(doc, key=lambda w: (-doc[w], -tot[w], w))[:20]
        print(lang)
        for i, w in enumerate(rows, 1): print(f'{i:>2} {w:<20}{doc[w]:>4}{tot[w]:>5}')


if __name__ == '__main__':
    main()
