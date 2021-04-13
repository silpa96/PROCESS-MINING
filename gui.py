from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox,DISABLED,NORMAL
# import pymysql
import datetime
from functools import partial
from PIL import Image, ImageTk
from main import load_process
import time
title="Adaptive process mining"
path1="sample.jpg"
path2="sample1.jpg"
main_color='#271745'  

def logcheck():
     global username_var,pass_var
     uname=username_var.get()
     pass1=pass_var.get()
     if uname=="admin" and pass1=="admin":
        showcheck()
     else:
         messagebox.showinfo("alert","Wrong Credentials")   

# show home page
def showhome():
    top.config(menu=menubar)
    global f
    f.pack_forget()
    f=Frame(top)
    f.config(bg=main_color)
    f.pack(side="top", fill="both", expand=True,padx=10,pady=10)
    image = Image.open("leaf.jpg")
    photo = ImageTk.PhotoImage(image.resize((top.winfo_width(), top.winfo_height()), Image.ANTIALIAS))
    label = Label(f, image=photo, bg=main_color)
    label.image = photo
    label.pack()

    l=Label(f,text="Welcome",font = "Verdana 60 bold",fg="White",bg=main_color)
    l.place(x=500,y=300)

def showcheck():
    top.title(title)
    top.config(menu=menubar)
    global f
    f.pack_forget()
    f=Frame(top)
    f.config(bg=main_color)
    f.pack(side="top", fill="both", expand=True,padx=10,pady=10)

    f1=Frame(f)
    f1.pack_propagate(False)
    f1.config(bg=main_color,width=300)
    f1.pack(side="left",fill="both")

    global f2,f3
    # f2=Frame(f)
    # f2.pack_propagate(False)
    # f2.config(bg=main_color,width=300)
    # f2.pack(side="right",fill="both")

    f3=Frame(f)
    f3.pack_propagate(False)
    f3.config(bg=main_color,width=1000)
    f3.pack(side="right",fill="both")

    f4=Frame(f1)
    f4.pack_propagate(False)
    f4.config(bg=main_color,height=200)
    f4.pack(side="bottom",fill="both")

    f7=Frame(f1)
    f7.pack_propagate(False)
    f7.config(height=20)
    f7.pack(side="top",fill="both",padx="3")

    l2=Label(f7,text="Process",font="Helvetica 13 bold")
    l2.pack()

    global lb1,entvar
    b1= Button(f4,text="Choose a log file",command=upload)
    b1.pack(fill="both",pady=5,padx=10)
    entvar=StringVar()
    ent1=Entry(f4,textvariable=entvar)
    ent1.pack()
    b2=Button(f4,text="Start process mining",font="Verdana 10 bold",command=lambda:process1(path1,lb1))
    b2.pack(pady=5)
    

    global f6
    l1=Label(f3,text="Result",font="Helvetica 13 bold")
    l1.pack(side="top",fill="both")
    f6=Frame(f3)
    f6.config(bg=main_color)
    f6.pack(side="top",fill="both")
    f61=Frame(f6)
    f61.config(bg=main_color, height=500,width=300)
    f61.pack(side="left")
    f61.pack_propagate(False)

    l1=Label(f61,text="Events")
    l1.pack(pady=2)

    lb2=Listbox(f61,width=200,height=10,font="Helvetica 7 bold")
    lb2.pack(pady=10,padx=5)

    f62=Frame(f6)
    f62.config(bg=main_color, height=500,width=300)
    f62.pack(side="left")
    f62.pack_propagate(False)

    l2=Label(f62,text="Edges")
    l2.pack(pady=2)

    lb3=Listbox(f62,width=200,height=10,font="Helvetica 7 bold")
    lb3.pack(pady=10,padx=5)

    f63=Frame(f6)
    f63.config(bg=main_color, height=500,width=300)
    f63.pack(side="left")
    f63.pack_propagate(False)

    l3=Label(f63,text="thresholds")
    l3.pack(pady=2)

    lb4=Listbox(f63,width=200,height=10,font="Helvetica 7 bold")
    lb4.pack(pady=10,padx=5)

    

    lb1=Listbox(f1,width=400,height=200,font="Helvetica 7 bold")
    lb1.pack(pady=10,padx=5)
    
    

    
