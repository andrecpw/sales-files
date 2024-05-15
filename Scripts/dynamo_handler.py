import streamlit as st
import boto3
from botocore.exceptions import ClientError
import datetime as dt

def gvision_dynamodb_preprocess(data):
    # Iterate through all keys in the dictionary and replace None with empty strings
    for key in data.keys():
        if data[key] is None:
            data[key] = 'empty'  # Replace None with an empty string
    data['timestamp'] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['chassi+tstp'] = data['chassi'] + ' at ' + data['timestamp']
    return data

def fv_dynamodb_preprocess(data):
    for key in data.keys():
        if data[key] is None:
            data[key] = 'empty'  # Replace None with an empty string
    data['timestamp'] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['cpf+tstp'] = data['CPF'] + ' at ' + data['timestamp']    
    return data

def store_data(table_name, data):
    # Retrieve your AWS credentials from st.secrets
    aws_access_key_id = st.secrets["db_access_key"]
    aws_secret_access_key = st.secrets["db_secret_key"]

    # Set up the DynamoDB connection
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='eu-north-1',  # Make sure to use your region
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    table = dynamodb.Table(table_name)

    try:
        response = table.put_item(Item=data)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print('Successfully inserted data into DynamoDB')
        else:
            print('Response:', response)
    except ClientError as e:
        print('Failed to insert data into DynamoDB: {}'.format(e))