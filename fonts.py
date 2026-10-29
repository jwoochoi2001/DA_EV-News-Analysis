"""운영체제에 설치된 한글 폰트를 찾아 matplotlib/wordcloud에 쓴다."""
import matplotlib
from matplotlib import font_manager

CANDIDATES = ['Malgun Gothic', 'AppleGothic', 'NanumGothic', 'Noto Sans CJK KR', 'Noto Sans KR', 'UnDotum']

def korean_font():
    """(폰트 이름, 파일 경로). 없으면 (None, None)."""
    names = {f.name: f.fname for f in font_manager.fontManager.ttflist}
    for c in CANDIDATES:
        if c in names:
            return c, names[c]
    return None, None

def setup_matplotlib():
    name, path = korean_font()
    if name:
        matplotlib.rcParams['font.family'] = name
    else:
        print('경고: 한글 폰트를 찾지 못했습니다. 그래프의 한글이 깨질 수 있습니다. (README의 설치 안내 참고)')
    matplotlib.rcParams['axes.unicode_minus'] = False
    return path
