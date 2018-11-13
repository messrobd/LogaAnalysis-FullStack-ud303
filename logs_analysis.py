#!/usr/bin/env python3

top_articles = '''
  select title, count(*) as num
    from articles, log
    where position(slug in path) > 0
    group by articles.id
    order by num desc
    limit 3 '''
