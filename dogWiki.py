from tkinter import*
from tkinter import ttk
from tkinter import messagebox, scrolledtext
import random
import time
import io
import math
import datetime
import base64
from tkinter import messagebox
from datetime import date
import tkinter
import urllib.request
from PIL import Image, ImageTk

import os
import requests
from io import BytesIO
# instalarse para su ejecucion en otro lado, igual que requests, tkinter, base64 y PIL
import mysql.connector

class IEditBreed(Toplevel):
    def __init__(self,main,breedInfo,photoBreed,userId):
        Toplevel.__init__(self)
        self.update()
        self.resizable(0,0)
        self.geometry("500x450+0+0")
        self.grab_set()

        title=Label(self,bd=3,relief=RIDGE,text="Editando una entrada de raza canina",fg="#388087",bg="#badfe7",font=("lucida sans unicode",13,"bold"))
        title.pack(anchor=N,fill=X,pady=10,padx=15)

        EntryFr=Frame(self,bd=4,relief=RIDGE,bg="#c2edce")
        EntryFr.pack(fill=BOTH,expand=True,padx=20)
        EntryFr.update()

        canvasScroll=Canvas(EntryFr,bg="#c2edce")
        EntryFr.update()
        scroller=Scrollbar(EntryFr,orient="vertical",command=canvasScroll.yview)
        self.scrollerFrame=Frame(canvasScroll,width=EntryFr.winfo_width(),bg="#c2edce")

        self.scrollerFrame.bind(
            "<Configure>",
            lambda e: canvasScroll.configure(
                scrollregion=canvasScroll.bbox("all")
            )
           
        )

        canvasScroll.create_window((0,0), window=self.scrollerFrame, anchor="nw")
        canvasScroll.configure(yscrollcommand=scroller.set)
        canvasScroll.pack(side="left",fill="both",expand=True)
        scroller.pack(side="right",fill="y")

        # Entradas de los campos de cada raza de perro
        Title=Label(self.scrollerFrame,text="Editando la raza: "+breedInfo[0][1],fg="#388087",bg="#badfe7",font=("lucida sans unicode",12,"bold"))
        Title.pack(anchor=W,padx=20,pady=10)
        Descr=Label(self.scrollerFrame,text="Descripción:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Descr.pack(anchor=W,padx=20)
        self.DescT=scrolledtext.ScrolledText(self.scrollerFrame,font=("Century Gothic",9),height=10,width=int(EntryFr.winfo_width()/9))
        self.DescT.pack(anchor=W,padx=20)
        self.DescT.insert(INSERT,breedInfo[0][2])
        Hist=Label(self.scrollerFrame,text="Historia:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Hist.pack(anchor=W,padx=20)
        self.HistT=scrolledtext.ScrolledText(self.scrollerFrame,font=("Century Gothic",9),height=10,width=int(EntryFr.winfo_width()/9))
        self.HistT.pack(anchor=W,padx=20)
        self.HistT.insert(INSERT,breedInfo[0][3])
        Salud=Label(self.scrollerFrame,text="Salud:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Salud.pack(anchor=W,padx=20)
        self.SaludT=scrolledtext.ScrolledText(self.scrollerFrame,font=("Century Gothic",9),height=10,width=int(EntryFr.winfo_width()/9))
        self.SaludT.pack(anchor=W,padx=20)
        self.SaludT.insert(INSERT,breedInfo[0][4])
        Temper=Label(self.scrollerFrame,text="Temperamento:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Temper.pack(anchor=W,padx=20)
        self.TemperT=scrolledtext.ScrolledText(self.scrollerFrame,font=("Century Gothic",9),height=10,width=int(EntryFr.winfo_width()/9))
        self.TemperT.pack(anchor=W,padx=20)
        self.TemperT.insert(INSERT,breedInfo[0][5])
        Foto=Label(self.scrollerFrame,text="Foto (enviar un link al recurso .jpg de una página web)",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Foto.pack(anchor=W,padx=20,pady=10)
        Foto1=Label(self.scrollerFrame,text="Nota: (sólo se mostrará si es un link disponible para descarga):",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Foto1.pack(anchor=W,padx=20)
        self.FotoEntry=Entry(self.scrollerFrame,width=int(EntryFr.winfo_width()/9),font=("Century Gothic",9))
        self.FotoEntry.pack(anchor=W,padx=20)
        self.FotoEntry.insert(INSERT,breedInfo[0][6])
        self.FotoEntry.update()
        PreviewB=Button(self.scrollerFrame,text="Preview de foto",bg="#6fb3b8",font=("Century Gothic",9,"bold"),height=2)
        PreviewB.pack(anchor=W,side=LEFT,pady=10,padx=20)
        PreviewB.bind("<Button>",lambda event: self.getPicPrev(self.FotoEntry.get()))
        self.canvasPr=Canvas(self.scrollerFrame,width=120,height=120)
        self.canvasPr.pack(anchor=W,side=LEFT,pady=10,padx=20)
        imgae=ImageTk.PhotoImage(Image.open(os.getcwd()+photoBreed).resize((120,120)))
        self.imga=imgae
        self.canvasPr.create_image(0, 0, anchor=NW, image=imgae) 

        

        ButtonSend=Button(self,text="Mandar Entrada",bg="#6fb3b8",font=("lucida sans unicode",9,"bold"),height=2)
        ButtonSend.pack(anchor=S,pady=20)
        ButtonSend.bind("<Button>",lambda event: self.enviar(breedInfo[0][1],self.DescT.get('1.0', 'end-1c'),self.HistT.get('1.0', 'end-1c'),self.SaludT.get('1.0', 'end-1c'),self.TemperT.get('1.0', 'end-1c'),self.FotoEntry.get(),userId,breedInfo[0][0]))
    
    def getPicPrev(self,entryurl):
        urllib.request.urlretrieve(
            entryurl,
            "imagetemp/gfg.jpg")  
        img = ImageTk.PhotoImage(Image.open(os.getcwd()+"\imagetemp\gfg.jpg").resize((120,120)))  
        self.img=img
        self.canvasPr.create_image(0, 0, anchor=NW, image=img) 

    def enviar(self,titulo,desc,hist,sal,temper,foto,userId,entryId):
        if desc=='' or hist=='' or sal=='' or temper=='' or foto=='': 
            messagebox.showwarning("Precaución","Todos los campos deben estar llenados")
        else:
            conn=mysql.connector.connect(host="127.0.0.1",username="nicky",password="Hopeinthegalaxy",database="wikican")
            cursor=conn.cursor()
            cursor.execute("update dogbreeds set descripcion=%s, historia=%s, salud=%s, temperamento=%s, foto=%s where titulo=%s",(desc,hist,sal,temper,foto,titulo))
            conn.commit()
            today = str(date.today())
            cursor.execute("insert into edicion(identry,ideditors,dateedit) values(%s,%s,%s)",(entryId,userId,today))
            conn.commit()
            self.destroy()
            obj=Web(root)
    

class IUser(Toplevel):
    def __init__(self,main):
        Toplevel.__init__(self)
        self.update()
        self.resizable(0,0)
        self.geometry("500x420+{}+0".format(int(self.winfo_screenwidth()/2 - self.winfo_reqwidth()/2)))
        self.grab_set()

        title=Label(self,bd=3,relief=RIDGE,text="Registrate como usuario modificador en Wikican",fg="#388087",bg="#badfe7",font=("lucida sans unicode",13,"bold"))
        title.pack(anchor=N,fill=X,pady=10,padx=15)

        

        EntryFr=Frame(self,bd=4,relief=RIDGE,bg="#c2edce")
        EntryFr.pack(fill=BOTH,expand=True,padx=20)
        EntryFr.update()

        NamesF=Frame(EntryFr,relief=FLAT,bg="#c2edce")
        NamesF.pack(side=TOP,fill=BOTH,expand=True)

        NameFr=Frame(NamesF,relief=FLAT,bg="#c2edce")
        NameFr.pack(side=LEFT,fill=BOTH,expand=True)
        NameFr.update()


        Name=Label(NameFr,text="Nombre:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Name.pack(anchor=W,padx=20,pady=5)
        self.NameEntry=Entry(NameFr,width=int(EntryFr.winfo_width()/18),font=("Century Gothic",9))
        self.NameEntry.pack(anchor=W,padx=20)


        SNameFr=Frame(NamesF,relief=FLAT,bg="#c2edce")
        SNameFr.pack(side=LEFT,fill=BOTH,expand=True)
        SNameFr.update()

        SName=Label(SNameFr,text="Apellido:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        SName.pack(anchor=W,padx=20,pady=5)
        self.SNameEntry=Entry(SNameFr,width=int(EntryFr.winfo_width()/18),font=("Century Gothic",9))
        self.SNameEntry.pack(anchor=W,padx=20)
        
        PassEmailFr=Frame(EntryFr,relief=FLAT,bg="#c2edce")
        PassEmailFr.pack(side=TOP,fill=BOTH,expand=True)
        PassEmailFr.update()

        email=Label(PassEmailFr,text="E-mail:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        email.pack(anchor=W,padx=20,pady=5)
        self.emailEntry=Entry(PassEmailFr,width=int(EntryFr.winfo_width()/9),font=("Century Gothic",9))
        self.emailEntry.pack(anchor=W,padx=20)

        passw=Label(PassEmailFr,text="Contraseña (8 caracteres min):",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        passw.pack(anchor=W,padx=20,pady=5)
        self.passwEntry=Entry(PassEmailFr,width=int(EntryFr.winfo_width()/9),font=("Century Gothic",9))
        self.passwEntry.pack(anchor=W,padx=20)

        passw2=Label(PassEmailFr,text="Verificar contraseña:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        passw2.pack(anchor=W,padx=20,pady=5)
        self.passwEntry2=Entry(PassEmailFr,width=int(EntryFr.winfo_width()/9),font=("Century Gothic",9))
        self.passwEntry2.pack(anchor=W,padx=20)

        uname=Label(PassEmailFr,text="Nombre de usuario: ",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        uname.pack(anchor=W,padx=20,pady=5)
        self.UserNameEntry=Entry(PassEmailFr,width=int(EntryFr.winfo_width()/9),font=("Century Gothic",9))
        self.UserNameEntry.pack(anchor=W,padx=20)
        

    
        ButtonSend=Button(self,text="Registrate!",bg="#6fb3b8",font=("lucida sans unicode",9,"bold"),height=2)
        ButtonSend.pack(anchor=S,pady=15)
        ButtonSend.bind("<Button>",lambda event:self.sendUser(self.UserNameEntry.get(),self.NameEntry.get(),self.SNameEntry.get(),self.emailEntry.get(),self.passwEntry.get(),self.passwEntry2.get()))
    

    def sendUser(self,uname,name,sname,email,passW,passVer):
        if uname=='' or name=='' or sname=='' or email=='' or passW=='':
            messagebox.showwarning("Precaución","Los campos deben estar llenados")
        elif passW!=passVer:
            messagebox.showwarning("Contraseñas","Las contraseñas no coinciden")
        elif len(passW)<8:
            messagebox.showwarning("Contraseñas","La contraseña no tiene la longitud necesaria")
        else:
            conn=mysql.connector.connect(host="127.0.0.1",username="nicky",password="Hopeinthegalaxy",database="wikican")
            cursor=conn.cursor()
            cursor.execute("insert into editors(username,password,email,nombre,apellido) values(%s,%s,%s,%s,%s)",(uname,passW,email,name,sname))
            conn.commit()
            messagebox.showinfo("Exito","Se registró en Wikican de manera correcta")
            cursor.close()
            self.destroy()




# Pantalla de ingreso de nueva entrada de razas de perro
class IUpdateBreed(Toplevel):
    def __init__(self,main):
        Toplevel.__init__(self)
        self.update()
        self.resizable(0,0)
        self.geometry("500x450+0+0")
        self.grab_set()
        title=Label(self,bd=3,relief=RIDGE,text="Ingresa una nueva entrada en WikiCan",fg="#388087",bg="#badfe7",font=("lucida sans unicode",15,"bold"))
        title.pack(anchor=N,fill=X,pady=10,padx=15)

        EntryFr=Frame(self,bd=4,relief=RIDGE,bg="#c2edce")
        EntryFr.pack(anchor=CENTER,fill=BOTH,expand=True,padx=20)
        EntryFr.update()

        canvasScroll=Canvas(EntryFr,bg="#c2edce")
        EntryFr.update()
        scroller=Scrollbar(EntryFr,orient="vertical",command=canvasScroll.yview)
        self.scrollerFrame=Frame(canvasScroll,width=EntryFr.winfo_width(),bg="#c2edce")

        self.scrollerFrame.bind(
            "<Configure>",
            lambda e: canvasScroll.configure(
                scrollregion=canvasScroll.bbox("all")
            )
           
        )

        canvasScroll.create_window((0,0), window=self.scrollerFrame, anchor="nw")
        canvasScroll.configure(yscrollcommand=scroller.set)
        canvasScroll.pack(side="left",fill="both",expand=True)
        scroller.pack(side="right",fill="y")

        # Entradas de los campos de cada raza de perro
        Title=Label(self.scrollerFrame,text="Nombre de la raza:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Title.pack(anchor=W,padx=20,pady=10)
        self.TitleEntry=Entry(self.scrollerFrame,width=int(EntryFr.winfo_width()/9),font=("Century Gothic",9))
        self.TitleEntry.pack(anchor=W,padx=20)
        Descr=Label(self.scrollerFrame,text="Descripción:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Descr.pack(anchor=W,padx=20,pady=10)
        self.DescT=scrolledtext.ScrolledText(self.scrollerFrame,font=("Century Gothic",9),height=10,width=int(EntryFr.winfo_width()/9))
        self.DescT.pack(anchor=W,padx=20,pady=10)
        Hist=Label(self.scrollerFrame,text="Historia:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Hist.pack(anchor=W,padx=20,pady=10)
        self.HistT=scrolledtext.ScrolledText(self.scrollerFrame,font=("Century Gothic",9),height=10,width=int(EntryFr.winfo_width()/9))
        self.HistT.pack(anchor=W,padx=20,pady=10)
        Salud=Label(self.scrollerFrame,text="Salud:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Salud.pack(anchor=W,padx=20,pady=10)
        self.SaludT=scrolledtext.ScrolledText(self.scrollerFrame,font=("Century Gothic",9),height=10,width=int(EntryFr.winfo_width()/9))
        self.SaludT.pack(anchor=W,padx=20,pady=10)
        Temper=Label(self.scrollerFrame,text="Temperamento:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Temper.pack(anchor=W,padx=20,pady=10)
        self.TemperT=scrolledtext.ScrolledText(self.scrollerFrame,font=("Century Gothic",9),height=10,width=int(EntryFr.winfo_width()/9))
        self.TemperT.pack(anchor=W,padx=20,pady=10)
        Foto=Label(self.scrollerFrame,text="Foto (enviar un link al recurso .jpg de una página web)",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Foto.pack(anchor=W,padx=20,pady=10)
        Foto1=Label(self.scrollerFrame,text="Nota: (sólo se mostrará si es un link disponible para descarga):",fg="#388087",bg="#badfe7",font=("lucida sans unicode",9,"underline"))
        Foto1.pack(anchor=W,padx=20)
        self.FotoEntry=Entry(self.scrollerFrame,width=int(EntryFr.winfo_width()/9),font=("Century Gothic",9))
        self.FotoEntry.pack(anchor=W,padx=20)
        self.FotoEntry.update()
        PreviewB=Button(self.scrollerFrame,text="Preview de foto",bg="#6fb3b8",font=("Century Gothic",9,"bold"),height=2)
        PreviewB.pack(anchor=W,side=LEFT,pady=10,padx=20)

        PreviewB.bind("<Button>",lambda event: self.getPicPrev(self.FotoEntry.get()))
        self.canvasPr=Canvas(self.scrollerFrame,width=120,height=120)
        self.canvasPr.pack(anchor=W,side=LEFT,pady=10,padx=20)

        

        ButtonSend=Button(self,text="Mandar Entrada",bg="#6fb3b8",font=("lucida sans unicode",9,"bold"),height=2)
        ButtonSend.pack(anchor=S,pady=20)
        ButtonSend.bind("<Button>",lambda event: self.enviar(self.TitleEntry.get(),self.DescT.get('1.0', 'end-1c'),self.HistT.get('1.0', 'end-1c'),self.SaludT.get('1.0', 'end-1c'),self.TemperT.get('1.0', 'end-1c'),self.FotoEntry.get()))
    
    def enviar(self,titulo,desc,hist,sal,temper,foto):
        if titulo=='' or desc=='' or hist=='' or sal=='' or temper=='' or foto=='': 
            messagebox.showwarning("Precaución","Todos los campos deben estar llenados")
        else:
            conn=mysql.connector.connect(host="127.0.0.1",username="nicky",password="Hopeinthegalaxy",database="wikican")
            cursor=conn.cursor()
            cursor.execute("insert into dogbreeds(titulo,descripcion,historia,salud,temperamento,foto) values(%s,%s,%s,%s,%s,%s)",(titulo,desc,hist,sal,temper,foto))
            conn.commit()
            cursor.close()
            self.destroy()
            obj=Web(root)
            

    def getPicPrev(self,entryurl):
        urllib.request.urlretrieve(
            entryurl,
            "imagetemp/gfg.jpg")  
        img = ImageTk.PhotoImage(Image.open(os.getcwd()+"\imagetemp\gfg.jpg").resize((120,120)))  
        self.img=img
        self.canvasPr.create_image(0, 0, anchor=NW, image=img) 

# Pantalla de verificación de cuenta
class Ilog(Toplevel):
    numberSw=0
    def __init__(self,main,num,rowBreed,photoBreed):
        self.numberSw=num
        self.breedR=rowBreed
        self.breedPh=photoBreed
        Toplevel.__init__(self)
        self.update()
        self.resizable(0,0)
        self.geometry("500x350+{}+0".format(int(self.winfo_screenwidth()/2 - self.winfo_reqwidth()/2)))
        self.grab_set()
        bgLog=Frame(self,bd=5,relief=RIDGE,bg="#badfe7")
        bgLog.pack(fill=BOTH,expand=True)
        title=Label(bgLog,text="Confirma tu cuenta en WikiCan",fg="#388087",bg="#badfe7",font=("lucida sans unicode",15,"bold"))
        title.pack(anchor=N,fill=X,pady=10)
        title=Label(bgLog,text="(Procedimiento necesario en cada operación por motivos de seguridad)",fg="#388087",bg="#badfe7",font=("Century Gothic",9,"bold"))
        title.pack(anchor=N,fill=X,pady=10)
        CloseFrame=Frame(bgLog,bd=5,relief=RIDGE,bg="#c2edce")
        CloseFrame.pack(anchor=CENTER,fill=BOTH,expand=True,padx=70)

        # Ingreso del username y password
        User=Label(CloseFrame,text="Usuario:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",12,"underline"))
        User.pack(anchor=W,padx=30,pady=10)
        CloseFrame.update()
        self.UserEntry=Entry(CloseFrame,width=int(CloseFrame.winfo_width()/8),font=("Century Gothic",9))
        self.UserEntry.pack(anchor=W,padx=30)
        self.UserEntry.update()
        Pass=Label(CloseFrame,text="Contraseña:",fg="#388087",bg="#badfe7",font=("lucida sans unicode",12,"underline"))
        Pass.pack(anchor=W,padx=30,pady=10)
        CloseFrame.update()
        self.PassEntry=Entry(CloseFrame,show="*",width=int(CloseFrame.winfo_width()/8),font=("Century Gothic",9))
        self.PassEntry.pack(anchor=W,padx=30)
        self.PassEntry.update()
        SendButton=Button(bgLog,text="Iniciar conexión",bg="#6fb3b8",font=("lucida sans unicode",9,"bold"),height=2)
        SendButton.pack(anchor=S,pady=20)
        SendButton.bind("<Button>",lambda event: self.verifyUser(self.UserEntry.get(),self.PassEntry.get()))

    def verifyUser(self,user,password):
        conn=mysql.connector.connect(host="127.0.0.1",username="nicky",password="Hopeinthegalaxy",database="wikican")
        cursor=conn.cursor()
        select="select * from editors where username= %(user)s && password= %(password)s"
        cursor.execute(select,{'user':user,'password':password})
        rows=cursor.fetchall() 
        
        if len(rows)==0:
            messagebox.showwarning("Precaución","Su contraseña o nombre de usuario son incorrectos o inexistentes")
        else:
            self.indU=rows[0][0]
            self.callWin()
            self.destroy()

    def callWin(self):
        if self.numberSw==0:
            self.window =IUpdateBreed(self)
        else:
            self.window=IEditBreed(self,self.breedR,self.breedPh,self.indU)


# Pantalla principal de WikiCan
class Web:
    def __init__(self, root):
        self.root=root
        self.root.title("WikiCan")
        windowWidthRoot = self.root.winfo_reqwidth()
        positionRight = int(root.winfo_screenwidth()/2 - windowWidthRoot/2)

        self.root.geometry("1300x680+{}+0".format(positionRight-550))
        self.root.resizable(0,0)
        self.root.configure(background="#f6f6f2")
        lblTitle=Label(self.root,bd=5,relief=RIDGE,text="WikiCan: Sobre y para cada raza de can",fg="#388087",bg="#badfe7",font=("lucida sans unicode",30,"bold"))
        lblTitle.pack(side=TOP,anchor=CENTER,fill=X)

        # ========================DataFrame=================================

        Dataframe=Frame(self.root,bd=5,relief=RIDGE,bg="#badfe7")
        Dataframe.place(x=0,y=70,width=1300,height=490)

        # ======================ScrollDB: El scrolling de razas de perros en la BD====================================

        WikiFrame=LabelFrame(Dataframe,relief=RIDGE,bd=5,bg="#badfe7",font=("lucida sans unicode",12,"bold"),text="Razas de Perros")
        WikiFrame.place(x=10,y=10,width=500,height=450)
        
        canvasScroll=Canvas(WikiFrame,bg="#f6f6f2")
        WikiFrame.update()
        self.setWiki(WikiFrame.winfo_width()-455)
        scroller=Scrollbar(WikiFrame,orient="vertical",command=canvasScroll.yview)
        self.scrollerFrame=Frame(canvasScroll)

        self.scrollerFrame.bind(
            "<Configure>",
            lambda e: canvasScroll.configure(
                scrollregion=canvasScroll.bbox("all")
            )
           
        )

        canvasScroll.create_window((0,0), window=self.scrollerFrame, anchor="nw")
        canvasScroll.configure(yscrollcommand=scroller.set)
        canvasScroll.pack(side="left",fill="both",expand=True)
        scroller.pack(side="right",fill="y")


        # ================================Pantalla donde se muestra la entrada de WikiCan============================
        self.infoFrame=LabelFrame(Dataframe,bd=5,relief=RIDGE,bg="#badfe7",font=("lucida sans unicode",12,"bold"),text="Información")
        self.infoFrame.place(x=550,y=10,width=710,height=450)
        
        canvasScroll2=Canvas(self.infoFrame,bg="#c2edce")
        scroller2=Scrollbar(self.infoFrame,orient="vertical",command=canvasScroll2.yview)
        self.infoFrame.update()
        self.infoFrameS=self.infoFrame.winfo_width()-455
        self.scrollerFrame2=Frame(canvasScroll2,bg="#c2edce")

        self.scrollerFrame2.bind(
            "<Configure>",
            lambda e: canvasScroll2.configure(
                scrollregion=canvasScroll2.bbox("all")
            )  
        )

        canvasScroll2.create_window((0,0), window=self.scrollerFrame2, anchor="nw")
        canvasScroll2.configure(yscrollcommand=scroller2.set)
        canvasScroll2.pack(side="left",fill="both",expand=True)
        scroller2.pack(side="right",fill="y")
        # =====================================Botones de ingreso de entradas, búsqueda de entradas y creación de cuentas=======================================

        ButtonLogframe=Frame(self.root,bd=5,relief=RIDGE,bg="#badfe7")
        ButtonLogframe.place(x=0,y=562,width=1300,height=115)

        UpgradeButton=Button(ButtonLogframe,bg="#6fb3b8",text="Subir una raza de canes en la página!",font=("lucida sans unicode",9,"bold"),height=2)
        UpgradeButton.bind("<Button>",lambda event: self.callWin(0,None,None))
        UpgradeButton.pack(side=LEFT)

        UserButton=Button(ButtonLogframe,bg="#6fb3b8",text="Registrate para aportar a WikiCan!",font=("lucida sans unicode",9,"bold"),height=2)
        UserButton.bind("<Button>",lambda event: self.calluserW())
        UserButton.pack(side=RIGHT)

        ButtonLogframe.update()



        SearchFr=Frame(ButtonLogframe,relief=RIDGE,bg="#c2edce")
        SearchFr.place(x=270,y=0,width=770,height=105)

        TitleSearch=Label(SearchFr,text="Busca tu entrada favorita de razas caninas aqui!",bg="#c2edce",fg="#388087",font=("lucida sans unicode",20,"bold"))
        TitleSearch.pack(side=TOP)
        SearchFr.update()
        
        self.SearchText=Entry(SearchFr,font=("Century Gothic",9),width=math.ceil(SearchFr.winfo_width()/20))
        self.SearchText.pack(side=LEFT,padx=30)
        self.SearchText.update()
        self.SearchText.bind("<KeyRelease>",lambda event: self.check())
        

        self.listSearch=Listbox(SearchFr,width=200)
        self.listSearch.pack(side=RIGHT,padx=100)
        self.listSearch.bind("<<ListboxSelect>>",lambda event:self.checkSel(self.listSearch.get(ACTIVE)))

        self.initalize()

        #para realizar el buscador
        conn1=mysql.connector.connect(host="127.0.0.1",username="nicky",password="Hopeinthegalaxy",database="wikican")
        cursor1=conn1.cursor()
        select1="select titulo from dogbreeds order by titulo desc"
        cursor1.execute(select1)
        
        rows=cursor1.fetchall()
        for num in range(len(rows)):
            if os.path.exists('images/image-{}.jpg'.format(num)):
                os.remove('images/image-{}.jpg'.format(num))
        for item in rows:
            
            self.dataIList.append(item[0])
        
        self.start(self.dataIList)
        self.iB()
    
        

    attributes=[]
    photos=[]
    img=[]
    paths=[]
    buttonsList=[]
    columnSaver=[]
    Infoframes=[]
    titlef=[]
    descf=[]
    dataList=[]
    dataIList=[]

    wikiSize=0

    def initalize(self):
        self.attributes=[]
        self.photos=[]
        self.img=[]
        self.paths=[]
        self.buttonsList=[]
        self.columnSaver=[]
        self.Infoframes=[]
        self.titlef=[]
        self.descf=[]
        self.dataList=[]
        self.dataIList=[]

    # Mostrar los titulos de las entradas disponibles (según busqueda)    
    def checkSel(self,text):
        conn=mysql.connector.connect(host="127.0.0.1",username="nicky",password="Hopeinthegalaxy",database="wikican")
        cursor=conn.cursor()
        select="select titulo,foto from dogbreeds where titulo= %(title)s"
        cursor.execute(select,{'title':text})
        rows=cursor.fetchall()
        for ip in rows:
            indIm=self.photos.index(ip[1])
            path="\images\image-{}.jpg".format(indIm)
            self.show(ip[0],path)

    # Interacción de la busqueda de entradas según el Entry
    def check(self):
        type=self.SearchText.get()
        if type=='':
            self.dataList=self.dataIList
        else:
            self.dataList=[]
            for item in self.attributes:
                if type.lower() in item.lower():
                    self.dataList.append(item)
        self.start(self.dataList)        
    
    # Inicializar la lista
    def start(self,list):
        self.listSearch.delete(0,END)
        for it in list:
            self.listSearch.insert(0,it)

    # Destruyendo la ventana de información de cada entrada al traspasar a otra
    def getRid(self):
        for widgets in self.scrollerFrame2.winfo_children():
            widgets.destroy()
        self.Infoframes.clear()
        self.titlef.clear()
        self.descf.clear()


    # Mostrando la entrada y sus descripciones
    def show(self,name,photo):
        conn=mysql.connector.connect(host="127.0.0.1",username="nicky",password="Hopeinthegalaxy",database="wikican")
        cursor=conn.cursor()
        select="select * from dogbreeds where titulo= %(title)s"
        cursor.execute(select,{'title':name})
        rows=cursor.fetchall()
        desc=cursor.description

        self.getRid()

        self.scrollerFrame2.update()
        TitAndEdit=Frame(self.scrollerFrame2,width=self.scrollerFrame2.winfo_width(),relief=RIDGE,bg="blue")
        TitAndEdit.pack(fill=X)
        Title=Label(TitAndEdit,bd=5,width=21,relief=RIDGE,fg="#437fc7",bg="#6daffe",font=("lucida sans unicode",30,"bold"),text=rows[0][1])
        Title.pack(side=LEFT,fill=BOTH)
        canvas = Canvas(TitAndEdit, height = 150,bg="#388087")  
        canvas.pack(side=RIGHT,fill=BOTH)  
        imgae=ImageTk.PhotoImage(Image.open(os.getcwd()+photo).resize((150,150)))
        self.imga=imgae
        canvas.create_image(0, 0, anchor=NW, image=imgae) 

        
        for i in range(5):
            if i<4:
                self.Infoframes.append(Frame(self.scrollerFrame2))
                self.Infoframes[i].pack(side=LEFT)
                textTit=desc[i+2][0]
                textTit=textTit.capitalize()+":"
                self.scrollerFrame2.update()
                self.titlef.append(Label(self.Infoframes[0],width=15,text=textTit,fg="#388087",font=("lucida sans unicode",30,"bold")))
                self.titlef[i].configure(anchor=W)
                self.titlef[i].pack()
                Fact=rows[0][2+i]
                rowSiz=((len(Fact)/100))+1
                self.descf.append(Text(self.Infoframes[0],bg="#c2edce",width=97,font=("Century Gothic",10),height=(math.ceil(rowSiz))))
                self.descf[i].insert(END,rows[0][2+i])
                self.descf[i].pack(anchor=W)
            else:
                self.Infoframes.append(Frame(self.scrollerFrame2))
                self.Infoframes[i].pack(side=LEFT)
                Buttone=Button(self.Infoframes[0],text="Edita esta entrada!",bg="#6fb3b8",font=("lucida sans unicode",9,"bold"),width=84)
                Buttone.pack(anchor=W)
                Buttone.bind("<Button>",lambda event:self.callWin(1,rows,photo))
        
    # Seteando el width de los botones
    def setWiki(self,inte):
        self.wikiSize=inte

    # Inicialiando la lista scrollable de botones e imagenes de las razas de perros
    def iB(self):
        conn=mysql.connector.connect(host="127.0.0.1",username="nicky",password="Hopeinthegalaxy",database="wikican")
        cursor=conn.cursor()
        cursor.execute("select titulo,foto from dogbreeds order by titulo")
        rows=cursor.fetchall()
       
        for i in rows:
            self.attributes.append(i[0])
            self.photos.append(i[1])

        FILE_PATH='images/'   
        for i in range(len(self.photos)):
          self.url_to_jpg(i,self.photos[i],FILE_PATH)

        for i in range(len(self.attributes)):
           pathe="\images\image-{}.jpg".format(i)
           self.paths.append(pathe)
           frame=Frame(self.scrollerFrame,height=3,width=100,bg="#c2edce")
           frame.pack()
           canvas = Canvas(frame,width=100, height = 100,bg="#388087")  
           canvas.pack(side=LEFT)  
           self.img.append(ImageTk.PhotoImage(Image.open(os.getcwd()+pathe).resize((100,100))))
           self.img[i]=self.img[i]
           canvas.create_image(0, 0, anchor=NW, image=self.img[i]) 
           frame.update()
           self.buttonsList.append(Button(frame,width=self.wikiSize-10,height=3,bg="#6fb3b8",text=self.attributes[i],font=("lucida sans unicode",12,"bold"),command=lambda c=i: self.show(self.buttonsList[c].cget("text"),self.paths[c])))
           self.buttonsList[i].pack(side=RIGHT)

        conn.commit()
        conn.close()
    
    # Importando los url a imagenes según el orden
    def url_to_jpg(self,i,url,filepath):
        filename= 'image-{}.jpg'.format(i)
        full_path ='{}{}'.format(filepath,filename)
        urllib.request.urlretrieve(url,full_path)

    def calluserW(self):
       self.window=IUser(self)
    # Llamando a la ventana de logging
    def callWin(self,num,list,photo):
       self.window =Ilog(self,num,list,photo)


root=Tk()
ob=Web(root)
root.mainloop()