from math import *
from vector_math import *
import string
from tkinter import *
from cmu_112_graphics import *          # Taken from CMU 15-112 course website.


funcLib = {
    "cos" : cos,
    "sin" : sin,
    "sqrt" : sqrt,
    "ln" : log,
    "abs" : abs,
    'x' : "Var1",
    'y' : "Var2"
}


# Returns the index of e in a list L, or 99 if not found.
def find(L,e):
    if e in L:
        return L.index(e)
    else:
        return 99 
    

# Creates a graph class that will interpret strings.
class Graph(object):

    def __init__(self,name):
        self.name = name
    
    # Prints the equation of the graph in LaTeX font. Not yet implemented.
    def __repr__(self):
        return self.name
    
    def eval(self):
        raise NotImplementedError


class Function(Graph):
    def __init__(self,name):
        super().__init__(name)
        self.type = "Function"
        self.list = self.identifyInput(self.name)

    # Extracts the function.
    def eval(self,args):        
        newL = []
        for i,e in enumerate(self.list):
            if e in ["Var1","Var2","Var3"]:
                i = ["Var1","Var2","Var3"].index(e)
                newL.append(args[i])
            else:
                newL.append(e)
        return self.evalInput(newL)
    
    # Returns a list separating numbers, functions, operations.
    def identifyInput(self,s):
        if s == "":
            return []
        elif s in funcLib:
            return [funcLib[s]]
        elif s.isdigit():
            return [int(s)]
        elif s[0] in "(+-*/)":
            return [s[0]] + self.identifyInput(s[1:])
        else:
            endIndex = -1
            isNum = True if s[0].isdigit() else False
            for i,c in enumerate(s):
                if c in "(+-*/)" or c.isdigit() != isNum:
                    endIndex = i
                    break
            if endIndex == -1: return [None]
            return self.identifyInput(s[:endIndex]) + self.identifyInput(s[endIndex:])

    # Given a list that represents a mathematical expression, this recursively
    # evaluates that expression. This follows the order of operations. This 
    # returns None if the expression cannot be evaluated.
    def evalInput(self,L):
        try:
            if L[0] == None:
                return None
            if len(L) == 1:
                if isinstance(L[0],int) or isinstance(L[0],float):
                    return L[0]
                else:
                    return None
            else:
                funcIndex = -1
                for i in range(len(L)):
                    if L[i] in funcLib.values():
                        funcIndex = i
                        break
                if funcIndex != -1:
                    return self.evalFunc(L,funcIndex)
                elif ")" in L:
                    return self.evalParen(L)
                elif "*" in L or "/" in L:
                    return self.evalMulDiv(L)
                elif "+" in L or "-" in L:
                    return self.evalPlusMin(L)
        except:
            return

    # Evaluates a function in a given expression.
    def evalFunc(self,L,funcIndex):
        leftParen = funcIndex+1
        rightParen = None
        parenCounter = 0
        for i,e in enumerate(L[leftParen:]):
            if e == "(":
                parenCounter += 1
            elif e == ")":
                parenCounter -= 1
            if parenCounter == 0:
                rightParen = i + leftParen
                break
        if rightParen != None:
            left = L[:funcIndex]
            func = L[funcIndex](self.evalInput(L[leftParen+1:rightParen]))
            right = L[rightParen+1:]
            return self.evalInput(left + [func] + right)

    # Evaluates a parenthetical subexpression in a given expression.
    def evalParen(self,L):
        if "(" not in L:
            return None
        rightParen = find(L,")")
        leftParen = rightParen - find(L[:rightParen][::-1],"(") - 1
        parenExpr = self.evalInput(L[leftParen+1:rightParen])
        return self.evalInput(L[:leftParen] + [parenExpr] + L[rightParen+1:])

    # Evaluates multiplication and division in a given expression.
    def evalMulDiv(self,L):
        i = min(find(L,"*"), find(L,"/"))
        if L[i] == "*":
            prod = self.evalInput([L[i-1]]) * self.evalInput([L[i+1]])
            return self.evalInput(L[:i-1] + [prod] + L[i+2:])
        else:
            quot = self.evalInput([L[i-1]]) / self.evalInput([L[i+1]])
            return self.evalInput(L[:i-1] + [quot] + L[i+2:])
    
    # Evaluates addition and subtraction in a given expression.
    def evalPlusMin(self,L):
        i = min(find(L,"+"),find(L,"-"))
        if L[i] == "+":
            summ = self.evalInput([L[i-1]]) + self.evalInput([L[i+1]])
            return self.evalInput(L[:i-1] + [summ] + L[i+2:])
        else:
            diff = self.evalInput([L[i-1]]) - self.evalInput([L[i+1]])
            return self.evalInput(L[:i-1] + [diff] + L[i+2:])


