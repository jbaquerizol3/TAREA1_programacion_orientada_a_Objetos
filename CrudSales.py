from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce

#Ruta Absoluta
path, _ = os.path.split(os.path.abspath(__file__))

# Procesos de las Opciones del Menu Facturacion
class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            time.sleep(2)
            borrarPantalla()
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line);
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
            time.sleep(2)    
            borrarPantalla()
    
    def update(self):
        validar = Valida()
        borrarPantalla()
        json_file = JsonFile(path+'/archivos/invoices.json')
        print('\033c', end='')
        # Imprimir el encabezado
        gotoxy(2, 1)
        print(blue_color + "*" * 68 + reset_color)
        gotoxy(2, 2)
        print(blue_color + "*            ╔════════════════════════════════════════╗            *")
        gotoxy(2, 3)
        print(blue_color + "*            ║        Actualización de Factura        ║            *")
        gotoxy(2, 4)
        print(blue_color + "*            ╚════════════════════════════════════════╝            *")
        gotoxy(2, 5)
        print(blue_color + "*          " +Company.get_business_name()+"         *")
        gotoxy(2, 6)
        print(f"{blue_color}*                  Ingrese el número de factura:                   *")
        gotoxy(2, 8)
        print(blue_color + "*" * 68 + reset_color)
        inv_facture = int(validar.solo_numeros("Número de factura:", 23, 7))
        facture = json_file.find("factura", inv_facture)
        borrarPantalla()
        if not facture:
            gotoxy(35, 8)
            print(f"{red_color}¡La factura no existe!{reset_color}")
            time.sleep(2)
            borrarPantalla()
            return
        facture = facture[0]
        gotoxy(1, 8)
        print(f"{blue_color}╔════════════════════════════════════════════════════════════════════════╗")
        print(f"{blue_color}║ Factura#:F{facture['factura']} {' '*3} Fecha:{facture['Fecha']} {' '*3} cliente:{facture['cliente']}{' '*(26-len(str(facture['cliente'])))}║{reset_color}")
        
        detalles = facture["detalle"]
        for i, detalle in enumerate(detalles):
            gotoxy(1, 10 + i*6)
            print(f"{yellow_color}╔════════════════════════════════════════════════════════════════════════╗{reset_color}")
            print(f"{yellow_color}║ Producto: {detalle['poducto']}{' '*(54-len(detalle['poducto']))}       ║{reset_color}")
            print(f"{yellow_color}║ Precio: {detalle['precio']}{' '*(57-len(str(detalle['precio'])))}      ║{reset_color}")
            print(f"{yellow_color}║ Cantidad: {detalle['cantidad']}{' '*(61-len(str(detalle['cantidad'])))}║{reset_color}")
            print(f"{yellow_color}╚════════════════════════════════════════════════════════════════════════╝{reset_color}")
        y_position = 10 + len(detalles)*6 + 3
        print(f"{yellow_color}╔════════════════════════════════════════════╗")
        print(f"{yellow_color}║   ¿Qué desea actualizar?                   ║")
        print(f"{yellow_color}║   1) Agregar más Productos                 ║")
        print(f"{yellow_color}║   2) Eliminar productos                    ║")
        print(f"{yellow_color}║   Ingrese opción:                          ║")
        print(f"{yellow_color}╚════════════════════════════════════════════╝")
        gotoxy(27, y_position + 3)
        opcion = int(validar.solo_numeros("Error: solamente números", 27, y_position + 4))
        if opcion == 1:
            borrarPantalla()
            json_file = JsonFile(path+'/archivos/products.json')
            productos = json_file.read()
            gotoxy(2, y_position + 5)
            print(blue_color + "╔══════════════════════════════════════════════════════════════════════════════╗" + reset_color)
            gotoxy(2, y_position + 6)
            print(yellow_color + "║" + f"{'ID': <6} {'PRODUCTO': <20} {'STOCK': <10} {'PRECIO': <5}" + " "*(73 - 40) + "║" + reset_color)
            gotoxy(2, y_position + 7)
            print(yellow_color + "╠══════════════════════════════════════════════════════════════════════════════╣" + reset_color)
            for i, producto in enumerate(productos):
                gotoxy(2, y_position + 8 + i)
                print(green_color + "║" + f"{producto['id']: <6} {producto['descripcion']: <20} {producto['stock']: <10} {producto['precio']: <5}" + " "*(77 - len(str(producto['precio'])) - 40) + "║" + reset_color)
            print(f"{yellow_color}¿Qué producto desea ingresar? \n Ingrese ID del producto: ")
            gotoxy(2, y_position + len(productos) + 10)
            id = int(validar.solo_numeros("Error: solo números", 2, y_position + len(productos) + 11))
            product = json_file.find("id", id)

            if not product:
                gotoxy(3,4+len(productos))
                print(f"{red_color}Producto no existe{reset_color}")
                time.sleep(2)
                borrarPantalla()
                return
            product = product[0]
            name = product["descripcion"]
            product_exists = any(detalle["poducto"] == name for detalle in detalles)
            if product_exists:
                gotoxy(27, y_position + 13)
                print(f"{yellow_color}Actualización de la cantidad de producto")
                gotoxy(27, y_position + 14)
                nueva_cantidad = int(validar.solo_numeros("Error: Solo numeros ", 27, y_position + 15))
                for detalle in facture["detalle"]:
                    if detalle["poducto"] == product["descripcion"]:
                        detalle["cantidad"] += nueva_cantidad
                subtotal = round(sum(detalle["precio"] * detalle["cantidad"] for detalle in facture["detalle"]), 2)
                total_sin_descuento = subtotal * (1 + facture["iva"])
                total_con_descuento = total_sin_descuento - facture["descuento"]
                total = round(total_con_descuento, 2)
                facture["subtotal"] = subtotal
                facture["total"] = total
                json_file = JsonFile(path+'/archivos/invoices.json')
                facturas = json_file.read()
                for i, inv_fact in enumerate(facturas):
                    if inv_fact["factura"] == facture["factura"]:
                        facturas[i] = facture
                json_file.save(facturas)
                gotoxy(27, y_position + 16);print(f"{green_color}Cantidad de producto actualizada en la factura{reset_color}")
                time.sleep(2)
                return
            else:
                borrarPantalla()
                gotoxy(27, y_position + 17)
                print(f"{yellow_color}¿Cuántos desea llevar?: ")
                cantidad = int(validar.solo_numeros("Error: Solo números", 27, y_position + 18))
                facture["detalle"].append({"poducto": product["descripcion"], "precio": product["precio"], "cantidad": cantidad})
                subtotal = round(sum(detalle["precio"] * detalle["cantidad"] for detalle in facture["detalle"]), 2)
                total_sin_descuento = subtotal * (1 + facture["iva"])
                total_con_descuento = total_sin_descuento - facture["descuento"]
                total = round(total_con_descuento, 2)
                facture["subtotal"] = subtotal
                facture["total"] = total 
                # Abrir json
                json_file = JsonFile(path+'/archivos/invoices.json')
                facturas = json_file.read()
                for i, inv_fact in enumerate(facturas):
                    if inv_fact["factura"] == facture["factura"]:
                        facturas[i] = facture
                json_file.save(facturas)
                gotoxy(27, y_position + 19);print(f"{green_color}Producto agregado a la factura{reset_color}")
                time.sleep(2)
                return
        elif opcion == 2:
            borrarPantalla()
            facturas = json_file.read()
            print(f"{yellow_color}¿Qué producto desea eliminar?")
            detalles = facture["detalle"]
            for i, detalle in enumerate(detalles):
                producto = detalle["poducto"]
                precio = detalle["precio"]
                cantidad = detalle["cantidad"]
                print(f"{i+1}: PRODUCTO: {producto.ljust(20)} PRECIO: {str(precio).ljust(10)} CANTIDAD: {str(cantidad).ljust(10)}")
            id_producto = int(validar.solo_numeros("Ingrese el ID del producto a eliminar: ", 27, y_position + 12))
            if 1 <= id_producto <= len(detalles):
                producto_eliminar = detalles[id_producto - 1]
                detalles.pop(id_producto - 1)
                subtotal = sum(detalle["precio"] * detalle["cantidad"] for detalle in detalles)
                total_sin_descuento = subtotal * (1 + facture["iva"])
                total_con_descuento = total_sin_descuento - facture["descuento"]
                total = round(total_con_descuento, 2)
                facture["subtotal"] = subtotal
                facture["total"] = total
                for i, factura in enumerate(facturas):
                    if factura["factura"] == facture["factura"]:
                        facturas[i] = facture
                json_file.save(facturas)
                print(f"{green_color}Producto eliminado de la factura. Subtotal y total recalculados.{reset_color}")
                time.sleep(2)
                borrarPantalla()
            else:
                print(f"{red_color}ID de producto no válido. Producto no eliminado.{reset_color}")
                time.sleep(2)
                borrarPantalla()
            time.sleep(2)
        else:
            print("Error: Escoja bien la opción")
            time.sleep(2)
            borrarPantalla()
        gotoxy(27, y_position + 20)
        print(green_color + "*" * 90 + reset_color)

    def delete(self):
        validar = Valida()
        Json_File = JsonFile(path + '/archivos/invoices.json')
        borrarPantalla()
        gotoxy(3, 2); print("=" * 100)
        gotoxy(3, 3); print("                                   Eliminación de factura")
        gotoxy(3, 4); print("=" * 100)

        try:
            facturas = Json_File.read()
            while True:
                for i, fac in enumerate(facturas):
                    gotoxy(3, 5 + i)
                    print(f"{yellow_color}ID: {i+1}   Fecha: {fac['Fecha']: <10}   Cliente: {fac['cliente']: <20}   Subtotal: {fac['subtotal']: <10}   Total: {fac['total']}{reset_color}")
                
                options = int(validar.solo_numeros("Error: Ingrese solo números", 3, len(facturas)+7))
                if options == 0:
                    return
                elif options < 1 or options > len(facturas):
                    print("Opción no válida.")
                    time.sleep(2)
                    borrarPantalla()
                    continue
                factura = facturas.pop(options - 1)  
                for i, fac in enumerate(facturas):
                    fac['factura'] = i + 1
                Json_File.save(facturas)
                print("Factura eliminada exitosamente.")
                time.sleep(2)
                borrarPantalla()
                break 
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)
            borrarPantalla()

    def consult(self):
        borrarPantalla()
        print('\033c', end='')
        line = 1
        gotoxy(2,1);print(yellow_color + "█"*90)
        gotoxy(2,2);print("██" + " "*34 + "Consulta de Venta" + " "*35 + "██")
        gotoxy(5,4);invoice = input("Ingrese Factura: ")
        if invoice.isdigit():
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("    Consulta de Facturas")
            for fac in invoices:
                gotoxy(2, 6); print("┌" + "─"*88 + "┐")
                gotoxy(2, 7); print("│" + f"Factura #{fac['factura']}" + " "*(88 - len(f"Factura #{fac['factura']}")) + "│")
                gotoxy(2, 8); print("├" + "─"*88 + "┤")
                gotoxy(2, 9); print("│" + f"Fecha: {fac['Fecha']}" + " "*(88 - len(f"Fecha: {fac['Fecha']}")) + "│")
                gotoxy(2, 10); print("│" + f"Cliente: {fac['cliente']}" + " "*(88 - len(f"Cliente: {fac['cliente']}")) + "│")
                gotoxy(2, 11); print("│" + f"Total: {fac['total']}" + " "*(88 - len(f"Total: {fac['total']}")) + "│")
                gotoxy(2, 12); print("└" + "─"*88 + "┘")

                detalles = fac["detalle"]
                gotoxy(2, 14); print("┌" + "─"*30 + "┬" + "─"*30 + "┬" + "─"*25 + "┐")
                gotoxy(2, 15); print("│" + "Producto" + " "*(28 - len("Producto")) + "  │" + "  Precio" + " "*(28 - len("Precio")) + "│" + "Cantidad" + " "*(23 - len("Cantidad")) + "  │")
                gotoxy(2, 16); print("├" + "─"*30 + "─" + "─"*30 + "─" + "─"*25 + "┤")
                y_position = 17
                for detalle in detalles:
                    gotoxy(2, y_position)
                    print("│" + f"{detalle['poducto']}" + " "*(28 - len(f"{detalle['poducto']}")) + "  │" + f"{detalle['precio']}" + " "*(28 - len(f"{detalle['precio']}")) + "  │" + f"{detalle['cantidad']}" + " "*(23 - len(f"{detalle['cantidad']}")) + "  │")
                    y_position += 1
                gotoxy(2, y_position)
                print("└" + "─"*30 + "┴" + "─"*30 + "┴" + "─"*25 + "┘")
            suma = reduce(lambda total, invoice: round(total+ invoice["total"], 2), invoices, 0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))
            max_invoice = round(max(totales_map),2)
            min_invoice = round(min(totales_map),2)
            tot_invoices = round(sum(totales_map),2)
            totales_func = [totales_map, max_invoice, min_invoice, tot_invoices]
            gotoxy(2, 20); print("┌" + "─"*30 + "┬" + "─"*30 + "┬" + "─"*25 + "┐")
            gotoxy(2, 21); print("│" + "Total Facturas" + " "*(25 - len("Total Facturas")) + "     │" + "Máximo Factura" + " "*(25 - len("Máximo Factura")) + "     │" + "Mínimo Factura" + " "*(20 - len("Mínimo Factura")) + "     │")
            gotoxy(2, 22); print("├" + "─"*30 + "┼" + "─"*30 + "┼" + "─"*25 + "┤")
            gotoxy(2, 23); print("│" + f"{tot_invoices}" + " "*(25 - len(f"{tot_invoices}")) + "     │" + f"{max_invoice}" + " "*(25 - len(f"{max_invoice}")) + "     │" + f"{min_invoice}" + " "*(20 - len(f"{min_invoice}")) + "     │")
            gotoxy(2, 24); print("└" + "─"*30 + "┴" + "─"*30 + "┴" + "─"*25 + "┘")
            time.sleep(2)
        x = input("presione una tecla para continuar...")




