from flask import Flask
from flask import request
from flask import render_template
from flask.ext.pymongo import PyMongo
import sys,os
import Document

app = Flask(__name__)

path = 'C:/rd code/TA Demo/data/'

def readFilesFromDirectory(path):
		collection.remove()
		dirs = os.listdir(path)
		return_string = "{\"data\":["
		for dir in dirs:
			if(os.path.isdir(path+"/"+dir)):
				readDirectory(path+"/"+dir)
			else:
				document = createDocument(path,dir)
				id = loadtomongo(document)
				#print str(id)
				return_string = return_string + "{ \"id\" : \" "  +str(id)+ "\" , \"name\" : \"" + document.getName()+ "\" } ," 
		return_string = return_string.rstrip(",") + "]}"
		return return_string

def createDocument(path,dir):
	document_obj = Document.Document(dir,path+"/"+dir)
	return document_obj


def loadtomongo(document):
	#print document.getPath()
	insert_string = {'name': str(document.getName()) , 'path': str(document.getPath()) }
	id = collection.insert(insert_string)
	#print id
	return id

#connect to mongo db
mongo = PyMongo(app)
from pymongo import Connection
connection = Connection()
db = connection.ta
collection = db.documents

@app.route('/index.html')
def mainpage():
	return render_template('index.html')

@app.route('/tokenize.html')
def tokenizepage():
	return render_template('tokenize.html')

@app.route('/postags.html')
def postagspage():
	return render_template('postags.html')

@app.route('/loadFileNames')
def loafIleName():
	return_String = readFilesFromDirectory(path)
	return return_String

@app.route('/getContent/<name>')
def getContent(name):
	for document in collection.find({'name' : name}):
		path = document['path']
	File = open(path,'r')
	output = ""
	for line in File:
		#if line != '\n':
		output = output + line + "\n"
	#print output
	return output		

if __name__ == '__main__':
	app.run(debug=True)







			






