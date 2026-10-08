import re, json, time, html
from resolve_media import *
res = json.load(open('media_resolved.json', encoding='utf-8'))
for i in ['18','85','168','136']:
    r = res[i]
    try:
        u = r['url'] or decode_gnews(pd.read_csv('ev_news.csv',dtype=str,keep_default_na=False).loc[int(i),'링크'])
        if i == '136': time.sleep(8)
        final, h = get(u)
        pub = re.findall(r'"publisher"\s*:\s*\{[^}]*?"name"\s*:\s*"([^"]+)"', h)
        title = re.search(r'<title[^>]*>([^<]+)', h)
        print(i, u, '| publisher:', pub[:2], '| title:', html.unescape(title.group(1))[-60:] if title else None)
        r['url'] = u
    except Exception as e:
        print(i, 'ERR', e)
json.dump(res, open('media_resolved.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
