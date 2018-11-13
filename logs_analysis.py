#!/usr/bin/env python3

top_articles = '''
  select title, count(*) as num
    from articles, log
    where path like '%' || slug
    group by articles.id
    order by num desc
    limit 3 '''
