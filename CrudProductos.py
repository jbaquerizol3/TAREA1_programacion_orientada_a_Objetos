from product import Product
from utilities import gotoxy, borrarPantalla, blue_color, red_color, reset_color, green_color ,purple_color
from company import Company
from iCrud import ICrud
from clsJson import JsonFile
import os, time
from components import Valida

#Ruta Absoluta
path, _ = os.path.split(os.path.abspath(__file__))

class CrudProducts(ICrud):
    def create(self):
        while True:
            borrarPantalla()
            valida = Valida()
            json_file = JsonFile(path+'/archivos/products.json')
            productos = json_file.read()
            try:
                if productos:
                    id = max(producto['id'] for producto in productos) + 1
                else:
                    id = 1

                gotoxy(3,1);name = valida.solo_letras("Ingrese el nombre del producto: ", "Error: SOLO Letras")
                gotoxy(3,2);price = valida.solo_decimales("Ingrese el precio del producto: ", "Error: solo numeros")
                gotoxy(3,3);print("Ingresa el stock:")
                stock = int(valida.solo_numeros(f"Ingrese el stock de {name}: ",3,4))
                producto = Product(id, name, price, stock)
                if json_file.find("descripcion", name):
                    print("¡Error! El producto ya existe en el JSON.")
                    time.sleep(2)
                    borrarPantalla()
                    continue
                data = producto.getJson()
                productos.append(data)
                json_file.save(productos)
                gotoxy(3,5);print(f"Producto registrado con éxito.")
                time.sleep(2)
            except Exception as e:
                print(f"Error al crear el producto: {e}")
                time.sleep(2)
                borrarPantalla()
            opcion = input("¿Desea ingresar otro producto? (s/n): ")
            if opcion.lower() != 's':
                break
    
    def update(self):
        validar = Valida()
        borrarPantalla()
        json_file = JsonFile(path+'/archivos/products.json')
        try:
            while True:
                productos = json_file.read()
                borrarPantalla()
                gotoxy(3, 3)
                print(purple_color+"╔══════════════════════════════════════════════════════════╗")
                gotoxy(3, 4)
                print("║                      LISTA DE PRODUCTOS                  ║")
                gotoxy(3, 5)
                print("╠══════════════════════════════════════════════════════════╣")
                gotoxy(3, 6)
                print("║ No.│ DESCRIPCIÓN                    │ PRECIO  │ STOCK    ║")
                gotoxy(3, 7)
                print("╟──────────────────────────────────────────────────────────╢")
                for i, producto in enumerate(productos, 1):
                    descripcion = producto['descripcion'][:30].ljust(30)
                    precio = str(producto['precio']).ljust(8)
                    stock = str(producto['stock']).ljust(10)
                    gotoxy(3, i+7)
                    print(f"║ {i:<4} {descripcion}  {precio}  {stock}║")
                print("  ╚══════════════════════════════════════════════════════════╝")
                gotoxy(3, len(productos) + 10)
                print("Escoja un producto a actualizar: 0 PARA SALIR")
                option = int(validar.solo_numeros("Error: Solo números ", 3, len(productos) + 11))
                if option == 0:
                    return
                elif option < 1 or option > len(productos):
                    gotoxy(3, len(productos) + 11)
                    print("Opción no válida.")
                    time.sleep(2)
                    borrarPantalla()
                    continue
                producto = productos[option - 1]
                borrarPantalla()
                gotoxy(10, len(productos) + 12)
                print(f"╔{'═'*18}╦{'═'*12}╦{'═'*10}╗")
                gotoxy(10, len(productos) + 13)
                print(f"║ PRODUCTO:        │ PRECIO:    │ STOCK:   ║")
                gotoxy(10, len(productos) + 14)
                print(f"║ {producto['descripcion']:<17}│ {producto['precio']:<10} │ {producto['stock']:<8} ║")
                gotoxy(10, len(productos) + 15)
                print(f"╚{'═'*18}╩{'═'*12}╩{'═'*10}╝")
                while True:
                    gotoxy(3, len(productos) + 15)
                    print("\n¿Qué desea actualizar?  1) Precio 2) Stock 3) Salir Seleccione una opción:\n")
                    select = int(validar.solo_numeros("Error: Solo números", 10, len(productos) + 18))
                    if select == 1:
                        borrarPantalla()
                        try:
                            gotoxy(3, len(productos) + 21)
                            precio = validar.solo_decimales("Ingrese el nuevo precio del producto: ", "Solo decimales")
                            producto["precio"] = precio
                            borrarPantalla()
                        except ValueError as e:
                            gotoxy(3, len(productos) + 22)
                            print(f"Error al actualizar el precio del producto: {e}")
                            time.sleep(2)
                            borrarPantalla()
                    elif select == 2:
                        borrarPantalla()
                        try:
                            gotoxy(3, len(productos) + 19)
                            print("Ingrese el nuevo stock del producto:")
                            stock = int(validar.solo_numeros("Error: Solo números ", 3, len(productos) + 20))
                            producto["stock"] = stock
                            borrarPantalla()
                        except ValueError as e:
                            gotoxy(3, len(productos) + 20)
                            print(f"Error al actualizar el stock del producto: {e}")
                            time.sleep(2)
                            borrarPantalla()
                    elif select == 3:
                        break
                    else:
                        gotoxy(3, len(productos) + 20)
                        print("Opción no válida.")
                        time.sleep(3)
                        borrarPantalla()
                json_file.save(productos)
                gotoxy(15, len(productos) + 22)
                print("  ╔══════════════════════════════════════════════════════════╗")
                gotoxy(15, len(productos) + 23)
                print("  ║                    ACTUALIZADO CON EXITO                 ║")
                gotoxy(15, len(productos) + 24)
                print("  ╚══════════════════════════════════════════════════════════╝")
                time.sleep(2)
        except FileExistsError:
            print("El archivo de productos no se ha encontrado.")
            time.sleep(2)
            borrarPantalla()
            return
    
    def delete(self):
        validar = Valida()
        borrarPantalla()
        json_file = JsonFile(path+'/archivos/products.json')
        try:
            while True:
                productos = json_file.read()
                borrarPantalla()
                print(purple_color + "╔═══════════════════════════════════════════════════════════╗" + reset_color)
                print(purple_color + "║                    LISTA DE PRODUCTOS                     ║" + reset_color)
                print(purple_color + "╠═══════════════════════════════════════════════════════════╣" + reset_color)
                print(purple_color + "║ No. │ DESCRIPCIÓN                     │ PRECIO   │ STOCK  ║" + reset_color)
                print(purple_color + "╟─────┼─────────────────────────────────┼──────────┼────────╢" + reset_color)
                for i, producto in enumerate(productos):
                    gotoxy(1, 6+i)
                    print(purple_color + f"║ {i+1:<4}│ {producto['descripcion']:<32}│ {producto['precio']:<8} │ {producto['stock']:<7}║" + reset_color)
                print(purple_color + "╚═════╧═════════════════════════════════════════════════════╝" + reset_color)
                
                gotoxy(5, len(productos) + 8); print("¿Qué producto deseas eliminar? \n presione 0 PARA SALIR")
                option = int(validar.solo_numeros("Error: solo números ", 5, len(productos) + 10))
                if option == 0:
                    break
                elif option > len(productos):
                    gotoxy(5, len(productos) + 12)
                    print(green_color + "Opción no válida." + reset_color)
                    time.sleep(2)
                    borrarPantalla()
                    continue
                    
                producto = productos[option - 1]
                gotoxy(5, len(productos) + 12)
                print(f"Producto seleccionado: {producto['descripcion']} {producto['precio']} (Stock: {producto['stock']})")
                
                continuar = validar.solo_letras("¿Estás seguro de querer eliminar ese producto? \n1) Si \n2) No \n","Error: solo letras").lower()
                if continuar == "si":
                    productos.remove(producto)
                    json_file.save(productos)
                    gotoxy(5, len(productos) + 21)
                    print(green_color + "╔══════════════════════════════════╗" + reset_color)
                    gotoxy(5, len(productos) + 22)
                    print(green_color + "║   Producto eliminado con éxito   ║" + reset_color)
                    gotoxy(5, len(productos) + 23)
                    print(green_color + "╚══════════════════════════════════╝" + reset_color)
                    time.sleep(2)
                    borrarPantalla()
                elif continuar == "no":
                    continue
                else:
                    print(green_color + "╔══════════════════════════════════╗" + reset_color)
                    gotoxy(5, len(productos) + 22)
                    print(green_color + "║         Opcion no valida         ║" + reset_color)
                    gotoxy(5, len(productos) + 23)
                    print(green_color + "╚══════════════════════════════════╝" + reset_color)
                    time.sleep(2)
                    borrarPantalla()
                    continue
        except FileNotFoundError:
            print(red_color + "No se puede ejecutar esa operación" + reset_color)
            time.sleep(2)
            borrarPantalla()
            return

    def consult(self):
        validar = Valida()
        borrarPantalla()
        json_file = JsonFile(path+'/archivos/products.json')
        try:
            while True:
                borrarPantalla()
                productos = json_file.read()
                gotoxy(5, 2)
                print(purple_color + "Consulta de Producto")
                try:
                    gotoxy(5,3); print("¿Qué producto deseas consultar? \n   Ingresa el ID del producto: ")
                    id = int(validar.solo_numeros("Error: Solo numeros",5,5))
                except ValueError:
                    gotoxy(5,5); print("Por favor, ingresa un ID válido.")
                    time.sleep(2)
                    borrarPantalla()
                    continue
                encontrado = False
                producto = json_file.find("id", id)
                if not producto:
                    gotoxy(5, 6)
                    print("Ese producto no se encuentra dentro de nuestro sistema")
                    time.sleep(2)
                    borrarPantalla()
                else:
                    producto = producto[0]
                    gotoxy(5, 7)
                    print("╔" + "═" * 50 + "╗")
                    gotoxy(5,8)
                    print("║" + f" Producto seleccionado ".center(50) + "║")
                    gotoxy(5,9)
                    print("╠" + "═" * 50 + "╣")
                    gotoxy(5,10)
                    print("║" + f" Descripción: {producto['descripcion']}".ljust(50) + "║")
                    gotoxy(5,11)
                    print("║" + f" Precio: {producto['precio']}".ljust(50) + "║")
                    gotoxy(5,12)
                    print("║" + f" Stock: {producto['stock']}".ljust(50) + "║")
                    gotoxy(5,13)
                    print("╚" + "═" * 50 + "╝")
                    
                continuar = input("¿Deseas continuar consultando productos? (s/n): ")
                if continuar.lower() != 's':
                    break
        except FileNotFoundError:
            gotoxy(5, 8)
            print("El archivo de productos no se ha encontrado.")
            time.sleep(2)
            borrarPantalla()
            return
