The resulting file portfolioPerformance.html shows a bubble graph with 3-year-, 1-year and 3-month-performances for
portfolio positions.
3-year-performance is the x-axis, 1-year-performance the y-axis while 3-month-performances are encoded in colour values.
The least performance 20% are red, next orange, yellow, light green up to the 20% best performing values with dark green.

Create the chart:
- create comdirect Musterportfolio
- create there "Meine Ansicht" with Columns "3 Monate, 1 Jahr, 3 Jahre"
- sort by name
- export as csv
- add missing performances in the specific notebook cell
- run and show the resulting portfolioPerformance.html in your browser 

Remarks:
- for initial try copy the given musterdepot_Komplett_meineuebersicht_example.csv to musterdepot_Komplett_meineuebersicht.csv and start the script
- be careful when adding missing values
- the portfolio value that's written to the file is not the real value but a value showing a depot-bubble in appropiate size
- the color bubbles are added to the chart to sort the legend