def upload():
    global path1,entvar
    path1=askopenfilename()
    showcheck()
    entvar.set(path1)



def process1(path2,lb1):
    global f6,f3,top,lb2,lb3,lb4
    f6.pack_forget()
    f6=Frame(f3)
    f6.config(bg=main_color, height=500)
    f6.pack(side="top",fill="both")
    f6.pack_propagate(False)

    f61=Frame(f6)
    f61.config(bg=main_color, height=500,width=300)
    f61.pack(side="left")
    f61.pack_propagate(False)

    l1=Label(f61,text="Events")
    l1.pack(pady=2)

    lb2=Listbox(f61,width=200,height=10,font="Helvetica 7 bold")
    lb2.pack(pady=10,padx=5)

    f62=Frame(f6)
    f62.config(bg=main_color, height=500,width=300)
    f62.pack(side="left")
    f62.pack_propagate(False)

    l2=Label(f62,text="Edges")
    l2.pack(pady=2)

    lb3=Listbox(f62,width=200,height=10,font="Helvetica 7 bold")
    lb3.pack(pady=10,padx=5)

    f63=Frame(f6)
    f63.config(bg=main_color, height=500,width=300)
    f63.pack(side="left")
    f63.pack_propagate(False)

    l3=Label(f63,text="thresholds")
    l3.pack(pady=2)

    lb4=Listbox(f63,width=200,height=10,font="Helvetica 7 bold")
    lb4.pack(pady=10,padx=5)

    
    global edges,events,f_thresh,corr_thrseshold,p_thresh
    t,edges,events,f_thresh,corr_thrseshold,p_thresh=load_process(path2,lb1)
    print(p_thresh)
    lb1.after(t,delayed_display)
    #lb2.after(14000,showresult,ret)
    
def load():
    global edges,events,f_thresh,corr_thrseshold,p_thresh,t,path2,lb1
    t,edges,events,f_thresh,corr_thrseshold,p_thresh=load_process(path2,lb1)
    print(p_thresh)

    
def showresult(res):
    global lb2
    lb2.insert(0,res)

from PIL import Image
def delayed_display():
    print('display called')
    global f6,f3,lb2,lb3,lb4,edges,events,f_thresh,corr_thrseshold,p_thresh

    lb2.insert(0,*events)
    lb3.insert(0,*edges)
    lb4.insert(0,'Frequency threshold :%s'%(str(f_thresh)))
    lb4.insert(0,'Parallel structure decision threshold :%s'%(str(p_thresh)))
    lb4.insert(0,'Correlation threshold :%s'%(str(corr_thrseshold)))
    image = Image.open('results/main.png')
    image.show()

def delayed_insert(label,index,message):
    label.insert(index,message)  
    

if __name__=="__main__":

    top = Tk()  
    top.title("Login")
    top.geometry("1900x700")
    footer = Frame(top, bg='grey', height=30)
    footer.pack(fill='both', side='bottom')

    lab1=Label(footer,text="Developed by ",font = "Verdana 8 bold",fg="white",bg="grey")
    lab1.pack()

    menubar = Menu(top)  
    # menubar.add_command(label="Home",command=showhome)  
    menubar.add_command(label="Check",command=showcheck)

    top.config(bg=main_color,relief=RAISED)  
    f=Frame(top)
    f.config(bg=main_color)
    f.pack(side="top", fill="both", expand=True,padx=10,pady=10)
    l=Label(f,text=title ,font = "Verdana 35 bold",fg="white",bg=main_color)
    l.place(x=300,y=50)
    l2=Label(f,text="Username:",font="Verdana 10 bold",bg=main_color,fg="white")
    l2.place(x=550,y=300)
    global username_var
    username_var=StringVar()
    e1=Entry(f,textvariable=username_var,font="Verdana 10 bold")
    e1.place(x=700,y=300)

    l3=Label(f,text="Password:",font="Verdana 10 bold",bg=main_color,fg="white")
    l3.place(x=550,y=330)
    global pass_var
    pass_var=StringVar()
    e2=Entry(f,textvariable=pass_var,font="Verdana 10 bold",show="*")
    e2.place(x=700,y=330)

    b1=Button(f,text="Login", command=logcheck,font="Verdana 10 bold")
    b1.place(x=750,y=360)

    top.mainloop() 
