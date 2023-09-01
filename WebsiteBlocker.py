# %%
##msvcrt only works on the windows command line (cmd)
import msvcrt
import time
from datetime import datetime as dt
import numpy as np
import random as rdm
from WordSearchGame import *

#Windows host file path
#r"C:\Windows\System32\drivers\etc\hosts"
#r"C:\Users\mauro\Documents\Archivos python\Proyectos_Copados\test123"
hostsPath=r"C:\Windows\System32\drivers\etc\hosts"
redirect="127.0.0.1"
#Add the website you want to block, in this list
websites=["www.youtube.com", "youtube.com", "www.reddit.com", "reddit.com", "www.netflix.com","netflix.com"]

horas_bloq = int(input("¿Bloquear redes sociales por cuántas horas? "))
target_hour = horas_bloq + dt.now().hour
target_day = dt.now().day

if target_hour >= 24:
    target_hour = target_hour%24
    target_day = target_day + 1

###Add at the end definitions by webscraping the RAE. 
###Agregar las palabras faltantes

with open(hostsPath,'r+') as file:
    content = file.read()
    for site in websites:
        if not site in content:
            file.write(redirect+" "+site+"\n")

print(f"Acceso denegado a redes sociales por {horas_bloq} horas.")
print()
print("Presione la tecla 'p' para hacer el rompecabezas y detener el bloqueo.")
completed = False

while not completed:
    if (dt(dt.now().year, dt.now().month, target_day, target_hour) < dt.now()):
        break
    
    inp = msvcrt.getche().decode()

    if inp=="p":
        size = 10
        print()
        grid, answers, ans_locations, game_instructions  = Grid(size=size, n_words=4,max_wrd_size=8)

        ans_mapping = {ans:loc for ans,loc in zip(answers,ans_locations)}
        answers = [answ.lower() for answ in answers]

        print()
        words = "Palabras: | "
        for word in answers:
            words += word + " | "
        print(words)
        print(game_instructions)
        print()
        print("  " + "  ".join([str(i) for i in range(0,size)]))
        for j,row in enumerate(grid):
            print(str(j) + " " + "  ".join(row))
        
        answered = False
        prev_answers = []
        prev_locations = []
        while not answered:
            print("Ingresá 'q' para salir del juego y seguir esperando.")
            answer = input("Respuesta: ").strip().split(",")
            if answer[0] == "q":
                print("Esperando...\n")
                print("Presione la tecla 'p' para reintentar la sopa de letras y detener el bloqueo.")
                answered = True
                completed = False

            else:
                invalid = False
                try:
                    answer = [int(ans.strip()) for ans in answer]
                except ValueError:
                    invalid = True

                if invalid:
                    print(f"La respuesta {answer} es inválida. Inténtalo de nuevo.\n")

                elif answer in ans_locations:
                    prev_answers.append(str(answer) + " [c]")
                    ans_locations.remove(answer)
                    print(f"¡Bien! Quedan {len(ans_locations)}. Hasta ahora has dicho: {prev_answers}.")

                else:
                    prev_answers.append(str(answer) + " [i]")
                    # print(f"Respuesta incorrecta. Quedan {len(ans_locations)} palabras. Hasta ahora has dicho: {prev_answers}. Y has encontrado: {}")

            print()
            if len(ans_locations) == 0:
                print("¡Bien, ganaste! Redes sociales satisfactoriamente reactivadas.")
                show_definitions = input("¿Quieres saber las definiciones de las palabras? [y/n]" ).lower().strip()
                if show_definitions == "y":
                    word_definitions = [SearchWordDefinition(word) for word in answers]
                    for w in word_definitions:
                        print(w)
                answered = True
                completed = True
                

with open(hostsPath,'r+') as file:
    content = file.readlines()
    file.seek(0)
    for line in content:
        if not any(site in line for site in websites):
            file.write(line)  ##overwrite lines until reaching the end (the point where sites are added). The pointer goes down after each file.write() call.
    file.truncate()   ##truncate everything left below the pointer (below the overwritten original lines)

print("\n¡Acceso permitido!")


