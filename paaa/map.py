from PIL import Image, ImageDraw, ImageTk
import random
import numpy as np
import tkinter as tk
from tkinter import ttk

# Constants
width = 1500
height = 1500
max_width = 400
road_width = 20
space = 20
zoom_factor = 1.0
INITIAL_WIDTH = 800
INITIAL_HEIGHT = 600
viewport_x = INITIAL_WIDTH // 2 - 50
viewport_y = INITIAL_HEIGHT // 2 - 50
viewport_width = 800
viewport_height = 600

# Canvas setup
canvas = Image.new("RGBA", (width, height), "green")
draw = ImageDraw.Draw(canvas)
batas = [(0, 0)]

# Load images
building = [
    Image.open("bangunan/house.png").convert("RGBA").resize((20, 20)),
    Image.open("bangunan/house2.png").convert("RGBA").resize((20, 20)),
    Image.open("bangunan/large2.png").convert("RGBA").resize((100, 50)),
    Image.open("bangunan/large.png").convert("RGBA").resize((100, 50)),
    Image.open("bangunan/medium.png").convert("RGBA").resize((100, 50)),
    Image.open("bangunan/medium2.png").convert("RGBA").resize((50, 30)),
    Image.open("bangunan/medium3.png").convert("RGBA").resize((50, 30)),
    Image.open("bangunan/medium4.jpg").convert("RGBA").resize((50, 30)),
    Image.open("bangunan/small.png").convert("RGBA").resize((50, 30))

]

environment = [
    Image.open("environment/rock1.png").convert("RGBA").resize((20, 20)),
    Image.open("environment/rock2.png").convert("RGBA").resize((20, 20)),
    Image.open("environment/rumput1.png").convert("RGBA").resize((20, 20)),
    Image.open("environment/rumput2.png").convert("RGBA").resize((40, 20)),
    Image.open("environment/tree2.png").convert("RGBA").resize((20, 20)),
    Image.open("environment/tree3.png").convert("RGBA").resize((20, 20)),
    Image.open("environment/tree4.png").convert("RGBA").resize((20, 20))
]

car_images = [
    Image.open("cars/car1.png").convert("RGBA").resize((20, 10)),
    Image.open("cars/car2.png").convert("RGBA").resize((20, 10)),
    Image.open("cars/car3.png").convert("RGBA").resize((20, 10)),
    Image.open("cars/car4.png").convert("RGBA").resize((20, 10))
]

# Car setup
cars = [{"image": random.choice(car_images), "position": (random.randint(0, width), random.randint(0, height)), "velocity": (random.choice([-1, 1]) * 5, 0)} for _ in range(5)]

