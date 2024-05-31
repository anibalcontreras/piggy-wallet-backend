import csv

# Definir los datos
datos = [
    {"id": 1, "gasto": "Compré una hamburguesa en el almuerzo"},
    {"id": 2, "gasto": "Compré frutas y verduras en el supermercado"},
    {"id": 3, "gasto": "Cena en un restaurante italiano"},
    {"id": 4, "gasto": "Pedí una pizza para la cena"},
    {"id": 5, "gasto": "Compré café en Starbucks"},
    {"id": 6, "gasto": "Almuerzo en la cafetería del trabajo"},
    {"id": 7, "gasto": "Compré un pastel de cumpleaños"},
    {"id": 8, "gasto": "Desayuno en una panadería local"},
    {"id": 9, "gasto": "Compré sushi para llevar"},
    {"id": 10, "gasto": "Compré snacks y bebidas para la fiesta"},
    {"id": 11, "gasto": "Pago del boleto del metro"},
    {"id": 12, "gasto": "Llené el tanque de gasolina del coche"},
    {"id": 13, "gasto": "Pago del peaje en la autopista"},
    {"id": 14, "gasto": "Compré un boleto de avión para las vacaciones"},
    {"id": 15, "gasto": "Pago del taxi para ir al aeropuerto"},
    {"id": 16, "gasto": "Pago del boleto de autobús"},
    {"id": 17, "gasto": "Renta de un coche para el fin de semana"},
    {"id": 18, "gasto": "Pago del servicio de transporte escolar"},
    {"id": 19, "gasto": "Compré una bicicleta nueva"},
    {"id": 20, "gasto": "Mantenimiento del coche en el taller"},
    {"id": 21, "gasto": "Pago del alquiler del apartamento"},
    {"id": 22, "gasto": "Pago de la hipoteca de la casa"},
    {"id": 23, "gasto": "Pago de la factura de la electricidad"},
    {"id": 24, "gasto": "Pago de la factura del agua"},
    {"id": 25, "gasto": "Compré muebles nuevos para la sala"},
    {"id": 26, "gasto": "Pago del servicio de internet"},
    {"id": 27, "gasto": "Reparación de la plomería en la cocina"},
    {"id": 28, "gasto": "Pintura nueva para las paredes del dormitorio"},
    {"id": 29, "gasto": "Pago del seguro de la vivienda"},
    {"id": 30, "gasto": "Compré cortinas nuevas para las ventanas"},
    {"id": 31, "gasto": "Pago de la matrícula de la universidad"},
    {"id": 32, "gasto": "Compré libros de texto para el semestre"},
    {"id": 33, "gasto": "Pago del curso online de programación"},
    {"id": 34, "gasto": "Inscripción a clases de inglés"},
    {"id": 35, "gasto": "Pago de la excursión escolar"},
    {"id": 36, "gasto": "Pago de la colegiatura del colegio privado"},
    {"id": 37, "gasto": "Compré útiles escolares para el nuevo ciclo"},
    {"id": 38, "gasto": "Pago de la suscripción a una plataforma educativa"},
    {"id": 39, "gasto": "Pago del curso de verano para niños"},
    {"id": 40, "gasto": "Pago de la conferencia sobre marketing digital"},
    {"id": 41, "gasto": "Pago de la consulta médica"},
    {"id": 42, "gasto": "Compra de medicamentos en la farmacia"},
    {"id": 43, "gasto": "Pago del seguro médico"},
    {"id": 44, "gasto": "Pago de la terapia física"},
    {"id": 45, "gasto": "Pago de la consulta dental"},
    {"id": 46, "gasto": "Compra de vitaminas y suplementos"},
    {"id": 47, "gasto": "Pago de la cirugía ambulatoria"},
    {"id": 48, "gasto": "Pago del servicio de ambulancia"},
    {"id": 49, "gasto": "Pago del examen de laboratorio"},
    {"id": 50, "gasto": "Pago de la sesión de terapia psicológica"},
    {"id": 51, "gasto": "Compré boletos para el cine"},
    {"id": 52, "gasto": "Pago de la suscripción a Netflix"},
    {"id": 53, "gasto": "Compré entradas para un concierto"},
    {"id": 54, "gasto": "Pago del servicio de streaming de música"},
    {"id": 55, "gasto": "Pago del evento deportivo"},
    {"id": 56, "gasto": "Compré un videojuego nuevo"},
    {"id": 57, "gasto": "Alquiler de una película en línea"},
    {"id": 58, "gasto": "Pago del servicio de cable"},
    {"id": 59, "gasto": "Compré un libro de aventuras"},
    {"id": 60, "gasto": "Pago del club social mensual"},
    {"id": 61, "gasto": "Depósito en la cuenta de ahorros"},
    {"id": 62, "gasto": "Transferencia a la cuenta de ahorros a largo plazo"},
    {"id": 63, "gasto": "Apertura de una nueva cuenta de ahorros"},
    {"id": 64, "gasto": "Transferencia al fondo de emergencia"},
    {"id": 65, "gasto": "Pago al plan de ahorro para la jubilación"},
    {"id": 66, "gasto": "Depósito en la cuenta de ahorros para la universidad"},
    {"id": 67, "gasto": "Transferencia al fondo de ahorro para la casa"},
    {"id": 68, "gasto": "Depósito en el certificado de depósito"},
    {"id": 69, "gasto": "Pago al plan de ahorro automático mensual"},
    {"id": 70, "gasto": "Transferencia al fondo de ahorro de viaje"},
    {"id": 71, "gasto": "Compra de acciones en la bolsa"},
    {"id": 72, "gasto": "Inversión en un fondo mutuo"},
    {"id": 73, "gasto": "Compra de bonos del gobierno"},
    {"id": 74, "gasto": "Pago al asesor financiero"},
    {"id": 75, "gasto": "Compra de bienes raíces para inversión"},
    {"id": 76, "gasto": "Inversión en una startup"},
    {"id": 77, "gasto": "Compra de criptomonedas"},
    {"id": 78, "gasto": "Aporte al fondo de inversión"},
    {"id": 79, "gasto": "Pago de la comisión de corretaje"},
    {"id": 80, "gasto": "Inversión en un fondo indexado"},
]

# Escribir los datos en un archivo CSV
with open('AI/sets//gastos.csv', mode='w', encoding='utf-8', newline='') as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=["id", "gasto"])
    escritor.writeheader()
    escritor.writerows(datos)

print("Archivo CSV generado con éxito.")
