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

bad_days = '''
    select *
        from
        (select error_count_daily.date, (cast(errors as real) / cast(requests as real)) as error_frac
            from
            (select date_trunc('day', time) as date, count(*) as requests
                from log
                group by date) as request_count_daily,
            (select date_trunc('day', time) as date, count(*) as errors
                from log
                where not status = '200 OK'
                group by date) as error_count_daily
            where error_count_daily.date = request_count_daily.date) as error_frac_daily
        where error_frac > 0.01; '''
