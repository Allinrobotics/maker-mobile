#!/usr/bin/env python3

import ctypes
import mmap
import os
import time
from tkinter import *


class App:

    def __init__(self, master):

        master.title("Telefono")
        master.resizable(1,1)
        master.geometry("%dx%d%+d%+d"%(480, 800, 0, 0))

        frame = Frame(master, height=800, width=480)
        frame.pack_propagate(0) # don't shrink
        frame.pack()
        self.phone_num=""
	#self.cont=0
        h = 5
        w = 10
        #columns
        cols = [50, 180, 310]
        #rows
        rows = [300, 400, 500, 600]

        #entry text
        self.e = Entry(master)
        self.e.pack()
        
        self.e.place(x= 50, width=370, height=150)
        self.e.focus_set()


        self.delete = Button(
            frame, text="DEL", width=5, height=h, 
            wraplength=1, command=self.delete)
        self.delete.pack()
        self.delete.place(x=50, y=150)


        self.button = Button(
            frame, text="QUIT", width=w, height=h, 
            wraplength=1, command=self.quit) #frame.quit)

        self.button.pack()
        self.button.place(x=cols[2], y=rows[3])

        self.call = Button(
            frame, text="CALL", width=w, height=h,
             wraplength=1, command=self.call)

        self.call.pack()
        self.call.place(x=cols[0], y=rows[3])

        self.one = Button(
            frame, text="1", width=w, height=h, 
            wraplength=1, command=self.one)

        self.one.pack()
        self.one.place(x=cols[0], y=rows[0])

        self.two = Button(
            frame, text="2", width=w, height=h, 
            wraplength=1, command=self.two)

        self.two.pack()
        self.two.place(x=cols[1], y=rows[0])

        self.three = Button(
            frame, text="3", width=w, height=h, 
            wraplength=1, command=self.three)

        self.three.pack()
        self.three.place(x=cols[2], y=rows[0])

        self.four = Button(
            frame, text="4", width=w, height=h, 
            wraplength=1, command=self.four)

        self.four.pack()
        self.four.place(x=cols[0], y=rows[1])

        self.five = Button(
            frame, text="5", width=w, height=h, 
            wraplength=1, command=self.five)

        self.five.pack()
        self.five.place(x=cols[1], y=rows[1])

        self.six = Button(
            frame, text="6", width=w, height=h, 
            wraplength=1, command=self.six)

        self.six.pack()
        self.six.place(x=cols[2], y=rows[1])

        self.seven = Button(
            frame, text="7",  width=w, height=h, 
            wraplength=1, command=self.seven)

        self.seven.pack()
        self.seven.place(x=cols[0], y=rows[2])

        self.eigth = Button(
            frame, text="8",  width=w, height=h, 
            wraplength=1, command=self.eigth)

        self.eigth.pack()
        self.eigth.place(x=cols[1], y=rows[2])

        self.nine = Button(
            frame, text="9",  width=w, height=h, 
            wraplength=1, command=self.nine)

        self.nine.pack()
        self.nine.place(x=cols[2], y=rows[2])

        self.cero = Button(
            frame, text="0",  width=w, height=h, 
            wraplength=1, command=self.cero)

        self.cero.pack()
        self.cero.place(x=cols[1], y=rows[3])
        self.cont=0        

    def one(self):
        self.e.insert(END,"1")
        self.cont+=1

    def two(self):
        self.e.insert(END,"2")
        self.cont+=1

    def three(self):
        self.e.insert(END,"3")
        self.cont+=1

    def four(self):
        self.e.insert(END,"4")
        self.cont+=1

    def five(self):
        self.e.insert(END,"5")
        self.cont+=1

    def six(self):
        self.e.insert(END,"6")
        self.cont+=1

    def seven(self):
        self.e.insert(END,"7")
        self.cont+=1

    def eigth(self):
        self.e.insert(END,"8")
        self.cont+=1

    def nine(self):
        self.e.insert(END,"9")
        self.cont+=1

    def cero(self):
        self.e.insert(END,"0")
        self.cont+=1

    def call(self):
        global s
        a = self.e.get()
        #print("ATD" + a + ";")

        new_s = str("ATD" + a + ";")

        s.raw = bytes(new_s, 'UTF-8')
        print(new_s)
        time.sleep(5)

    def delete(self):
        print("del")
        self.e.delete(self.cont-1)
        if(self.cont > 0):
            self.cont-=1
        a = self.e.get()
        print(a)

    def quit(self):
        s.raw = bytes("ATH            ", 'UTF-8')
        time.sleep(5)
        
        

if __name__ == '__main__':

    # Open the file for reading
    fd = os.open('/tmp/mmaphone', os.O_RDWR)
    # Zero out the file to insure it's the right size
    assert os.write(fd, bytes('\x00', 'UTF-8') * mmap.PAGESIZE) == mmap.PAGESIZE

    # Memory map the file
    buf = mmap.mmap(fd, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE)

    # Now ceate a string containing 'foo' by first creating a c_char array
    s_type = ctypes.c_char * len('               ')

    # Now create the ctypes instance
    s = s_type.from_buffer(buf, 3)

    print ('First 10 bytes of memory mapping: %r' % buf[:10])

    root = Tk()

    app = App(root)

    root.mainloop()

    root.destroy() # optional; see description below
