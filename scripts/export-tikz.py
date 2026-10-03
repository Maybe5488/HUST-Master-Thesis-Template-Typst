"""Export the original TikZ drawings once; normal Typst builds need no TeX."""
from pathlib import Path
import re, subprocess, tempfile, shutil
ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT.parent
OUT = ROOT / 'typst/assets'
PREAMBLE = r'''\documentclass[12pt,border=0pt]{standalone}
\usepackage{fontspec,xeCJK,amsmath,amssymb,tikz}
\setmainfont{Times New Roman}
\setCJKmainfont[Path=font/]{SimSun.ttf}
\newcommand{\song}{\CJKfamily{song}}
\setCJKfamilyfont{song}[Path=font/]{SimSun.ttf}
\usetikzlibrary{fadings,patterns,shadows.blur,shapes,arrows,automata,decorations.pathmorphing,decorations.pathreplacing}
\begin{document}
'''
def export(name, tex):
    with tempfile.TemporaryDirectory(prefix='hust-tikz-') as directory:
        source = Path(directory) / (name + '.tex')
        source.write_text(PREAMBLE + tex + '\n\\end{document}\n')
        result = subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error', '-output-directory=' + directory, str(source)], cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stdout[-5000:])
        shutil.copyfile(source.with_suffix('.pdf'), OUT / (name + '.pdf'))
        subprocess.run(['pdftocairo', '-svg', str(OUT / (name + '.pdf')), str(OUT / (name + '.svg'))], check=True)
        print(name)
if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for name in ['fig2subat','fig2subbt','phase_partition']:
        export(name, (SOURCE_ROOT / ('figures/' + name + '.tex')).read_text())
    for group in ['lowerbound_opt','lowerbound_alg']:
        source = (SOURCE_ROOT / ('figures/' + group + '.tex')).read_text()
        for index, picture in enumerate(re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',source,re.S),1):
            export(f'{group}-{index}',picture)
