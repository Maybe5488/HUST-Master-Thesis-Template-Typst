// Multi-line figure/table captions must retain the LaTeX single baseline.
#import "../../typst/hust-thesis.typ": *
#show: hust-thesis
#hust-chapter[图表说明核验]
#figure(rect(width: 5cm, height: 1cm), caption: [图说明基线甲\ 图说明基线乙])
#figure(table(columns: 2, [列甲], [列乙], [内容甲], [内容乙]),
  kind: table, caption: [表说明基线甲\ 表说明基线乙])
