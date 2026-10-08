import re, json, sys, html, urllib.request, urllib.parse, pandas as pd
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124 Safari/537.36"}
def get(url, data=None, headers=None, timeout=20):
    h = dict(UA); h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    r = urllib.request.urlopen(req, timeout=timeout)
    return r.geturl(), r.read().decode('utf-8', 'replace')
def decode_gnews(link):
    gid = link.split('/articles/')[1].split('?')[0]
    _, page = get(f'https://news.google.com/rss/articles/{gid}?hl=en-US&gl=US&ceid=US:en')
    sig = re.search(r'data-n-a-sg="([^"]+)"', page).group(1)
    ts = re.search(r'data-n-a-ts="([^"]+)"', page).group(1)
    inner = ["garturlreq", [["X","X",["X","X"],None,None,1,1,"US:en",None,1,None,None,None,None,None,0,1],"X","X",1,[1,1,1],1,1,None,0,0,None,0],gid,int(ts),sig]
    body = "f.req=" + urllib.parse.quote(json.dumps([[["Fbv4je", json.dumps(inner), None, "generic"]]]))
    _, txt = get('https://news.google.com/_/DotsSplashUi/data/batchexecute', body.encode(),
                 {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"})
    return json.loads(json.loads(txt.split('\n\n')[1])[0][2])[1]
def site_name(url):
    final, h = get(url)
    for pat in [r'<meta[^>]+property=["\']og:site_name["\'][^>]+content=["\']([^"\']+)', r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:site_name["\']',
                r'<meta[^>]+name=["\']application-name["\'][^>]+content=["\']([^"\']+)']:
        m = re.search(pat, h, re.I)
        if m: return final, html.unescape(m.group(1)).strip()
    return final, None
if __name__ == '__main__':
    d = pd.read_csv('ev_news.csv', dtype=str, keep_default_na=False)
    dom = d[d['매체'].str.match(r'^[\w.-]+\.(com|net|org|kr|tv|gov|co)$', case=False)]
    res = {}
    for i, r in dom.iterrows():
        try:
            u = decode_gnews(r['링크']); final, name = site_name(u)
            res[i] = dict(domain=r['매체'], url=u, name=name)
        except Exception as e:
            res[i] = dict(domain=r['매체'], url=None, name=None, err=str(e)[:80])
        print(i, res[i], flush=True)
    json.dump(res, open('media_resolved.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
