from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFile
from allFunction import *
import binascii
import os

class Window(tk.Toplevel):
    def __init__(self, parent,title,geometry,**kwargs):
        super().__init__(parent)
        self.title(title)
        self.geometry(geometry)
        self.dictionary = {}
    def updtDict(self,type,item):
        if type == 'add':
            self.dictionary.update(item)
        if type == 'delete':
            self.dictionary[item].destroy()
            self.dictionary.pop(item)

    def addInput(self,type,name,*args,**kwargs):
        if type == 'Button':
            inp = Button(self,*args,**kwargs)
        if type == 'OptionMenu':
            inp = OptionMenu(self,*args,**kwargs)
        if type == 'Entry':
            inp = Entry(self,*args,**kwargs)
        if type == 'Scale':
            inp = Scale(self,*args,**kwargs)
        item = {name:inp}
        self.updtDict('add',item)
        #inp.pack()
    def addLabel(self,name,**kwargs):
        lab = Label(self,**kwargs)
        #lab.pack()
        item = {name:lab}
        self.updtDict('add',item)

    def packAll(self):
        for item in self.dictionary:
            self.dictionary[item].pack()

    def addGrid(self,name,**kwargs):
        self.dictionary[name].grid(**kwargs)

    def addImage(self,name,hexCompil,hexDecomp,hexSave):
        eCheck = False
        try:
            with open('mod.bmp', 'wb') as img:
                img.write(bytes.fromhex(hexCompil))
                img = ImageTk.PhotoImage(Image.open('mod.bmp'))
            self.dictionary[name].destroy()
            self.addLabel(name,image = img)
            self.dictionary[name].image = img
            self.dictionary[name].pack()
                # img.close()
        except:
            with open('mod.bmp', 'wb') as img:
                img.write(bytes.fromhex(hexDecomp[0] + hexSave + '00'))
                img = ImageTk.PhotoImage(Image.open('mod.bmp'))
            self.dictionary[name].destroy()
            self.addLabel(name, image=img)
            self.dictionary[name].image = img
            self.dictionary[name].pack()
                # img.close()
            eCheck = True
        if eCheck == True:
            hexDecomp[1] = hexSave

            warnFram = Toplevel()
            warnLab = Label(warnFram, text='Bad Input')
            warnLab.pack()

class App(tk.Tk):
    def __init__(self):
        global origPic
        global modiPic
        global origLabel
        global modiLabel
        global origCanvas
        global modiCanvas
        global hexDecomp
        global filename
        super().__init__()

        self.title('Controls')
        modiPic = Window(self,'Modified Picture','500x500')
        origPic = Window(self,'Original Picture','500x500')
        modiPic.addLabel('imLab')
        origPic.addLabel('imLab')

    def addButton(self,text,function):
        butt = Button(self, text = text, command = function)
        butt.pack()
        return
def loadImage():
    global origPic
    global modiPic
    global origLabel
    global modiLabel
    global origCanvas
    global modiCanvas
    global hexDecomp
    global filename


    filename = filedialog.askopenfilename(initialdir="/",title="Select a File",
                                          filetypes=(("png files","*.png*"),("all files","*.*")))

    try:
        img = Image.open(filename)
        try:
            r, g, b, a = img.split()
        except:
            r, g, b = img.split()
        img = Image.merge("RGB", (r, g, b))
        filename = os.path.splitext(filename)[0]+ 'mod' + '.bmp'
        img.save(filename)
        with open(filename, "rb") as infile:
            content = infile.read()
        hex_bytes = binascii.hexlify(content)
        hex_str = hex_bytes.decode('utf-8')
        hexDecomp = ["", ""]
        hexDecomp = [hex_str[0:12], hex_str[12:len(hex_str)]]
        img = ImageTk.PhotoImage(Image.open(filename))

        hexCompil = hexDecomp[0] + hexDecomp[1]
        hexSave = hexDecomp[1]
        modiPic.addImage('imLab',hexCompil,hexDecomp,hexSave)
        origPic.addImage('imLab',hexCompil,hexDecomp,hexSave)



    except:
        'xd'
    return

