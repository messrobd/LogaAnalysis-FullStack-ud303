# LogsAnalysis-FullStack-ud303
Project #1: Logs analysis, of Full Stack Udacity Nanodegree


How to use

To print reports to the console:
  1. Run the script:
    python3 logs_analysis.py
  2. Select an option (by number):
        1. Top 3 articles
        2. Top Authors
        3. Bad days (those with >1% errors)
  3. The program exits after the report has been written

To print reports to file, run the script with the -f option. The remainder is
as above


Design

class Reports(title, formatter, query [, query_args])
  * Attributes:
    Title (string)
      - used in displays, and for the file name
    Formatter (function)
      - converts raw output from the db query into formatted text for
      presentation
    Query (string)
      - sql query to be passed the db
    Query_args (string or tuple) (optional)
      - passes parameters to the query
  * Methods:
    make_report()
      - a generator that calls get_data() (below) to submit the
      report's query to the db and yields lines to the print function (below)

get_data(query)
  * Args:
    query (string): the sql query to be executed by the db
  * connects to the db and executes the query, returning the result to the
  caller
    - db is defined via the global DBName variable
  * connection utilises the psycopg2 module

print_report(report, file_out)
  * Args:
    report (Report instance): everything the method needs to generate the
    report (see above)
    file_out (bool)
      - True: a file will be written to the current working directory, with
      no output to the console
      - False: report will be written to the console  
  * prints the report using properties on the report instance

main(options, file_out=False)
  * Args:
    - options: the user may supply the -f option to cause a file to be written,
    setting file_out to True
      - command line parsing is done using the sys and getopt modules
    - file_out: supplies the value of the file option in the absence of the -f
    command line option
  * collects the reports that have been defined and prompts the user to select
  one
    - reports are defined as a global dictionary variable (see below)
    - in the event that an invalid selection is made, the user will be prompted
    to try again
  * calls print_report() on the selected report
  * the program exits after completing

Report definitions
  * queries:
    - a query (string) global variable is defined for each report to be supported
    - the query string must be a valid sql query
    - the variable contains the whole query; no views are used in the db
    - in the case of the bad days report, the tolerance (0.01) is supplied as a
    variable via query_args (see above)
    - queries do not format return data
  * formatters:
    - a formatter is defined for each report, since the presentation of the
    data in the report must be customised
    - in the case of the bad days report, date format is hardcoded via this
    function
  * a Report instance is created for each report to be supported

Other Global variables:
  * DBName (string): the name of the db from which we get the data
  * reports (dictionary): a collection of the reports, used by the main()
  procedure to present report options and invoke them


Dependencies:
  psycpg2: database connections and queries
  sys: get command line options
  getopt: parse command line options
  os: write files


References:
  * command line options:
  https://www.tutorialspoint.com/python3/python_command_line_arguments.htm
  * flexible constructors:
  https://stackoverflow.com/questions/682504/what-is-a-clean-pythonic-way-to-have-multiple-constructors-in-python
