# Inusah Diallo Bonumose LLC 10/20/2019 gui.py
#code for a GUI interface for autoblast
from tkinter import*
from tkinter import filedialog
from tkinter.ttk import*
import theclass
from theclass import main_run
import time
import threading
import csv
import shutil
import traceback
import sys
import os

# progress bar curtosy of https://stackoverflow.com/questions/33768577/tkinter-gui-with-progress-bar
root = Tk(screenName="AutoBlast!",baseName="AutoBlast!",className="AutoBlast!")
root.geometry("600x400") # set size of the window
topFrame=Frame(root)
topFrame.pack()
N=StringVar()
bottom=Frame(root)
bottom.pack(side=BOTTOM)
#information label
info=Label(topFrame,text="In order to run enter at least 2 protein names\nSeperate by commas and press Submit")
info.pack()
pro=Entry(topFrame)
labs=Label(topFrame,text="Output type")
labs.pack()
rb=Radiobutton(topFrame,text="CSV",value='0',var=N) #radio button for csv file
rb.pack()
xb=Radiobutton(topFrame,text="EXCEL",value='1',var=N) #radio button for excel file 
xb.pack()
#protein name entry label
prol=Label(topFrame,text="Enter Protein Names here")
pro.pack(side=RIGHT)
prol.pack(side=LEFT)
#threshold level entry label
therl=Label(text="Enter Quary Coverage Threshold here")
ther=Entry()
ther.pack(side=BOTTOM)
therl.pack(side=BOTTOM)
# fuction that is used by the reset button to reset things 
def file_save():
    if(N.get()==0):
        f = filedialog.asksaveasfilename(defaultextension='.csv') #determines whether the output file type is an excel or csv file 
    else:
        f = filedialog.asksaveasfilename(defaultextension='.xlsx')

    newpath=os.path.join(os.getenv('appdata'),'Autoblast')
    if f is None:
        return
    shutil.copy(newpath+r'\Results.csv',f) #copies output file to the destination location 
def reset(): # resets the forms 
    pro.delete(0,'end')
    ther.delete(0,'end')
    progress['value']=0
    info['text']="In order to run enter at least 2 protein names\nSeperate by commas and press Submit"
# main function for running the actual analysis 
def runs():
    newpath=os.path.join(os.getenv('appdata'),'Autoblast')
    try:
        info.config(text="Analysis in Progress.....")
        info.update()
        #if the user enters nothing for threshold default is 50%
        fin=[]
        if(ther.get()==""):
            x=50
        else:
            x=int(ther.get())
        if(pro.get()==""): #if the user inputs nothing for names causes error
            y=int("fake") # bad code to create error
        else:
            if "," in pro.get():
                fin=pro.get().split(',')
            else:
                y=pro.get().split(']')#split string input by comma into list
                for a in y:
                    k=(a.strip('[]'))
                    if(k!=""):
                        fin.append(k.strip('""'))

        t=threading.Thread(target=main_run,args=(fin,x)) #thread for main function
        t.start()
        while(t.is_alive()):
            bar()#progress bar
            
        info['text']="Complete!"  
        file_save()
    except: # error logging 
        info['text']="Input Error Please Try Again"
        pro.delete(0,'end')
        ther.delete(0,'end')
        f = open(newpath+r'\error.log', 'w')
        e = traceback.format_exc()
        f.write(str(e))
        f.close()
        

sub=Button(bottom,text="Submit",command=runs) #submit button
sub.pack()
siv=Button(bottom,text="Save",command=file_save) #save button
siv.pack()
re=Button(bottom,text="Reset",command=reset)# reset button
re.pack()
progress=Progressbar(root,orient=HORIZONTAL,length=200,mode='indeterminate')
#progress bar code 
def bar():
    import time
    progress['value']=0
    root.update_idletasks()
    time.sleep(1)
    progress['value']=20
    root.update_idletasks()
    time.sleep(1)
    progress['value']=50
    root.update_idletasks()
    time.sleep(1)
    progress['value']=80
    root.update_idletasks()
    time.sleep(1)
    progress['value']=100
progress.pack(side=BOTTOM)

root.mainloop()