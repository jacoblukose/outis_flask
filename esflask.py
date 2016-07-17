
from flask import render_template,request,Flask,json
from outis import elastopy
from werkzeug import secure_filename
from werkzeug.wsgi import LimitedStream
from datetime import datetime, timedelta
import csv
import os
from flask.ext.cors import CORS

c=elastopy()
temp_index = 'outis/test_index'

class StreamConsumingMiddleware(object):
	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		stream = LimitedStream(environ['wsgi.input'],
							   int(environ['CONTENT_LENGTH'] or 0))
		environ['wsgi.input'] = stream
		app_iter = self.app(environ, start_response)
		try:
			stream.exhaust()
			for event in app_iter:
				yield event
		finally:
			if hasattr(app_iter, 'close'):
				app_iter.close()

app = Flask(__name__, static_folder='static')
UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))+'/uploads'
print UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
CORS(app)


@app.route('/')
def dashboard():

	return render_template('/home.html',indexes=c.get_indices())

@app.route('/api/v1/data/search',methods=['GET','POST'])
def search():
	from tzlocal import get_localzone
	import iso8601
	from datetime import datetime
	from pytz import timezone
	
	if request.method == 'POST':
		
		data=request.get_json()
		search_data=[]

		try:
			if data['option'] == '10d' :
				interval='d'
				rounding='d'
				time_param='%b %d '
			elif data['option'] == '7d':
				data['option']='1h'
				interval='d'
				time_param='%b %d '
				rounding='w'
			elif data['option'] == '1M':
				data['option']='1d'
				interval='d'
				time_param='%b %d '
				rounding='M'
			elif data['option'] == '1y':
				data['option']='1d'
				interval='M'
				time_param=' %b %Y'
				rounding='y'
			elif data['option'] == '2y':
				data['option']='1y'
				interval='M'
				time_param=' %b %Y'
				rounding='y'
			else:
				interval = 'y'
				time_param='%Y '
				rounding='y'
			val=c.search(data['query'],['something'],data['option'],interval,rounding,temp_index)
			
			for i in val['hits']['hits']:
				time=i['_source']['time']
		
				local_tz = get_localzone()
				m=iso8601.parse_date(time)
				time_utc=m.astimezone(timezone('UTC'))
				local_time=time_utc.astimezone(local_tz)

				i['_source']['time']=local_time.strftime('%A, %B %d, %Y at %H:%M hours')
				search_data.append(i)

			if search_data==[]:
				
				search_data=["No entries found"]
			
		except:
			search_data=["No entries found "]

		
		l=c.map_key(temp_index)
		l=l.keys()
		global outis1,outis2
		outis1= search_data
		
		for idx,value in enumerate(val['aggregations']['2']['buckets']):
			time=val['aggregations']['2']['buckets'][idx]['key_as_string']
			p=datetime.strptime(time,'%Y-%m-%dT%H:%M:%S.%f+{}'.format(time[-5:]))
			val['aggregations']['2']['buckets'][idx]['key_as_string']=p.strftime("{}".format(time_param))
		
		search_data.append(val['aggregations']['2']['buckets'])
		return json.dumps(search_data)
		
	
@app.route('/api/v1/data/estimate',methods=['POST'])
def aggregate():
	if request.method == 'POST':
		data=request.get_json()
		l=c.aggregate(data['option'],data['query'],temp_index)
		if data['option'] == 'terms':
			return json.dumps(l['sample_name']['buckets'])
		else:
			return json.dumps(l['sample_name']['value'])

@app.route('/api/v1/data/upload',methods=['POST'])
def upload():
	if request.method =='POST':
		file = request.files['file']
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			c.upload(filename,temp_index,UPLOAD_FOLDER)
			return 'success'

@app.route('/api/v1/data/export',methods=['POST'])	
def export():
	if request.method == 'POST':
		data=json.loads(request.body)
		l=c.map_key(temp_index)
		l=l.keys()
		l.sort()
		l2=[]
	
		
		for items in l:
			try:
				if data[items] == True:
					l2.append(items)
			except:
				pass
		
		global outis1
		
		with open('outis/static/data.csv', 'wb') as output_file:
			dict_writer = csv.DictWriter(output_file, l2,extrasaction='ignore')
			dict_writer.writeheader()
			try:
				for k in outis1[:-1]:
					dict_writer.writerows([k['_source']])
			except:
				pass
	

		file_data=open("static/data.csv", "rb").read()
		resp=HttpResponse(file_data,content_type='text/csv;charset=utf-8')
		resp['Content-Disposition'] = 'attachment;filename=table.csv'
		return resp



if __name__ == "__main__":
	app.debug = True
	app.run()
	app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)
