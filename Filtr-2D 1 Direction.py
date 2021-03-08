from turtle import *
import numpy as np

# functions ***********BEGGINING*************

# rysowanie pola mapy, na podstawie zdefiniowanego lewego gornego rogu


def draw_box(left_top_corner_x, left_top_corner_y, color):
    # szerokosc przeszkody
    obstacle_width = 1
    # wysokosc przeszkody
    obstacle_height = 1
    # ukrycie ikony agenta,
    turtle1.hideturtle()
    # wylaczenie rysowania
    turtle1.penup()
    turtle1.setx(left_top_corner_x*factor)
    turtle1.sety(left_top_corner_y*factor)
    # wlaczenie rysowania
    turtle1.pendown()
    # rysownie wypelnionego kolorem niebieskim prostokata,
    turtle1.fillcolor(color)
    turtle1.begin_fill()
    # ustawiamy poczatkowy kierunek na polnoc, polnoc jest skierowna w prawo,
    turtle1.setheading(0)
    turtle1.forward(obstacle_width*factor)
    turtle1.right(90)
    turtle1.forward(obstacle_height*factor)
    turtle1.right(90)
    turtle1.forward(obstacle_width*factor)
    turtle1.right(90)
    turtle1.forward(obstacle_height*factor)
    turtle1.right(90)
    turtle1.end_fill()

# pokazanie aktualnego prawdopodobienstwa na mapie,
# do przerobienia gdy zmienimy wiersz rysowania mapy


def show_p(mapa_size, world_row_position):
    for i in range(0, mapa_size):
        for j in range(0, 6):
            turtle1.penup()
            temp = j + 0.2
            turtle1.setx(temp*factor)
            turtle1.sety((world_row_position-0.5)*factor)
            turtle1.write(np.around(probability[i][j], decimals=3))
        world_row_position -= 1

# update prawdopodobienstwa po pomiarze, step1


def sense(sense_precision, sense_temp, mapa_size):
    for i in range(0, mapa_size):
        for j in range(0, 6):
            if mapa[i][j] == sense_temp:
                probability[i][j] = probability[i][j] * sense_precision
            else:
                probability[i][j] = probability[i][j] * (1.-sense_precision)
        # update prawdopodobienstwa po pomiarze, step2
        # normalizacja,
    suma = np.sum(probability)
    for i in range(0, mapa_size):
        for j in range(0, 6):
            probability[i][j] = probability[i][j]/suma
# pamietamy ze swiat jest cykliczny z 6 trafiamy do 0, za pomoca modulo,


def move_right(mapa_size, move_precision_zostaje, move_precision_cel, move_precision_kolejna):
    probability_apriori = probability.copy()
    for i in range(0, mapa_size):
        for j in range(0, 6):
            if i < 1:
                if j == 0:
                    probability[i][j] = probability_apriori[i][j] * move_precision_zostaje
                if j == 1:
                    probability[i][j] = probability[i][j] + probability_apriori[i][j + 1] * move_precision_cel
                if j == 2:
                    probability[i][j] = probability[i][j] + probability_apriori[i][j + 2] * move_precision_kolejna


def move_up(mapa_size, move_precision_zostaje, move_precision_cel, move_precision_kolejna):
    probability_apriori = probability.copy()
    for j in range(0, 6):
        for i in range(mapa_size - 1, -1, -1):
            if j < 1:
                if i == 2:
                    probability[i][j] = probability_apriori[i][j] * move_precision_zostaje
                if i == 1:
                    probability[i][j] = probability[i][j] + probability_apriori[i - 1][j] * move_precision_cel
                if i == 0:
                    probability[i][j] = probability[i][j] + probability_apriori[i - 2][j] * move_precision_kolejna


def move_down(mapa_size, move_precision_zostaje, move_precision_cel, move_precision_kolejna):
    probability_apriori = probability.copy()
    for j in range(0, 6):
        for i in range(0, mapa_size):
            print(i)
            if j < 1 and i <= 1:
                if i == 0:
                    probability[i][j] = probability_apriori[i][j] * move_precision_zostaje
                if i == 1:
                    probability[i][j] = probability[i][j] + probability_apriori[i + 1][j] * move_precision_cel
                if i == 2:
                    probability[i][j] = probability[i][j] + probability_apriori[i + 2][j] * move_precision_kolejna


def move_left(mapa_size, move_precision_zostaje, move_precision_cel, move_precision_kolejna):
    probability_apriori = probability.copy()
    for i in range(0, mapa_size):
        for j in range(0, 6):
            if i < 1:
                if j == 2:
                    probability[i][j] = probability_apriori[i][j] * move_precision_zostaje
                if j == 1:
                    probability[i][j] = probability[i][j] + probability_apriori[i][j - 1] * move_precision_cel
                if j == 0:
                    probability[i][j] = probability[i][j] + probability_apriori[i][j - 2] * move_precision_kolejna


def find_max(mapa_size):
    # szukam max,
    temp_max = 0
    # numer pola z wartoscia max
    max_index = 0
    slownik = {}
    for i in range(0, mapa_size):
        for j in range(0, 6):
            if probability[i][j] > temp_max:
                temp_max = probability[i][j]
                max_index_i = i
                max_index_j = j
                slownik = {'max_index_i': i, 'max_index_j': j}
    print('temp_max = ', temp_max)
    return slownik


