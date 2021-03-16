#!/usr/local/bin/python3
#import pandas as pd
import re
import sys
import os
#import matplotlib.pyplot as plt
import os.path
from os import path


def raplclean(url2):
    frapl = open(url2,"r")
    rapl = frapl.read()
    rapl = re.sub(r"\s,\s",",",rapl)
    rapl = re.sub(r'([-](?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?', "0.0", rapl)
    frapl.close()
    frapl = open(url2,"w")
    frapl.write(rapl)
    frapl.close()
    return frapl

def ardclean(url1):
    fard = open(url1, "r")
    disco = fard.read()
    disco = re.sub(r"\n\n","\n",disco)
    disco = re.sub("Joules","Disco",disco)
    disco = re.sub(r"Arduino Ready\n","",disco)
    disco = re.sub(r"\n$","",disco)
    disco = re.sub(r'([-](?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?', "0.0", disco)
    fard.close()
    fard = open(url1, "w")
    fard.write(disco)
    fard.close()
    return fard

#media do sleep
def printmediasleep(energySpent,results,text):
    txt = "" 
    energyPerUs = {}
    for i in energySpent.keys():
        if(i == "Disco"):
            txt = txt + str(energySpent[i]/len(results[i])) + "\n"
            energyPerUs[i] = energySpent[i]/len(results[i])
        else:
            txt = txt + str(energySpent[i]/len(results[i])) + ";"
            energyPerUs[i] = energySpent[i]/len(results[i])
    finalfile = open(text+".final", "w") 
    finalfile.write(txt)
    finalfile.close()
    return energyPerUs


def crp(url1,url2,txt): #Processar dados e organizar
    energySpent = {}
    results = {}
    frapl = open(url2, "r")
    text = frapl.read()
    text = re.split(r'\n',text)
    vals = re.split(r',',text[0])
    #Adicionar os valores do RAPL aos resultados
    for i in vals:
        results[i] = []
        energySpent[i] = 0.0
    for line in text[1:]:
        aux = re.split(r',',line)
        if aux == [''] :
            continue
        j = 0
        for i in vals:
            if( j==0 and float(aux[j]) <= 0):
                continue
            results[i].append(float(aux[j]))
            energySpent[i] += float(aux[j])
            j = j+1
    frapl.close()
    #Adicionar os valores do ard aos resultados
    if(path.exists(urlard)):
        fard = open(url1, "r")
        text = fard.read()
        text = re.split(r'\n',text)
        results[text[0]] = []
        energySpent[text[0]] = 0.0
        for line in text[1:]:
            results[text[0]].append(float(line))
            energySpent[text[0]]+=float(line)
        fard.close()
    printSoma(energySpent,txt,urlrapl)

        

## Resultados - Energia Gasta - energia do sistema operativo
def printResults(results,energySpent,energyPerUs,txt):
    txt = "" 
    for i in energySpent.keys():
        if(i == "Disco"):
            print("Energy Spent on Disk:",energySpent[i],"J")
            txt = txt + str(energySpent[i]-(energyPerUs[i]*len(results[i]))) +"\n"

        elif(i == "GPU"):
            txt = txt + "0" + ";"
        else:

            txt = txt + str(energySpent[i]-(energyPerUs[i]*len(results[i]))) + ";"
    finalfile = open(text+".sum", "a+") 
    finalfile.write(txt)
    finalfile.close()            

## Resultados - Energia Gasta 
def printSoma(energySpent,text,urlrapl):
    txt = "" 
    print("Somas de ",urlrapl," :")
    for i in energySpent.keys():
        if(i == "Disco"):
            print("Energy Spent on Disk:",energySpent[i],"J")
            txt = txt + str(energySpent[i]) +"\n"

        elif(i == "GPU"):
            txt = txt + "0" + ";"
        else:
            print("Energy Spent on Rapl(",i,"):",energySpent[i],"J")            
            txt = txt + str(energySpent[i]) + ";"
    finalfile = open(text+".sum", "a+") 
    finalfile.write(txt)
    finalfile.close()            



##tratar dos resultados
text = sys.argv[1]
finalfile = open(text+".sum", "w") 
finalfile.write("Package;CPU;GPU;DRAM;Disco\n")
finalfile.close()     
urlard= text+".ard"
urlrapl= text+".rapl"
if(path.exists(urlard)):
    ardclean(urlard)
if(path.exists(urlrapl)):
    raplclean(urlrapl)
    crp(urlard,urlrapl,text)
else:
    print("ficheiro nao existe")
#sequiseres varios ficheiros
#for i in range(1,11):
#        urlard= str(i)+text+".ard"
#        urlrapl= str(i)+text+".rapl"
#        if(path.exists(urlard)):
#            ardclean(urlard)   
#        if(path.exists(urlrapl)):
#            raplclean(urlrapl)
#            crp(urlard,urlrapl,text)
 
