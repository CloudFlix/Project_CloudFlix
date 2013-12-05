cd ~/CloudFlix
rm -Rf mahout_coll/output/
cd /usr/local/mahout/
export MAHOUT_HOME=/home/hadoop/mahout
export MAHOUT_LOCAL=/home/hadoop/mahout
chmod 777 bin
cd bin
chmod u+x mahout
cd ..
rm -Rf temp
bin/mahout recommenditembased --input /home/ubuntu/CloudFlix/mahout_coll/ratingsFile.dat --usersFile /home/ubuntu/CloudFlix/mahout_coll/userslist.dat --numRecommendations 30 --output /home/ubuntu/CloudFlix/mahout_coll/output/ --similarityClassname SIMILARITY_PEARSON_CORRELATION
cd /home/ubuntu/CloudFlix
python ~/CloudFlix/s3Uploader.py final.demo.bucket ~/CloudFlix/mahout_coll/output/part-r-00000 mahout_coll.txt