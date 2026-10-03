"""One-time source migration. Edit typst/body/*.typ after migration.
Requires Pandoc. Does not overwrite the original LaTeX sources.
"""
from pathlib import Path
import re, subprocess
ROOT=Path(__file__).resolve().parents[1]
SOURCE_ROOT=ROOT.parent
DEST=ROOT/'typst/body'
TOKENS={}
WARNINGS=[]
def token(content, block=True):
    key=f'HUSTPLACEHOLDER{len(TOKENS):05d}'
    TOKENS[key]=content
    return '\n\n'+key+'\n\n' if block else key
def strip_comments(s):
    return re.sub(r'(?<!\\)%[^\n]*','',s)
def group(s,start):
    assert s[start]=='{'
    depth=1; i=start+1
    while depth:
        if s[i]=='{' and s[i-1]!='\\': depth+=1
        if s[i]=='}' and s[i-1]!='\\': depth-=1
        i+=1
    return s[start+1:i-1],i
def command_arg(s,name):
    m=re.search(r'\\'+name+r'\s*\{',s)
    return group(s,m.end()-1)[0] if m else ''
def pandoc(s):
    p=subprocess.run(['pandoc','-f','latex','-t','typst','--wrap=none'],input=s,text=True,capture_output=True,cwd=SOURCE_ROOT)
    if p.returncode or p.stderr:
        WARNINGS.append(p.stderr)
        if p.returncode: raise RuntimeError(p.stderr)
    out=p.stdout.strip().replace('\u200b','')
    # Pandoc reference token boundaries need explicit calls before adjacent Chinese.
    out=re.sub(r'@([A-Za-z0-9_:.-]+)',r'#ref(<\1>, supplement: none)',out)
    for key,val in TOKENS.items(): out=out.replace(key,val)
    return out
MACROS={'ralgo':'RDSA','TOPI':'TOPI','OPTE':r'$\mathrm{Match}_{even}$','OPTO':r'$\mathrm{Match}_{odd}$','Inter':r'\mathtt{Internal}','Exter':r'\mathtt{External}','OPT':r'\mathrm{OPT}','ALG':r'\mathrm{ALG}','tlr':r'\tilde{R}','Nat':r'\mathbb{N}','Real':r'\mathbb{R}','ve':r'\varepsilon','ep':r'\epsilon'}
def prepare(s):
    s=strip_comments(s)
    for k,v in MACROS.items(): s=re.sub(r'\\'+k+r'\b',lambda _:v,s)
    s=re.sub(r'\\renewcommand\{\\labelenumi\}\{.*?\}\}', '',s)
    s=re.sub(r'\\(song|xiaosi)\b(?:\[[^]]*\])?','',s)
    return s
