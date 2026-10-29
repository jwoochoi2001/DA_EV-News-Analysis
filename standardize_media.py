"""매체 열 표준화: media_map.csv(도메인 또는 링크 → 매체명)를 적용한다.

- 도메인으로 적힌 매체와 표기가 다른 매체(예: Chosunbiz)를 media_map.csv 기준으로 바꾼다.
- 매핑에 없는 도메인은 그대로 두고 media_unmapped.csv에 기록한다. (--resolve: 기사에 접근해 제안값 추가)
- 접근이 막혀 확인하지 못한 도메인(wsj.com 등)은 매핑에 넣지 않고 도메인으로 남긴다.
"""
import re, sys, pandas as pd

d = pd.read_csv('ev_news.csv', dtype=str, keep_default_na=False)
mp = pd.read_csv('media_map.csv', dtype=str, keep_default_na=False)
by_key = {k.lower(): v for k, v in zip(mp['key'], mp['name'])}
DOMAIN = re.compile(r'^[\w.-]+\.(com|net|org|kr|tv|gov|co)$', re.I)

new, changed = [], 0
for link, m in zip(d['링크'], d['매체']):
    name = by_key.get(link.lower()) or by_key.get(m.lower()) or m
    changed += name != m
    new.append(name)
d['매체'] = new
d.to_csv('ev_news.csv', index=False, encoding='utf-8-sig')
print(f'매체명 표준화 {changed}건 적용')

left = d[d['매체'].map(lambda x: bool(DOMAIN.match(x)))][['언어', '제목', '매체', '링크']]
left.to_csv('media_unmapped.csv', index=False, encoding='utf-8-sig')
print(f'도메인 그대로 남은 매체 {len(left)}건 -> media_unmapped.csv:', sorted(left['매체'].unique()))

if '--resolve' in sys.argv and len(left):
    from resolve_media import decode_gnews, site_name
    for _, r in left.iterrows():
        try:
            print(r['매체'], '->', site_name(decode_gnews(r['링크']))[1])
        except Exception as e:
            print(r['매체'], '접근 실패:', str(e)[:60])
    print('위 제안값을 확인한 뒤 media_map.csv에 직접 추가하세요.')
