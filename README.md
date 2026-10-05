# HUST Master Thesis Template · Typst

华中科技大学硕士学位论文的 Typst 模板，由 HUSTThesis LaTeX 模板移植而来。字号、版心、章节与目录等参数参照 LaTeX 模板，页眉配色等外观细节参照仓库内的 Word 模板。

支持中英文封面、声明页、中英文摘要、目录、正文、参考文献和附录。主编译入口为 **[`main.typ`](main.typ)**，普通编译无需 LaTeX、Pandoc 或在线 Typst 包。

[草稿 PDF](main-typst.pdf) · [终稿 PDF](main-typst-final.pdf) · [格式核验记录](FORMAT-AUDIT.md)

## 快速开始

### 1. 获取仓库

```sh
git clone https://github.com/Maybe5488/HUST-Master-Thesis-Template-Typst.git
cd HUST-Master-Thesis-Template-Typst
```

### 2. 准备 Typst 和字体

模板已在 **Typst 0.15.1** 上验证。先确认命令行可用：

```sh
typst --version
```

编译使用仓库 `font/` 中的宋体、黑体、楷体和华文中宋，并需要本机提供 **Times New Roman** 与 **STKaiti（华文楷体）**。数学字体使用 Typst 内置的 New Computer Modern Math。

```sh
# 查看 Typst 当前可识别的字体
typst fonts --font-path font
```

若缺少字体，请先安装对应字体，或在 [`typst/hust-thesis.typ`](typst/hust-thesis.typ) 中调整字体配置。字体回退会影响字形与断行。

### 3. 编译

在仓库根目录执行：

```sh
# 草稿：红色页眉、两条页眉横线及一条页脚横线
make typst

# 终稿：移除页眉和装饰线，保留页码
make typst-final

# 编辑时自动重新编译
make typst-watch
```

输出分别为 `main-typst.pdf` 和 `main-typst-final.pdf`。

没有 Make 的环境也可以直接运行：

```sh
typst compile --root . --font-path font main.typ main-typst.pdf
typst compile --root . --font-path font --input format=final main.typ main-typst-final.pdf
```

请保留 `--root .` 与 `--font-path font`。这些命令直接从本仓库根目录执行，无需再进入同名子目录。

## 填写论文

| 要修改的内容 | 文件 |
| --- | --- |
| 论文题目、姓名、专业、导师、日期、学位类型、中英文摘要与关键词 | [`typst/metadata.typ`](typst/metadata.typ) |
| 正文各章 | [`typst/body/`](typst/body/) 中的 `chap01.typ` 至 `chap04.typ` |
| 总结与展望 | [`typst/body/conclusion.typ`](typst/body/conclusion.typ) |
| 致谢 | [`typst/body/ack.typ`](typst/body/ack.typ) |
| 参考文献数据库与列表 | [`ref/`](ref/) 与 [`typst/body/references.typ`](typst/body/references.typ) |
| 附录的启用顺序 | [`typst/body/backmatter.typ`](typst/body/backmatter.typ) |
| 字体、字号、页边距、目录与编号规则 | [`typst/hust-thesis.typ`](typst/hust-thesis.typ) |
| 中英文封面与声明页 | [`typst/frontmatter.typ`](typst/frontmatter.typ) |

`typst/metadata.typ` 中的 `professional: true` 表示勾选专业型；改为 `false` 则勾选学术型。方框与勾号使用统一的矢量图形绘制。

仓库当前包含占位信息、摘要测试文字和部分仅保留标题的章节，可直接替换为自己的论文内容。可选样式示例位于 [`typst/examples.typ`](typst/examples.typ)，不加入主论文。

## 文件结构

```text
.
├── main.typ                 # 主编译入口
├── Makefile                 # 草稿、终稿及监听编译
├── README.md
├── FORMAT-AUDIT.md          # 格式依据、测量结果与已知差异
├── main-typst.pdf           # 草稿预览
├── main-typst-final.pdf     # 终稿预览
├── font/                   # 模板使用的中文字体
├── ref/                    # BibTeX 文献数据库
├── typst/
│   ├── metadata.typ        # 论文信息、摘要与关键词
│   ├── hust-thesis.typ     # 核心排版规则
│   ├── frontmatter.typ     # 封面、声明与摘要
│   ├── examples.typ        # 可选样式示例
│   ├── body/               # 正文、致谢、文献及附录
│   └── assets/             # 校名字样及原 TikZ 图的矢量文件
└── scripts/
    ├── verify-typst.py     # 编译与格式验证
    ├── fixtures/          # 格式回归样例
    ├── migrate-to-typst.py # 原 LaTeX 的一次性迁移工具
    └── export-tikz.py      # 原 TikZ 图的导出工具
```

仓库根目录还保留用于对照的 Word 模板及其 PDF。原 LaTeX 工程不包含在本独立仓库中；只有可选迁移、图形导出脚本依赖它。

## 排版规则

