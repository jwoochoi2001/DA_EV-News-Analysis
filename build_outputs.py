"""정리된 제목(ev_news.csv)에서 정규화·검수용 파일을 만든다.
   -> ev_news_norm.csv (제목_정규화, 토큰), ev_news_review.csv (원본/정리/정규화 제목 비교)"""
import re, pandas as pd
from normalize import normalize, tokens, SYN

d = pd.read_csv('ev_news.csv', dtype=str, keep_default_na=False)
d['제목_정규화'] = [normalize(t, l) for t, l in zip(d['제목'], d['언어'])]
d['토큰'] = [' '.join(tokens(t, l)) for t, l in zip(d['제목'], d['언어'])]
d.to_csv('ev_news_norm.csv', index=False, encoding='utf-8-sig')

raw = pd.read_csv('ev_news_raw.csv', dtype=str, keep_default_na=False)[['링크', '제목']].rename(columns={'제목': '원본_제목'})
m = d.merge(raw, on='링크', how='left')

def rules(t, lang):
    out = []; s = SYN[SYN.lang == lang]
    for v, c in zip(s.variant, s.canonical):
        pat = re.compile(r'(?<![A-Za-z0-9])' + re.escape(v) + r'(?![A-Za-z0-9])', re.I) if lang == 'en' else re.compile(re.escape(v))
        k = len(pat.findall(t))
        if k: out.append(f'{v}→{c.strip()}' + (f'(x{k})' if k > 1 else ''))
    return '; '.join(out)

m['적용_규칙'] = [rules(t, l) for t, l in zip(m['제목'], m['언어'])]
m['매체명_제거'] = (m['원본_제목'] != m['제목']).map({True: 'Y', False: 'N'})
m['동의어_변환'] = (m['제목'] != m['제목_정규화']).map({True: 'Y', False: 'N'})
m[['언어', '원본_제목', '제목', '제목_정규화', '매체명_제거', '동의어_변환', '적용_규칙', '매체', '발행일', '링크']] \
    .rename(columns={'제목': '정리_제목'}).to_csv('ev_news_review.csv', index=False, encoding='utf-8-sig')
print(f'정규화 {len(d)}건, 동의어 변환 {(m["동의어_변환"] == "Y").sum()}건')
