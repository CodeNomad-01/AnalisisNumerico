def registrar_notas():
    datos = [
        {"nombre": "Ana García",      "notas": [85, 92, 78, 88]},
        {"nombre": "Carlos López",    "notas": [72, 68, 75, 70]},
        {"nombre": "María Rodríguez", "notas": [90, 95, 92, 94]},
        {"nombre": "Juan Martínez",   "notas": [55, 60, 58, 52]},
        {"nombre": "Laura Fernández", "notas": [82, 79, 85, 80]},
        {"nombre": "Pedro Sánchez",   "notas": [45, 50, 48, 42]},
        {"nombre": "Sofía Gómez",     "notas": [95, 98, 96, 97]},
        {"nombre": "David Ruiz",      "notas": [65, 62, 68, 64]}
    ]
    return datos

def calcular_promedios(estudiantes):
    for est in estudiantes:
        suma = sum(est["notas"])
        cantidad = len(est["notas"])
        promedio = suma / cantidad
        est["promedio"] = round(promedio, 2) # Redondeamos a 2 decimales
    return estudiantes

def determinar_estado(estudiantes, nota_minima=60):
    for est in estudiantes:
        if est["promedio"] >= nota_minima:
            est["estado"] = "Aprobado"
        else:
            est["estado"] = "Reprobado"
    return estudiantes

def generar_reportes(estudiantes):
    print(f"{'NOMBRE':<20} | {'PROMEDIO':<10} | {'ESTADO':<10}")
    print("-" * 46)

    suma_total = 0
    aprobados = 0
    reprobados = 0

    for est in estudiantes:
        print(f"{est['nombre']:<20} | {est['promedio']:<10} | {est['estado']:<10}")
        suma_total += est["promedio"]

        if est["estado"] == "Aprobado":
            aprobados += 1
        else:
            reprobados += 1

    promedio_curso = suma_total / len(estudiantes)

    print("-" * 46)
    print("\n--- RESUMEN ESTADÍSTICO ---")
    print(f"Promedio general del curso: {promedio_curso:.2f}")
    print(f"Total de Aprobados: {aprobados}")
    print(f"Total de Reprobados: {reprobados}")

    # Extra: Mejor estudiante
    mejor_estudiante = max(estudiantes, key=lambda x: x["promedio"])
    print(f"Mejor promedio: {mejor_estudiante['nombre']} ({mejor_estudiante['promedio']})")

# --- EJECUCIÓN DEL PROGRAMA ---
def main():
    # 1. Registrar (Cargar datos)
    lista_clase = registrar_notas()

    # 2. Calcular Promedios
    lista_clase = calcular_promedios(lista_clase)

    # 3. Determinar Aprobados/Reprobados (Asumiendo nota mínima de 60)
    lista_clase = determinar_estado(lista_clase, nota_minima=60)

    # 4. Generar Reportes
    generar_reportes(lista_clase)

if __name__ == "__main__":
    main()