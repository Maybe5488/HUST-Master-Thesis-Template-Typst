# 华中科技大学硕士论文 Typst 版

这是当前 LaTeX 工程的可编辑 Typst 移植。原有 `.tex`、`.cls`、`.sty`、`.bib`、字体和 `main.pdf` 均保留。Typst 相关文件集中在 `typst-template/`，入口为此目录下的 `main.typ`，已在 Typst 0.15.1 上编译验证。字体与参考文献各保留一份副本，因此可以单独复制此文件夹进行编译。

## 编译与编辑

在 `typst-template` 目录运行（从原工程目录先执行 `cd typst-template`）：

```sh
# 对应原 main.tex 的 draftformat
make typst
# 输出 main-typst.pdf

# 对应 finalformat：移除页眉和装饰线，保留页码
make typst-final
# 输出 main-typst-final.pdf

# 编辑时自动重编译
make typst-watch
```

不使用 Make 时：

```sh
typst compile --root . --font-path font main.typ main-typst.pdf
typst compile --root . --font-path font --input format=final main.typ main-typst-final.pdf
```

封面信息、日期、中文和英文摘要集中在 `typst/metadata.typ`。正文在 `typst/body/chap01.typ` 至 `chap04.typ`，总结在 `conclusion.typ`；致谢、参考文献和各附录也有独立文件。`typst/hust-thesis.typ` 负责字体与版面，`typst/frontmatter.typ` 负责封面和声明。

正常编译只需要 Typst 和字体，不需要 LaTeX、Pandoc、在线 Typst 包或网络。

## 字体和原版参数

| 项目 | 移植规则 |
| --- | --- |
| 中文正文 | 复用 `font/SimSun.ttf`，12 TeX pt |
| 英文正文 | Times New Roman；使用本机安装的字体，不重新分发 |
| 章、节标题 | 复用 `font/SimHei.ttf`；16、14、13、12 TeX pt |
| 页眉 | 对照 Word 模板：华文楷体（STKaiti），16.5pt，加粗；汉字间空格并增加 1pt 字距 |
| 封面“硕士学位论文” | 复用 `font/STZhongsong.ttf`，45 TeX pt，5bp 字距 |
| 页面 | A4，左右各 2.8cm；正文区域上缘 4.4cm，下缘 3.4cm |
| 正文基线 | 以原类文件实际生效的 23.5 TeX pt 为目标校准 |
| 段落 | 两端对齐，首行缩进两个汉字 |
| 页眉页脚 | 草稿保留双线页眉、单线页脚；终稿仅保留页码 |
| 页码 | 封面和声明无页码；摘要和目录罗马数字；正文从 1 开始 |
| 编号 | 章节 1.1；图、表、定理按章重置；公式 (3.1)；算法 3-1；附录 1–5 |

TeX 的 pt 是 1/72.27 英寸，Typst 的 pt 是 1/72 英寸，因此字号通过 `texpt` 换算。原类文件说明文字中有“上 4.5cm、下 2.8cm”的表述，但实际代码的 `topmargin + headheight + headsep` 为 4.4cm，正文高度为 21.9cm；本版按实际代码移植。

原中文字体没有独立粗体文件。原 XeCJK 使用 `AutoFakeBold=2.25`；Typst 对应的中文粗体按字号施加同等强度的描边（描边宽度为 TeX 字号的 2.25%），覆盖封面、章/节标题、目录章标题、页眉、关键词、定理标签和正文 `#strong[...]`。英文使用 Times New Roman 的原生粗体，不额外描边。三级节标题和附录章标题按原类文件保持常规黑体。两个引擎的字形栅格化仍可能有细微差异。

页眉文字与双线均使用 Word 模板文件中保存的不透明红色 `#FF0000`；各线 1pt、间隙 1pt。

请保留 `--font-path font`，并安装 Times New Roman 和华文楷体（STKaiti）。Typst 找不到字体时会警告并回退；字体回退会改变断行。

## 图形、公式与引用