# Creats a button class to easily manage the buttons.
class Button(object):
    def __init__(self,cx,cy,s,name,tgt,color,call):
        self.cx = cx
        self.cy = cy
        self.s = s
        self.name = name
        self.tgt = tgt
        self.color = color
        self.call = call
    
    # Returns true if point is "in" the button.
    def isPressed(self,point):
        x,y = point
        return (self.cx-self.s < x and
                self.cx+self.s > x and
                self.cy-self.s < y and
                self.cy+self.s > y)


# Creates the Grapher with a splash screen, help screen, and graph mode.
class Grapher(ModalApp):
    
    txtSize = 12

    def appStarted(self):
        self.splashMode = SplashMode()
        self.graphMode = GraphMode()
        self.helpMode = HelpMode()
        self.setActiveMode(self.splashMode)

# Draws a nice design. Any event will change the mode to Help Mode.
class SplashMode(Mode):

    def keyPressed(self,event):
        self.app.setActiveMode(self.app.helpMode)
    
    def mousePressed(self,event):
        self.app.setActiveMode(self.app.helpMode)

    # Modified from my submission on HW2.
    def redrawAll(self,canvas):
        canvas.create_rectangle(0,0,self.width,self.height,fill='black')
        a, b, c = -0.3, 0.4, 0
        def P(x,y,z):
            return ( self.width/2 + \
                    10*x*(sin(a)*cos(c)+cos(a)*sin(b)*sin(c)) + \
                    10*y*(cos(a)*cos(c)-sin(a)*sin(b)*sin(c)) + \
                    10*z*(-cos(b)*sin(c)), \
                    self.height/2 + \
                    10*x*(sin(a)*cos(c)-cos(a)*sin(b)*cos(c)) + \
                    10*y*(cos(a)*sin(c)+sin(a)*sin(b)*cos(c)) + \
                    10*z*(cos(b)*cos(c)) )
        def f(x,y):
            return cos(sqrt(x*x+y*y))
        du = 1
        dv = 1
        u = -25
        while u < 25:
            v = -25
            while v < 25:
                canvas.create_line( P(u,v,f(u,v)), P(u,v+dv,f(u,v+dv)), fill='green' )
                v += dv
            u += du
        v = -25
        while v < 25:
            u = -25
            while u < 25:
                canvas.create_line( P(u,v,f(u,v)), P(u+du,v,f(u+du,v)), fill='blue' )
                u += du
            v += dv
        canvas.create_text(self.width/2,
                           2*self.app.txtSize,
                           text='Grapher',
                           font=f"Arial {self.app.txtSize} bold",
                           fill='red')
        canvas.create_text(self.width/2,
                           self.height - 2*self.app.txtSize,
                           text='Press any key to start!',
                           font=f"Arial {self.app.txtSize} italic",
                           fill='red')

# Displays a help message. Any event will switch the mode to the Graph Mode.
class HelpMode(Mode):

    helpTxt = """
        Welcome to 3D Graphing!

        Type to alter the desired function.

        Use the buttons on the lower-right to change 
        the view.
            P : precision
            R : range/zoom
            x,y,z : center shifts
            a,b,c : view angles

        Press the esc key to return to the splash screen.
        Press the tab key to return to the help screen.
        Press the del key to return to the default values.
        
        Press any key to start!
    """

    def keyPressed(self,event):
        self.app.setActiveMode(self.app.graphMode)
    
    def mousePressed(self,event):
        self.app.setActiveMode(self.app.graphMode)
        
    def redrawAll(self,canvas):
        canvas.create_rectangle(0,0,self.width,self.height,fill='black')
        canvas.create_text(self.width/2,
                           self.height/2,
                           text=HelpMode.helpTxt,
                           font=f"Arial {self.app.txtSize}",
                           fill='red')

