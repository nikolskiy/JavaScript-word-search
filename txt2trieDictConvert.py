#!/usr/bin/python

import argparse # for command line argument parsing
import os.path   # for path manipulation
import sys         # for script exit

class TrieNode:
    def __init__(self, char, childrenList, complete=False):
        self.letter = char
        self.children = childrenList
        self.complete = complete
     
    def mergeWith(self, trieNode):
        # if self object has only one node, append the other node to its children
        # and return
        if len(self.children) < 1:
            self.children.append(trieNode)
            return self
        
        # compare children of self and the other node
        for child in self.children:
            if child.letter == trieNode.letter:
                if len(trieNode.children) < 1: # can't go deeper in second node
                    # those two sub-tries have the same information
                    # we just need to return self
                    return self
                #look deeper along the branch
                #TODO: raise an error if more then one child is present
                return child.mergeWith(trieNode.children[0])
        
        # at this point we know that the other branch is new in our Trie
        # so we just add it and return self    
        self.children.append(trieNode)
        return self
    
    def getListOfWords(self):
        subWordList = []
        if self.complete:
            subWordList.append(self.letter)
        
        for item in self.children:
            subWordsBelow = item.getListOfWords()
            for ii in subWordsBelow:
                subWordList.append(self.letter + ii)
        
        return subWordList
    
    def getJSstring(self):
        string = ""
        extraClosingBracket = ''
        # check for complete word mark
        if self.complete:
            if len(self.children) < 1:
                # since the node has no children, we mark complete word with an integer
                string += '"%s":1' % self.letter
            else:
                # this node has children so we need to mark it with "$":1
                string += '"%s":{"$":1,' % self.letter
                # we have an extra bracket that will have to be closed later
                extraClosingBracket += '}'
        else: # the node doesn't have a complete word mark
            string += '"%s":{' % self.letter
            # we have an extra bracket that will have to be closed later
            extraClosingBracket += '}'
        
        #print all children letters recursively
        position = 0
        for child in self.children:
            string += '%s' % child.getJSstring()
            #place comma between children
            if(position != len(self.children) - 1):
                string += ','
            position += 1
        
        #close any unclosed brackets at the current level
        if extraClosingBracket != '':
            string += extraClosingBracket
        
        return string
        
class Trie:
    nodeList = []
    
    def branchifyWord(self, word):
        if len(word) < 2: # the last node
            return TrieNode(word[0], [], True)
        else:
            childNodeList = [self.branchifyWord(word[1:])]
            return TrieNode(word[0], childNodeList)
           
    def addWord(self, word):
        branch = self.branchifyWord(word)
        
        if len(self.nodeList) < 1:
            self.nodeList.append(branch)
        else:
            match = False
            for item in self.nodeList:
                if item.letter == branch.letter: # go deeper
                    item.mergeWith(branch.children[0])
                    match = True
                    break
                
            if not match:
                self.nodeList.append(branch)
    
    def getListOfAllWords(self):
        wordList = []
        for node in self.nodeList:
            subWordList = node.getListOfWords()
            for ii in subWordList:
                wordList.append(ii)
        
        return wordList
      
def main(): 
    # parse command line arguments
    parser = argparse.ArgumentParser(description="Convert text dictionary to JSON trie dictionary")
    parser.add_argument('dictionary_file_path')
    args = parser.parse_args()
    
    # get the dictionary path
    file_path = args.dictionary_file_path
    
    # make sure that the file is there
    if not os.path.isfile(file_path):
        print "I'm sorry but I couldn't find a dictionary file at '%s'." % file_path
        sys.exit()
    
    # create an instance of our trie
    trie = Trie()
    
    with open(file_path, "r") as f:
        print 'Adding words to the trie ...'
        numOfWords = 0
        for line in f:
            trie.addWord(line.strip('\n'))
            numOfWords += 1
        print '%s words were added to the trie.' % str(numOfWords)
    
    dir_name, dict_name = os.path.split(file_path)
    
    # get rid of file extension 
    dict_name = os.path.splitext(dict_name)[0]
    # add new extension 
    dictJSname = dict_name + '.js'
    
    dictJSpath = os.path.join(dir_name, dictJSname)
    
    with open(dictJSpath, "w") as fw:
        print 'Constructing %s file ...' % dictJSname 
        fw.write('{')
        nodePosition = 0
        for node in trie.nodeList:
            string = node.getJSstring()
            if nodePosition != len(trie.nodeList) - 1:
                string += ',\n'
            fw.write(string)
            nodePosition += 1
        fw.write('}')
    
    print 'Done!'
       
if __name__ == "__main__":
    main()
    



