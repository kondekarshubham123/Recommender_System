import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

df = pd.read_csv('Model/preprocessing.csv')
events = df.iloc[:,3:]

eve,dom = pickle.load(open('Model/Events.pickle','rb')),pickle.load(open('Model/Domain.pickle','rb'))

lookup,recommendations = [],[]


def predict():
    s = input('Enter the sentence for Job/Internship: ')
    
    ev = [i for i in eve if i in s]
    d = [i for i in dom if i in s]
    
    event1 = input("Enter Event 1: ")
    event2 = input("Enter Event 2: ")
    
    event1 = eve[event1.lower()]
    event2 = eve[event2.lower()]
    
    similar_metrics = cosine_similarity(events)
    result = np.where(events == [event1,event2])[0][0]
    
    result = list(enumerate(similar_metrics[result]))
    result = sorted(result,key= lambda x: x[1],reverse=True)
    top = result[:5]
    
    lst = [(df['Name'].iloc[i[0]]) for i in top]
    
    print("Recommended Students ",end="")
    print(s, '||', lst[0], ',' ,lst[1], ',' ,lst[2], ',', lst[3], ',', lst[4])
    print()
    
    global lookup
    global recommendations
    
    lookup.append(",".join([s, lst[0], lst[1] ,lst[2], lst[3], lst[4]]))
    recommendations.append(lst)
    
N = int(input("Enter total no of test to be done: "))

for _ in range(N):
    predict()
lookup = [data.split(',') for data in lookup]
df1 = pd.DataFrame([lookup[i][0] for i in range(N)], columns=['Event Name'])
df1['Employee Name'] = recommendations

def converttostr(input_seq, seperator=', '):
   final_str = seperator.join(input_seq)
   return final_str


## Saving file to xls
import xlwt 
from xlwt import Workbook 
  
wb = Workbook() 
  
sheet1 = wb.add_sheet('Sheet 1')

sheet1.write(0, 0, 'Event Name') 
sheet1.write(0, 1, 'Employee Name') 

for i in range(0,N):
    sheet1.write(i+1, 0, lookup[i][0])
    sheet1.write(i+1, 1, converttostr(recommendations[i]))
    
wb.save('output.xls')
print("----------------------------------------------------")
print()
print("Xls sheet created with the name of output.xls ")
print()
print()
print("Thanks !!")