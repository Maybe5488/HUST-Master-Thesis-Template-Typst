# 华中科技大学硕士学位论文（Typst）
:rocket: LaTeX编译太慢,Word使用太麻烦

:rocket: 参考了学校官方的word模板和一些开源的LaTeX和typst项目

:rocket: 全程使用CodeX 6.1Sol-Medium 实现

:warning:无法做到百分百还原官方模板，欢迎PR完善修正！

本项目保留论文编译所需的 Typst 源文件、插图、参考文献和字体，统一输出一份带红色页眉的 PDF。

[查看最终论文 thesis.pdf](thesis.pdf)

## 当前版本

- 输出文件：`thesis.pdf`，重新编译时覆盖更新。
- 页面样式：红色页眉、页眉双线、页脚横线与页码；封面和声明页不显示页眉、页脚。
- 匿名处理：中英文论文题目、作者姓名、学号、导师姓名使用占位符，PDF 作者元数据也使用匿名姓名。
- 项目仅保留这一套编译方式。

当前源稿仍含摘要、关键词和部分章节的占位内容，需继续补充；`thesis.pdf` 是当前源稿的统一导出文件。

## 项目结构

```text
.
├── main.typ                   # 论文入口与正文章节顺序
├── thesis.pdf                 # 唯一的 PDF 输出
├── Makefile                   # 编译与自动重编译
├── README.md
├── template/
│   ├── metadata.typ           # 中英文论文信息、摘要与关键词
│   ├── frontmatter.typ        # 封面、声明与摘要页面
│   └── hust-thesis.typ        # 页眉页脚、标题、目录等排版规则
├── chapters/                  # 正文、结论、致谢与附录
│   ├── chap01.typ … chap04.typ
│   ├── conclusion.typ
│   ├── backmatter.typ         # 致谢、参考文献及附录的组织入口
│   └── …
├── figures/                   # 正文插图与校徽（SVG）
├── references/                # BibTeX 文献库
└── fonts/                     # 随项目提供的中文字体
```

## 编译与预览

需要安装 Typst；当前 PDF 使用 Typst 0.15.1 编译。在项目根目录运行：

```sh
make
```

也可以直接执行：

```sh
typst compile --root . --font-path fonts main.typ thesis.pdf
```

编辑时自动重编译：

```sh
make watch
```

无 Make 的环境可运行：

```sh
typst watch --root . --font-path fonts main.typ thesis.pdf
```

每次编译均更新根目录的 `thesis.pdf`。打开该文件即可查看结果。

`fonts/` 包含 SimSun、SimHei、KaiTi 和 STZhongsong 字体。编译环境还需提供 Times New Roman 和 STKaiti；缺少字体时的回退可能改变字形和断行。可检查当前可用字体：

```sh
typst fonts --font-path fonts
```

## 修改位置

| 内容 | 文件 |
| --- | --- |
| 论文题目、专业、作者、学号、导师、日期与学位类型 | [template/metadata.typ](template/metadata.typ) |
| 中英文摘要与关键词 | [template/metadata.typ](template/metadata.typ) |
| 正文内容 | `chapters/chap01.typ` 至 `chapters/chap04.typ` |
| 正文章节顺序、结论与后置内容入口 | [main.typ](main.typ) |
| 致谢、参考文献和附录的组织顺序 | [chapters/backmatter.typ](chapters/backmatter.typ) |
| 参考文献库的加载列表 | [chapters/references.typ](chapters/references.typ) |
| 封面和声明页 | [template/frontmatter.typ](template/frontmatter.typ) |
| 页眉页脚、目录、标题及正文样式 | [template/hust-thesis.typ](template/hust-thesis.typ) |

新增插图放入 `figures/`，从正文使用 `../figures/文件名.svg` 引用。新增文献写入 `references/` 中已加载的 `.bib` 文件；若新建文献库，还需在 `chapters/references.typ` 中加入对应路径。