def replaceNum():
    global modiLabel
    global modiPic
    global hexDecomp
    global filename
    global hexSave

    okVar = IntVar()
    origHex = ''
    replHex = ''
    inputFrame = Window(app,'Replace Num','')
    inputFrame.addLabel('oBoxLab', text = 'Original Hex')
    inputFrame.addInput('Entry','origBox', width = 6,textvariable = origHex)
    inputFrame.addLabel('rBoxLab', text = 'Replaced Hex')
    inputFrame.addInput('Entry','replBox', width = 6,textvariable = replHex)
    inputFrame.addInput('Button','runButton',text = 'Run',command = lambda:okVar.set(1))
    inputFrame.packAll()
    inputFrame.wait_variable(okVar)
    echeck = False

    origHex = inputFrame.dictionary['origBox'].get()
    replHex = inputFrame.dictionary['replBox'].get()
    inputFrame.destroy()

    hexSave = hexDecomp[1]
    hexDecomp[1] = hexDecomp[1].replace(origHex, replHex)
    hexCompil = hexDecomp[0] + hexDecomp[1] + '00'
    modiPic.addImage('imLab',hexCompil,hexDecomp,hexSave)

    return

def copyPaste():
    global modiLabel
    global modiPic
    global hexDecomp
    global filename
    global hexSave

    okVar = IntVar()
    inputFrame = Window(app, 'Copy Paste','')

    startVar = DoubleVar()
    insertVar = DoubleVar()
    endVar = DoubleVar()

    inputFrame.addLabel('startLab',text = 'Starting Position')
    inputFrame.addInput('Scale','startScale',from_ = 0, to = len(hexDecomp[1]), orient = HORIZONTAL, variable = startVar)
    inputFrame.addLabel('endLab', text='Ending Position')
    inputFrame.addInput('Scale','endScale', from_=0, to=len(hexDecomp[1]), orient=HORIZONTAL, variable=endVar)
    inputFrame.addLabel('insertLab', text = 'Insertion Position')
    inputFrame.addInput('Scale','insertScale',from_=0, to=len(hexDecomp[1]), orient=HORIZONTAL, variable=insertVar)
    inputFrame.addInput('Button','runButton', text = 'Run',command = lambda: okVar.set(1))
    inputFrame.addInput('Entry','startBox',width =8,textvariable = startVar)
    inputFrame.addInput('Entry', 'endBox', width=8,textvariable = endVar)
    inputFrame.addInput('Entry', 'insertBox', width=8,textvariable = insertVar)

    inputFrame.addGrid('startLab',row = 0, columnspan = 2)
    inputFrame.addGrid('startScale',row = 1, column =0,ipady = 10)
    inputFrame.addGrid('startBox', row = 1,column = 1)

    inputFrame.addGrid('endLab',row = 2,columnspan = 2)
    inputFrame.addGrid('endScale',row = 3,column = 0,ipady = 10)
    inputFrame.addGrid('endBox',row = 3,column = 1)

    inputFrame.addGrid('insertLab', row=4, columnspan=2)
    inputFrame.addGrid('insertScale', row=5, column=0,ipady = 10)
    inputFrame.addGrid('insertBox', row=5, column=1)



    inputFrame.wait_variable(okVar)
    startPos = inputFrame.dictionary['startScale'].get()
    endPos = inputFrame.dictionary['endScale'].get()
    insertPos = inputFrame.dictionary['insertScale'].get()
    inputFrame.destroy()
    echeck = False

    hexSave = hexDecomp[1]
    hexGrab = hexDecomp[1][startVar:endVar]
    #hexDecomp[1][insertPos] = hexGrab
    hexDecomp[1] = hexDecomp[1][0:insertVar] + hexGrab + hexDecomp[1][insertPos:len(hexDecomp[1])]
    hexCompil = hexDecomp[0] + hexDecomp[1] + '00'
    modiPic.addImage('imLab',hexCompil,hexDecomp,hexSave)

    return

