from CrudSales import CrudSales
from CrudCliente import CrudClients
from CrudProductos import CrudProducts
from utilities import borrarPantalla, gotoxy
from components import Menu
import time

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()
            Client = CrudClients()
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                Client.create()
            elif opc1 == "2":
                Client.update()
            elif opc1 == "3":
                Client.delete()
            elif opc1 == "4":
                Client.consult()
            print("Regresando al menu Clientes...")
            # time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()    
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            producto = CrudProducts()
            opc2 = menu_products.menu()
            if opc2 == "1":
                producto.create()
            elif opc2 == "2":
                producto.update()
            elif opc2 == "3":
                producto.delete()
            elif opc2 == "4":
                producto.consult()
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
            elif opc3 == "2":
                sales.consult()
                time.sleep(2)
            elif opc3 == "3":
                sales.update()
            elif opc3 == "4":
                sales.delete()
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            
borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()