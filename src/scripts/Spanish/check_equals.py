import difflib

with open("checktrans-output - copia.txt", "r") as f:
    text1 = f.readlines()
with open("checktrans-output.txt", "r") as f2:
    text2 = f2.readlines()

if len(text1) != len(text2):
    raise ValueError("No hay cómo hacer la diferencia!")

for i, (line1, line2) in enumerate(zip(text1, text2), start=1):
    ratio = difflib.SequenceMatcher(None, line1, line2).ratio()
    print(f"Línea {i} similitud: {ratio:.2f}")
    if ratio < 1.0:
        print(f"Copia: {line1}")
        print(f"Actual: {line2}")
print("Listo, patrón.")