原 TikZ 图导出为矢量 SVG，存于 `typst/assets/`，保留原图形、颜色和图中文字；相应矢量 PDF 也保留。正文中的图注和编号为原生 Typst，可编辑、可引用。图形本身需要修改时，编辑上一级 LaTeX 工程中的 `../figures/*.tex` 后，在本目录运行：

```sh
python3 scripts/export-tikz.py
```

该可选导出步骤需要 XeLaTeX 和 Poppler 的 `pdftocairo`。原校名字样从 `hust-logo.eps` 导出。

公式已转换为原生 Typst 数学语法；数学字体使用内置 New Computer Modern Math。LaTeX 原稿采用传统 Computer Modern 分体数学字体，两者并非同一字体文件。多行有编号的 `align` 转为逐行编号的 Typst 方程，因此部分对齐位置和行距会有差异。

正文写作示例：

```typst
#hust-chapter[新章标题]
#heading(level: 2)[节标题] <sec:new>

正文首行会自动缩进。见第 #ref(<sec:new>, supplement: none) 节。

#math.equation(block: true, numbering: hust-equation-number)[$E = m c^2$] <eq:new>

#hust-theorem("lemma", "引理")[这里填写引理。] <lem:new>
#hust-proof[这里填写证明。]

#cite(<yao1977probabilistic>)
```

图片和表格使用 `#figure(...)`，自动按章编号。参考文献直接复用原 `.bib`，通过 Typst 内置 `gb-7714-2015-numeric` 样式生成；该 CSL 与原 `HUSTThesis.bst` 并不完全相同，后续增加文献时需对照具体著录要求检查。

## 可选样例与原稿问题

原 `chap07.tex` 的样式说明、三线表和参考文献示例也已移植，默认不加入主论文。样例使用 `typst/refs-examples.bib`，其内容来自原 `ref/refs.bib`，补充了原文件缺失的 `IEEE_J_MTT` 缩写定义。单独预览：

```sh
typst compile --root . --font-path font typst/examples.typ /tmp/hust-typst-examples.pdf
```

`denotation.typ` 为主要符号表；`patent.typ` 和 `other.typ` 为可选附录。原 `appendix04.tex` 为空，对应 Typst 文件也保留为空。

原主文档未启用答辩委员会表页，本版同样不自动增加。原类文件中已经停用的 `patent` 环境在可选 Typst 示例中提供了可用替代。`chap07` 原文的 Word 操作说明按原内容保留，并不是 Typst 操作教程。

原第三章引用了不存在的 `alg:PhaseIdentification`；原可选样例引用了已注释的 `Fig2-1`。本版保留可见 `??`，等待作者提供相应算法和图片，不补造学术内容。

现有 LaTeX PDF 没有参考文献页，正文中姚氏原理的引用也未正确生成。本版从已有 `ref/mpmd.bib` 恢复引用与文献列表。这会额外增加一页。

## 相似度与限制

本版复用原中文字体和图形，重建了原版字号、版心、页眉页脚、章节、目录、摘要和附录体系，但**不是逐像素复刻**。字体粗体模拟、数学字体、CJK 标点压缩、断行、浮动图形位置、多行公式对齐和部分段落间距仍有差异；页码也可能随正文编辑变化。章节参数保存在单一模板文件，可继续针对最终论文校准。

`scripts/migrate-to-typst.py` 是一次性迁移工具，需要 Pandoc。它读取上一级 LaTeX 工程的 `body/` 和 `ref/`；`export-tikz.py` 同样依赖上一级工程的 `figures/`。普通 Typst 编译不需要这些上级目录。它只针对本工程的语法，不是通用 LaTeX 转换器。运行会覆盖由其生成的章节 `.typ`；迁移完成后，请直接编辑 Typst 文件，避免用该脚本覆盖后续写作。

原 HUSTThesis 模板的贡献者署名和 Perl Artistic License 说明保留在原文件及 Typst 模板头部。

## 验证

运行 `python3 scripts/verify-typst.py` 可重新检查草稿、终稿与可选样例的编译、A4 页面、字体嵌入、参考文献、交叉引用计数，以及终稿是否去除了页眉。需要 Typst 和 Poppler，无需额外 Python 包。