# Function to draw area and roads
def drawArea(pos1, pos2, batAs, sisa):
    global building, environment

    # Fungsi untuk menentukan apakah suatu titik berada di atas jalan atau tidak
    def is_on_road(x, y):
        # Pastikan koordinat berada dalam batas gambar
        if 0 <= x < width and 0 <= y < height:
            # Dapatkan warna piksel pada posisi (x, y) pada gambar jalan
            pixel_color = canvas.getpixel((x, y))
            # Jika warna piksel tersebut adalah warna jalan (hitam), kembalikan True, jika tidak, kembalikan False
            return pixel_color == (0, 0, 0, 255)
        else:
            # Jika koordinat di luar batas gambar, kembalikan False
            return False

    pos1 = (pos1[0], max(pos1[1], batAs))
    xsort = np.sort([pos1[0], pos2[0]])
    ysort = np.sort([pos1[1], pos2[1]])
    if pos1[0] < pos2[0] and pos1[1] < pos2[1]:
        draw.rectangle(((pos1[0] + 1, pos1[1] + 1), (pos2[0] - 1, pos2[1] - 1)), "gray")
    pos1 = (pos1[0] + 20, pos1[1] + 20)
    pos2 = (pos2[0] - 20, pos2[1] - 20)
    x = xsort[0] + 20
    y = ysort[0] + 20
    if pos1[0] < pos2[0] and pos1[1] < pos2[1]:
        draw.rectangle((pos1, pos2), "white")
    while y <= ysort[1] - 60:
        while x <= xsort[1]:
            gedung = [gedung for gedung in building if gedung.size[0] + x < xsort[1] - 20]
            if not gedung:
                break
            bangunan = random.choice(gedung)
            if x + bangunan.size[0] >= xsort[1] - 20:
                break
            canvas.paste(bangunan, (x, y), bangunan)
            x += bangunan.size[0] + space
        y += 70
        x = xsort[0] + 20


        # Add rocks randomly outside the gray lines
        if random.random() < 0.2:
            rock = random.choice(environment[:2])  # Select rock image randomly
            max_x = min(pos2[0] - rock.size[0], xsort[1] - rock.size[0])  # Update max_x
            min_x = max(pos1[0], xsort[0])  # Update min_x

            # Check if the range is not empty
            if max_x > min_x:
                rock_x = random.randint(min_x, max_x)  # Random x-coordinate within the area
                rock_y = random.randint(max(pos1[1], ysort[0]), min(ysort[1] - rock.size[1], ysort[1] - rock.size[
                    1]))  # Random y-coordinate within the area

                # Ensure rock_x and rock_y are within the image boundaries
                rock_x = max(0, min(rock_x, width - rock.size[0]))
                rock_y = max(0, min(rock_y, height - rock.size[1]))

                # Check if the rock position is not on the road or gray line
                if (not is_on_road(rock_x, rock_y)) and (not is_on_road(rock_x + rock.size[0], rock_y)) and (
                        not is_on_road(rock_x, rock_y + rock.size[1])) and (
                        not is_on_road(rock_x + rock.size[0], rock_y + rock.size[1])):
                    canvas.paste(rock, (rock_x, rock_y), rock)

        # Add trees randomly
        if random.random() < 0.3:
            tree = random.choice(environment[4:])  # Select tree image randomly
            max_x = min(pos2[0] - tree.size[0], xsort[1] - tree.size[0])
            min_x = max(pos1[0], xsort[0])
            if max_x >= min_x:
                tree_x = random.randint(min_x, max_x)  # Random x-coordinate within the area
                tree_y = random.randint(max(pos1[1], ysort[0]), min(ysort[1] - tree.size[1], ysort[1] - tree.size[
                    1]))  # Random y-coordinate within the area
                canvas.paste(tree, (tree_x, tree_y), tree)

        x += space

        # Add trees randomly
        if random.random() < 0.3:
            tree = random.choice(environment[4:])  # Select tree image randomly
            max_x = min(pos2[0] - tree.size[0], xsort[1] - tree.size[0])
            min_x = max(pos1[0], xsort[0])
            if max_x >= min_x:
                tree_x = random.randint(min_x, max_x)  # Random x-coordinate within the area
                tree_y = random.randint(max(pos1[1], ysort[0]), min(ysort[1] - tree.size[1], ysort[1] - tree.size[
                    1]))  # Random y-coordinate within the area
                canvas.paste(tree, (tree_x, tree_y), tree)

        # Add rocks randomly outside the gray lines
        if random.random() < 0.2:
            rock = random.choice(environment[:2])  # Select rock image randomly
            max_x = min(pos2[0] - rock.size[0], xsort[1] - rock.size[0])  # Update max_x
            min_x = max(pos1[0], xsort[0])  # Update min_x

            # Check if the range is not empty
            if max_x > min_x:
                rock_x = random.randint(min_x, max_x)  # Random x-coordinate within the area
                rock_y = random.randint(max(pos1[1], ysort[0]), min(ysort[1] - rock.size[1], ysort[1] - rock.size[
                    1]))  # Random y-coordinate within the area

                # Ensure rock_x and rock_y are within the image boundaries
                rock_x = max(0, min(rock_x, width - rock.size[0]))
                rock_y = max(0, min(rock_y, height - rock.size[1]))

                # Check if the rock position is not on the road or gray line
                if (not is_on_road(rock_x, rock_y)) and (not is_on_road(rock_x + rock.size[0], rock_y)) and (
                        not is_on_road(rock_x, rock_y + rock.size[1])) and (
                not is_on_road(rock_x + rock.size[0], rock_y + rock.size[1])):
                    canvas.paste(rock, (rock_x, rock_y), rock)

# Tambahkan batu dan rumput secara acak dengan penempatan yang lebih rapi
def add_rocks_and_grass():
    global canvas, width, height

    # Tentukan jumlah maksimum batu yang ingin ditambahkan
    max_rocks = 10

    # Hitung jumlah batu yang sudah ditambahkan
    rocks_added = 0

    for _ in range(100):  # Batasi percobaan hingga 100 kali
        # Pilih titik acak di dalam area
        x = random.randint(20, width - 20)
        y = random.randint(20, height - 20)

        # Pastikan titik yang dipilih tidak berada di atas jalan atau bangunan
        if not is_on_road(x, y) and not is_on_building(x, y):
            # Tambahkan batu secara acak dengan probabilitas 0.2
            if random.random() < 0.2 and rocks_added < max_rocks:
                rock = random.choice(environment[:2])  # Pilih gambar batu secara acak
                canvas.paste(rock, (x, y), rock)
                rocks_added += 1

            # Jika sudah mencapai jumlah maksimum, hentikan iterasi
            if rocks_added >= max_rocks:
                break

