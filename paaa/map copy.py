from PIL import Image, ImageDraw, ImageTk
import random
from numpy import sort
import tkinter as tk
from tkinter import ttk

width = 1500
height = 1500
max_width = 400
road_width = 20
canvas = Image.new("RGBA",(width , height ), "green")
draw = ImageDraw.Draw(canvas)
batas = [(0,0)]
space = 20
building = [
    Image.open("bangunan/small.jpg").resize((20,20)), 
    Image.open("bangunan/small2.jpg").resize((20,20)), 
    Image.open("bangunan/large-x.jpg").resize((100,50)),
    Image.open("bangunan/large2x.jpg").resize((100,50)), 
    Image.open("bangunan/large3x.jpg").resize((100,50)), 
    Image.open("bangunan/medium-x.jpg").resize((50,30)),
    Image.open("bangunan/medium2-x.jpg").resize((50,30))
    ]

environment = [
    Image.open("environment/batu1.png").convert("RGBA").resize((20,20)),
    Image.open("environment/rumput1.png").convert("RGBA").resize((20,20)),
    Image.open("environment/rumput2.jpg").convert("RGBA").resize((40,20)),
    Image.open("environment/pohon1.jpg").convert("RGBA").resize((20,20)),
    Image.open("environment/pohon2.png").convert("RGBA").resize((20,20)),
    Image.open("environment/pohon3.png").convert("RGBA").resize((20,20))
]

def drawArea(pos1, pos2, batAs, sisa):
    global building
    print(sisa , ": ", pos1, pos2)
    pos1 = (pos1[0], max(pos1[1], batAs))
    xsort = sort([pos1[0],pos2[0]])
    ysort = sort([pos1[1],pos2[1]])
    if pos1[0] < pos2[0] and pos1[1] < pos2[1]: draw.rectangle(((pos1[0]+1, pos1[1]+1), (pos2[0]-1 , pos2[1]-1)), "gray")
    pos1 = (pos1[0] + 20 , pos1[1]+20)
    pos2 = (pos2[0] - 20 , pos2[1]-20)
    x = xsort[0] + 20
    y = ysort[0] + 20
    if pos1[0] < pos2[0] and pos1[1] < pos2[1]: draw.rectangle((pos1,pos2), "green")
    while y <= ysort[1] - 60:
        while x <= xsort[1] : 
            gedung = [gedung for gedung in building if gedung.size[0] + x < xsort[1] - 20]
            if not gedung : break
            bangunan = random.choice(environment if y > ysort[0] + 20 and y <= ysort[1]-150 else gedung)
            if x + bangunan.size[0] >= xsort[1] -20 : break
            if y > ysort[0] + 20 and y < ysort[1]-150  : canvas.paste(bangunan, (x,(y + random.randint(0, 60-bangunan.size[1]))))
            else : canvas.paste(bangunan, (x,y if y <= ysort[1]-150 else ysort[1]-bangunan.size[1]-20))
            x += bangunan.size[0] + space
        y += 70
        x = xsort[0] + 20
    # if len(sisa) and pos1[1] < batAs :
    #     print("aha")
    #     drawArea(pos1, (sisa[0][0] , ysort[0]), pos1[1], [])
    # if len(sisa) and pos1[1] > batAs :
    #     print("aha")
    #     drawArea(sisa[0], (xsort[1] , ysort[0]), pos1[1], [])

def makeArea(startPoint):
    global width, height, road_width, batas
    print(startPoint)
    y = startPoint[1]  + 200
    x = startPoint[0] 
    tempX = 0
    tempY = 0
    limit_reached = 0
    tempAtas = []
    while y <= height and  not limit_reached:
        tempX = 0
        if y >= height : limit_reached += 1
        while x <= width + 200 :
            batAs,batEs = batas[len(batas)-1][1],batas[len(batas)-1][1]
            yey = random.choice([0,100])
            tempAtas.append((x,y-yey))
            list_atas = []
            for atas in reversed(batas):
                batAs = atas[1] if atas[0] > x else batAs
                batEs = atas[1] if atas[0] > tempX else batEs
                if tempX < atas[0] < x : list_atas.append(atas)
            # if tempX < x :  draw.rectangle(((x,y), (x+road_width, y+road_width)), "black")
            if batEs < y-yey : 
                if tempX < x and y <= height: draw.rectangle(((tempX,y-yey), (x+20, y-yey+20)), "black")
                if tempX < x and y <= height: draw.line(((tempX+20,y-yey+10), (x, y-yey+10)), "white", 1)
                if tempX < x and y <= height: draw.rectangle(((x,batAs), (x+20, y-yey)), "black")
                if tempX < x and y <= height: draw.line(((x+10,batAs+20), (x+10, y-yey)), "white", 1)
                if tempX < x and y <= height and tempX >= 20: draw.rectangle(((tempX,batEs+10), (tempX+20, y-yey)), "black")
                if tempX < x and y <= height and tempX >= 20: draw.line(((tempX+10,batEs+20), (tempX+10, y-yey)), "white",1)
                drawArea((tempX+20 , batEs+20 ), (x  , y-yey), batAs+20, list_atas)
            tempX = x
            tempY = batAs
            x += random.randint(2,4) * 100
        y += 300
        tempAtas.append((tempX,tempY))
        if y > height : 
            y = height
        batas = tempAtas
        tempAtas = []
        x = startPoint[0]
        



