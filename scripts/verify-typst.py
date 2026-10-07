"""Verify the migrated thesis and optional examples using Typst and Poppler.
Run with python3 scripts/verify-typst.py. No Python packages are required.
"""
from pathlib import Path
import json, re, subprocess, tempfile
import xml.etree.ElementTree as ET
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
        ('format-regression', 'scripts/fixtures/format-regression.typ', []),
        ('caption-regression', 'scripts/fixtures/caption-regression.typ', []),
        ('heading-spacing', 'scripts/fixtures/heading-spacing.typ', []),
        ('heading-consecutive', 'scripts/fixtures/heading-consecutive.typ', []),
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
        if name == 'format-regression':
            assert re.search(r'Abstract\.+IV', compact), 'Multi-page abstract must use Roman IV in TOC'
            xml = ET.fromstring(run('pdftotext', '-bbox-layout', str(pdf), '-'))
            ns = {'x': 'http://www.w3.org/1999/xhtml'}
            rendered_pages = xml.findall('.//x:page', ns)
            toc_lines = rendered_pages[4].findall('.//x:line', ns)
            # Continuation lines must start at LaTeX's title columns.
            start = next(i for i, line in enumerate(toc_lines) if '长章标题格式核验' in ''.join(line.itertext()))
            continuation = toc_lines[start+1:start+3]
            expected = 2.8 / 2.54 * 72 + 2.1 * 14 * 72 / 72.27
            assert len(continuation) == 2
            assert all(abs(float(line.attrib['xMin']) - expected) < 0.05 for line in continuation), 'Wrapped chapter TOC alignment'
            start = next(i for i, line in enumerate(toc_lines) if '长节标题格式核验' in ''.join(line.itertext()))
            continuation = toc_lines[start+1:start+3]
            expected = 2.8 / 2.54 * 72 + 3.24 * 14 * 72 / 72.27
            assert len(continuation) == 2
            assert all(abs(float(line.attrib['xMin']) - expected) < 0.05 for line in continuation), 'Wrapped section TOC alignment'
            body_lines = [line for line in rendered_pages[5].findall('.//x:line', ns)
                          if ''.join(line.itertext()).strip().startswith('行距核验')]
            assert len(body_lines) == 3
            ys = [float(line.attrib['yMin']) for line in body_lines]
            assert all(abs((ys[i+1] - ys[i]) - 23.5 * 72 / 72.27) < 0.01 for i in range(2)), 'Body baseline must match LaTeX 23.5 TeX pt'
        if name == 'caption-regression':
            xml = ET.fromstring(run('pdftotext', '-bbox-layout', str(pdf), '-'))
            ns = {'x': 'http://www.w3.org/1999/xhtml'}
            words = xml.findall('.//x:word', ns)
            for prefix in ['图说明基线', '表说明基线']:
                ys = [float(word.attrib['yMin']) for word in words if (word.text or '').startswith(prefix)]
                assert len(ys) == 2, f'Missing caption fixture: {prefix}'
                assert abs(ys[1] - ys[0] - 11 * 72 / 72.27) < 0.01, f'{prefix}: single caption baseline'
        if name in ('heading-spacing', 'heading-consecutive'):
            xml = ET.fromstring(run('pdftotext', '-bbox-layout', str(pdf), '-'))
            ns = {'x': 'http://www.w3.org/1999/xhtml'}
            rendered_pages = xml.findall('.//x:page', ns)
            expected = ([[142.471, 184.307, 213.517, 245.640, 271.213, 299.480, 333.412, 362.825],
                         [142.471, 183.307], [150.971, 197.807]] if name == 'heading-spacing'
                        else [[142.471, 180.105, 207.388, 230.176, 259.588]])
            for page, reference in zip(rendered_pages, expected):
                ys = [float(line.attrib['yMin']) for line in page.findall('.//x:line', ns)
                      if 120 < float(line.attrib['yMin']) < 760]
                # Poppler can emit the Latin number and Chinese title as
                # separate lines despite sharing a visual baseline.
                merged = []
                for y in sorted(ys):
                    if not merged or y - merged[-1] > 3.5:
                        merged.append(y)
                ys = merged
                assert len(ys) == len(reference), (name, ys)
                assert all(abs(actual - target) < 0.02 for actual, target in zip(ys, reference)), (name, ys)
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