SUBREFS={'fig:costfunction':'3.1a','fig:statefunction':'3.1b','fig:opt_1':'3.3a','fig:opt_2':'3.3b','fig:alg-1':'3.4a','fig:alg-2':'3.4b','fig:alg-3':'3.4c','fig:alg-4':'3.4d','enu:casea':'1','enu:caseb':'2','enu:decisiona':'a','enu:decisionb':'b'}
def convert(s):
    while (match:=re.search(r'\\textcolor\{(red|blue)\}\s*\{',s)):
        body,end=group(s,match.end()-1)
        s=s[:match.start()]+token('#text(fill: '+match[1]+')['+convert(body).strip()+']', block=False)+s[end:]
    # Preserve references missing from the original source as visible ?? markers.
    s=s.replace(r'\ref{alg:PhaseIdentification}',r'\textbf{??}').replace(r'\ref{Fig2-1}',r'\textbf{??}')
    for key,val in SUBREFS.items():
        if key.startswith('fig:'):
            parent={'3.1':'fig:Cost_State','3.3':'fig:lowerbound-opt','3.4':'fig:lowerbound-alg'}[val[:-1]]
            value=token('#hust-subref(<'+parent+'>, "'+val[-1]+'")', block=False)
        else: value=val
        s=s.replace('\\ref{'+key+'}',value)
    # Citations remain linked to the existing BibTeX database.
    s=re.sub(r'\\lcite\{([^}]+)\}', lambda m:token('#hust-inlinecite(<'+m[1]+'>)', block=False),s)
    s=re.sub(r'\\cite\{([^}]+)\}',lambda m:token(''.join('#cite(<'+k.strip()+'>)' for k in m[1].split(',')), block=False),s)
    # Environment replacement is recursive, so theorem bodies retain all their math.
    envs=r'table|enumerate|figure|algorithm|lemma|theorem|corollary|definition|proposition|proof|equation\*?|align\*?'
    pattern=re.compile(r'\\begin\{('+envs+r')\}(?:\[[^]]*\])?')
    while (m:=pattern.search(s)):
        env=m[1]; end='\\end{'+env+'}'; j=s.index(end,m.end())
        body=s[m.end():j]; label=command_arg(body,'label')
        if env=='table':
            replacement=convert_table(body)
        elif env=='enumerate':
            body=re.sub(r'\\renewcommand\{\\labelenumi\}\{[^\n]*\}', '', body)
            items=re.split(r'\\item\b',body)[1:]
            items=[re.sub(r'\\label\{enu:[^}]+\}', '', i).strip() for i in items]
            items=[i[1:-1] if i.startswith('{') and i.endswith('}') else i for i in items]
            scheme='(a)' if 'enu:decisiona' in body else '(1)'
            replacement='#enum(numbering: '+repr(scheme).replace("'",'"')+',\n'+',\n'.join('['+convert(i)+']' for i in items)+'\n)'
        elif env=='figure': replacement=figure(body)
        elif env=='algorithm': replacement=algorithm(body)
        elif env.startswith(('equation','align')):
            replacement=equation(body,env)
        else:
            body=re.sub(r'^\s*\\label\{[^}]+\}','',body, count=1)
            inner=convert(body).strip()
            if env=='proof': replacement='#hust-proof[\n'+inner+'\n]'
            else:
                titles={'lemma':'引理','theorem':'定理','corollary':'推论','definition':'定义','proposition':'命题'}
                replacement=f'#hust-theorem("{env}", "{titles[env]}")[\n{inner}\n]'+ (' <'+label+'>' if label else '')
        s=s[:m.start()]+token(replacement)+s[j+len(end):]
    # Display math is unnumbered; inline math is handled by Pandoc.
    s=re.sub(r'\$\$(.*?)\$\$',lambda m:token(equation(m[1],'equation*')),s,flags=re.S)
    def heading(m):
        name=m[1]; title,i=group(s,m.end()-1)
        return title,i
    pat=re.compile(r'\\(chapter|section|subsection|subsubsection)\s*\{')
    while (m:=pat.search(s)):
        title,i=heading(m)
        converted=pandoc(title)
        if m[1]=='chapter': repl='#hust-chapter['+converted+']'
        else: repl='#heading(level: '+str({'section':2,'subsection':3,'subsubsection':4}[m[1]])+')['+converted+']'
        # Attach an immediately following label to its heading, not a paragraph.
        after=re.match(r'\s*\\label\{([^}]+)\}',s[i:])
        if after: repl+=' <'+after[1]+'>'; i+=after.end()
        s=s[:m.start()]+token(repl)+s[i:]
    out=pandoc(s)
    # The source's enumerate lists use (1), except the explicitly lettered case list.
    out=out.replace('+  <enu:decisiona>','+  <enu:decisiona>').replace('~◻','')
    return out+'\n'
def math(s):
    s=re.sub(r'\\label\{[^}]+\}|\\nonumber','',s)
    out=pandoc('$$'+(r'\begin{aligned}'+s.strip()+r'\end{aligned}' if '&' in s or r'\\' in s else s.strip())+'$$')
    if not(out.startswith('$') and out.endswith('$')): raise RuntimeError('Unconverted math: '+s)
    return out[1:-1].strip()
def equation(body,env):
    if '若' in body and r'\left\{' in body:
        return '#math.equation(block: true, numbering: none)[$s(t) = cases(frac(o d d(t) - e v e n(t) + 1, 2) & "若" d "为奇", frac(e v e n(t) - o d d(t) + 1, 2) & "若" d "为偶")$]'
    if env.startswith('align') and not env.endswith('*'):
        rows=re.split(r'\\\\\s*',body.strip())
        results=[]
        for row in rows:
            if not row.strip(): continue
            label=command_arg(row,'label')
            numbered=r'\nonumber' not in row
            results.append('#math.equation(block: true, numbering: '+('hust-equation-number' if numbered else 'none')+')['+'$'+math(row)+'$]'+(' <'+label+'>' if label else ''))
        return '\n'.join(results)
    label=command_arg(body,'label')
    return '#math.equation(block: true, numbering: '+('none' if env.endswith('*') else 'hust-equation-number')+')['+'$'+math(body)+'$]'+(' <'+label+'>' if label else '')
