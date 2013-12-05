'''
Created on Dec 1, 2013

@author: pratiksomanagoudar
'''
import boto,sys
from boto.s3.key import Key

def main(argv):
    s3 = boto.connect_s3()
    print 'downloading from S3....'
    key = s3.get_bucket('cloudflixbucket').get_key('predictionresult/recommend_'+str(argv[0])+'.dat')
    # key.get_contents_to_filename('/var/www/Project_CloudFlix/UI2/recommend_'+str(argv[0])+'.dat')
    key.get_contents_to_filename('~/Desktop/recommend_'+str(argv[0])+'.dat')
    print 'download successful....'
if __name__ == "__main__":
   main(sys.argv[1:])