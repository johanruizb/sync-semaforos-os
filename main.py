import threading
import os

tenedores = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]
tenedoresNumero = [0, 0, 0, 0, 0]
numeroCenas = [0, 0, 0, 0, 0]
hiloSiguiente = 0
hilos = [0, 0, 0, 0, 0]
continua = True


def clear_console():
    os.system('clear')


def visualizar():
    global tenedores
    global tenedoresNumero
    global numeroCenas
    num: int
    for num in range(5):
        print(f'Filosofo {num} - Cenas: {numeroCenas[num]}')
        print(f'Tenedores Izq: {tenedores[num][0]} Der: {tenedores[num][1]}')
        if tenedoresNumero[num] < 2:
            print(f'Tenedores en mano: {tenedoresNumero[num]}\n')
        else:
            print(f'Tenedores en mano: {tenedoresNumero[num]} - Yummy yummy! \n')
            numeroCenas[num] += 1


# tenedores[i][0] = Tenedor izquierdo
# tenedores[i][1] = Tenedor derecho
def tenedorIzq(num):
    if num == 0 and tenedores[4][1] - 1 == 0:
        tenedores[num][0] -= 1
        tenedores[4][1] -= 1
        tenedoresNumero[num] += 1

    elif tenedores[num - 1][1] - 1 == 0:
        tenedores[num][0] -= 1
        tenedores[num - 1][1] -= 1
        tenedoresNumero[num] += 1


def tenedorDer(num):
    if num == 4 and tenedores[0][0] - 1 == 0:
        tenedores[num][1] -= 1
        tenedores[0][0] -= 1
        tenedoresNumero[num] += 1

    elif num != 4 and tenedores[num + 1][0] - 1 == 0:
        tenedores[num][1] -= 1
        tenedores[num + 1][0] -= 1
        tenedoresNumero[num] += 1


def soltarTenedores(num):
    # Soltar tenedor izquierdo
    if num == 0 and tenedores[4][1] + 1 == 1:
        tenedores[num][0] += 1
        tenedores[4][1] += 1
        tenedoresNumero[num] -= 1

    elif num != 0 and tenedores[num - 1][1] + 1 == 1:
        tenedores[num][0] += 1
        tenedores[num - 1][1] += 1
        tenedoresNumero[num] -= 1

    # Soltar tenedor derecho
    if num == 4 and tenedores[0][0] + 1 == 1:
        tenedores[num][1] += 1
        tenedores[0][0] += 1
        tenedoresNumero[num] -= 1
    elif num != 4 and tenedores[num + 1][0] + 1 == 1:
        tenedores[num][1] += 1
        tenedores[num + 1][0] += 1
        tenedoresNumero[num] -= 1


def esperarSiguiente():
    global continua
    siguiente = input("¿Desea continuar?")
    print(siguiente)
    if str(siguiente) == 'n':
        continua = False
    else:
        clear_console()


def continuar():
    global tenedores
    global tenedoresNumero
    global hiloSiguiente
    global continua
    hilo_actual = int(threading.current_thread().getName())

    while continua:
        bloquea.acquire()
        if hilo_actual == hiloSiguiente:
            esperarSiguiente()

            tenedorIzq(hilo_actual)
            tenedorDer(hilo_actual)
            print(f'= Filosofo {hilo_actual} =')
            visualizar()

            if tenedoresNumero[hilo_actual] == 2:
                soltarTenedores(hilo_actual)

            if hiloSiguiente < 4:
                hiloSiguiente += 1
            else:
                hiloSiguiente = 0
        bloquea.release()


def iniciar():
    global tenedores
    global tenedoresNumero
    hilo_actual = int(threading.current_thread().getName())

    bloquea.acquire()
    if hilo_actual < 4:
        if hilo_actual == 0:
            tenedorDer(4)
        tenedorIzq(hilo_actual)
    elif hilo_actual == 4:
        visualizar()
    bloquea.release()


bloquea = threading.Lock()

for num_hilo in range(5):
    hilos[num_hilo] = threading.Thread(name=f'{num_hilo}', target=iniciar)
    hilos[num_hilo].start()

for hilo in hilos:
    hilo.join()

for num_hilo in range(5):
    hilos[num_hilo] = threading.Thread(name=f'{num_hilo}', target=continuar)
    hilos[num_hilo].start()

for hilo in hilos:
    hilo.join()
