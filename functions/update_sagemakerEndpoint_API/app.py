import os,traceback, json
import logging
import boto3
from time import sleep

logger = logging.getLogger()
logger.setLevel(logging.INFO)

api_id=os.environ['HttpApiID']
sns_arn=os.environ['SNSArn']

lambda_client =  boto3.client('lambda')
sns = boto3.client('sns')
sagemaker=boto3.client('sagemaker')

def lambda_handler(event, context):
    print(event)     
    sagemaker_endpoint= event['EndpointArn'].split('endpoint/')[1]       
    sagemaker_response = sagemaker.describe_endpoint(
                EndpointName=sagemaker_endpoint
            )        
    status = sagemaker_response['EndpointStatus']
    print(f'Sagemaker Endpoint {status=}')

    while status == 'Creating':
        sagemaker_response = sagemaker.describe_endpoint(
                EndpointName=sagemaker_endpoint
            )        
        status = sagemaker_response['EndpointStatus']
        print(f'Sagemaker Endpoint {status=}')
        sleep(10)    # 5 second throttle

    msg_body=''
    if status == 'InService':           
        url_template_sucess = f'https://{api_id}.execute-api.us-east-1.amazonaws.com/v1/invokeSagemakerAPI?sagemaker_endpoint={sagemaker_endpoint}'
        msg_body = f'''
            API Sagemaker Inference Endpoint: {url_template_sucess}            
        '''
        print(f'{url_template_sucess=}')
    else:
        msg_body =f'ERROR creating Sagemaker Endpoint {status=} '         
        print(f'ERROR creating Sagemaker Endpoint {status=} ')
    

    sns_response = sns.publish(
            TopicArn=sns_arn,    
            Message=msg_body,
            Subject='Sagemaker Inference endpoint',
            MessageStructure='string'
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Email sent with API endpoint')
    }    
