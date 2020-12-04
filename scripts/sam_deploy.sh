S3_BUCKET=bucket-mlops
S3_BUCKET_MODEL=mlops-cicd
STACK_NAME=sam-sf-sagemaker-workflow
sam build  -t cfn/sam-template.yaml
sam deploy --template-file .aws-sam/build/template.yaml --stack-name ${STACK_NAME} --force-upload --s3-bucket ${S3_BUCKET} \
           --s3-prefix sam --parameter-overrides S3ModelBucket=${S3_BUCKET_MODEL} --capabilities CAPABILITY_IAM