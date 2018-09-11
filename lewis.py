from random import randint
import _thread
import time
from tkinter import *
from tkinter import messagebox
import copy

game = True

window = Tk()
window.title("Lewis V1.5")
window.geometry('400x400')

#Load all images
happy = PhotoImage(file='happy.png')
sad = PhotoImage(file='sad.png')
tired = PhotoImage(file='tired.png')
hungry = PhotoImage(file='hungry.png')
neutral = PhotoImage(file='neutral.png')
toPub = PhotoImage(file='left.png')
gooseBoss = PhotoImage(file='gooseBoss.png')
gooseDead = PhotoImage(file='gooseDead.png')
gooseWins = PhotoImage(file='gooseWins.png')

#Build the frames
frameTop = Frame(width=200, height=50)
frameTop.pack(side = TOP, fill="both", expand=False, padx=20, pady=0)

frameMiddle = Frame(width=200, height=200)
frameMiddle.pack(side = TOP, fill="both", expand=False, padx=20, pady=20)
imgLabel = Label(window, image = happy)
imgLabel.place(in_=frameMiddle, anchor="c", relx=.5, rely=.5)

frameBottom = Frame(width=200, height=50)
frameBottom.pack(side = BOTTOM, fill="both", expand=False, padx=20, pady=20)

lbl = Label(window, text="")
lb2 = Label(window, text="")
lb3 = Label(window, text="")

lbl.place(in_=frameTop, anchor="c", relx=.5, rely=.5)
lb2.place(in_=frameTop, anchor="c", relx=.5, rely=1)
lb3.place(in_=frameTop, anchor="c", relx=.5, rely=0.2)

#Set the default values
guy = {
    'name' : 'Lewis',
    'hungry' : True,
    'hunger' : 15.0,
    'entertainment' : 10.0,
    'health' : 5,
    'intoxication': 0.0,
    'tired' : False,
    'paused' : False,
    'battleEnabled' : True,
}

#Make a copy of the original values
og = guy.copy()

#Set all thresholds
hungerThresh = og['hunger'] - 3 # Hungry if hunger is original hunger value - 3
tiredThresh = 3.5 # Tired if value reaches 2.5
gooseThresh = 100 #Threshhold for starting gooe battle
beerThresh = 100 # If random number >= this then get a beer
beer = 3 # Number of beers
gooseHealth = 50 #Setting health of the goose battle
ogGooseHealth = 50

#List of actions Lewis can perform
actions = ['drinking beer', 'going bowling', 'moaning about Gary', 'praised the 1.5!']

def feed(stick):
    if stick['hungry'] == True:
        stick['hunger'] += (randint(1, 10)/10)
        res = stick['name'] + ' ate some food'
        if stick['hunger'] >= hungerThresh:
            stick['hungry'] = False
        if stick['hunger'] <= hungerThresh:
            imgLabel.configure(image = hungry)
        else:
            imgLabel.configure(image = neutral)
    else:
        #print(stick['name'] + ' is not hungry')
        res = stick['name'] + ' is not hungry'
    lb2.configure(text= res)
    printStats(stick)

def entertain(stick) :
    if stick['entertainment'] < 8:
        #print(stick['name'] + ' started ' + actions[randint(0,len(actions)-1)])
        stick['entertainment'] += (randint(1, 10)/10)
        res = stick['name'] + ' started ' + actions[randint(0,len(actions)-1)]
        if stick['entertainment'] <= tiredThresh:
            imgLabel.configure(image = tired)
        else:
            imgLabel.configure(image = neutral)
            stick['tired'] = False
    else:
        #print(stick['name'] + ' is not bored')
        res = stick['name'] + ' is not bored'
    lb2.configure(text= res)
    printStats(stick)
    
def giveBeer(stick):
    global beer
    if beer <= 0:
        lb2.configure(text='You don\'t have any beer!')
        return
        
    stick['hungry'] = og['hungry']
    stick['hunger'] = og['hunger']
    stick['entertainment'] = og['entertainment']
    stick['intoxication'] += 1
    stick['tired'] = og['tired']
    imgLabel.configure(image = happy)
    beer -= 1
    beerString = 'GIVE BEER (' + str(beer) + ')'
    beerBTN.configure(text=beerString)
    printStats(stick)

def fightGoose(stick):
    global gooseHealth
    gooseHealth -= (randint(1, 10)/10)
    gooseText = 'Goose Health: ' + str(round(gooseHealth, 1)) + '/' + str(ogGooseHealth)
    lb2.configure(text=gooseText)
    if(gooseHealth <= 0):
        winBattle(stick)
    
def runGoose(stick):
    lb2.configure(text='You can\'t run away!')
      
fightBTN = Button(window, text="Fight!", command= lambda: fightGoose(guy))
runBTN = Button(window, text="Run Away", command= lambda: runGoose(guy))

