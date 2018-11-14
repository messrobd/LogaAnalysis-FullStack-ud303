#!/usr/bin/env python3
import psycopg2
import sys
import getopt
import os

DBName = 'news'


class Report():
    def __init__(self, title, formatter, query, query_args=None):
        self.title = title
        self.formatter = formatter
        if query_args:
            self.query = query % query_args
        else:
            self.query = query
    def make_report(self):
        for line in get_data(self.query):
            yield line


def get_data(query):
    connection = psycopg2.connect(dbname=DBName)
    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data


def print_report(report, file_out):
    if file_out:
        # write file to cwd:
        report_file = open(report.title.replace(' ', '_') + '.txt', 'w')
        report_file.write(report.title + '\n')
        for line in report.make_report():
            report_file.write(report.formatter(line) + '\n')
        report_file.close()
    else:
        print(report.title)
        for line in report.make_report():
            print(report.formatter(line))


top_arts_query = '''
    select title, count(*) as num
        from articles, log
        where path like '%' || slug
        group by articles.id
        order by num desc
        limit 3; '''


def top_arts_formatter(line):
    line_template = '"%s" - %s views'
    return line_template % line


top_articles = Report('Top 3 articles', top_arts_formatter, top_arts_query)


top_auths_query = '''
    select authors.name, count(*) as num
        from articles, log, authors
        where path like '%' || slug
            and author = authors.id
        group by authors.name
        order by num desc; '''


def top_auths_formatter(line):
    line_template = '%s - %s views'
    return line_template % line


top_authors = Report('Top authors', top_auths_formatter, top_auths_query)


bad_days_query = '''
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


bad_day_tol = 0.01


def bad_days_formatter(line):
    line_template = '%s - %s%% errors'
    (timestamptz, error_frac) = line
    date = timestamptz.strftime('%B %d, %Y')
    error_percent = round(error_frac * 100, 2)
    return line_template % (date, error_percent)


bad_days = Report('Bad days', bad_days_formatter, bad_days_query, bad_day_tol)


reports = {
    1: top_articles,
    2: top_authors,
    3: bad_days
}


def main(options, file_out=False):
    try:
        opts, args = getopt.getopt(options, 'f')
    except getopt.GetoptError:
        print('usage: logs_analysis.py [-f]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-f':
            file_out = True
    print('Select a report:')
    for report in reports:
        print('%s - %s' % (report, reports[report].title))
    valid_report = False
    while not valid_report:
        choice = input()
        try:
            report = reports[int(choice)]
        except (KeyError, ValueError):
            print('Please pick a number 1 - 3')
        else:
            valid_report = True
    print_report(report, file_out)


if __name__ == '__main__':
    main(sys.argv[1:])
