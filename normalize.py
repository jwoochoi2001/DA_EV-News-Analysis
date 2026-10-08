import re, pandas as pd
from kiwipiepy import Kiwi
SYN = pd.read_csv('synonyms.csv', dtype=str, keep_default_na=False)
RULES = {}
for lang in ('ko', 'en'):
    s = SYN[SYN['lang'] == lang].copy()
    s['n'] = s['variant'].str.len()
    s = s.sort_values('n', ascending=False)          # 긴 표현부터 치환
    RULES[lang] = [(re.compile(r'(?<![A-Za-z0-9])' + re.escape(v) + r'(?![A-Za-z0-9])', re.I) if lang == 'en'
                    else re.compile(re.escape(v)), c) for v, c in zip(s['variant'], s['canonical'])]
_kiwi = Kiwi(); _kiwi.load_user_dictionary('user_dict.txt')
def normalize(text, lang):
    for pat, canon in RULES[lang]:
        text = pat.sub(canon, text)
    return re.sub(r'\s+', ' ', text).strip()
def tokens(text, lang):
    if lang == 'ko':
        return [t.form for t in _kiwi.tokenize(normalize(text, 'ko')) if t.tag.startswith(('NN', 'SL', 'SN', 'VV', 'VA', 'MAG'))]
    return re.findall(r"[a-z0-9_]+(?:['’.-][a-z0-9_]+)*", normalize(text.lower(), 'en'))
