from customer import Client, RegularClient, VipClient
from utilities import gotoxy, borrarPantalla, blue_color, red_color, green_color, yellow_color,reset_color
from company import Company
from iCrud import ICrud
from clsJson import JsonFile
import os, time
from components import Valida

#Ruta Absoluta
path, _ = os.path.split(os.path.abspath(__file__))

#Crud de Clientes 
class CrudClients(ICrud):
    def create(self):
        def print_box(text):
            lines = text.split('\n')
            max_length = max(len(line) for line in lines)
            print("╔" + "═" * (max_length + 2) + "╗")
            for line in lines:
                print("║ " + line.ljust(max_length) + " ║")
            print("╚" + "═" * (max_length + 2) + "╝")
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(30, 2);print(blue_color + "Registro de Cliente 📃" + reset_color)
        gotoxy(17, 3);print(yellow_color + Company.get_business_name() + reset_color)
        gotoxy(5, 5)
        name = validar.solo_letras("Cual es el primer nombre que desea ingresar del cliente?: ", "Ingrese bien el nombre")
        gotoxy(5, 7)
        last_name = validar.solo_letras(f"cual es el segundo nombre de {name}: ", "Ingrese bien el apellido")
        gotoxy(5, 9)
        dni = input(f"          ------>   |¿cual es el dni del cliente?: ")
        validate_dni = validar.cedula(dni)
        if validate_dni:
            gotoxy(5, 13)
            valor = input(f"¿Es cliente regular o vip? (r o v): ").lower()
            if valor == "r":
                client = RegularClient(first_name=name, last_name=last_name, dni=dni, card=True)
            elif valor == "v":
                client = VipClient(first_name=name, last_name=last_name, dni=dni)
            else:
                gotoxy(5, 12)
                print_box(f"{red_color}Valor no valido{reset_color}")
                time.sleep(2)
                borrarPantalla()
                return
        else:
            gotoxy(5, 14);print(blue_color + "=" * 50 + reset_color)
            gotoxy(5, 15);print(red_color + "DNI INVALIDO" + reset_color)
            gotoxy(5, 16);print(blue_color + "=" * 50 + reset_color)
            time.sleep(2)
            borrarPantalla()
            return
        json_file = JsonFile(path + '/archivos/clients.json')
        clientes = json_file.read()
        if json_file.find("dni", dni):
            gotoxy(5, 17);print(red_color+"El DNI ya existe en el JSON."+reset_color)
            borrarPantalla()
            time.sleep(2)
            return
        data = client.getJson()
        clientes.append(data)
        json_file.save(clientes)
        gotoxy(30, 14);print(blue_color + "=" * 50 + reset_color)
        gotoxy(30, 15);print("Cliente registrado con éxito.")
        gotoxy(30, 16);print(blue_color + "=" * 50 + reset_color)
        time.sleep(2)
    
    def update(self):
        validar = Valida()
        borrarPantalla()
        json_file = JsonFile(path+'/archivos/clients.json')
        clientes = json_file.read()
        while True:
            borrarPantalla()
            print('\033c', end='')
            gotoxy(30, 2)
            print(blue_color + "Actualización de Cliente" + reset_color)
            gotoxy(5, 4)
            print(red_color + "Nº".ljust(5) + "CLIENTE:".ljust(20) + "DNI:".ljust(10) + reset_color)
            print("-" * 35)
            for i, cliente in enumerate(clientes):
                nombre = cliente['nombre'] + ' ' + cliente['apellido']
                dni = cliente['dni']
                gotoxy(5, i + 6)
                print(str(i+1).ljust(5) + nombre.ljust(20) + dni.ljust(10))
            print("-" * 35)
            time.sleep(2)
            try:
                gotoxy(5, len(clientes) + 7); print("Seleccione el cliente que desea actualizar (0 para salir):")
                seleccion = int(validar.solo_numeros("Error, solo numeros: ", 5, len(clientes) + 8))
                if seleccion == 0:
                    break
                elif seleccion > len(clientes):
                    print("Cliente no válido.")
                    borrarPantalla()
                    continue
            except ValueError:
                print("Por favor, ingrese un número válido.")
                continue

            cliente = clientes[seleccion - 1]
            try:
                gotoxy(5, len(clientes) +11);print("¿Qué desea actualizar?")
                gotoxy(5, len(clientes) +12);print(" 1) Nombre y apellido ✏️")
                gotoxy(5, len(clientes) +13);print(" 2) DNI 💳")
                opcion = int(validar.solo_numeros("Error,solo numeros", 10, len(clientes) + 14))
                if opcion != 1 and opcion != 2:
                    print("Opción no válida.")
                    borrarPantalla()
                    continue
            except ValueError:
                print("Por favor, ingrese un número válido.")
                borrarPantalla()
                continue

            if opcion == 1:
                try:
                    gotoxy(5, len(clientes) + 15);name = validar.solo_letras("Ingrese el nuevo nombre del cliente: ", "Error solo letras")
                    gotoxy(5, len(clientes) + 16);apellido = validar.solo_letras("Ingrese el nuevo apellido del cliente: ", "error solo letras")
                    cliente["nombre"] = name
                    cliente["apellido"] = apellido
                except Exception as e:
                    gotoxy(5, len(clientes) + 17);print(f"Error al actualizar los datos del cliente: {e}")
                    borrarPantalla()
                    continue
            elif opcion == 2:
                try:
                    dni = input("Ingrese el nuevo DNI del cliente: ")
                    dni_validate = validar.cedula(dni)
                    if dni_validate:
                        if json_file.find("dni", dni):
                            gotoxy(5, len(clientes) + 18);print("El DNI ingresado ya pertenece a otro cliente.")
                            time.sleep(2)
                            borrarPantalla()
                            continue
                        cliente["dni"] = dni
                except Exception as e:
                    gotoxy(5, len(clientes) + 19);print(f"Error al actualizar el DNI del cliente: {e}")
                    borrarPantalla()
                    continue

            try:
                json_file.save(clientes)
                gotoxy(5, len(clientes) + 20);print(red_color + "😊Cliente actualizado con éxito😊" + reset_color)
                time.sleep(2)
                borrarPantalla()
            except Exception as e:
                gotoxy(5, len(clientes) + 17);print(f"Error al guardar los cambios: {e}")
                borrarPantalla()
                continue
    def delete(self):
        validar = Valida()
        borrarPantalla()
        while True:
            try:
                json_file = JsonFile(path+'/archivos/clients.json')
                clientes = json_file.read()

                # Imprimir lista de clientes como tabla
                gotoxy(5, 2)
                print(blue_color + "Eliminación de Cliente 🧍")
                gotoxy(5, 3)
                print("Nº".ljust(5) + "CLIENTE:".ljust(25) + "DNI:".ljust(15))
                print("-" * 45)

                for i, cliente in enumerate(clientes):
                    nombre = cliente['nombre'] + ' ' + cliente['apellido']
                    dni = cliente['dni']
                    gotoxy(5, i+4)
                    print(str(i+1).ljust(5) + nombre.ljust(25) + dni.ljust(15))

                gotoxy(5, len(clientes) + 4)
                print("-" * 45)
                gotoxy(5, len(clientes) + 5)
                print("Escoja el cliente a eliminar: 0 para salir")
                seleccion = int(validar.solo_numeros("Error, solo numero:", 5, len(clientes) + 6))
                if seleccion == 0:
                    break
                elif seleccion < 1 or seleccion > len(clientes):
                    print("Número de cliente no válido.")
                    time.sleep(2)
                    borrarPantalla()
                    continue
                cliente = clientes.pop(seleccion - 1)
                json_file.save(clientes)
                print("Cliente eliminado con éxito ✔️")
                time.sleep(2)
                borrarPantalla()
            except FileNotFoundError:
                print("El archivo de clientes no se ha encontrado.")
                time.sleep(2)
                borrarPantalla()
                return
    def consult(self):
        validar = Valida()
        while True:
            try:
                json_file = JsonFile(path+'/archivos/clients.json')
                clientes = json_file.read()

                # Imprimir lista de clientes como tabla
                borrarPantalla()
                print('\033c', end='')
                gotoxy(5, 2)
                print(blue_color + "Consulta de Cliente")
                gotoxy(5, 3)
                print("Nº".ljust(5) + "CLIENTE:".ljust(25))
                gotoxy(5, 4)
                print("-" * 30)

                for i, cliente in enumerate(clientes):
                    nombre = cliente['nombre'] + ' ' + cliente['apellido']
                    gotoxy(5, i+5)
                    print(str(i+1).ljust(5) + nombre.ljust(25))

                gotoxy(5, len(clientes) + 5)
                print("-" * 30)
                gotoxy(5, len(clientes) + 6)
                print("Seleccione el cliente que desea consultar (0 para salir):")

                seleccion = int(validar.solo_numeros("Error, solo numero: ", 5, len(clientes) + 8))
                if seleccion == 0:
                    break
                elif seleccion < 1 or seleccion > len(clientes):
                    print("Cliente no válido 👎.")
                    time.sleep(2)
                    borrarPantalla()
                    continue
                
                cliente = clientes[seleccion - 1]
                borrarPantalla()
                print(green_color + "=" * 70 + reset_color)
                print(f"\n1. Cliente: {cliente['nombre']} {cliente['apellido']} 😊")
                print(f"3. DNI: {cliente['dni']} 🔍")
                print(f"4. Límite o Descuento: {cliente['valor']} 💳")
                print(green_color + "=" * 70 + reset_color)
                time.sleep(2)
            except FileNotFoundError:
                print("El archivo de clientes no se ha encontrado.")
                time.sleep(2)
                borrarPantalla()
                return
