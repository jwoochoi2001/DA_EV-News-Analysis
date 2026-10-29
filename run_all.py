"""전체 파이프라인을 순서대로 실행한다.

  python run_all.py             저장소에 들어 있는 수집 원본(ev_news_raw.csv)부터 전 과정을 다시 실행
  python run_all.py --collect   Google 뉴스에서 새로 수집한 뒤 전 과정을 실행 (결과 숫자가 README와 달라진다)
"""
import os, subprocess, sys, time

STEPS = [
    ('collect_news.py', '수집 (--collect일 때만)'),
    ('clean_news.py', '정제: 중복·HTML·공백·매체명 접미사'),
    ('standardize_media.py', '매체명 표준화'),
    ('build_outputs.py', '동의어 정규화, 검수 파일'),
    ('top_words.py', '단어 빈도 집계'),
    ('charts.py', '막대그래프, 워드클라우드'),
    ('word_articles.py', '단어별 기사 목록'),
    ('embed.py', '문장 임베딩 (처음 실행 시 모델 약 470MB 다운로드)'),
    ('pca_plot.py', 'PCA'),
    ('umap_compare.py', 'PCA vs UMAP'),
    ('static_plots.py', 'README용 정적 그림'),
]
env = dict(os.environ, PYTHONIOENCODING='utf-8')
here = os.path.dirname(os.path.abspath(__file__))
for script, desc in STEPS:
    if script == 'collect_news.py' and '--collect' not in sys.argv:
        continue
    print(f'\n===== {script}: {desc}', flush=True)
    t = time.time()
    if subprocess.run([sys.executable, script], cwd=here, env=env).returncode:
        sys.exit(f'실패: {script}')
    print(f'----- {time.time() - t:.1f}초', flush=True)
print('\n완료')
