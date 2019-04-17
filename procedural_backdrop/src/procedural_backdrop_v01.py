########################################################################################################################

__author__ = "Boris Martinez Castillo"
__version__ = "1.0.1"
__maintainer__ = "Boris Martinez Castillo"
__email__ = "boris.vfx@outlook.com"

########################################################################################################################


#IMPORTS
import nuke
import nukescripts
import random


#DEFINITIONS   
def randomize_colors(): 

    for i in nuke.allNodes():
        colors = {"green":int(93950720.0),
              "pink":int(3596850175.0),
              "dark":int(68228863.0),
              "yellow":int(4293503743.0),
              "grey":int(2846468607.0),
              "light_green": 2063565055,
              "redred": 44282656255282656255,
              "seablue": 947890687,
              "orange": 3512929279,
              "lemon": 4292490239,
              "kiwi": 1102186239,   
              "brown": 2186546349   }

        color = random.choice(colors.keys())    
        random_color = colors[color]
        i['tile_color'].setValue(random_color)

    return random_color


def create_dots(node,axis):
    #QUERY H/W VALUES
    w = int(node.knob("bdwidth").getValue())
    h = int(node.knob("bdheight").getValue())
    dot = nuke.nodes.Dot()
    sel = dot

    #PLACING DOTS
    if axis == "horizontal":  
       dot.setYpos(node.ypos() + (h/2) )
       dot.setXpos(node.xpos() - (w/2))
    
    elif axis == "vertical":
       dot.setYpos(node.ypos())
       dot.setXpos(node.xpos() - ((w/2)))  
    #SELECTION HANDLING
    dot["selected"].setValue(False)
    node["selected"].setValue(True)

    return sel      

    
def replicate_backdrop(axis,sel,count,spacing):
      
    #CATCHING NUKE OBJECT
    source = nuke.selectedNode()
    source['selected'].setValue(False)
    #QUERYING & PROCCESSING NUKE'S OBJECT'S COORDINATES
    w = int(source.knob("bdwidth").getValue())
    h = int(source.knob("bdheight").getValue())
    #QUERYING & PROCCESSING NUKE'S OBJECT'S COLOR AND LABEL
    color = int(source["tile_color"].getValue())
    txt =  str(source['label'].getValue()) 
    txt1 = bytearray(txt)
    del txt1[0:]
    txt = str(txt1)
    
    #QUERYING NUKE'S OBJECT'S COLOR AND LABEL
    size = int(source['note_font_size'].getValue())
    #CREATING BACKDROP REPLICA
    node = nukescripts.autoBackdrop()

    #SETTING NEW BACKDROP SIZE 
    if axis == "horizontal":
        node.setYpos(source.ypos())
        node.setXpos(source.xpos() + (w+spacing))

        dot = nuke.createNode("Dot")
        if count == 0 :
            dot.setInput(0,sel)
        dot.setYpos(source.ypos() + (h/2) )
        dot.setXpos(source.xpos() + (w+spacing/2))
        
    elif axis == "vertical":
        node.setXpos(source.xpos())
        node.setYpos(source.ypos() + (h+spacing/2))

        dot = nuke.createNode("Dot")
        if count == 0 :
            dot.setInput(0,sel)          
        dot.setYpos(source.ypos() + (h+spacing/6))
        dot.setXpos(source.xpos() - ((w/2)))    
    
    node.knob("bdwidth").setValue(w) 
    node.knob("bdheight").setValue(h)
    #SETTING NEW BACKDROP'S VARIOUS KNOBS
    node['tile_color'].setValue(color)
    node['label'].setValue(txt + str(count+1))
    txt = "" 
    node['note_font_size'].setValue(size)
    node['selected'].setValue(True)


def custom_backdrop(txt,fontsize,align,color,times,axis,spacing):

    #CREATING BACKDROP
    node = nukescripts.autoBackdrop()
    #DEFINING COLORS
    colors = {"green":int(93950720.0),
              "pink":int(3596850175.0),
              "dark":int(68228863.0),
              "yellow":int(4293503743.0),
              "grey":int(2846468607.0),
              "random":int(2846468607.0)}
    #CLEARING SELECTION
    prev_sel = nuke.selectedNodes()

    for i in prev_sel:
        i['selected'].setValue(False) 
    node['selected'].setValue(True)
    #SETTING BACKDROP'S VARIOUS KNOBS
    node['label'].setValue('<'+align+'>'+txt)
    node['note_font_size'].setValue(fontsize)
    node['tile_color'].setValue(colors[color])
    
    #CREATING DOTS
    dots = create_dots(node,axis)
    #REPLICATE BACKDROP BASED ON CONDITION
    if times == 0:
        pass   
    elif times > 0:
        [replicate_backdrop(axis,dots,i,spacing) for i in range(times)]
        

class modalPanel(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self,"b_procedural_backdrop")

    #CREATE KNOBS
        self.note_size = nuke.Int_Knob("Note Size:")
        self.note_size.clearFlag(nuke.STARTLINE)
        self.frame_display = nuke.String_Knob("Label:")
        self.frame_display.clearFlag(nuke.STARTLINE)
        self.align = nuke.Enumeration_Knob("Align", "Align", ["left","center","right"])
        self.color = nuke.Enumeration_Knob("Color", "Color", ["green","pink","dark","yellow","grey","random"])        
        self.color.clearFlag(nuke.STARTLINE)
        self.axis = nuke.Enumeration_Knob("Axis", "Axis", ["horizontal","vertical"])
        self.multi = nuke.Text_Knob("Multi")
        self.axis.clearFlag(nuke.STARTLINE)    
        self.amount = nuke.Int_Knob("Amount:")
        self.note_size.clearFlag(nuke.STARTLINE)
        self.spacing = nuke.Int_Knob("Spacing:")
        self.spacing.clearFlag(nuke.STARTLINE)
        self.author = nuke.Text_Knob("by Boris Martinez")

    #SET DEFAULTS
        self.set_note_size_default_value()
        self.spacing_default_value()

    #ADD KNOBS
        for i in (self.note_size , self.frame_display,self.align,self.color,self.multi,self.amount,self.axis,self.spacing,self.author):
            self.addKnob(i)

    #METHODS
    def set_note_size_default_value(self):
        self.note_size.setValue(100)

    def spacing_default_value(self):
        self.spacing.setValue(100)

def main_function():

    #CREATE PANEL INSTANCE   
    panel = modalPanel()

    if not panel.showModalDialog():
        print "script aborted"
        return
    else:
        fontsize = panel.note_size.getValue()
        note = panel.frame_display.getValue()
        align = panel.align.value()
        color = panel.color.value()    
        times = panel.amount.value()
        axis = panel.axis.value()
        spacing = panel.spacing.value()
    #TRIGGER FUNCTIONS
    custom_backdrop(note,fontsize,align,color,times,axis,spacing)

    if not color == "random":
        pass
    else:
        randomize_colors()
            

if __name__ == "__main__":
    main_function()