def deleFunc():
    global modiLabel
    global modiPic
    global hexDecomp
    global filename
    global hexSave

    okVar = IntVar()
    startPos = DoubleVar()
    endPos = DoubleVar()

    inputFrame = Window(app,'Delete Function','')
    inputFrame.addLabel('startLab',text = 'Starting Position')
    inputFrame.addInput('Scale','startScale',from_ = 0, to = len(hexDecomp[1]),orient=HORIZONTAL,variable = startPos)
    inputFrame.addLabel('endLab', text = 'Ending Position')
    inputFrame.addInput('Scale','endScale',from_ = 0, to = len(hexDecomp[1]),orient=HORIZONTAL,variable = endPos)
    inputFrame.addInput('Button','runButton',text = 'Run',command=lambda:okVar.set(1))
    inputFrame.packAll()
    inputFrame.wait_variable(okVar)

    startPos = inputFrame.dictionary['startScale'].get()
    endPos = inputFrame.dictionary['endScale'].get()

    echeck = False
    inputFrame.destroy()

    hexSave = hexDecomp[1]
    hexGrab = hexDecomp[1][startPos:endPos]
    #hexDecomp[1][insertPos] = hexGrab
    hexDecomp[1] = hexDecomp[1].replace(hexGrab,'')
    hexCompil = hexDecomp[0] + hexDecomp[1] + '00'

    modiPic.addImage('imLab',hexCompil,hexDecomp,hexSave)

    return
def undoFunc():
    global modiLabel
    global modiPic
    global hexDecomp
    global filename
    global hexSave
    hexDecomp[1] = hexSave
    hexCompil = hexDecomp[0] + hexSave + '00'

    modiPic.addImage('imLab',hexCompil,hexDecomp,hexSave)
    return


def marchFunc():
    global modiLabel
    global modiPic
    global hexDecomp
    global filename
    global hexSave
    global app
    global inputFrame

    options = ["Delete", "Hex Insert", "Copy Paste"]
    inputFrame = Window(app,'March Options','')
    variable = StringVar(inputFrame)
    variable.set("")
    inputFrame.addLabel('optionLabel',text = 'Setting')
    inputFrame.addInput('OptionMenu','marchOption',variable, *options, command = marchUpdate)
    inputFrame.addGrid('optionLabel',row = 0,column = 0)
    inputFrame.addGrid('marchOption',row = 0,column = 1)

    return
