#!/usr/bin/python


class TrieNode:
    def __init__(self, char, childrenList, complete = False):
        self.letter = char
        self.children = childrenList
        self.complete = complete
     
    def mergeWith(self, trieNode):
        if len(self.children) < 1:
            self.children.append(trieNode)
            return self
        
        for child in self.children:
            if child.letter == trieNode.letter:
                if len(trieNode.children) < 1: # can't go deeper in second node
                    return self
                #look deeper along the branch
                #print "look deeper"
                return child.mergeWith(trieNode.children[0])#TODO: through error if more then one child
            
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
        if self.complete:
            #print self.letter
            if len(self.children) < 1:
                string += '"%s":1'%self.letter
            else:
                string += '"%s":{"$":1,'%self.letter
                extraClosingBracket += '}'
        else:
            string += '"%s":{'%self.letter
            extraClosingBracket += '}'
        
        position = 0
        for child in self.children:
            string += '%s'%child.getJSstring()
            if(position != len(self.children) - 1):
                string +=','
            position += 1
        
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
      
            
trie = Trie()

# read dict file and print words

#dictName = "test_dict.txt"
dictName = "ospd3.txt"
dictPath = "/home/denis/Projects/tutorials/canvas/dicts/"

filePath = dictPath + dictName

f = open(filePath, "r")

print 'Adding words to the trie'
numOfWords = 0
for line in f:
    trie.addWord(line.strip('\n'))
    numOfWords += 1
print '%s words added to the trie'%str(numOfWords)

f.close()

dictJSname = 'dict.js'

fw = open(dictPath + dictJSname, "w")
print 'constructing %s file'%dictJSname 
fw.write('{')
nodePosition = 0
for node in trie.nodeList:
    string = node.getJSstring()
    if nodePosition != len(trie.nodeList)-1:
        string += ',\n'
    fw.write(string)
    nodePosition += 1
fw.write('}')
fw.close()
print 'done'

#firstB = trie.branchifyWord("hello")
#secondB = trie.branchifyWord("hellobar")

#print trie.getListOfNodeWords(firstB)
#print trie.getListOfNodeWords(secondB)

#firstB.mergeWith(secondB.children[0])

#print trie.getListOfNodeWords(firstB)




