from math import sqrt
import sys
invertedIndex = {}
docDict ={}
idfDict = {}
docCount = 0
def readDocs(fileName):
    global docCount
    global invertedIndex
    global docDict
    with open(fileName, 'r') as docs:
        doc = docs.readline()
        while doc:
            docCount += 1
            docID = doc.split('\t')[0]
            terms = (doc.split('\t')[1]).split()
            docDict[docID] = terms
            for term in terms:
                if term in invertedIndex.keys():
                    if docID not in invertedIndex[term]:
                        invertedIndex[term].append(docID)
                else:
                    invertedIndex[term] = [docID]
            doc = docs.readline()

def getPostings(terms, outputPath):
    for term in terms:
        with open(outputPath, 'a', encoding='utf8') as f:
            f.write('GetPostings' + '\n')
            f.write(term + '\n')
            if term in invertedIndex:
                out = ''
                for doc in sorted(invertedIndex[term]):
                    out +=  ' ' + doc
                f.write('Postings list:' + out + '\n')

def frequency(term):
    return len(invertedIndex[term])
    
def intersect(p1, p2):
    intersectionList = []
    index1, index2 = 0, 0
    count = 0
    skip = int(sqrt(len(p2)))
    while index1 < len(p1) and index2 < len(p2):
        #Skip pointer Implementation
        #Start:
        """if len(p2) > 10:
            prev = index2
            while p1[index1] > p2[index2]:
                if (index2 % skip == 0) and (index2 + skip < len(p2)):
                    prev = index2
                    index2 += skip
                else:
                    break
            else:
                index2 = prev"""
        #End
        if p1[index1] == p2[index2]:
            intersectionList.append(p1[index1])
            index1 += 1
            index2 += 1
        elif p1[index1] < p2[index2]:
            index1 += 1
        else:
            index2 += 1
        count += 1
            
    return intersectionList, count

def DaatAnd(terms):
    terms.sort(key = frequency)
    result = invertedIndex[terms[0]]
    terms = terms[1:]
    comparision = 0
    while len(result) > 0 and len(terms) > 0:
        result, count = intersect(result, invertedIndex[terms[0]])
        terms = terms[1:]
        comparision += count
    
    strResult = ''
    if (len(result) > 0):
        for term in sorted(result):
            strResult +=  ' ' + term
    else:
        strResult = ' empty'
    return strResult, comparision, len(result)

def union (p1, p2):
    unionList = p1
    count = 0
    for id in p2:
        if id not in unionList:
            unionList.append(id)
        count += 1
    return unionList, count
    
def DaatOr(terms):
    terms.sort(key = frequency, reverse = True)
    result = invertedIndex[terms[0]]
    terms = terms[1:]
    comparision = 0
    while len(terms) > 0:
        result, count = union(result, invertedIndex[terms[0]])
        terms = terms[1:]
        comparision += count
    
    strResult = ''
    if (len(result) > 0):
        for term in sorted(result):
            strResult +=  ' ' + term
    else:
        strResult = ' empty'
    return strResult, comparision, len(result)

def idf(tokens):
    global idfDict
    for term in tokens:
        idfDict[term] = float(docCount) / len(invertedIndex[term])

def tf_idf(query, docList):
    score = {}
    strScore = ''
    if len(docList) == 1 and docList[0] == 'empty':
        strScore = ' empty'
    else:
        for doc in docList:
            score[doc] = 0.0
            N = len(docDict[doc])
            for term in query:
                tf = docDict[doc].count(term)
                score[doc] += float(tf) / N * idfDict[term]
                
        sortedScore = sorted(score.items(), key = lambda x : x[1], reverse = True)
        for key in sortedScore:
            strScore += ' ' + key[0]
    return strScore

if __name__ == '__main__':
    inputPath = sys.argv[1]
    outputPath = sys.argv[2]
    queryPath = sys.argv[3]
    
    readDocs(inputPath)
    idf(invertedIndex.keys())
    with open(queryPath, 'r') as queryFile:
        query = queryFile.readline()
        while query:
            queryTerms = query.split()
            getPostings(queryTerms, outputPath)
            outTerms = ''
            for term in queryTerms:
                outTerms += term + ' '
            with open(outputPath, 'a', encoding='utf8') as f:
                f.write('DaatAnd' + '\n')
                f.write(outTerms + '\n')
                andDocIds, comparisions, numOfDocs = DaatAnd(queryTerms)
                f.write('Results:' + andDocIds + '\n')
                f.write('Number of documents in results: ' + str(numOfDocs) + '\n')
                f.write('Number of comparisons: ' + str(comparisions) + '\n')
                f.write('TF-IDF' + '\n')
                rankedDocs  = tf_idf(queryTerms, andDocIds.split())
                f.write('Results:' + rankedDocs + '\n')
                
                f.write('DaatOr' + '\n')
                f.write(outTerms + '\n')
                OrDocIds, comparisions, numOfDocs = DaatOr(queryTerms)
                f.write('Results:' + OrDocIds + '\n')
                f.write('Number of documents in results: ' + str(numOfDocs) + '\n')
                f.write('Number of comparisons: ' + str(comparisions) + '\n')
                f.write('TF-IDF' + '\n')
                rankedDocs  = tf_idf(queryTerms, OrDocIds.split())
                f.write('Results:' + rankedDocs + '\n')
                
                f.write('\n')
                
                query = queryFile.readline()
