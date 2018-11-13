#!/usr/bin/env python3

top_articles = '''
    select title, count(*) as num
        from articles, log
        where path like '%' || slug
        group by articles.id
        order by num desc
        limit 3; '''

top_authors = '''
    select authors.name, count(*) as num
        from articles, log, authors
        where path like '%' || slug
            and author = authors.id
        group by authors.name
        order by num desc; '''
