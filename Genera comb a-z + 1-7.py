import os
import string
import itertools

path = "output"
os.makedirs(path, exist_ok=True)

file_path = os.path.join(path, "comb1.txt")

letters = string.ascii_lowercase
numbers = [str(i) for i in range(1, 8)]  # 1-7

with open(file_path, "w") as f:
    first = True
    
    # 1. Combinazioni di 2 lettere
    for c in itertools.product(letters, repeat=2):
        base = "".join(c)
        # Solo lettere
        s = "'" + base + "'"
        if first:
            f.write(s)
            first = False
        else:
            f.write(", " + s)
        
        # Lettere + numero
        for num in numbers:
            s_num = "'" + base + num + "'"
            f.write(", " + s_num)
    
    # 2. Combinazioni di 3 lettere
    for c in itertools.product(letters, repeat=3):
        base = "".join(c)
        # Solo lettere
        s = "'" + base + "'"
        f.write(", " + s)
        
        # Lettere + numero
        for num in numbers:
            s_num = "'" + base + num + "'"
            f.write(", " + s_num)
    
    # 3. Combinazioni di 4 lettere
    for c in itertools.product(letters, repeat=4):
        base = "".join(c)
        # Solo lettere
        s = "'" + base + "'"
        f.write(", " + s)
        
        # Lettere + numero
        for num in numbers:
            s_num = "'" + base + num + "'"
            f.write(", " + s_num)
    
    # 4. Combinazioni di 5 lettere
    for c in itertools.product(letters, repeat=5):
        base = "".join(c)
        # Solo lettere
        s = "'" + base + "'"
        f.write(", " + s)
        
        # Lettere + numero
        for num in numbers:
            s_num = "'" + base + num + "'"
            f.write(", " + s_num)
    
    # 5. Combinazioni di 6 lettere
    for c in itertools.product(letters, repeat=6):
        base = "".join(c)
        # Solo lettere
        s = "'" + base + "'"
        f.write(", " + s)
        
        # Lettere + numero
        for num in numbers:
            s_num = "'" + base + num + "'"
            f.write(", " + s_num)

# Calcolo totale combinazioni
total_combinations = 0
for length in range(2, 7):
    total_combinations += (26 ** length) * 8  # 8 = 1 (solo lettere) + 7 (con numeri)

print("File creato:", file_path)
print("Totale combinazioni:", total_combinations)
print("Formato: combinazioni separate da virgola con apici")