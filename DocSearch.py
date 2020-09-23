import numpy as np
import math
import re
def calc_angle(x, y):
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    cos_theta = np.dot(x, y) / (norm_x * norm_y) 
    theta = math.degrees(math.acos(cos_theta)) 
    return theta

file2 = open("queries.txt","r")
file1 = open("docs.txt","r")

#takes sentences from the txt
text=[]
regex = re.compile(r'[\n\t\r]')
for line in file1:
    text.append(regex.sub(" ",line).rstrip())


#puts the quiries in a list called "query"
query=[]
for x in file2:
    query.append(x.rstrip())


file1.close()
file2.close()

#puts the sentences in dictionary with ID
dic_sentences={}
for x in enumerate (text,1):
    dic_sentences[x[0]]=x[1]

#puts all the words from text in string called "words"
documents=""
for x in text:
    documents += x + " "
words = documents.split(" ")
words.remove("")


#counts how many times a word appear in the doc.txt and puts them the list dic_words
dic_words={}
for x in words:
    if x not in dic_words:
        dic_words[x]=1
    else:
        dic_words[x]+=1

print("Words in dictionary:",len(dic_words))


#creates inverted index
dic_inverted_index = {}

s=0
for x in dic_words:
    s=s+1
    for m in x:
        if m not in dic_inverted_index:
            dic_inverted_index[m]=[]
            dic_inverted_index[m].append(s)
        else:
            if s not in dic_inverted_index[m]:
                dic_inverted_index[m].append(s)


sentences_words=[]
for x in dic_sentences:
    sentences_words.append(dic_sentences[x].split(" "))



for l in query:
    dic_angles={}
    rel=[]
    list_vec_query=[]
    more_than_one=[]
    relevants=""
    dic_rel_ids_words={}

    print("Query:",l)

    splitted = l.split(" ")

    for l in splitted:
        if l not in dic_words:
            splitted.remove(l)
    for m in dic_sentences:
        if set(splitted).issubset(dic_sentences[m].split()):
            rel.append(m)
            relevants+=str(m)+" "

    print("Relevant documents:",relevants)
    

    for m in rel:
        list_of_document_IDs=[]
        dic_doc1={}
        for word in sentences_words[m-1]:
            if word not in dic_doc1:
                dic_doc1[word]=1
            else:
                dic_doc1[word]+=1

        for x in dic_doc1:   
            list_of_document_IDs.append(dic_doc1[x])

        zero_one=[]
        for x in range(0,len(list_of_document_IDs)):
                zero_one.append(0)
        for i in splitted:
            for x in range(0,len(list_of_document_IDs)):
                if i == list(dic_doc1)[x]:
                    zero_one[x]=1
        
        a = np.array(list_of_document_IDs)
        b = np.array(zero_one)
        dic_angles[m]=calc_angle(a,b)

    sorted_results=sorted(dic_angles.items(), key = lambda kv:(kv[1]))

    for x,y in sorted_results:
        print(f"{x} {y:.2f}")
