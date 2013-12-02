'''
Created on Dec 1, 2013

@author: pratiksomanagoudar
'''
import boto
path = "/CloudFlix/senti-Anl/output/file.dat"
bucket_name = "cloudflixbucket.test"



s3 = boto.connect_s3()
try:
    bucket = s3.get_bucket(bucket_name)  
except boto.exception.S3ResponseError:
    print ('Creating bucket')
    bucket = s3.create_bucket(bucket_name)  
from boto.s3.key import Key

