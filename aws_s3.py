import boto3
import pandas as pd
from boto3 import client
import glob
import os




# Creating the low level functional client
def get_client(aws_key_id, aws_key):
    client = boto3.client(
        's3',
        aws_access_key_id=aws_key_id,
        aws_secret_access_key=aws_key,
        region_name='us-east-2'
    )
    return client

# Fetch the list of existing buckets and get the list name
def get_bucket_list(client):
    client_response = client.list_buckets()

    # Print the bucket names one by one
    print('Printing bucket names...')
    for bucket_each in client_response['Buckets']:
        print(f'Bucket Name: {bucket_each["Name"]}')

def get_file_name(session, bucket):
    s3 = session.resource('s3')
    bucket_aws = s3.Bucket(bucket)
    for s3_file in bucket_aws.objects.all():
        print(s3_file.key)



# Create the S3 object
# bucket_name: lin13798888mlb, Key = basic_info_pitcher.csv
def create_s3_object(client, bucket_name, file_key):
    obj = client.get_object(
        Bucket=bucket_name,
        Key=file_key
    )
    return obj

# Read data from the S3 object
def get_csv_file(obj):
    data_csv = pd.read_csv(obj['Body'])
    return data_csv

#set session:
def get_session(aws_key_id, aws_key):
    session = boto3.Session(
        aws_access_key_id=aws_key_id,
        aws_secret_access_key=aws_key,
    )
    return session

#upload file:
def upload_file(session, file_name_path, bucket,file_key):
    s3 = session.resource('s3')
    s3.meta.client.upload_file(Filename=file_name_path, Bucket=bucket, Key=file_key)


if __name__ == "__main__":

    aws_key_id = ""
    aws_key = ""
    bucket = ""

    session = get_session(aws_key_id, aws_key)
    #
    # os.chdir("/Users/leechilin/Desktop/python scrape/new_folder")
    #
    # for file_key in glob.glob("*.csv"):
    #     file_name_path = "/Users/leechilin/Desktop/python scrape/pitcher/" + file_key
    #     upload_file(session, file_name_path, bucket, file_key)

    client = get_client(aws_key_id, aws_key)
    get_file_name(session, bucket)