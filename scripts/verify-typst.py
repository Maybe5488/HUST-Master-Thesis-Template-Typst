"""Verify the migrated thesis and optional examples using Typst and Poppler.
Run with python3 scripts/verify-typst.py. No Python packages are required.
"""
from pathlib import Path
import json, re, subprocess, tempfile
ROOT = Path(__file__).resolve().parents[1]
def run(*args):
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    if result.returncode or result.stderr.strip():
        raise RuntimeError(f'{args[0]} failed or emitted diagnostics:\n{result.stderr}\n{result.stdout}')
    return result.stdout
with tempfile.TemporaryDirectory(prefix='hust-typst-check-') as temporary:
    outputs = {}
    for name, source, inputs in [
        ('draft', 'main.typ', []),
        ('final', 'main.typ', ['--input', 'format=final']),
        ('examples', 'typst/examples.typ', []),
    ]:
        pdf = Path(temporary)/(name+'.pdf')
        run('typst','compile','--root','.', '--font-path','font', *inputs, source, str(pdf))
        metadata = run('pdfinfo', str(pdf))
        assert '595.276 x 841.89' in metadata, f'{name}: expected A4'
        pages = int(re.search(r'Pages:\s*(\d+)',metadata)[1])
        text = run('pdftotext','-layout',str(pdf),'-')
        assert '\ufffd' not in text, f'{name}: replacement glyph found'
        assert not re.search(r'\\(?:begin|frac|OPT|Inter|textsc)',text), f'{name}: unconverted TeX'
        compact = re.sub(r'\s+','',text)
        header_count = compact.count('华中科技大学硕士学位论文')
        if name == 'draft':
            assert header_count == pages-3, f'Expected headers on all {pages-3} thesis pages; got {header_count}'
            for title in ['独创性声明','学位论文版权使用授权书','绪论','XX算法研究方法','总结与展望','参考文献','中英文缩写对照表']:
                assert title in compact, f'Missing content: {title}'
            assert 'YAO' in text and 'Probabilistic computations' in text, 'Missing bibliography entry'
            fonts = run('pdffonts',str(pdf))
            for font in ['SimSun','SimHei','STKaiti','STZhongsong','TimesNewRomanPSMT','NewCMMath']:
                assert font in fonts, f'Missing embedded font: {font}'
        if name == 'final':
            assert header_count == 0, 'Final format still has running header'
        outputs[name] = pages
        print(f'{name}: {pages} A4 pages, compilation without diagnostics')
    assert outputs['draft'] == outputs['final'], 'Draft/final pagination differs'
expression = '''(
  equation: counter(math.equation).at(<eq:oddeven>),
  last: counter(math.equation).at(<eq:lowerbound_3>),
  figure: counter(figure.where(kind: image)).at(<fig:Cost_State>),
  lemma: counter(figure.where(kind: "lemma")).at(<state-value>),
  algorithm: counter(figure.where(kind: "algorithm")).at(<alg:randomizedalgo>),
  section: counter(heading).at(<sec:3-optimal>),
)'''
numbers = json.loads(run('typst','eval','--root','.', '--font-path','font','--in','main.typ',expression))
assert numbers == {'equation':[1], 'last':[13], 'figure':[1], 'lemma':[1], 'algorithm':[1], 'section':[3,1]}, numbers
print('Cross-reference counters, embedded fonts, bibliography, and format variants verified.')
