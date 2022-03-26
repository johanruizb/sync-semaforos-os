import threading
import os

# Estado neutro
# tenedores = [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]
# tenedoresNumero = [0, 0, 0, 0, 0]

# Estado de inicio
tenedores = [[0, 0], [0, 0], [0, 0], [0, 1], [1, 0]]
tenedoresNumero = [0, 1, 1, 1, 1]
numeroCenas = [0, 0, 0, 0, 0]


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
        # print(f'Izq: {num}')
        tenedores[num][0] -= 1
        tenedores[4][1] -= 1
        tenedoresNumero[num] += 1

    elif num != 0 and tenedores[num - 1][1] - 1 == 0:
        # print(f'Izq: {num}')
        tenedores[num][0] -= 1
        tenedores[num - 1][1] -= 1
        tenedoresNumero[num] += 1


def tenedorDer(num):
    if num == 4 and tenedores[0][0] - 1 == 0:
        # print(f'Der: {num}')
        tenedores[num][1] -= 1
        tenedores[0][0] -= 1
        tenedoresNumero[num] += 1

    elif num != 4 and tenedores[num + 1][0] - 1 == 0:
        # print(f'Der: {num}')
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


def continuar(semf):
    global tenedores
    global tenedoresNumero
    hilo_actual = int(threading.current_thread().getName())

    with semf:
        tenedorDer(hilo_actual)
        tenedorIzq(hilo_actual)

        if tenedoresNumero[hilo_actual] == 2:
            numeroCenas[hilo_actual] += 1
            soltarTenedores(hilo_actual)


"""def iniciar(semf):
    global tenedores
    global tenedoresNumero
    hilo_actual = int(threading.current_thread().getName())
    with semf:
        if hilo_actual < 4:
            if hilo_actual == 0:
                tenedorDer(4)
            tenedorIzq(hilo_actual)


bloquea = threading.Lock()

semaforo = threading.Semaphore(1)
for num_hilo in range(5):
    hilo = threading.Thread(name=f'{num_hilo}', target=iniciar, args=(semaforo,))
    hilo.start()
    hilo.join()
"""
visualizar()

number = input('Numero de iteraciones deseadas: ')
semaforo = threading.Semaphore(5)
for iteraciones in range(int(number)):
    for num_hilo in range(5):
        hilo = threading.Thread(name=f'{num_hilo}', target=continuar, args=(semaforo,))
        hilo.start()
        hilo.join()

clear_console()
print(f'= Resultado despues de {number} iteraciones =')
visualizar()
