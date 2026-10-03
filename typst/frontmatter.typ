#import "hust-thesis.typ": *
#let authorization() = {
  set text(weight: "regular", stroke: none)
  set par(first-line-indent: (amount: 2em, all: true), leading: 12 * texpt)
  align(center, text(font: hei, size: 16 * texpt, weight: "bold")[独创性声明])
  v(1cm)
  [本人声明所呈交的学位论文是我个人在导师的指导下进行的研究工作及取得的研究成果。尽我所知，除文中已标明引用的内容外，本论文不包含任何其他人或集体已经发表或撰写过的研究成果。对本文的研究做出贡献的个人和集体，均已在文中以明确方式标明。本人完全意识到本声明的法律结果由本人承担。]
  v(1.5cm)
  align(right)[学位论文作者签名：#h(2cm)\ 日期：#h(1em)年#h(1em)月#h(1em)日#h(1cm)]
  v(1.5cm)
  align(center, text(font: hei, size: 16 * texpt, weight: "bold")[学位论文版权使用授权书])
  v(1cm)
  [本学位论文作者完全了解学校有关保留、使用学位论文的规定，即：学校有权保留并向国家有关部门或机构送交论文的复印件和电子版，允许论文被查阅和借阅。本人授权华中科技大学可以将本学位论文的全部或部分内容编入有关数据库进行检索，可以采用影印、缩印或扫描等复制手段保存和汇编本学位论文。]
  v(8pt)
  [本论文属于#h(1em)保密 □，在#underline[#h(2em)]年解密后适用本授权书。\ #h(7em)不保密 □。]
  [(请在以上方框内打“√”)]
  v(1cm)
  grid(columns: (1fr, 1fr),
    [学位论文作者签名：\ 日期：#h(1em)年#h(1em)月#h(1em)日],
    [指导教师签名：\ 日期：#h(1em)年#h(1em)月#h(1em)日])
}
#let frontmatter(info) = {
  // Covers and authorization have no running header or page number.
  set page(header: none, footer: none, numbering: none)
  set par(first-line-indent: 0pt)
  set text(weight: "bold")
  block(width: 100%, height: 21.5cm)[
    #place(top + left, dy: -0.5cm)[
      #set text(size: 12 * texpt)
      #grid(columns: (1fr, 1fr), column-gutter: 6cm,
        [分 类 号 #underline[#box(width: 5em, align(center)[#info.class-number])]\ 学校代码 #underline[#box(width: 5em, align(center)[#info.school-code])]],
        [学号 #underline[#box(width: 7em)[#h(1em)#info.student-id]]\ 密级 #underline[#box(width: 7em)[#h(1em)#info.secrecy]]])
    ]
    #place(top + center, dy: 3.4cm, image("assets/hust-logo.svg", width: 7.5cm))
    #place(top + center, dy: 5.75cm, text(font: "STZhongsong", size: 45 * texpt, tracking: 5pt)[硕士学位论文])
    #place(top + center, dy: 7.9cm, text(size: 15 * texpt)[( 学术型 #if info.professional { [□] } else { [#box[□#place(center + horizon, text(font: "New Computer Modern Math")[✓])]] } #h(2em) 专业型 #if info.professional { [#box[□#place(center + horizon, text(font: "New Computer Modern Math")[✓])]] } else { [□] } )])
    #place(top + center, dy: 10.5cm)[
      #set text(size: 28 * texpt)
      #set par(leading: 0.42em)
      #align(center, info.title)
    ]
    #place(top + center, dy: 16.3cm)[
      #set text(size: 15 * texpt)
      #grid(columns: (5em, 2em, auto), align: left, row-gutter: 18pt,
        [学位申请人], [：], [#info.author],
        [学 科 专 业], [：], [#info.subject],
        [指 导 教 师], [：], [#info.supervisor #h(1em) #info.supervisor-title],
        [答 辩 日 期], [：], [#info.defense-date])
    ]
  ]
  pagebreak()
  block(width: 100%, height: 21.5cm)[
    #place(top + center, dy: -1.2cm)[
      #set text(size: 15 * texpt)
      #set par(leading: 0.1em)
      #align(center)[A Dissertation Submitted in Partial Fulfillment of the Requirements for #info.english-degree]
    ]
    #place(top + center, dy: 4.8cm, block(width: 100%)[

      #set text(size: 22 * texpt)
      #set par(leading: 0.3em)
      #align(center, info.english-title)
    ])
    #place(top + center, dy: 10.2cm)[
      #set text(size: 15 * texpt)
      #grid(columns: (auto, auto, auto), align: left, column-gutter: 0.5em, row-gutter: 16pt,
        [Candidate], [:], [#info.english-author],
        [Major], [:], [#info.english-subject],
        [Supervisor], [:], [#info.english-supervisor])
    ]
    #place(top + center, dy: 17cm)[
      #set text(size: 14 * texpt)
      #set par(leading: 1em)
      #align(center)[Huazhong University of Science and Technology\ Wuhan 430074, P. R. China\ #info.english-date]
    ]
  ]
  pagebreak()
  authorization()
  pagebreak()
}
#let abstracts(info) = {
  set page(numbering: "I")
  counter(page).update(1)
  hust-unnumbered([摘#h(2em)要])
  info.abstract
  parbreak()
  grid(columns: (4em, 1fr), text(font: hei, weight: "bold")[关键词：], info.keywords)
  hust-unnumbered([Abstract])
  info.english-abstract
  parbreak()
  grid(columns: (5em, 1fr), strong[Keywords:], info.english-keywords)
  pagebreak()
}
