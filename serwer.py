import socket, pickle, random
from projectile import Projectile
from mob import Mob
from player import Player
from settings import *


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("127.0.0.1", 4444))
serversocket.listen(2)


p1_posy = HEIGHT - p_height - 50
p2_posy = HEIGHT - p_height - 50


connection = []



mobs = []
for i in range(0, 7):
    m = [random.randrange(0, WIDTH, 20), random.randrange(-100, -40, 5), mob_size, mob_size, RED, random.randrange(2, 5, 1), random.randrange(-3, 3, 1), i, 100]
    mobs.append(m)

bullets_p1 = []
bullets_p2 = []
players = []
mobs_left = 30
conn_len = 0
gameState = [round_score, mobs_left, conn_len]
#------------------------# 0                                      # 1                       #2      #3        #4           #5
arr = [[p1_pos, p1_posy, 30, 40, BLUE,100], [p2_pos, p2_posy, 30, 40, (0, 255, 0), 100,], mobs, bullets_p1, bullets_p2, gameState]

vel = 6
count = 0
waveCount = 50

def process_positions(array, gracz1, player_2):
    global jumpCount, waveCount, mobs_left, bullet_timer, bullet_amount, conn_len
    conn_len = len(connection)

    # -------------- MOBY I KOLIZJE Z GRACZEM NR 1 -------------------------------------

    mob_r_x = random.randrange(0, WIDTH, 20)
    mob_r_y = random.randrange(-100, -40, 5)
    mob_r_vy = random.randrange(2, 5, 1)
    mob_r_vx = random.randrange(-3, 3, 1)

    for i in range(0, len(mobs)):
        if mobs[i][7] == i and (arr[0][0] + p_width > mobs[i][0] and arr[0][0] < mobs[i][0] + mob_size) and arr[0][1] < mobs[i][1]:
            mobs[i][1] = mob_r_y
            mobs[i][0] = mob_r_x
            arr[0][4] = DARK_RED
            arr[0][5] -= 10
            waveCount -= 1
            arr[5][0] -= mob_point

        arr[0][4] = (0, 0, 255)

    # ------------- KOLIZJA MOBÓW Z POCISKAMI ----------------
        for b in bullets_p1:
            if mobs[i][1]+mob_size > b.y:
                if mobs[i][0] < b.x and mobs[i][0]+mob_size > b.x :
                    mobs[i][8] -= bullet_dmg
                    waveCount -= 1
                    mobs[i][1] -= bullet_knockout
                    arr[5][0] -= mob_point
                    bullets_p1.pop(bullets_p1.index(b))
                    if mobs[i][8] < 0:
                        arr[5][1] -= 1
                        mobs[i][1] = mob_r_y
                        mobs[i][0] = mob_r_x
                        mobs[i][8] = 100

        for b in bullets_p2:
            if mobs[i][1]+mob_size > b.y:
                if mobs[i][0] < b.x and mobs[i][0]+mob_size > b.x :
                    mobs[i][8] -= bullet_dmg
                    waveCount -= 1
                    mobs[i][1] -= bullet_knockout
                    arr[5][0] -= mob_point
                    bullets_p2.pop(bullets_p2.index(b))
                    if mobs[i][8] < 0:
                        arr[5][1] -= 1
                        mobs[i][1] = mob_r_y
                        mobs[i][0] = mob_r_x
                        mobs[i][8] = 100

    # ---------------- MOBY I KOLIZJE Z GRACZEM NR 2---------
    for i in range(0, len(mobs)):
        if mobs[i][7] == i and (arr[1][0] + p_width > mobs[i][0] and arr[1][0] < mobs[i][0] + mob_size) and arr[1][1] < mobs[i][1]:
            mobs[i][1] = mob_r_y
            mobs[i][0] = mob_r_x
            arr[1][4] = DARK_RED
            arr[1][5] -= 10

            waveCount -= 1
            arr[5][0] -= mob_point
        arr[1][4] = GREEN

    # print(waveCount)
    # if waveCount < 0:
    #     for m in mobs:
    #         m[2] = mob_size
    #         m[3] = mob_size

    # ---------------- RUCH MOBÓW --------------------------
    for i,m in enumerate(mobs):
        m[1] += m[5]
        m[0] += m[6]

        if m[1] >= HEIGHT-10:
            m[1] = mob_r_y
            m[0] = mob_r_x
            arr[5][0] -= mob_point

        if m[0] <= 0:
            m[6] = m[6] * -1
        if m[0] >= WIDTH-mob_size:
            m[6] = m[6] * -1
    # ----------------- RUCH GRACZY -------------------------
    if gracz1[0]:
        arr[0][0] -= vel
    elif gracz1[1]:
        arr[0][0] += vel
    if gracz2[0]:
        arr[1][0] -= vel
    elif gracz2[1]:
        arr[1][0] += vel

    # # ---------- BLOKADA WYCHODZENIA POZA EKRAN -----------

    if arr[0][0] <= 0:
        arr[0][0] = 0

    if arr[0][0] >= WIDTH - 30:
        arr[0][0] = WIDTH - 30

    if arr[1][0] <= 0:
        arr[1][0] = 0

    if arr[1][0] >= WIDTH - 30:
        arr[1][0] = WIDTH - 30
    # --------------------STRZELANIE ---------------------------
    dt1 = gracz1[8]
    dt2 = gracz1[9]

    if gracz1[2]:
        if len(bullets_p1) < bullet_amount:
            b_center = arr[0][0] + p_width//2
            bullet_timer -= dt1

            if bullet_timer < 0.9:
                bullet_timer = 1
                b = Projectile(b_center, arr[0][1], 4, (255,255,0))
                bullets_p1.append(b)

    if gracz2[2]:
        if len(bullets_p2) < bullet_amount:
            b_center = arr[1][0] + p_width//2
            bullet_timer -= dt2
            if bullet_timer < 0.9:
                bullet_timer = 1
                b = Projectile(b_center, arr[1][1], 4, (255,255,0))
                bullets_p2.append(b)

    for bullet in bullets_p1:
        if bullet.y > 0:
            bullet.y -= bullet.vel
        else:
            bullets_p1.pop(bullets_p1.index(bullet))

    for bullet in bullets_p2:
        if bullet.y > 0:
            bullet.y -= bullet.vel
        else:
            bullets_p2.pop(bullets_p2.index(bullet))

    # ------------------- ROZGRYWKA -------------------------


    return array

def waiting_for_connections():
    print("Waiting for connection...")
    while len(connection) < 2:

        conn, addr = serversocket.accept()
        connection.append(conn)
        print(addr, ' connected.')


def recieve_information():
    gracz1_info = pickle.loads(connection[0].recv(1024))
    gracz2_info = pickle.loads(connection[1].recv(1024))

    return gracz1_info, gracz2_info


waiting_for_connections()

while True:

    data_arr = pickle.dumps(arr)

    connection[0].send(data_arr)
    connection[1].send(data_arr)

    gracz1, gracz2 = recieve_information()

    arr = process_positions(arr, gracz1, gracz2)