| 项目 | 设置 |
| --- | --- |
| 页面 | A4；左右页边距 2.8cm；正文区域上缘 4.4cm、下缘 3.4cm |
| 正文 | 中文宋体，英文 Times New Roman；12 TeX pt；基线距离 23.5 TeX pt |
| 段落 | 两端对齐，首行缩进两个汉字 |
| 章及三级节标题 | 黑体；依次为 16、14、13、12 TeX pt |
| 标题字重 | 章、一级节、二级节标题加粗；三级节与附录章标题保持常规黑体 |
| 封面大标题 | 华文中宋，45 TeX pt，5bp 字距 |
| 页眉 | STKaiti，16.5 TeX pt，加粗；汉字间距 0.8em |
| 页眉与装饰线 | 不透明红色 `#FF0000`；线宽 0.4 TeX pt，页眉双线间隙 1 TeX pt |
| 目录 | 展示章与一级节；正文普通章不显示点线和页码；长标题续行对齐标题列 |
| 页码 | 封面与声明无页码；摘要、目录为罗马数字；正文从 1 开始 |
| 图表说明 | 宋体，11 TeX pt；图说明在下，表说明在上 |
| 编号 | 图、表、定理与公式按章重置；公式如 `(3.1)`，算法如 `3-1` |
| 脚注 | 9 TeX pt；圈号，每章重置 |
| 参考文献 | BibTeX 数据库，内置 `gb-7714-2015-numeric` 样式 |

TeX 的 pt 与 Typst 的 pt 不同：本模板通过 `texpt = 72 / 72.27 * 1pt` 换算字号；LaTeX 的 bp 对应 Typst 的 pt。正文区域按原类文件实际生效的参数设置。

中文字体没有独立粗体字形，因此使用对应原 XeCJK `AutoFakeBold=2.25` 的描边；英文使用原生粗体。页眉字体保留 Word 对照采用的 STKaiti，LaTeX 页眉原本使用 KaiTi。

## 写作示例

在 `typst/body/` 中新建章节时，先导入模板：

```typst
#import "../hust-thesis.typ": *

#hust-chapter[新章标题]
#heading(level: 2)[节标题] <sec:new>

正文首行自动缩进。见第 #ref(<sec:new>, supplement: none) 节。

#math.equation(block: true, numbering: hust-equation-number)[
  $E = m c^2$
] <eq:new>

#hust-theorem("lemma", "引理")[这里填写引理。] <lem:new>
#hust-proof[这里填写证明。]

#cite(<yao1977probabilistic>)
```

然后在 `main.typ` 中加入对应的 `#include`。图片与表格使用 `#figure(...)`，可通过标签进行交叉引用；文献列表读取的 `.bib` 文件由 `typst/body/references.typ` 指定。

## 验证与样例

完整验证需要 Python 3、Typst 和 Poppler，无需额外 Python 包：

```sh
python3 scripts/verify-typst.py
```

验证包括草稿、终稿、可选样例与格式回归样例的编译，以及 A4 页面、字体嵌入、参考文献、交叉引用计数和终稿页眉移除。格式回归样例另检查跨页摘要的罗马页码、长目录标题续行对齐和正文基线。

单独预览可选示例：

```sh
typst compile --root . --font-path font typst/examples.typ examples.pdf
```

## 与原模板的差异

本项目重建了原模板的主要格式参数，并进行了 PDF 测量与渲染核验；两个排版引擎之间仍有以下差异：

- 数学字体使用 New Computer Modern Math，与原 LaTeX 的传统 Computer Modern 分体字体不同。
- 中文标点压缩、断行、图形浮动位置、多行公式对齐及部分段落间距可能不同，不能保证逐像素或逐页一致。
- 内置 GB/T 7714 CSL 与原 `HUSTThesis.bst` 并非完全相同。原预览缺失的参考文献列表已由已有数据库恢复。
- 原稿中的缺失引用仍显示 `??`，包括第三章不存在的 `alg:PhaseIdentification`；可选样例也保留原稿缺失图片的引用。

具体参数、修正过程和测量结果见 [`FORMAT-AUDIT.md`](FORMAT-AUDIT.md)。

## 可选迁移工具

普通写作和编译不需要运行以下脚本：

```sh
python3 scripts/migrate-to-typst.py
python3 scripts/export-tikz.py
```

它们要求原 LaTeX 工程位于本仓库的上一级目录，提供 `body/`、`figures/`、`ref/` 等资源。迁移脚本另需 Pandoc；图形导出另需 XeLaTeX 与 Poppler。

**迁移脚本会覆盖生成的章节文件。** 已经开始写作后，请直接编辑 `.typ` 文件。现有矢量 SVG 可直接用于编译，原 TikZ 图无需重复导出。

## 来源与许可说明

Typst 排版规则移植自 HUSTThesis V3.2，保留原贡献者署名和 Perl Artistic License 说明。原贡献者包括 Feng Jiang、Huikan Liu、Xinze Zhang、Lianghao Li 和 Jianqing Lin。

字体、校名字样、Word 模板和原有内容属于各自的资源；上述模板代码的许可说明不表示这些资源统一采用相同许可。Times New Roman 和 STKaiti 由使用者本机提供。