# Fungsi untuk mengecek apakah suatu titik berada di atas bangunan
def is_on_building(x, y):
    global building

    # Loop melalui daftar bangunan dan periksa apakah titik berada di atas salah satunya
    for b in building:
        if x >= b.size[0] and x <= width - b.size[0] and y >= b.size[1] and y <= height - b.size[1]:
            return True
    return False

def is_forest_area(x, y):
    forest_color = (34, 139, 34, 255)  # Green color for forest
    try:
        # Check the color of the pixel at (x, y) and determine if it matches the forest color
        pixel_color = canvas.getpixel((x, y))
        return pixel_color == forest_color
    except IndexError:
        print("Error: Index out of range for coordinates:", (x, y))
        return False

# Function to create area with roads and forests
def makeArea(startPoint):
    global width, height, road_width, batas, cars

    cars = []
    y = startPoint[1] + 200
    x = startPoint[0]
    tempX = 0
    tempY = 0
    limit_reached = 0
    tempAtas = []
    while y <= height and not limit_reached:
        tempX = 0
        if y >= height:
            limit_reached += 1
        while x <= width + 200:
            batAs, batEs = batas[len(batas) - 1][1], batas[len(batas) - 1][1]
            yey = random.choice([0, 100])
            tempAtas.append((x, y - yey))
            list_atas = []
            for atas in reversed(batas):
                batAs = atas[1] if atas[0] > x else batAs
                batEs = atas[1] if atas[0] > tempX else batEs
                if tempX < atas[0] < x:
                    list_atas.append(atas)
            if batEs < y - yey:
                if tempX < x and y <= height:
                    draw.rectangle(((tempX, y - yey), (x + 20, y - yey + 20)), "black")
                if tempX < x and y <= height:
                    draw.line(((tempX + 20, y - yey + 10), (x, y - yey + 10)), "white", 1)
                if tempX < x and y <= height:
                    draw.rectangle(((x, batAs), (x + 20, y - yey)), "black")
                if tempX < x and y <= height:
                    draw.line(((x + 10, batAs + 20), (x + 10, y - yey)), "white", 1)
                if tempX < x and y <= height and tempX >= 20:
                    draw.rectangle(((tempX, batEs + 10), (tempX + 20, y - yey)), "black")
                if tempX < x and y <= height and tempX >= 20:
                    draw.line(((tempX + 10, batEs + 20), (tempX + 10, y - yey)), "white", 1)
                drawArea((tempX + 20, batEs + 20), (x, y - yey), batAs + 20, list_atas)

                # Check if the area is non-forest (white) and add trees
                if is_non_forest_area(x, y - yey):
                    tree = random.choice(environment[4:])  # Select tree image randomly
                    max_x = min(x + 100 - tree.size[0], width - tree.size[0])
                    min_x = max(x, 20)
                    max_y = min(batEs + 10, y - yey + 20) - tree.size[1]  # Update max_y for tree placement
                    min_y = max(batAs + 20, y - yey)  # Update min_y for tree placement
                    # Check if the range is not empty for both x and y
                    if max_x >= min_x and max_y >= min_y:
                        tree_x = random.randint(min_x, max_x)  # Random x-coordinate within the area
                        tree_y = random.randint(min_y, max_y)  # Random y-coordinate within the area
                        canvas.paste(tree, (tree_x, tree_y), tree)

            tempX = x
            tempY = batAs
            x += random.randint(2, 4) * 100
        y += 300
        tempAtas.append((tempX, tempY))
        if y > height:
            y = height
        batas = tempAtas
        tempAtas = []
        x = startPoint[0]

