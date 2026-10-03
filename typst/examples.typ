#import "hust-thesis.typ": *
#show: hust-thesis.with()

// Optional original style examples, not included in the thesis by default.
#include "body/chap07.typ"
#hust-unnumbered[参考文献]
#bibliography("refs-examples.bib", title: none, style: "gb-7714-2015-numeric")
#hust-unnumbered[主要符号对照表]
#table(columns: (2.5cm, 1fr), stroke: none, [MPMD], [带延迟最小代价完美匹配问题])
#hust-appendices()
#include "body/patent.typ"
#include "body/other.typ"