# Displays the 3-D grapher.
class GraphMode(Mode):

    # Initializes the default view settings and the buttons.
    def appStarted(self):
        self.initRotationPars()
        self.updateRotationPars()
        self.viewPosition = coordVector(0, 0, 0)
        self.range = 8
        self.precisionLevel = 10
        self.graph = Function("")
        self.getButtons()
    
    def initRotationPars(self):
        self.viewAngles = coordVector(-0.5, 0.4, 0)
    
    def updateRotationPars(self):
        a,b,c = self.viewAngles.elements
        # Horizontal vector parallel to the screen.
        self.viewX = coordVector(sin(a)*cos(c)+cos(a)*sin(b)*sin(c),
                                 cos(a)*cos(c)-sin(a)*sin(b)*sin(c),
                                 -cos(b)*sin(c))
        # Vertical vector parallel to the screen.
        self.viewY = coordVector(sin(a)*cos(c)-cos(a)*sin(b)*cos(c),
                                 cos(a)*sin(c)+sin(a)*sin(b)*cos(c),
                                 cos(b)*cos(c))
        # Calculations incorporates linear algera and spherical coordinates
        # but are hidden.
    
    # Creates all the buttons and their respective calls.
    def getButtons(self):
        self.buttons = []
        margin = min(20,self.height/20,self.width/20)
        sideLength = margin/3
        buttonConstructor = [
            { "name" : "a+", "tgt" : "angle", "color" : "red", "call" : (lambda graph : graph.viewAngles + coordVector(-tau/30,0,0)) },
            { "name" : "a-", "tgt" : "angle", "color" : "red", "call" : (lambda graph : graph.viewAngles + coordVector(tau/30,0,0)) },
            { "name" : "b+", "tgt" : "angle", "color" : "red", "call" : (lambda graph : graph.viewAngles + coordVector(0,pi/30,0)) },
            { "name" : "b-", "tgt" : "angle", "color" : "red", "call" : (lambda graph : graph.viewAngles + coordVector(0,-pi/30,0)) },
            { "name" : "c+", "tgt" : "angle", "color" : "red", "call" : (lambda graph : graph.viewAngles + coordVector(0,0,tau/30)) },
            { "name" : "c-", "tgt" : "angle", "color" : "red", "call" : (lambda graph : graph.viewAngles + coordVector(0,0,-tau/30)) },
            { "name" : "x+", "tgt" : "center", "color" : "blue", "call" : (lambda graph : graph.viewPosition + coordVector(1,0,0)) },
            { "name" : "x-", "tgt" : "center", "color" : "blue", "call" : (lambda graph : graph.viewPosition + coordVector(-1,0,0)) },
            { "name" : "y+", "tgt" : "center", "color" : "blue", "call" : (lambda graph : graph.viewPosition + coordVector(0,1,0)) },
            { "name" : "y-", "tgt" : "center", "color" : "blue", "call" : (lambda graph : graph.viewPosition + coordVector(0,-1,0)) },
            { "name" : "z+", "tgt" : "center", "color" : "blue", "call" : (lambda graph : graph.viewPosition + coordVector(0,0,1)) },
            { "name" : "z-", "tgt" : "center", "color" : "blue", "call" : (lambda graph : graph.viewPosition + coordVector(0,0,-1)) },
            { "name" : "R+", "tgt" : "range", "color" : "green", "call" : (lambda graph : graph.range * 2) },
            { "name" : "R-", "tgt" : "range", "color" : "green", "call" : (lambda graph : graph.range / 2) },
            { "name" : "P+", "tgt" : "preci", "color" : "yellow", "call" : (lambda graph : graph.precisionLevel + 1) },
            { "name" : "P-", "tgt" : "preci", "color" : "yellow", "call" : (lambda graph : graph.precisionLevel - 1) },
        ]
        def xOffset(i): return (floor(i/2)+1)*margin
        def yOffset(i): return 0.125*margin if i%2==0 else -1.125*margin
        for i,button in enumerate(buttonConstructor):
            self.buttons.append(Button(self.width - xOffset(i),
                                       self.height-2.5*margin - yOffset(i),
                                       sideLength,
                                       button["name"],
                                       button["tgt"],
                                       button["color"],
                                       button["call"]))

    # Takes a point in 3-space and projects it into the viewing window.
    def projectPoint(self,point):
        if not isinstance(point,coordVector):
            point = coordVector(point)
        distanceV = point + -1*self.viewPosition
        viewV = coordVector(distanceV*self.viewX,-distanceV*self.viewY)
        viewV = self.range * viewV
        viewV += coordVector(self.width/2,self.height/2)
        return viewV.elements

    # Checks if the user has pressed a button. If so, call that button.
    def mousePressed(self,event):
        for button in self.buttons:
            if button.isPressed((event.x,event.y)):
                if button.tgt == 'angle':
                    self.viewAngles = button.call(self)
                    self.updateRotationPars()
                elif button.tgt == 'center':
                    self.viewPosition = button.call(self)
                elif button.tgt == 'range':
                    self.range = button.call(self)
                elif button.tgt == 'preci':
                    self.precisionLevel = button.call(self)

    # Writes the desired function or switch between modes.
    def keyPressed(self,event):
        if event.key == 'Backspace':
            if self.graph.name == "":
                return
            else:
                self.graph = Function(self.graph.name[:-1])
        elif event.key in string.ascii_lowercase + string.digits + "(+-*/)":
            self.graph = Function(self.graph.name + event.key)
        elif event.key == 'Escape':
            self.app.setActiveMode(self.app.splashMode)
        elif event.key == 'Tab':
            self.app.setActiveMode(self.app.helpMode)
        elif event.key == 'Delete':
            self.appStarted()

    # Draws the x,y,z axes.
    def drawAxes(self,canvas):
        origin = self.projectPoint((0,0,0))
        axisLength = self.range
        xEnd = self.projectPoint((axisLength,0,0))
        yEnd = self.projectPoint((0,axisLength,0))
        zEnd = self.projectPoint((0,0,axisLength))
        for axisName,axisEnd in [ ("x",xEnd), ("y",yEnd), ("z",zEnd) ]:
            canvas.create_line(origin[0],
                               origin[1],
                               axisEnd[0],
                               axisEnd[1],
                               fill='white')
            canvas.create_text(axisEnd[0],
                               axisEnd[1],
                               text=axisName,
                               font=f"Arial {self.app.txtSize}",
                               fill='white')

    # Draws the given function.
    def drawFunction(self,canvas):
        dt = self.range/self.precisionLevel
        pointDict = {}
        xVals = [self.viewPosition.elements[0] + i*dt for i in range(-self.precisionLevel,self.precisionLevel+1) ]
        yVals = [self.viewPosition.elements[1] + i*dt for i in range(-self.precisionLevel,self.precisionLevel+1) ]
        for x in xVals:
            for y in yVals:
                z = self.graph.eval((x,y))
                if z != None:
                    pointDict[(x,y)] = self.projectPoint((x,y,z))
        for i in range(len(xVals)-1):
            for j in range(len(yVals)):
                if (xVals[i],yVals[j]) in pointDict and (xVals[i+1],yVals[j]) in pointDict:
                    canvas.create_line(pointDict[(xVals[i],yVals[j])], 
                                       pointDict[(xVals[i+1],yVals[j])], 
                                       fill='blue')
        for i in range(len(xVals)):
            for j in range(len(yVals)-1):
                if (xVals[i],yVals[j]) in pointDict and (xVals[i],yVals[j+1]) in pointDict:
                    canvas.create_line(pointDict[(xVals[i],yVals[j])], 
                                       pointDict[(xVals[i],yVals[j+1])], 
                                       fill='green')
        boxMargin = 5
        canvas.create_text(2*boxMargin, 
                           self.height - boxMargin, 
                           text=f"f(x,y)={self.graph.name}",
                           font=f'Arial {self.app.txtSize}', 
                           anchor='sw', 
                           fill='white')

    # Draws the buttons and their names.
    def drawButtons(self,canvas):
        for i,button in enumerate(self.buttons):
            canvas.create_rectangle(button.cx - button.s,
                                    button.cy - button.s,
                                    button.cx + button.s,
                                    button.cy + button.s,
                                    fill=button.color)
            if i%2 == 0:
                canvas.create_text(button.cx,
                                   button.cy - 2*button.s,
                                   text=button.name,
                                   fill='white')
            else:
                canvas.create_text(button.cx,
                                   button.cy + 2*button.s,
                                   text=button.name,
                                   fill='white')

    # Draws everything.
    def redrawAll(self,canvas):
        canvas.create_rectangle(0,0,self.width,self.height,fill='black')
        self.drawAxes(canvas)
        self.drawFunction(canvas)
        self.drawButtons(canvas)


Grapher(width=400,height=400)