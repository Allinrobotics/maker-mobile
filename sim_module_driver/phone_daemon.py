#!/usr/local/bin/python
import serial   
import os, time, sys, stat 
import RPi.GPIO as GPIO
import mmap
import struct
import Tkinter as tk
import threading
from datetime import datetime


class App(threading.Thread):

    def __init__(self, master=None):
        threading.Thread.__init__(self)
        self.daemon=True
        self.start()
        self.port=master
        self.answer_call=0

    def callback(self):
        if(self.answer_call == 0):
            self.root.destroy()
        

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        self.root.title("Llamada entrante...")
        msg = tk.Message(self.root, text='Llamada entrante...')
        msg.pack()

        w = 400 # width for the Tk root
        h = 150 # height for the Tk root

        # get screen width and height
        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.after(20000, self.callback)

        self.button = tk.Button(self.root, text="Llamar", width=15, height=5, wraplength=0, command=self.llamar)
        self.button.pack()
        self.button.place(x=10, y=50)
        self.button.configure(background='green')
        self.button2 = tk.Button(self.root, text="Colgar", width=15, height=5, wraplength=0, command=self.colgar)
        self.button2.pack()
        self.button2.place(x=250, y=50)
        self.button2.configure(background='red')

        self.root.mainloop()

        self.root.quit()

    def colgar(self):
        self.port.write('ATH'+'\r\n') 
        time.sleep(0.5)
        print("colgar")
        self.answer_call=0
        self.callback()

    def llamar(self):
        print("hola")
        self.port.write('ATA'+'\r\n')
        self.answer_call=1


class Phone():

    def __init__(self):
        self.power = 0
        # Enable Serial Communication
        self.port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=5)
        self.x = 0
        

    def power_on_phone(self):
        #seting up gpio ping
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.OUT)

        #counter and triger for power up
        count = 3
        
        #define filters for wake up message
        line = ""
        new_line = "\r\n"
        ok_answer = "OK\r\n"

        #here check if power is set to false if it is true try to  power on
        while self.power==0:
            #try to connect "cont" times
            self.port.write('AT'+'\r\n')
            time.sleep(0.5)

            cmgs = self.port.readline()
            
            #filtering message loking for a clear answer
            if (cmgs != line and cmgs != new_line):
                if cmgs == ok_answer:
                    self.power = 1

            #try to wake up sim_module
            if count == 0:
                #turn on pin
                GPIO.output(12, 1)
                time.sleep(3)

                #turn off pin
                GPIO.output(12, 0)
                time.sleep(10)
                count = 20
                
            count -= 1
            print (count)


    def setting_up(self):

        # Transmitting AT Commands to the Modem
        # '\r\n' indicates the Enter key
        if self.power == 1:

            self.port.write('AT'+'\r\n')
            time.sleep(0.5)

            self.port.write('AT+CLVL=50'+'\r\n')
            time.sleep(0.5)

            self.port.write('AT+CLIP=1'+'\r\n')
            time.sleep(0.5)

            self.port.write('AT+CMGF=1'+'\r\n')
            time.sleep(0.5)

            self.port.write('AT+CNMI=2,2,0,0,0'+'\r\n')
            time.sleep(0.5)
        

    def reading(self):

        global buf, s

        #define filters for wake up message
        line = ""
        new_line = "\r\n"
        ok_answer = "OK\r\n"
        error_answer=("ERROR\r\n")
        answer_call=0
        ring=0
        app = list()

        try:
            while True:
                cmgs = self.port.readline()
                new_s = struct.unpack('15s', buf[1:16])
                ringtimefinal = datetime.now()
                        
                if (ring == 1):
                    tiempo = ringtimefinal - ringtimeini # Devuelve un objeto timedelta
                    segundos = tiempo.seconds
                    if (segundos >= 5):
                        ring = 0

                if  s!=new_s:
                    s = new_s
                    self.port.write('%s'% s +'\r\n')                    
                
                if cmgs!="\r\n":
                    #filtering message loking for a clear answer
                    if (cmgs != line and cmgs != new_line):
                        print (cmgs)

                        if cmgs == ok_answer:
                            print("Todo ok")
                            
                        if cmgs == error_answer:
                            print("Hubo un error")

                        if cmgs == "RING\r\n":
                            ringtimeini = datetime.now()
                            print("Llamada entrante")

                            if(ring == 0):
                                ring = 1
                                app.append(App(self.port))
                                

                        if (cmgs == "NO CARRIER\r\n"):
                            print("Llamada terminada")
                            ring = 0
                            self.port.write('ATH'+'\r\n') 
                            time.sleep(0.5)
                            answer_call =0

                            

        except KeyboardInterrupt, e:

            logging.info("Stopping...")


if __name__ == '__main__':

    # Open the file for reading
    fd = os.open('/tmp/mmaphone', os.O_CREAT | os.O_TRUNC | os.O_RDWR)

    # Zero out the file to insure it's the right size
    assert os.write(fd, '\x00' * mmap.PAGESIZE) == mmap.PAGESIZE

    # Memory map the file
    buf = mmap.mmap(fd, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE)
                              
    os.chmod("/tmp/mmaphone", stat.S_IRWXO|stat.S_IRWXO|stat.S_IRWXO) 

    s = None

    p = Phone()
    p.power_on_phone()
    p.setting_up()
    p.reading()