# Loop to place cars on roads
    for y in range(startPoint[1] + 20, height, 300):
        for x in range(startPoint[0] + 20, width - 20, 200):
            lane_center = x + (road_width // 2)  # Calculate lane center
            # Check if the lane center is on the road
            if is_on_road(lane_center, y):
                cars.append({"image": random.choice(car_images), "position": (lane_center, y),
                             "velocity": (random.choice([-1, 1]) * 5, 0)})

# Tambahkan batu dan rumput secara acak
    add_rocks_and_grass()

def is_non_forest_area(x, y):
    non_forest_color = (255, 255, 255, 255)  # White color for non-forest area
    # Check if the coordinates (x, y) are within the image boundaries
    if 0 <= x < width and 0 <= y < height:
        # Check the color of the pixel at (x, y) and determine if it matches the non-forest color
        pixel_color = canvas.getpixel((x, y))
        return pixel_color == non_forest_color
    else:
        # If the coordinates are out of bounds, consider it as non-forest area
        return False


def is_on_road(x, y):
    # Pastikan koordinat berada dalam batas gambar
    if 0 <= x < width and 0 <= y < height:
        # Dapatkan warna piksel pada posisi (x, y) pada gambar jalan
        pixel_color = canvas.getpixel((x, y))
        # Jika warna piksel tersebut adalah warna jalan (hitam), kembalikan True, jika tidak, kembalikan False
        return pixel_color == (0, 0, 0, 255)
    else:
        # Jika koordinat di luar batas gambar, kembalikan False
        return False

# Function to update car positions
def update_car_positions():
    for car in cars:
        x, y = car["position"]
        vx, vy = car["velocity"]

        # Move the car along the x-axis
        new_x = (x + vx) % width

        # Check if the new position is on the road
        if is_on_road(new_x, y):
            car["position"] = (new_x, y)

# Function to update the map
def update_map():
    global draw, canvas, batas
    batas = [(0, 0)]
    canvas = Image.new("RGBA", (width, height), (34, 139, 34, 255))
    draw = ImageDraw.Draw(canvas)
    makeArea((0, 0))
    update_viewport()

# Function to update the viewport
def update_viewport():
    global canvas, viewport_x, viewport_y, viewport_width, viewport_height

    # Draw cars on the canvas
    update_car_positions()
    for car in cars:
        x, y = car["position"]
        car_image = car["image"]
        canvas.paste(car_image, (x, y), car_image)

    # Crop and resize the portion of the canvas to display in the viewport
    cropped_map = canvas.crop((viewport_x, viewport_y, viewport_x + viewport_width, viewport_y + viewport_height))
    resized_map = cropped_map.resize((INITIAL_WIDTH, INITIAL_HEIGHT))
    img_tk = ImageTk.PhotoImage(resized_map)

    # Update the map_label with the new image
    map_label.config(image=img_tk)
    map_label.image = img_tk

# Zoom in function
def zoom_in():
    global zoom_factor, viewport_x, viewport_y, viewport_width, viewport_height
    zoom_factor *= 1.1
    viewport_width = int(INITIAL_WIDTH / zoom_factor)
    viewport_height = int(INITIAL_HEIGHT / zoom_factor)
    viewport_x = max(0, min(width - viewport_width, viewport_x + (INITIAL_WIDTH - viewport_width) // 2))
    viewport_y = max(0, min(height - viewport_height, viewport_y + (INITIAL_HEIGHT - viewport_height) // 2))
    update_viewport()

# Zoom out function
def zoom_out():
    global zoom_factor, viewport_x, viewport_y, viewport_width, viewport_height
    zoom_factor /= 1.1
    viewport_width = int(INITIAL_WIDTH / zoom_factor)
    viewport_height = int(INITIAL_HEIGHT / zoom_factor)
    viewport_x = max(0, min(width - viewport_width, viewport_x - (viewport_width - INITIAL_WIDTH) // 2))
    viewport_y = max(0, min(height - viewport_height, viewport_y - (viewport_height - INITIAL_HEIGHT) // 2))
    update_viewport()

# Tkinter setup
root = tk.Tk()
root.geometry(f"{INITIAL_WIDTH}x{INITIAL_HEIGHT}")
root.title("Map Viewer")

map_frame = ttk.Frame(root)
map_frame.pack(fill=tk.BOTH, expand=True)

map_label = ttk.Label(map_frame)
map_label.pack(fill=tk.BOTH, expand=True)

zoom_in_button = ttk.Button(root, text="Zoom In", command=zoom_in)
zoom_in_button.pack(side=tk.LEFT, padx=5, pady=5)

zoom_out_button = ttk.Button(root, text="Zoom Out", command=zoom_out)
zoom_out_button.pack(side=tk.LEFT, padx=5, pady=5)

# Add Generate Map button
generate_map_button = ttk.Button(root, text="Generate Map", command=update_map)
generate_map_button.pack(side=tk.LEFT, padx=5, pady=5)

# Start the main loop, then update the map
root.after(100, update_map)
root.mainloop()
