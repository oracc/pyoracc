from __future__ import print_function
import sys
import os
import codecs
from ..atf.atffile import AtfFile


class Corpus(object):
    def __init__(self, pattern="*.atf", **kwargs):
        self.texts = []
        self.serialised_texts = []
        self.failures = 0
        self.failures2 = 0
        self.serialiser_failures = 0
        self.successes = 0
        self.successes2 = 0
        self.serialiser_successes = 0
        if 'source' in kwargs:
            for dirpath, _, files in os.walk(kwargs['source']):
                for file in files:
                    try:
                        path = os.path.join(dirpath, file)
                        print("Parsing file", path, "... ", end="")
                        content = codecs.open(path,
                                              encoding='utf-8-sig').read()
                        parsedAtf = AtfFile(content)
                        self.texts.append(parsedAtf)
                        self.successes += 1
                        print("OK")
                        
                        try:
                            print("Serialising first time file", path, "... ", end="")
                            serializedAtf = parsedAtf.serialize()
                            self.save_file(serializedAtf, path)
                            print("OK")
                            
                            try:
                                print("Parsing second time file", path, "... ", end="")
                                parsedAtf = AtfFile(serializedAtf)
                                self.successes2 += 1
                                print("OK")
                                
                                try:
                                    print("Serialising second time file", path, "... ", end="")
                                    serializedAtf = parsedAtf.serialize()
                                    self.serialised_texts.append(serializedAtf)
                                    self.save_file(serializedAtf, path)
                                    self.serialiser_successes += 1
                                    print("OK")
                                    
                                except:
                                    self.serialised_texts.append(None)
                                    self.serialiser_failures += 1
                                    print("Failed")
                                    
                            except:
                                self.failures2 += 1
                                print("Failed")
                            
                        except:
                            self.serialised_texts.append(None)
                            self.serialiser_failures += 1
                            print("Failed")
                        
                    except:
                        self.texts.append(None)
                        self.failures += 1
                        print("Failed")
                        
            print("self.failures: ", self.failures)
            print("self.successes: ", self.successes)
            print("self.failures2: ", self.failures2)
            print("self.successes2: ", self.successes2)
            print("self.serialiser_failures: ", self.serialiser_failures)
            print("self.serialiser_successes: ", self.serialiser_successes)
            print("Parser failed with ", self.failures, " out of ",
                  self.failures + self.successes, "(",
                  self.failures * 100.0 / (self.failures + self.successes),
                  "%)")
            if not(self.serialiser_failures==0 and self.serialiser_successes==0):
                print("Serializer failed with ", self.serialiser_failures, " out of ",
                  self.serialiser_failures + self.serialiser_successes, "(",
                  self.serialiser_failures * 100.0 / (self.serialiser_failures + self.serialiser_successes),
                  "%)")
                
         
        
    
    def save_file(self, content, filename):
        """
        Write serialized file on disk
        """
        serialized_file = codecs.open(filename+".ser", "w", "utf-8")
        serialized_file.write(content)
        serialized_file.close()

if __name__ == '__main__':
    corpus = Corpus(source=sys.argv[1])
    print()
#     print("Failed with ", corpus.failures, " out of ",
#           corpus.failures + corpus.successes, "(",
#           corpus.failures * 100.0 / (corpus.failures + corpus.successes),
#           "%)")
#     print("Failed with ", corpus.serialiser_failures, " out of ",
#           corpus.serialiser_failures + corpus.serialiser_successes, "(",
#           corpus.serialiser_failures * 100.0 / (corpus.serialiser_failures + corpus.serialiser_successes),
#           "%)")
