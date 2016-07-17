__version__ = "1.1"

import urllib2
import urllib
import json
import requests
from datetime import datetime, timedelta
import os

class elastopy():
	def __init__(self,host='localhost',port=9200):
		self.url="http://{}:{}".format(host,port)
		
	#add/update json data to a document
	def index(self,index_name,doc_type,body,_id=""):			
		try:
			ul=self.url+"/{}/{}/{}".format(index_name,doc_type,_id)
			p=urllib2.Request(ul,data=body)
			urllib2.urlopen(p)
			return 1
		except urllib2.HTTPError,e:
			return 0

	#create an index
	def create_index(self,index_name):						
		try:
			ul=self.url+"/{}".format(index_name)
			p=urllib2.Request(ul,data="")
			l=urllib2.urlopen(p)
			return 1
		except urllib2.HTTPError,e:
			return 0


	#returns all documents in inside a index
	def match_all(self,index_name="",size=100):						
		try:
			ul=self.url+"/{}/_search?size={}".format(index_name,size)
			req=urllib2.urlopen(ul)
			val=json.loads(req.read())['hits']['hits']
			return val
		except urllib2.HTTPError,e:
			return 0
	
	#get document
	def get(self,index_name,doc_type,_id):
		try:
			ul=self.url+"/{}/{}/{}".format(index_name,doc_type,_id)
			req=urllib2.urlopen(ul)
			val=json.loads(req.read())['_source']
			return val
		except urllib2.HTTPError,e:
			return 0
	
	#delete document
	def delete(self,index_name,doc_type="",_id=""):
			ul=self.url+"/{}/{}/{}".format(index_name,doc_type,_id)
			req=requests.delete(ul)
			return 1

	#get multiple documents		
	def multiget(self, index_name, doc_num, id_num, **params):
		if (doc_num>1):
			while doc_num>0:
				val=str(doc_num)
				ul=self.url+"/{}/{}/{}".format(index_name,params["doc_type"][val],params["_id"]["1"])
				req=urllib.urlopen(ul)
				print json.loads(req.read())
				doc_num = doc_num-1

		if (id_num>1):
			while  id_num>0:
				val = str(id_num)
				ul=self.url+"/{}/{}/{}".format(index_name,params["doc_type"]["1"],params["_id"][val])
				r=urllib.urlopen(ul)
				print json.loads(r.read())
				id_num= id_num-1


	def bulk(self,option,*params):
		try:
			ul=self.url+"/_bulk"
			t=0
			h=""
			p1=len(params)
			while p1>=3:
				example1 = OrderedDict([('_index', params[t+0]), ('_type', params[t+1]), ('_id', params[t+2])])
				if option == "cre":
					temp={ "create" : example1 } 
					h=h+json.dumps(temp)+"\n"+"{"":""}"+"\n"
				elif option == "del":
					temp={ "delete" : example1 } 
					h=h+json.dumps(temp)+"\n"
				else:
					temp={ "index" : example1 } 
					j='hihi'
					j1='jiji'
					h=h+json.dumps(temp)+"\n"+"{"+'"{}":"{}"'.format(j,j1)+"}"+"\n"
				p1=p1-3
				t=t+3
			p=urllib2.Request(ul,data=h)
			f = urllib2.urlopen(p)
		except urllib2.HTTPError,e:	
			print e.read()
			print "INDEX ALREADY PRESENT "

	#upload from file
	def upload(self,filename,index_name,path):
		filepath=path+"/{}".format(filename)
		print filepath
		# print filepat
		print path
		j=open(filepath)
		l=[]
		data=""
		count=0
		for i,val in enumerate(j.read()):
			if val == '{':
				count=count+1
			data=data+val
			if val == '}':
				count=count-1
				if count ==	 0:	
					self.index(index_name,"doc",data,"")
					data=""
					
	
	#get keys
	def map_key(self,index_name="",doc_type=""):
		if index_name not in self.get_indices():
			self.create_index(index_name)
		ul=self.url+"/{}/_mapping/{}".format(index_name,doc_type)
		req=urllib2.urlopen(ul)
		l=json.loads(req.read())
		templ=[] 
		for i in l:
			for j in l[i]['mappings']:
				temp=l[i]['mappings'][j]['properties']
		return temp
			


	
	def aggregate(self,aggregate_type,field_name,index_name=""):		
		day_tme = datetime.now()
		yest = day_tme + timedelta(days =365)
		yest_iso = yest.isoformat()		
		l=datetime.strptime(yest_iso,'%Y-%m-%dT%H:%M:%S.%f') 


		ul=self.url+"/{}/_search".format(index_name)
		if aggregate_type == 'range':
			h= {  
				   "aggs":{  
				      "sample_name":{  
				         aggregate_type:{  
				            "field":field_name,
				            "ranges":[  
				               {  
                                  "from":day_tme.isoformat(),  #change from and to values
				                  "to":yest_iso                 #accordingly
				               }
				            ]
				         }
				      }
				   }
				}
		else:
			
			h= {  
				   "aggs":{  
				      "sample_name":{  
				         aggregate_type:{  
				            "field":field_name
				         }
				      }
				   }
				}
		h=json.dumps(h)
		j=requests.post(ul,data=h)
		print j.json()['aggregations']
		return j.json()['aggregations']


	#get indices
	def get_indices(self):
		ul=self.url+"/_aliases"
		req=urllib2.urlopen(ul)
		l=json.loads(req.read())
		return l.keys()

	#perform search
	def search(self,query,fields,value,interval,rounding="",indexname=""):
		l=""
		# for i in indexname:
		# 	l=l+i+","
		# if fields != []:
		# 	if indexname != [] :
		# 		ul=self.url+"/{}/_search?".format(l)			
		# 	else:
		# 		ul=self.url+"/_search?"
		# else:
		# 	if l == []:
		# 		l = ""
		# 	ul=self.url+"/{}/_search?q={}".format(l,query)
		# 	f=requests.get(ul,data=None)
		# 	return f.json()
		ul=self.url+"/{}/_search?".format(indexname)

		f={"query":{"bool": 
						{
							"must":{"query_string": 
										{
        							    "query": query
        					    		}
      								},
							
							"filter":{
								          "range": 
								          {
									          "time":
									          {
									         	"lte":"now",
									          "gte":"now-{}/{}".format(value,rounding)
									          }
								          }
								        

									}	
						}
					
					},
					"size":200, 
					"sort": { "time": { "order": "desc" }},
					 "aggs": {
							    "2": {
							      "date_histogram": {
							        "field": "time",
							        "interval": "1{}".format(interval),
							        "time_zone": "Asia/Kolkata",
							        "min_doc_count": 0,
							        "extended_bounds" : { 
						                "min" : "now-{}/{}".format(value,rounding),
						                "max" : "now"
						            }

							      }
							    }
							  }



					
		  
		  }		

		f=json.dumps(f)
		f=requests.get(ul,data=f)
		return f.json()


