'''
Created on Dec 1, 2013

@author: pratiksomanagoudar
'''
import boto,sys
from boto.s3.key import Key

def main(argv):
    print 'bucket     :'+str(argv[0])
    print 'input file :'+str(argv[1])
    print 'output file:'+str(argv[2])
    bucket_name = str(argv[0])
    input_file = str(argv[1])
    output_file =str(argv[2])
    s3 = boto.connect_s3()
    try:
        bucket = s3.get_bucket(bucket_name)  
    except boto.exception.S3ResponseError:
        print ('Creating bucket')
    bucket = s3.create_bucket(bucket_name)  
    
    key = bucket.new_key(output_file)
    if key.exists:
        print 'deleting existing file ...'
        key.delete()
    print 'copying contents ...'
    key.set_contents_from_filename(input_file)
    key.set_acl('public-read')
if __name__ == "__main__":
   main(sys.argv[1:])