def show_localized_agent(max_index_i, max_index_j):
    turtle1.penup()  # wylaczenie rysowania
    turtle1.setx((max_index_j + 0.4) * factor)
    turtle1.sety((konwertuj_wspolrzedne_x(max_index_i) - 0.8) * factor)
    # turtle1.write('here')
    turtle1.showturtle()
    print('Agent localized itself')
    # arrow, turtle, circle, square, triangle,classic
    turtle1.shape("turtle")


def konwertuj_wspolrzedne_x(x):
    if x == 0:
        return 4
    if x == 1:
        return 3
    if x == 2:
        return 2
    if x == 3:
        return 1


def is_localized(mapa_size, world_row_position):
    max_index = find_max(mapa_size)
    temp_max = probability[max_index['max_index_i']][max_index['max_index_j']]
    # sprawdzam czy max jest tylko jeden, jezeli tak wstawiam ikone agenta,
    count = 0
    for i in range(0, mapa_size):
        for j in range(0, 6):
            if probability[i][j] == temp_max:
                count = count+1
    if count == 1:
        show_localized_agent(max_index['max_index_i'], max_index['max_index_j'])

# functions ***********THE END*************

# PROGRAM GLOWNY
# rysowani przestrzeni, na podstawie lewej dolnej i prawej górnej koordynaty


drawing_area = Screen()
setworldcoordinates(-20, -20, 1200, 1200)

turtle1 = Turtle()  # definicja agenta,
turtle1.hideturtle()  # ukrycie ikony agenta,
turtle2 = Turtle()  # definicja agenta,
turtle2.hideturtle()  # ukrycie ikony agenta,

# liczba pixeli na jednostkę,
factor = 150

turtle1.speed(10)  # szybkosc rysowania od 1 do 10,

# definicja swiata, jest cykliczny, ruch tylko w prawo,
# przechodzac z pola 6 w prawo trafiamy do 0,
# mapa
mapa = [['red', 'blue', 'red', 'orange', 'red', 'blue'],
        ['blue', 'orange', 'blue', 'orange', 'blue', 'blue'],
        ['orange', 'red', 'orange', 'red', 'yellow', 'red'],
        ['orange', 'orange', 'red', 'blue', 'yellow', 'yellow']]
mapa_size = len(mapa)

# wizualizacja swiata
world_row_position = 4
pomoc = world_row_position
for i in range(0, mapa_size):
    for j in range(0, 6):
        draw_box(j, pomoc, mapa[i][j])
    pomoc -= 1

# inicjacja prawdopodobienstwa
probability = [[], [], [], []]
for i in range(0, mapa_size):
    for j in range(0, 6):
        probability[i].append(1/(mapa_size * 6))

# prezentacja finalnego filra histogramowego
sense_precision = 0.8
move_precision_zostaje = 0.1  # pozostanie w miejscu
move_precision_cel = 0.8  # trafiamy do kratki docelowej
move_precision_kolejna = 0.1  # trafiamy do kolejnej kratki (wariant i)
move_precision_lewo_cel = 0.1  # trafiamy o jedna kratke w lewo od celu
move_precision_prawo_cel = 0.1  # trafiamy o jedna kratke w prawo od celu

# ===================================== MOVE RIGHT TEST =====================================
# sense(sense_precision, 'red', mapa_size)
# move_right(mapa_size, move_precision_zostaje, move_precision_cel, move_precision_kolejna)
#
# sense(sense_precision, 'blue', mapa_size)
# move_right(mapa_size, move_precision_zostaje, move_precision_cel, move_precision_kolejna)
#
# sense(sense_precision, 'red', mapa_size)

# ===================================== MOVE UP TEST ========================================
# sense(sense_precision, 'orange', mapa_size)
# move_up(mapa_size, move_precision_zostaje, move_precision_cel, move_precision_kolejna)
#
# sense(sense_precision, 'blue', mapa_size)
# move_up(mapa_size, move_precision_zostaje, move_precision_cel, move_precision_kolejna)
#
# sense(sense_precision, 'red', mapa_size)

# ===================================== MOVE DOWN TEST ======================================
sense(sense_precision, 'red', mapa_size)
move_down(mapa_size, move_precision_zostaje, move_precision_cel, move_precision_kolejna)

sense(sense_precision, 'blue', mapa_size)
move_down(mapa_size, move_precision_zostaje, move_precision_cel, move_precision_kolejna)

sense(sense_precision, 'orange', mapa_size)

# ===================================== MOVE LEFT TEST ======================================
# sense(sense_precision, 'red', mapa_size)
# move_left(mapa_size, move_precision_zostaje, move_precision_cel, move_precision_kolejna)
#
# sense(sense_precision, 'blue', mapa_size)
# move_left(mapa_size, move_precision_zostaje, move_precision_cel, move_precision_kolejna)
#
# sense(sense_precision, 'red', mapa_size)

# pokazanie obliczonego prawdopodobienstwa lokalizacji robota
show_p(mapa_size, world_row_position)
print(np.sum(probability))
# sprawdzenie czy robot zlokalizowal sie
is_localized(mapa_size, world_row_position)
Screen().exitonclick()
