Welcome to my milestone project!

This app accepts a stock ticker input from the user and plots closing price data for one month.
The data source is from the [Quandl WIKI](https://www.quandl.com/databases/WIKIP).
The app takes dataset and puts it into a pandas dataframe to be plotted via Bokeh embedding. Flask is used to tie the code to html and the app is deployed via Heroku. You can view my completed Heroku app [here](https://morteza-waskasi-milestone.herokuapp.com/). The app takes ticker, year, and various price metrics as inputs and outputs a time-series plot.

The app.py is the main python file that grabs stock data from Quandl API, plots it, and embeds to html with the help of Bokeh and Flask.

The Procfile, requirements.txt, conda-requirements.txt, and runtime.txt are config files that mainly tell Heroku what packages to include.

The templates directory contains html files for the index (index.html) and plot (graph.html) pages.