def figure(body):
    labels=re.findall(r'\\label\{([^}]+)\}',body); label=labels[-1] if labels else ''; cap=pandoc(command_arg(body,'caption'))
    if 'fig2subat' in body:
        content='''#grid(columns: (1fr,), row-gutter: 8pt,
  subfigure("../assets/fig2subat.svg", [(a) 成本函数 $o d d(t)$ 和 $e v e n(t)$], width: 255.64pt),
  subfigure("../assets/fig2subbt.svg", [(b) 状态函数 $s(t)$], width: 278.35pt),
)'''
    elif 'phase_partition' in body: content='#image("../assets/phase_partition.svg", width: 383.96pt)'
    elif 'lowerbound_opt' in body:
        label='fig:lowerbound-opt'
        content='#grid(columns: (1fr, 1fr), column-gutter: 4pt, '+', '.join('subfigure("../assets/lowerbound_opt-'+str(i)+'.svg", [('+c+') $O P T$情况'+str(i)+'], width: 210.76pt)' for i,c in enumerate('ab',1))+')'
    elif 'lowerbound_alg' in body:
        label='fig:lowerbound-alg'
        content='#grid(columns: (1fr, 1fr), gutter: 8pt, '+', '.join('subfigure("../assets/lowerbound_alg-'+str(i)+'.svg", [('+c+') $A L G$在$t$处于'+('等待时情况'+str(i) if i<4 else '空闲状态')+'], width: 210.76pt)' for i,c in enumerate('abcd',1))+')'
    else: raise RuntimeError('Unknown figure: '+body)
    return '#figure(\n[\n'+content+'\n], caption: ['+cap+'], supplement: [图])'+(' <'+label+'>' if label else '')
def convert_table(body):
    label=command_arg(body,'label'); cap=pandoc(command_arg(body,'caption'))
    match=re.search(r'\\begin\{tabular\}\{([^}]+)\}(.*?)\\end\{tabular\}',body,re.S)
    if not match: raise RuntimeError('Unsupported table')
    rows=re.split(r'\\\\',match[2]);cells=[]
    for row in rows:
        row=re.sub(r'\\(?:toprule|midrule|bottomrule|hline)\b','',row).strip()
        if row: cells.extend('['+pandoc(c.strip())+']' for c in row.split('&'))
    return '#figure(table(columns: 5, stroke: none, align: center, table.hline(stroke: 0.8pt),\n'+', '.join(cells[:5])+', table.hline(stroke: 0.4pt),\n'+', '.join(cells[5:])+', table.hline(stroke: 0.8pt)), kind: table, caption: ['+cap+'], supplement: [表])'+(' <'+label+'>' if label else '')
def algorithm(body):
    return r'''#hust-algorithm(caption: [状态化随机延迟算法 RDSA])[
#strong[输入：] 在线输入请求对 \
#strong[输出：] 匹配解 $M$ \
#algo-line(1)[初始化 $S_1 arrow.l 1.$]
#algo-line(2)[*while* 算法空闲时，在时刻 $t(p_i)$ 接收请求对 $p_i$ *do*]
#algo-line(3, indent: 1)[$S_i arrow.l min{1-S_(i-1)+l_(i-1), 1}$]
#algo-line(4, indent: 1)[采样 $X_i tilde.op bold(U)(0, S_i)$]
#algo-line(5, indent: 1)[*if* 在时间段 $(t(p_i), t(p_i)+X_i]$ 接收请求对 $p_(i+1)$ *then*]
#algo-line(6, indent: 2)[$S_(i+1) arrow.l min{1-S_i+l_i, 1}$]
#algo-line(7, indent: 2)[$M$ add $mono("External")(p_i,p_(i+1))$ at time $t(p_(i+1))$]
#algo-line(8, indent: 1)[*else*]
#algo-line(9, indent: 2)[$M$ add $mono("Internal")(p_i)$ at time $t(p_i)+X$]
#algo-line(10)[*return* $M$.]
] <alg:randomizedalgo>'''
if __name__=='__main__':
    DEST.mkdir(parents=True,exist_ok=True)
    for name in ['chap01','chap02','chap03','chap04','conclusion','chap07','other']:
        out=convert(prepare((SOURCE_ROOT/('body/'+name+'.tex')).read_text()))
        (DEST/(name+'.typ')).write_text('#import "../hust-thesis.typ": *\n\n'+out)
    (ROOT/'typst/migration-warnings.txt').write_text('\n'.join(WARNINGS))
    if any(WARNINGS): raise RuntimeError('Pandoc emitted warnings; inspect migration-warnings.txt')
    (ROOT/'typst/refs-examples.bib').write_text('@string{IEEE_J_MTT = {IEEE Transactions on Microwave Theory and Techniques}}\n\n'+(SOURCE_ROOT/'ref/refs.bib').read_text())
    print('Converted active chapters and optional examples; no Pandoc warnings.')
