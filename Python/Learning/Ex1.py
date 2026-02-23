nome = "Lucas Fernandes"
idade = 22
salario = 3800
ativo = True

print(f"Meu nome é {nome}, tenho {idade} anos, meu salário no banco\
       é de R${salario}, e a minha situação no mercado de trabalho é {ativo} ")

print(type(nome))
print(type(idade))
print(type(salario))
print(type(ativo))

ano = 12
aumento = 0.12
novo_salario = ((salario * aumento) + salario)

print(f"Em um ano, eu terei recebido R${salario * ano}")

print(f"Se receber o aumento que espero irei ganhar R${(salario * aumento)+salario} por mês e no ano será deR${ novo_salario * ano}")

print(f"\nCaixa alta: {nome.upper()}")

comida = "PASTEL"

print(f"\nLower case: {comida.lower()}")