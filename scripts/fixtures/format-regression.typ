// Regression fixture: multi-page abstracts and wrapped TOC/headings.
#import "../../typst/hust-thesis.typ": *
#show: hust-thesis
#set page(numbering: "I")
#counter(page).update(1)
#hust-unnumbered[摘要]
#for i in range(65) {
  [摘要核验段落：检验摘要跨越多页之后目录是否仍使用罗马数字页码。]
  parbreak()
}
#hust-unnumbered[Abstract] <audit:abstract>
English abstract.
#hust-outline()
#pagebreak()
#set page(numbering: "1")
#counter(page).update(1)
#hust-chapter[长章标题格式核验：#("论文结构与排版参数检查" * 5)] <audit:chapter>
#heading(level: 2)[长节标题格式核验：#("多行标题应该保持相应字号和基线距离" * 4)] <audit:section>
行距核验甲。\
行距核验乙。\
行距核验丙。
#hust-appendices()
#hust-chapter[长附录标题核验：#("科研成果与学位论文之间的对应关系" * 4)]
内容。