def marchUpdate(variable):
    global inputFrame
    global hexDecomp
    global okVar

    itemList = ['widthLab','widthScale','intLab','interScale','runButton',
                'hexLab','hexBox','startLab','startScale','endLab','endScale',
                'interBox', 'widthBox']
    for i in itemList:
        if i in inputFrame.dictionary:
            inputFrame.updtDict('delete',i)
    if variable == "Delete":

        okVar = IntVar()
        widthVar = DoubleVar()
        interVar = DoubleVar()

        inputFrame.addLabel('widthLab',text = 'Width')
        inputFrame.addInput('Scale', 'widthScale', from_=0, to=len(hexDecomp[1]), orient=HORIZONTAL,
                            variable=widthVar)
        inputFrame.addInput('Entry','widthBox', width = 8,textvariable = widthVar)
        inputFrame.addLabel('intLab', text = 'Interval')
        inputFrame.addInput('Scale', 'interScale', from_=0, to=len(hexDecomp[1]), orient=HORIZONTAL,
                            variable=interVar)
        inputFrame.addInput('Entry', 'interBox', width = 8,textvariable = interVar)
        inputFrame.addInput('Button', 'runButton', text='Run', command=lambda: okVar.set(1))

        inputFrame.addGrid('widthLab',row = 1)
        inputFrame.addGrid('widthScale',row = 1, column = 1,ipady = 10)
        inputFrame.addGrid('widthBox',row = 1, column = 2)

        inputFrame.addGrid('intLab',row = 2,column = 0)
        inputFrame.addGrid('interScale', row = 2, column = 1,ipady = 10)
        inputFrame.addGrid('interBox',row = 2, column = 2)
        inputFrame.addGrid('runButton', row = 3, column = 1)
        inputFrame.wait_variable(okVar)

        widthVar = inputFrame.dictionary['widthScale'].get()
        interVar = inputFrame.dictionary['interBox'].get()
        inputFrame.destroy()
        dMarch(widthVar,interVar)
    if variable == "Hex Insert":
        widthVar = DoubleVar()
        interVar = DoubleVar()

        inputFrame.addLabel('hexLab', text='Hex Characters')
        inputFrame.addInput('Entry', 'hexBox', width = 8)
        inputFrame.addLabel('intLab', text='Interval')
        inputFrame.addInput('Scale', 'interScale', from_=0, to=len(hexDecomp[1]), orient=HORIZONTAL, variable=interVar)
        inputFrame.addInput('Entry', 'interBox', width=8,textvariable = interVar)
        inputFrame.addInput('Button', 'runButton', text='Run', command=lambda: okVar.set(1))

        inputFrame.addGrid('hexLab',row = 1)
        inputFrame.addGrid('hexBox',row = 1, column = 1)

        inputFrame.addGrid('intLab',row = 2,column = 0)
        inputFrame.addGrid('interScale', row = 2, column = 1,ipady = 10)
        inputFrame.addGrid('interBox',row = 2, column = 2)
        inputFrame.addGrid('runButton', row = 3, column = 1)
    if variable == "Copy Paste":

        startVar = DoubleVar()
        interVar = DoubleVar()
        endVar = DoubleVar()

        inputFrame.addLabel('startLab', text='Starting Position')
        inputFrame.addInput('Scale', 'startScale', from_=0, to=len(hexDecomp[1]), orient=HORIZONTAL, variable=startVar)
        inputFrame.addInput('Entry', 'startBox', width=8, textvariable=startVar)
        inputFrame.addLabel('endLab', text='Ending Position')
        inputFrame.addInput('Scale', 'endScale', from_=0, to=len(hexDecomp[1]), orient=HORIZONTAL, variable=endVar)
        inputFrame.addInput('Entry', 'endBox', width=8, textvariable=endVar)
        inputFrame.addLabel('interLab', text='Interval')
        inputFrame.addInput('Scale', 'interScale', from_=0, to=len(hexDecomp[1]), orient=HORIZONTAL,
                            variable=interVar)
        inputFrame.addInput('Entry', 'interBox', width=8, textvariable=interVar)
        inputFrame.addInput('Button', 'runButton', text='Run', command=lambda: okVar.set(1))

        inputFrame.addGrid('startLab',row = 1)
        inputFrame.addGrid('startScale',row = 1, column = 1,ipady = 10)
        inputFrame.addGrid('startBox',row = 1, column = 2)

        inputFrame.addGrid('endLab',row = 2,column = 0)
        inputFrame.addGrid('endScale', row = 2, column = 1,ipady = 10)
        inputFrame.addGrid('endBox',row = 2, column = 2)

        inputFrame.addGrid('interLab', row=3, column=0)
        inputFrame.addGrid('interScale', row=3, column=1, ipady=10)
        inputFrame.addGrid('interBox', row=3, column=2)

        inputFrame.addGrid('runButton', row = 4, column = 1)

    return

def dMarch(widthVar,interVar):
    global modiLabel
    global modiPic
    global hexDecomp
    global filename
    global hexSave

    hexSave = hexDecomp[1]
    tempHex = ''

    iterCount = round(len(hexSave)/int(interVar))
    if iterCount > len(hexSave)/int(interVar):
        iterCount -= 1
    while widthVar*iterCount > len(hexSave)-20:
        iterCount -= 1
    print(iterCount)
    for i in range(1,iterCount):

        i = i*2
        #tempHex = tempHex + hexSave[20+(i-1)*widthVar:20+i*widthVar]
        tempHex = tempHex + hexSave[:20 + (i - 1) * widthVar]
        #print(tempHex)
        #print(i)
    hexCompil = hexDecomp[0]+tempHex+ hexSave[iterCount*widthVar:]+ '00'
    modiPic.addImage('imLab',hexCompil,hexDecomp,hexSave)


    return
def scatterFunc():
    global modiLabel
    global modiPic
    global hexDecomp
    global filename
    global hexSave

    with open('mod.bmp', 'wb') as img:
        img.write(bytes.fromhex(hexCompil))
        img = ImageTk.PhotoImage(Image.open('mod.bmp'))
    modiLabel.destroy()
    modiLabel = Label(modiPic, image=img)
    modiLabel.image = img
    modiLabel.pack()
    return


ImageFile.LOAD_TRUNCATED_IMAGES = True
app = App()
app.addButton('Load Image',loadImage)
app.addButton('Replace Hex',replaceNum)
app.addButton('Copy Paste Hex',copyPaste)
app.addButton('March',marchFunc)
app.addButton('Delete Hex',deleFunc)
app.addButton('Undo',undoFunc)


app.mainloop()
