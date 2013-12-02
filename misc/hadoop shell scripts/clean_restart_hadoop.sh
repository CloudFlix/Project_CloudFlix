cd $HADOOP_HOME/bin
sh stop-mapred.sh
sh stop-dfs.sh
rm -Rf ~/hadooptemp/
rm -Rf ~/tmp
cd $HADOOP_HOME/bin
hadoop namenode -format
sh start-dfs.sh
jps
sleep 10
sh start-mapred.sh
jps
