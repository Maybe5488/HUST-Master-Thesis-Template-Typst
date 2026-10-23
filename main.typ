#import "template/hust-thesis.typ": *
#import "template/metadata.typ": thesis
#import "template/frontmatter.typ": frontmatter, abstracts

// 统一使用红色页眉与装饰线。
#show: hust-thesis
#set document(author: thesis.author)

#frontmatter(thesis)
#set page(numbering: "I")
#abstracts(thesis)
#hust-outline()

#pagebreak()
#set page(numbering: "1")
#counter(page).update(1)
#include "chapters/chap01.typ"
#include "chapters/chap02.typ"
#include "chapters/chap03.typ"
#include "chapters/chap04.typ"
#include "chapters/conclusion.typ"
#include "chapters/backmatter.typ"
