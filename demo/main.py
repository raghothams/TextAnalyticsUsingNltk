from flask import Flask
from flask import request
from flask import render_template
from flask.ext.pymongo import PyMongo
import sys,os
import Document
import json
from nltk.tokenize import word_tokenize,wordpunct_tokenize, sent_tokenize 
from nltk import batch_ne_chunk ,pos_tag
import operator

app = Flask(__name__)

path = 'C:/rd code/TextAnalyticsUsingNltk/demo/data/'
#path = 'C:/rd code/TextAnalyticsUsingNltk/demo/data/amazon/iPhone/'

_tokens=[]
_postags=[]
_entities=[]
_chunked=[]

def readFilesFromDirectory(path):
		dirs = os.listdir(path)
		return_string = "{\"data\":["
		for dir in dirs:
			if(os.path.isdir(path+"/"+dir)):
				#print path+"/"+dir
				readFilesFromDirectory(path+"/"+dir)
			else:
				document = createDocument(path,dir)
				id = loadtomongo(document)
				#print str(id)
				return_string = return_string + "{ \"id\" : \" "  +str(id)+ "\" , \"name\" : \"" + document.getName()+ "\" } ," 
				print return_string
		return_string = return_string.rstrip(",") + "]}"
	
		return return_string

def createDocument(path,dir):
	#print dir,path+"/"+dir
	document_obj = Document.Document(dir,path+"/"+dir)
	return document_obj


def loadtomongo(document):
	#print document.getPath()
	insert_string = {'name': str(document.getName()) , 'path': str(document.getPath()) }
	id = collection.insert(insert_string)
	#print id
	return id

def getDataFromMongo(name):
	print name
	for document in collection.find({'name' : name}):
		path = document['path']
	File = open(path,'r')
	output = ""
	for line in File:
		if line != '\n':
			output = output + line
	#print output
	return output	

def getTokens(text):
	global _tokens
	_tokens = []
	documentContent = getDataFromMongo(text)
	sentences = sent_tokenize(documentContent)
	_tokens = [word_tokenize(sentence) for sentence in sentences]

def getPostags():
	global _postags
	_postags=[]
	_postags=[pos_tag(sentence) for sentence in _tokens]

def getChunks():
	#print _postags
	global _chunked
	_chunked =  batch_ne_chunk(_postags,binary=True)
	#print _chunked
	#return _chunked

def getEntities():
	global _entities
	_entities = []
	for tree in _chunked:
		_entities.extend(extractEntityNames(tree))
		# extractEntityNames(tree)
	return set(_entities)

def extractEntityNames(tree):
	entities=[]
	if hasattr(tree,'node') and tree.node:
		#print tree
		#print tree.node
		if tree.node == 'NE':
			for child in tree:
				print child
				entities.append(' '.join([child[0] for child in tree]))
		else:
			for child in tree:
				entities.extend(extractEntityNames(child))
	return entities


def getTfidf(documentName):
	document = getDataFromMongo(documentName)
	tf_table = {}
	stopWords = 'a about above after again against all am an and any are aren\'t as at be because been before being below between both but by can\'t cannot could couldn\'t did didn\'t do does doesn\'t doing don\'t down during each few for from further had hadn\'t has hasn\'t have haven\'t having he he\'d he\'ll he\'s her here here\'s hers herself him himself his how how\'s i i\'d i\'ll i\'m i\'ve if in into is isn\'t it it\'s its itself let\'s me more most mustn\'t my myself no nor not of off on once only or other ought our ours ourselves out over own same shan\'t she she\'d she\'ll she\'s should shouldn\'t so some such than that that\'s the their theirs them themselves then there there\'s these they they\'d they\'ll they\'re they\'ve this those through to too under until up very was wasn\'t we we\'d we\'ll we\'re we\'ve were weren\'t what what\'s when when\'s where where\'s which while who who\'s whom why why\'s with won\'t would wouldn\'t you you\'d you\'ll you\'re you\'ve your yours yourself yourselves'
	stopWordsList = list(stopWords)
	for entity in _entities:
		ent = str(entity)
		if ent in stopWordsList:
			continue
		else:
			if ent in tf_table.keys():
				value = tf_table[ent]
				value += 1
				del tf_table[ent]
				tf_table[ent] = value
			else:
				tf_table[ent] = 1
	return tf_table
#connect to mongo db
mongo = PyMongo(app)
from pymongo import Connection
connection = Connection()
db = connection.ta
collection = db.documents

@app.route('/index.html')
def mainpage():
	return render_template('index.html')

@app.route('/loadFileNames')
def loafIleName():
	collection.remove()
	return_String = readFilesFromDirectory(path)
	return return_String

@app.route('/getContent/<name>')
def getContent(name):
	output = getDataFromMongo(name)
	return output		

@app.route('/tokenizeData',methods=['POST'])
def tokenizeData():
	text = request.form['text']
	getTokens(text)
	tokens = str(_tokens).translate(None,"[]")
	return tokens
	
@app.route('/postags')
def postagData():
	getPostags()
	postags = str(_postags).translate(None,"[]")
	return postags

@app.route('/chunk')
def chunkData():
	getChunks()
	#return json.dumps(_chunked)
	chunks = str(_chunked).translate(None,"[]")
	return chunks

@app.route('/entities')
def entityData():
	uniqueEntities = getEntities()
	entities = str(uniqueEntities).translate(None,"set[]")
	return entities

@app.route('/tfidf',methods=['POST'])
def tfidfData():
	documentName = request.form['text']
	relevenceScore = getTfidf(documentName)
	sorted_x = sorted(relevenceScore.iteritems(),key=operator.itemgetter(1) ,reverse=True)
	return json.dumps(sorted_x)
	

if __name__ == '__main__':
	app.run()
