from datetime import date

ARCHIVO_LIBROS = "libros.txt"
ARCHIVO_PRESTAMOS = "prestamos.txt"

LIBROS_INICIALES = [
    {"codigo": 1, "titulo": "Python para todos", "autor": "Charles Severance", "estado": "Disponible"},
    {"codigo": 2, "titulo": "Aprende Java", "autor": "Ana Torres", "estado": "Disponible"},
    {"codigo": 3, "titulo": "Bases de datos", "autor": "Carlos Mora", "estado": "Disponible"},
]

def guardar_libros(libros):
    with open(ARCHIVO_LIBROS, "w", encoding="utf-8") as archivo:
        for libro in libros:
            linea = f"{libro['codigo']},{libro['titulo']},{libro['autor']},{libro['estado']}\n"
            archivo.write(linea)

def cargar_libros():
    libros = []
    try:
        with open(ARCHIVO_LIBROS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                if len(datos) >= 4:
                    libros.append({
                        "codigo": int(datos[0]), 
                        "titulo": datos[1],
                        "autor": datos[2], 
                        "estado": datos[3]
                    })
    except FileNotFoundError:
        print("No se encontró libros.txt: se usan los libros iniciales.")
        for libro in LIBROS_INICIALES:
            libros.append(dict(libro))
        guardar_libros(libros)
    return libros

def guardar_prestamos(prestamos):
    with open(ARCHIVO_PRESTAMOS, "w", encoding="utf-8") as archivo:
        for p in prestamos:
            linea = f"{p['numero']},{p['codigo_libro']},{p['estudiante']},{p['fecha']},{p['estado']}\n"
            archivo.write(linea)

def cargar_prestamos():
    prestamos = []
    try:
        with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                if len(datos) >= 5:
                    prestamos.append({
                        "numero": int(datos[0]),
                        "codigo_libro": int(datos[1]),
                        "estudiante": datos[2],
                        "fecha": datos[3],
                        "estado": datos[4]
                    })
    except FileNotFoundError:
        pass
    return prestamos

def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: debe escribir un número entero.")

def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if not texto:
            print("Error: el texto no puede estar vacío.")
        elif "," in texto:
            print("Error: el texto no puede contener comas.")
        else:
            return texto

def buscar_por_codigo(libros, codigo):
    for libro in libros:
        if libro["codigo"] == codigo:
            return libro
    return None

def registrar_libro(libros):
    print("\n--- REGISTRAR LIBRO ---")
    titulo = leer_texto("Título del libro: ")
    autor = leer_texto("Autor del libro: ")
    
    nuevo_codigo = max([l["codigo"] for l in libros], default=0) + 1
    nuevo_libro = {"codigo": nuevo_codigo, "titulo": titulo, "autor": autor, "estado": "Disponible"}
    
    libros.append(nuevo_libro)
    guardar_libros(libros)
    print(f"Éxito: Libro '{titulo}' registrado con el código {nuevo_codigo}.")
    return nuevo_libro

def mostrar_libros(libros):
    print(f"\n{'CÓDIGO':<8} | {'TÍTULO':<30} | {'AUTOR':<25} | {'ESTADO'}")
    print("-" * 85)
    for l in libros:
        print(f"{l['codigo']:<8} | {l['titulo']:<30} | {l['autor']:<25} | {l['estado']}")
    print("-" * 85)
    return len(libros)

def buscar_libro(libros):
    palabra = input("\nIngrese una palabra del título para buscar: ").strip().lower()
    encontrados = 0
    print("\nResultados de búsqueda:")
    for l in libros:
        if palabra in l["titulo"].lower():
            print(f"[{l['codigo']}] {l['titulo']} - {l['autor']} ({l['estado']})")
            encontrados += 1
    
    if encontrados == 0:
        print("No se encontraron libros con esa palabra.")
    return encontrados

def prestar_libro(libros, prestamos):
    print("\n--- PRESTAR LIBRO ---")
    codigo = leer_entero("Ingrese el código del libro a prestar: ")
    libro = buscar_por_codigo(libros, codigo)
    
    if not libro:
        print("Error: El libro no existe.")
        return False
    if libro["estado"] == "Prestado":
        print("Error: El libro ya se encuentra prestado.")
        return False
        
    estudiante = leer_texto("Nombre del estudiante: ")
    num_prestamo = max([p["numero"] for p in prestamos], default=0) + 1
    
    nuevo_prestamo = {
        "numero": num_prestamo,
        "codigo_libro": codigo,
        "estudiante": estudiante,
        "fecha": str(date.today()),
        "estado": "Activo"
    }
    
    prestamos.append(nuevo_prestamo)
    libro["estado"] = "Prestado"
    
    guardar_libros(libros)
    guardar_prestamos(prestamos)
    print("Préstamo registrado exitosamente.")
    return True

def devolver_libro(libros, prestamos):
    print("\n--- DEVOLVER LIBRO ---")
    codigo = leer_entero("Ingrese el código del libro a devolver: ")
    libro = buscar_por_codigo(libros, codigo)
    
    if not libro:
        print("Error: El libro no existe.")
        return False
    if libro["estado"] == "Disponible":
        print("Error: El libro no está prestado actualmente.")
        return False
        
    libro["estado"] = "Disponible"
    for p in prestamos:
        if p["codigo_libro"] == codigo and p["estado"] == "Activo":
            p["estado"] = "Devuelto"
            
    guardar_libros(libros)
    guardar_prestamos(prestamos)
    print("Libro devuelto exitosamente.")
    return True

def mostrar_prestamos(prestamos, libros):
    print(f"\n{'Nº':<4} | {'LIBRO':<30} | {'ESTUDIANTE':<20} | {'FECHA':<12} | {'ESTADO'}")
    print("-" * 90)
    for p in prestamos:
        libro = buscar_por_codigo(libros, p["codigo_libro"])
        titulo = libro["titulo"] if libro else "Desconocido"
        print(f"{p['numero']:<4} | {titulo:<30} | {p['estudiante']:<20} | {p['fecha']:<12} | {p['estado']}")
    print("-" * 90)
    return len(prestamos)

def reporte_general(libros, prestamos):
    total_libros = len(libros)
    disponibles = sum(1 for l in libros if l["estado"] == "Disponible")
    prestados = total_libros - disponibles
    activos = sum(1 for p in prestamos if p["estado"] == "Activo")
    
    try:
        porcentaje = (prestados / total_libros) * 100
    except ZeroDivisionError:
        porcentaje = 0.0

    print("\n--- REPORTE GENERAL ---")
    print(f"Total de libros: {total_libros}")
    print(f"Libros disponibles: {disponibles}")
    print(f"Libros prestados: {prestados}")
    print(f"Total préstamos registrados: {len(prestamos)}")
    print(f"Préstamos activos: {activos}")
    print(f"Porcentaje de libros prestados: {porcentaje:.1f}%")
    return total_libros

def main():
    libros = cargar_libros()
    prestamos = cargar_prestamos()
    
    opcion = 0
    while opcion != 8:
        print("\n==================================")
        print("   BIBLIOTECA DIGITAL TEC AZUAY   ")
        print("==================================")
        print("1. Registrar libro")
        print("2. Mostrar libros")
        print("3. Buscar libro")
        print("4. Prestar libro")
        print("5. Devolver libro")
        print("6. Mostrar préstamos")
        print("7. Reporte general")
        print("8. Salir")
        
        opcion = leer_entero("\nElija una opción: ")
        
        if opcion == 1:
            registrar_libro(libros)
        elif opcion == 2:
            mostrar_libros(libros)
        elif opcion == 3:
            buscar_libro(libros)
        elif opcion == 4:
            prestar_libro(libros, prestamos)
        elif opcion == 5:
            devolver_libro(libros, prestamos)
        elif opcion == 6:
            mostrar_prestamos(prestamos, libros)
        elif opcion == 7:
            reporte_general(libros, prestamos)
        elif opcion == 8:
            guardar_libros(libros)
            guardar_prestamos(prestamos)
            print("Datos guardados. ¡Hasta pronto!")
        else:
            print("Opción no válida: elija un número del 1 al 8.")

if __name__ == "__main__":
    main()