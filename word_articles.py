"""특정 단어가 나온 한국어 기사 목록. 사용: python word_articles.py [단어 ...]  (기본: 현대자동차 미국 배터리 출시)"""
import sys, pandas as pd
from top_words import ko_nouns

words = sys.argv[1:] or ['현대자동차', '미국', '배터리', '출시']   # 정규화된 단어로 입력 (현대차 -> 현대자동차)
r = pd.read_csv('ev_news_review.csv', dtype=str, keep_default_na=False)
r = r[r['언어'] == 'ko'].copy(); r['n'] = r['정리_제목'].map(ko_nouns)
out = []
for w in words:
    s = r[r['n'].map(lambda x: w in x)].sort_values('발행일', ascending=False)
    print(f'## {w} ({len(s)}건)')
    for _, x in s.iterrows(): print(f'- {x["원본_제목"]} | {x["매체"]} | {x["발행일"][:16]}')
    out.append(s.assign(단어=w)[['단어', '원본_제목', '매체', '발행일', '링크']])
pd.concat(out).to_csv('word_articles.csv', index=False, encoding='utf-8-sig')
