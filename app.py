import requests
import pandas as pd
from flask import Flask, render_template, request
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)

def getData (ticker, year, price):
	datestart = '%d-01-01' %year
	dateend = '%d-12-31' %year
	response = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/Prices.json?ticker=%s&date.gte=%s&date.lte=%s&qopts.columns=ticker,date,%s&api_key=4BTpkmyWHozgfQZzzesc' %(ticker,datestart,dateend,price))
	return response

def processData (ticker, year, price):
	r = getData(ticker, year, price)
	rjs = r.json()['datatable']['data']
	if rjs:
		df = pd.DataFrame(rjs)
		df.columns = pd.DataFrame(r.json()['datatable']['columns'])['name']
		df.set_index(pd.DatetimeIndex(df['date']), inplace=True)
	else:
		df = None #Return None if ticker or year are invalid
	return df

def makePlot (df, ticker, year, price):
	plot = figure(x_axis_type="datetime", title="Quandl WIKI Stock Data - %d" %year)
	plot.grid.grid_line_alpha=1.0
	plot.xaxis.axis_label = 'Date'
	plot.yaxis.axis_label = 'Price (USD)'
	plot.line(df.index, df[price], color='#0000FF', legend='%s: %s' %(ticker,price))
	plot.legend.location = "top_left"
	script, div = components(plot)
	return script, div

@app.route('/', methods=['GET','POST'])
def index():
	return render_template('index.html')

#df=processData('GOOG',2016,'low')
#################################
#@app.route('/graph', methods=['POST'])
#def graph():
#    script, div=makePlot(df,'GOOG',2016,'low')
#    return render_template('graph.html', div = div, script = script)

#@app.route('/graph', methods=['POST'])
#def graph():
#    ticker, price, year = request.form['tickerInput'].upper(), request.form['priceInput'], request.form['yearInput']
#    #Somewhat sloppy way of doing error checking...
#    year = int(year) #int(float(year)) #int(year)
#    df = processData(ticker, year, price)
#    script, div = makePlot(df, ticker, year, price)
#    return render_template('graph.html', div = div, script = script)

@app.route('/graph', methods=['POST'])
def graph():
	ticker, price, year = request.form['tickerInput'].upper(), request.form['priceInput'], request.form['yearInput']
	
	#Somewhat sloppy way of doing error checking...
	if ticker == '' or year == '':
		df = None
	else:
		year = int(year)	
		df = processData(ticker, year, price)

	if type(df) == pd.DataFrame:
		script, div = makePlot(df, ticker, year, price)
		return render_template('graph.html', div = div, script = script)
		#return "HELLO" #render_template('graph.html', div = div, script = script)
		
	else:
		err ='The ticker and year are not available on the database. Please enter a valid ticker and year.'
		return render_template('index.html', err=err)

if __name__ == '__main__':
	app.run(debug=True)
