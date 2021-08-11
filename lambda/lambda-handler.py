import json
import os
import boto3

print('Loading function')

def handler(event, context):
	
	
	s3 = boto3.resource('s3')

	BUCKETNAME = os.environ['BUCKETNAME']

	########### PARSE OUT THE MESSAGE BODY ###########

	raw_data=event['Records'][0]['body']

	########### CONSTRUCT THE BODY OF THE RESPONSE OBJECTS ###########

	########### CONSTRUCT HTTP RESPONSE OBJECT ###########
	responseObject = {}
	responseObject['statusCode'] = 200
	responseObject['headers'] = {}
	responseObject['headers']['Content-Type'] = 'application/json'
	responseObject['body'] = json.dumps(raw_data)
	
	object = s3.Object(BUCKETNAME, 'raw_data.txt')
	upload_reponse = object.put(Body=json.dumps(raw_data))

	if upload_reponse['ResponseMetadata']['HTTPStatusCode'] == 200:
		print("upload complete")
	else:
		print("some issue with the s3 upload, needs debugging!")

	########### RETURN THE RESPONSE OBJECT ###########
	return responseObject
