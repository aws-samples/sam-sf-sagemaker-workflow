import json
import boto3
import os
# import sagemaker     #.predictor #import csv_serializer,csv_deserializer

# grab environment variables
# ENDPOINT_NAME = os.environ['sagemaker_endpoint']
runtime= boto3.client('sagemaker-runtime')

def lambda_handler(event, context):    
    sagemaker_endpoint = event.get('queryStringParameters').get('sagemaker_endpoint')
    print(f'{sagemaker_endpoint=}')
    payload = json.loads(event['body'])
    print(f'{payload=}')
    
    response = runtime.invoke_endpoint(
        EndpointName=sagemaker_endpoint,
        Body=payload['data'],
        ContentType='text/csv'        
    )
    result = response['Body'].read().decode()
    print(f'{result=}')    

    return {
        'statusCode': 200,
        'body': json.dumps({'result':result.strip('\n')})
    }


if __name__ == "__main__":   
    event = {
        "queryStringParameters": {
            "sagemaker_endpoint": "7b730310-10-11-2020-16-37-4b"
        },
        # "body": "{  \"data\": \"4.5,1.3,10.3,0.3\" }"
        "body": "{  \"data\": \"5.9,3,5.1,1.8\" }"
    }
    
    print(lambda_handler(event,None))