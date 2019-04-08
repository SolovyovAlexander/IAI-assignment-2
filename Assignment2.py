from random import randint
import math
from PIL import Image, ImageDraw

ideal = Image.open("input.png")


# draws circle with random coordinates, random colour and random size
def draw_random_circle(draw):
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    radius = randint(12, 27)
    x = randint(0, 512)
    y = randint(0, 512)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(r, g, b), outline=None)


# draws circle with coordinates x and y, colour = list with RGB components, radius = 2
def draw_circle_with_cordinates(x: int, y: int, colour, draw1):
    radius = 2
    x = randint(x - 1, x + 1)
    y = randint(y - 1, y + 1)
    draw1.ellipse((x - radius, y - radius, x + radius, y + radius), fill=colour, outline=None)


# creates picture with 1500-1600 random circles
def create_picture():
    img = Image.new('RGB', (512, 512), 'WHITE')
    draw = ImageDraw.Draw(img)

    for i in range(randint(1500, 1600)):
        draw_random_circle(draw)

    img.save("pic.png", 'PNG')
    return img


# creates population of images, n = size of population
def create_population(n: int):
    population = []
    for i in range(n):
        population.append(create_picture())
    return population


# selects half of the best elements in the population
def fitness(population):
    arr = []
    chosen = []
    for i in range(len(population)):
        arr.append([score(population[i]), population[i]])
    arr.sort(key=lambda x: x[0])
    for i in range(len(arr) // 2):
        chosen.append(arr[i][1])

    return chosen


# how different is the image from the input
def score(image):
    n = 0
    for i in range(64):
        for j in range(64):
            ideal_pixel = ideal.getpixel((i * 8, j * 8))
            image_pixel = image.getpixel((i * 8, j * 8))
            n = n + abs(ideal_pixel[0] - image_pixel[0]) + abs(ideal_pixel[1] - image_pixel[1]) + abs(
                ideal_pixel[2] - image_pixel[2])
    return n


# crosses 2 images
def crossover(mum, dad):
    child = Image.new('RGB', (512, 512), 'WHITE')
    draw = ImageDraw.Draw(child)

    for i in range(512):
        for j in range(512):
            ideal_pixel = ideal.getpixel((i, j))
            mum_pixel = mum.getpixel((i, j))
            dad_pixel = dad.getpixel((i, j))
            if math.sqrt(((mum_pixel[0] - ideal_pixel[0]) ** 2 + (mum_pixel[1] - ideal_pixel[1]) ** 2 + (
                    mum_pixel[2] - ideal_pixel[2]) ** 2)) < math.sqrt(((dad_pixel[0] - ideal_pixel[0]) ** 2 + (
                    dad_pixel[1] - ideal_pixel[1]) ** 2 + (dad_pixel[2] - ideal_pixel[2]) ** 2)):
                draw_circle_with_cordinates(i, j, mum_pixel, draw)
            else:
                draw_circle_with_cordinates(i, j, dad_pixel, draw)
    mutation(draw)
    return child


# accidentally crosses elements of the population
def crossing(population: list):
    n = len(population)
    for i in range(n):
        mum = randint(0, n - 1)
        dad = randint(0, n - 1)
        if mum != dad:
            population.append(crossover(population[mum], population[dad]))
        else:
            population.append(crossover(population[mum], population[0]))

    return population


# this function run everything
def start():
    population = create_population(10)
    population = fitness(population)
    population = crossing(population)
    begin_evolution(population)



# continuation of the start function, for convenience
def begin_evolution(population):
    a = population
    for i in range(1000):
        a = fitness(a)
        a = crossing(a)
        print("population = " + str(i + 1))
        if i%10==0:
            string = "pic" + str(i + 1) + ".png"
            a[9].save(string, "PNG")
    a[0].show()
    return a


# mutates the image with some probability
def mutation(draw):
    for i in range(512):
        for j in range(512):
            rand = randint(0, 5000)
            if rand == 1:
                ideal_pixel = ideal.getpixel((i, j))
                draw_circle_with_cordinates(i, j, ideal_pixel, draw)
    return 1




start()