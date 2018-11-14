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

def print_to_console(report_title, report_decorator, report, report_args):
    print(report_title)
    report_line = '%s - %s %s'
    for (col1, col2) in report(*report_args):
        print(report_line % (col1, col2, report_decorator))

def main():
    bad_day_tolerance = 0.01
    reports = {
      1: ('Top 3 articles', 'views', top_articles, []),
      2: ('Top authors', 'views', top_authors, []),
      3: ('Bad days', 'errors', bad_days, [bad_day_tolerance])
    }
    print('Select a report:')
    for report in reports:
        print('%s - %s' % (report, reports[report][0]))
    valid_report = False
    while valid_report == False:
        choice = input()
        try:
            report = reports[int(choice)]
        except:
            print('Please pick a number 1 - 3')
        else:
            valid_report = True
    (title, decorator, method, method_args) = report
    print_to_console(title, decorator, method, method_args)

if __name__ == '__main__':
    main()
