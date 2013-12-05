
import collections
from mrjob.job import MRJob



class FileMapReduce(MRJob):
    # Map Reduce program to fetch the Ratings file(10,000,000 lines) and create the user ids without duplicates
    
    def mapper(self, _, line):
       
        part = line.split(',')
        yield (part[0], "")


    def reducer(self, ids, values):
                   
        yield (ids, "")


    def steps(self):
        return [
           self.mr(mapper=self.mapper,
                  reducer=self.reducer)
#            self.mr(mapper=self.mapper_sentiment)
        ]

if __name__ == '__main__':
    FileMapReduce.run()
