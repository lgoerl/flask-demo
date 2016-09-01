from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, save, output_file
from bokeh.embed import components
import requests
import pandas as pd

app = Flask(__name__)

app.symbol=''

@app.route('/',methods=['GET','POST'])
def index():
	if request.method == 'GET': return render_template('index.html')
	else: 
		app.symbol = request.form['ticker']
		return redirect('/graphme')

@app.route('/graphme',methods=['GET'])
def graph():
	api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json'%app.symbol
	session = requests.Session()
	session.mount('http://',requests.adapters.HTTPAdapter(max_retries=3))
	raw_data = session.get(api_url)
	stock = raw_data.json()
	df = pd.DataFrame(stock['data'],columns=stock['column_names'])
	to_plot = df[['Date','Close']][:30]

	TOOLS="pan,wheel_zoom,box_zoom,reset,save"
	p = figure(tools=TOOLS,title='Closing Price',plot_width=650, plot_height=650, x_axis_label='date',x_axis_type='datetime',y_axis_label='Closing Price ($)')
	p.line(x=pd.to_datetime(to_plot['Date']),y=to_plot['Close'])
  	script, dif = components(p)
	return render_template('graph.html',script=script, div=div)


if __name__ == '__main__':
  app.run(port=33507)
