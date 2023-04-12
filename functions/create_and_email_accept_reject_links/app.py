import json
import base64
import datetime
import os
import uuid
import sys
import traceback
import boto3
import urllib.parse

sns = boto3.client('sns')

def lambda_handler(event, context):
    # TODO implement
    print(event) 
   
    s3_batch_output=event['s3_batch_output']
    print(f'{s3_batch_output=}')
    api_id=os.environ['HttpApiID']
    sns_arn=os.environ['SNSArn']
    task_token= event['token']
    url_template_sucess = f'https://{api_id}.execute-api.us-east-1.amazonaws.com/v1/respond?type=success&{urllib.parse.urlencode({"token":task_token})}'
    url_template_fail = f'https://{api_id}.execute-api.us-east-1.amazonaws.com/v1/respond?type=fail&{urllib.parse.urlencode({"token":task_token})}'
    #encoded_str=urllib.parse.urlencode(url_template_sucess)
    msg_body = f'''
        Please find the transformed data in S3 bucket {s3_batch_output}, based on your findings approve or reject enpoint request</title> <body> Please find the transformed data in S3 bucket s3://mlops-cicd/output, based on your findings approve or reject enpoint request
        
        Accept: {url_template_sucess}

        Reject: {url_template_fail}

    '''

    response = sns.publish(
        TopicArn=sns_arn,    
        Message=msg_body,
        Subject='Approve or Reject',
        MessageStructure='string'
    )  
    return {
        'statusCode': 200,
        'body': json.dumps('Email send to Approve or Reject batch transform results')
    }    


