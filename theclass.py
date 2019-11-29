# Inusah Diallo Bonumose LLC 10/20/2019 theclass.py
#defines the main function for autoblast
#Uses selenium browser to input sequence names into uniprot.org to find protein sequences
#Secondly inputs the sequences into blast.ncbi.nlm.nih.gov then extracts percent identity
#lastly creates a matrix of extracted %identity values and then exports it to excel
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
import csv
import os
import sys 
from sys import*
def paths(x):#determines the location of the webdriver 
    try:
        base=sys._MEIPASS
    except:
        base=os.path.abspath(".")
    return os.path.join(base,x)
def main_run(list,thershold): #defines the main function that will be run 
    newpath=os.path.join(os.getenv('appdata'),'Autoblast')
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    options= Options()
    options.headless= True
    names=list
    ther=thershold
    seqs=[] #list of all protein sequences
    Completed=[]#list of all completed comparasions
    Completed2=[]# list of all non-repeating comparasions
    Completed3=[] #list of all-non-repeating comparasions with %identity
    dict={}
    #opens the fasta files for a given tag name then adds seqeunce to seq list
    
    driver = webdriver.Chrome(options=options,executable_path=paths("chromedriver.exe"))
    i=0
    for qu in names:
        driver.get("https://www.uniprot.org/uniprot/"+qu.strip()+".fasta")
        quary = driver.find_element_by_tag_name("pre").text
        seqs.append(quary)
        dict[quary]= names[i]
        i+=1
    #inputs the sequences into BLAST for comparasion
    firstrow=["Results "] # first row in the matrix which has the names of all proteins
    perident={} #dictionary  of all found %identity
    results=[]
    driver.get("https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome")
    for s in seqs:
        
        firstrow.append(dict[s])
        for i in seqs:
            #checks the box for allowing multiple inputs
            c1=dict[s]+" "+dict[i]
            c2=dict[i]+" "+dict[s]
            if not(c1 in Completed) and not(c2 in Completed):
                box1=driver.find_element_by_id("seq")
                box2=driver.find_element_by_id("subj")
                box1.send_keys(s)
                if(not box2.is_displayed() ):
                    elem1 = driver.find_element_by_id("bl2seq")
                    elem1.click()
                #submits the inputs
                #finds the input box
                box2=driver.find_element_by_id("subj")
                box2.send_keys(i)
                #clicks the "BLAST" button
                blast=driver.find_element_by_id("b1")
                blast.click()
                #waits 30 seconds for all elements to load before trying to copy %identity value
                driver.implicitly_wait(30)
                try:
                    quarycov=driver.find_element_by_css_selector('td.c5').text
                    per=driver.find_element_by_css_selector('td.c7')
                    num=int(quarycov[:-1])
                    if(not per.is_displayed()):
                        per_iden="Error Try again"
                    elif(num<ther):
                        per_iden= "Low Q/C"
                    else:
                        per_iden=per.text
                except:
                    per_iden="N/A"
                results.append(per_iden)
                Completed.append(c1)
                Completed2.append(c1)
                Completed.append(c2)
                driver.get("https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome")
    for i in range(len(results)):
        Completed3.append(Completed2[i]+" "+results[i])
        perident[Completed2[i]]=results[i]
    Completed2=[]
    Completed=[]
    Finalout=[]
    Finalout.append(firstrow)
    #creates the matrix
    for x in seqs:
        row=[]
        row.append(dict[x])
        for y in seqs:
            c1 = dict[x] + " " + dict[y]
            c2 = dict[y] + " " + dict[x]
            if not (c1 in Completed) and not (c2 in Completed):
                row.append(perident[c1])
                Completed.append(c1)
                Completed.append(c2)
            else:
                row.append("x")
        Finalout.append(row)
    
    #writes the matrix to a .CSV file
    with open(newpath+r'\Results.csv','w') as f:
        writer= csv.writer(f)
        for n in Finalout:
            writer.writerow(n)
    f.close()
    driver.close()
    
