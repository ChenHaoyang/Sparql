# coding: utf-8
'''
Created on 2016/04/12

@author: charles
'''
from SPARQLWrapper import SPARQLWrapper, JSON
import csv
import time
#import yahoodict

if __name__ == '__main__':
    file = open("/media/sf_Share/01_projects/06_研究/Task/keyword quality/kw_jp.csv", "r")
    
    text_line = file.readline().rstrip()
    results = None
    error_num = 0
    sparql = SPARQLWrapper("http://ja.dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(2)
    sparql.setUseKeepAlive()
    while text_line <> "":
        tokens = text_line.split(';')
        #tokens[1]="line スタンプ 無料"
        query = "select * where { ?s ?p <http://ja.dbpedia.org/resource/" + tokens[1].replace(' ', '') + "> . } limit 1"
        sparql.setQuery(query)
        try:
            results = sparql.query().convert()
            #results = yahoodict.lookup(word=u'死刑')
        except Exception:
            #text_line = file.readline().rstrip()
            print "Error" + ' ' + tokens[1]
            time.sleep(1)
            if error_num < 3:
                error_num += 1
            else:
                error_num = 0
                text_line = file.readline().rstrip()
            continue

        record_num = results["results"]["bindings"].__len__()
        
        if record_num == 1:
            rowlist = []
            rowlist.append(tokens[0])
            rowlist.append(tokens[1].decode('utf-8').encode('utf-8'))
            writer = csv.writer(open("/home/charles/kw_jp_filtered.csv", 'a'), lineterminator='\n')
            writer.writerow(rowlist)
        
        print tokens[1] 
        text_line = file.readline().rstrip()
        error_num = 0
        #time.sleep(0.02)
        #for result in results["results"]["bindings"]:
            #print(result["s"]["value"])