def gooseBattle(stick):
    global gooseHealth
    global ogGooseHealth
    stick['paused'] = True
    imgLabel.configure(image = gooseBoss)
    fightBTN.place(in_=frameBottom, anchor="c", width=100, relx=.2, rely=.0)
    runBTN.place(in_=frameBottom, anchor="c", width=100, relx=.8, rely=.0)

    feedBTN.config(state="disabled")
    entertainBTN.config(state="disabled")
    beerBTN.config(state="disabled")
    fightBTN.config(state="normal")
    runBTN.config(state="normal")
    
    gooseHealth = ogGooseHealth
    stick['health'] = og['health']

def winBattle(stick):
    stick['paused'] = False
    feedBTN.config(state="normal")
    entertainBTN.config(state="normal")
    beerBTN.config(state="normal")
    fightBTN.config(state="disabled")
    runBTN.config(state="disabled")
    lb2.configure(text="You beat the Goose in the pipes!")
    stick['health'] = og['health']
    #stick['battleEnabled'] = False
    lb3.configure(text="")
    imgLabel.configure(image = gooseDead)
    
def decVals(stick):
    global beer
    while(game == True):
        if(stick['paused'] == False):
            stick['entertainment'] -= round((randint(1, 10)/10), 1)
            stick['hunger'] -= round((randint(1, 10)/10), 1)
            if stick['hunger'] <= hungerThresh:
                lb2.configure(text='Lewis started to feel hungry!')
                stick['hungry'] = True
                imgLabel.configure(image = hungry)
            if stick['entertainment'] <= tiredThresh:
                lb2.configure(text='Lewis started to feel sleepy!')
                stick['tired'] = True
                imgLabel.configure(image = tired)
            if stick['hunger'] <= 0 or stick['entertainment'] <= 0:
                lb2.configure(text='Lewis is close to leaving!')
                imgLabel.configure(image = sad)
            if stick['hunger'] <= -1 or stick['entertainment'] <= -1:
                imgLabel.configure(image = toPub)
                dead()
            
            printStats(stick)
            if randint(1, 100) >= beerThresh:
                beer += 1
                beerString = 'GIVE BEER (' + str(beer) + ')'
                beerBTN.configure(text=beerString)
                lb2.configure(text='Lewis found a beer!')
            if(stick['battleEnabled'] == True):
                if randint(1, 100) >= gooseThresh:
                    gooseBattle(stick)
        time.sleep(randint(0,5))

def decBattleVals(stick):
    while(game == True):
        if(stick['paused'] == True):#If paused is true, the normal values are paused entering battle mode
            stick['health'] -= round((randint(1, 10)/10), 1)
            healthText = 'Lewis Health: ' + str(round(stick['health'], 1)) + '/' + str(og['health'])
            lb3.configure(text=healthText)
            if(stick['health'] <= 0):
                gooseWin()
        time.sleep(randint(0,5))        

def gooseWin():
    imgLabel.configure(image = gooseWins)
    messagebox.showerror("The Goose wins!","Unfortunately the Goose won.")
    dead()
        
def dead():
    imgLabel.configure(image = toPub)
    messagebox.showerror("Lewis felt neglected, it was SUPER EFFECTIVE!","You didn\'t look after Lewis. \nHe felt neglected and left to go to the pub, you loose.")
    window.destroy()
    
def printStats(stick):
    buff = []
    
    #buff.append(str(round(stick['entertainment']), 1) +  '/' + str(round(guy['entertainment']), 1))
    #buff.append(str(round(stick['hunger']), 1) + '/' + str(round(guy['hunger'])))
    
    buff.append( 'Hunger: ' + str(round(stick['hunger'], 1)) + '/' + str(og['hunger'])  + '    '  )
    buff.append( 'Entertainment: ' + str(round(stick['entertainment'], 1)) + '/' + str(og['entertainment']))
    
    
    #for k, v in stick.items():
    #    if type(v) == float:
    #        v = round(v,1)
    #    buff.append(k.capitalize() + ': ' + str(v) + '  ')
    bufferedString = ''.join(buff)
    #print(''.join(buff))
    lbl.configure(text= bufferedString)

#print('Welcome to StickyBoi')

_thread.start_new_thread(decVals, (guy , ))
_thread.start_new_thread(decBattleVals, (guy , ))

feedBTN = Button(window, text="Feed", command= lambda: feed(guy))
entertainBTN = Button(window, text="Entertain", command= lambda: entertain(guy))
beerBTN = Button(window, text="GIVE BEER (3)", command= lambda: giveBeer(guy))

feedBTN.place(in_=frameBottom, anchor="c", width=100, relx=.2, rely=.5)
entertainBTN.place(in_=frameBottom, anchor="c", width=100, relx=.8, rely=.5)
beerBTN.place(in_=frameBottom, anchor="c", width=100, relx=.5, rely=.5)

window.mainloop()