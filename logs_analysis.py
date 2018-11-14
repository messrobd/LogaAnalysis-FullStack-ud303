#!/usr/bin/env python3
import psycopg2

DBName = 'news'

def get_data(query):
    connection = psycopg2.connect(dbname=DBName)
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data

def top_articles():
    query = '''
        select title, count(*) as num
            from articles, log
            where path like '%' || slug
            group by articles.id
            order by num desc
            limit 3; '''
    for line in get_data(query):
        yield line

def top_authors():
    query = '''
        select authors.name, count(*) as num
            from articles, log, authors
            where path like '%' || slug
                and author = authors.id
            group by authors.name
            order by num desc; '''
    for line in get_data(query):
        yield line

def bad_days(tolerance):
    query = '''
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
            where error_frac > %s; '''
    for (timestamptz, error_frac) in get_data(query % tolerance):
        date = timestamptz.strftime('%B %d, %Y')
        error_percent = str(round(error_frac * 100, 2)) + '%'
        yield (date, error_percent)

def print_to_console(report, report_args):
    print(report.__name__)
    report_line = '%s - %s'
    for (col1, col2) in report(*report_args):
        print(report_line % (col1, col2))

if __name__ == '__main__':
    #main()
    print_to_console(bad_days, [0.01])
