import re, html, pandas as pd
d = pd.read_csv('ev_news_raw.csv', dtype=str, keep_default_na=False)
n0 = len(d)
orig = d['제목'].copy()
def clean(s):
    s = html.unescape(html.unescape(s))
    s = re.sub(r'<[^>]+>', ' ', s)
    s = s.replace('\xa0', ' ').replace('​', '')
    return re.sub(r'\s+', ' ', s).strip()
d['제목'] = d['제목'].map(clean)
d['매체'] = d['매체'].map(clean)
changed = (d['제목'] != orig).sum()
print('HTML/공백 정리로 바뀐 제목:', changed)
for o, n in zip(orig[d['제목'] != orig], d['제목'][d['제목'] != orig]): print('  ', repr(o), '->', repr(n))

# 매체명 접미사 제거
stripped = nomatch = 0; notail = []; odd = []
out = []
for _, r in d.iterrows():
    t, m = r['제목'], r['매체']
    suf = ' - ' + m
    if m and t.endswith(suf) and len(t) > len(suf):
        t = t[:-len(suf)].rstrip(); stripped += 1
    else:
        # 접미사가 있는데 매체 열과 다른 경우
        mm = re.search(r' - ([^-]+)$', t)
        if mm: odd.append((r['언어'], r['제목'], m))
        else: notail.append((r['언어'], r['제목'], m))
    out.append(t)
d['제목_원본'] = d['제목']; d['제목'] = out
print('매체명 제거:', stripped, '/ 접미사 없음:', len(notail), '/ 접미사 있으나 매체 열과 불일치:', len(odd))
for x in odd: print('  불일치', x)
for x in notail[:10]: print('  접미사없음', x)

# 중복 (제목+매체)
key = d['제목_원본'].str.casefold() + '|' + d['매체'].str.casefold()
dup = d[key.duplicated(keep=False)].sort_values('제목_원본')
print('중복 행(첫 건 포함):', len(dup))
print(dup[['언어','제목','매체','발행일']].to_string())
d = d[~key.duplicated(keep='first')]
# 제목만 같고 매체가 다른 경우
t2 = d[d['제목'].str.casefold().duplicated(keep=False)]
print('제목만 같고 매체 다름:', len(t2)); print(t2[['언어','제목','매체']].to_string())
# 링크 중복
print('링크 중복:', d['링크'].duplicated().sum())
d.drop(columns='제목_원본')[['언어','제목','발행일','매체','링크','수집시각']].to_csv('ev_news.csv', index=False, encoding='utf-8-sig')
print(n0, '->', len(d)); print(d['언어'].value_counts())
