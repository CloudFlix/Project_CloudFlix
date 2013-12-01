'''
Created on Nov 12, 2013

@author: pratiksomanagoudar
'''
import collections
from mrjob.job import MRJob



class FileMapReduce(MRJob):
    
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
