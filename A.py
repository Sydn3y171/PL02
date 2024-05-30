#
# Autores: [a20446-a23033-a23290]
# Data: 
#

#--------------------------------------------------------------------------------------------------------------------------
import re
import random

# Atribuição de uma expressão aritmética a uma variável
tmp_01 = 2 * 3 + 4
print("tmp_01:", tmp_01)

# Atribuição de uma expressão aritmética a uma variável
a1_ = 12345 - (5191 * 15)
print("a1_:", a1_)

# Atribuição de um valor introduzido pelo utilizador
idade_valida = int(input("Introduza um valor para idade_valida: "))
print("idade_valida:", idade_valida)

# Atribuição da geração aleatória de um valor
random_value = random.randint(1, 100)
print("random_value:", random_value)

# Atribuição de uma expressão aritmética a uma variável, usando o valor de outra variável
mult_3 = a1_ * 3
print("mult_3:", mult_3)

# Mostrar o valor do cálculo da última instrução
print("Resultado da última instrução (a1_ * 3):", mult_3)