zoom_factor = 1.0
INITIAL_WIDTH = 800
INITIAL_HEIGHT = 800
viewport_x = 0
viewport_y = 0
viewport_width = 800
viewport_height = 800
new_map = None
scale = 1.0
canvas_width = 800
canvas_height = 600

def update_map():
    global draw, canvas, batas
    batas = [(0,0)]
    canvas = Image.new("RGBA",(width , height ), "green")
    draw = ImageDraw.Draw(canvas)
    makeArea((0,0))
    canvas.save("map.png")
    new_map  = canvas
    cropped_map = new_map.crop((viewport_x, viewport_y, viewport_x + viewport_width, viewport_y + viewport_height))
    resized_map = cropped_map.resize((INITIAL_WIDTH, INITIAL_HEIGHT))
    img_tk = ImageTk.PhotoImage(resized_map)
    map_label.config(image=img_tk)
    map_label.image = img_tk
    update()
    
def update():
    print("zoom")
    global canvas
    cropped_map = canvas.crop((viewport_x * zoom_factor, viewport_y * zoom_factor, viewport_x* zoom_factor + viewport_width* zoom_factor, viewport_y* zoom_factor + viewport_height* zoom_factor))
    resized_map = cropped_map.resize((INITIAL_WIDTH*int(scale),int(scale)* INITIAL_HEIGHT))
    img_tk = ImageTk.PhotoImage(canvas)
    map_label.config(image=img_tk)
    map_label.image = img_tk
    
def zoom_out():
    global scale
    scale /= 1.1
    update()
    resize_canvas()

# Fungsi untuk zoom out
def zoom_in():
    global scale
    scale *= 1.1
    update()
    resize_canvas()   
         
def scroll(event):
    global viewport_x, viewport_y
    print(viewport_y)
    if event.delta > 0:
        viewport_y -= 20 if viewport_y > 0 else 0
    else:
        viewport_y += 20 if viewport_y < 1000 / zoom_factor else 0
    update()
           
def on_scrollbar_press(event, direction):
    print(f"Scrollbar {direction} pressed at position ({event.x}, {event.y})") 

def resize_canvas():
    # Resize canvas content based on scale
    canvass.config(scrollregion=(0, 0, canvas_width*scale, canvas_height*scale))
    canvass.scale("all", 0, 0, scale, scale)
    canvass.config(width=canvas_width*scale, height=canvas_height*scale)

root = tk.Tk()
root.title("Desain IKN City ")
root.geometry("800x800")  # Set initial window size (width x height)
root.minsize(600, 400)  # Set minimum window size
root.bind("<MouseWheel>", scroll)

# Configure grid layout for root
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configure grid layout for frame
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Create a canvas to hold the image
canvass = tk.Canvas(frame, bg='white')
canvass.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Add scrollbars
v_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvass.yview)
v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))

h_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvass.xview)
h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))

canvass.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
# Bind mouse button press events to the scrollbars
v_scroll.bind("<ButtonPress-1>", lambda event: on_scrollbar_press(event, "vertical"))
h_scroll.bind("<ButtonPress-1>", lambda event: on_scrollbar_press(event, "horizontal"))

# Add a label inside the canvas
map_label = ttk.Label(canvass)
canvass.create_window((0, 0), window=map_label, anchor='nw')

generate_button = ttk.Button(root, text="Generate Map", command=update_map)
generate_button.grid(row=1, column=0, pady=10)

zoom_in_button = ttk.Button(root, text="Zoom In", command=zoom_in)
zoom_in_button.grid(row=2, column=0, pady=5)

zoom_out_button = ttk.Button(root, text="Zoom Out", command=zoom_out)
zoom_out_button.grid(row=3, column=0, pady=5)

def on_frame_configure(event):
    # Update scroll region to match the size of the inner content
    canvass.configure(scrollregion=canvass.bbox("all"))
    print(event)

frame.bind("<Configure>", on_frame_configure)

update_map()
root.mainloop()