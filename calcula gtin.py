import random


def inverte_codigo(codigo):
  return codigo[::-1]


def calcula_dv(digitos_separados):

  digitos_multiplicados = []

  contador = 1
  for digito in digitos_separados:
    if contador % 2 == 0:
      digitos_multiplicados.append(int(digito) * 3)
    else:
      digitos_multiplicados.append(int(digito))
    if contador == len(digitos_separados):
      break
    else:
      contador += 1

  digitos_somados = sum(digitos_multiplicados)

  if digitos_somados % 10 == 0:
    dv = digitos_somados - digitos_somados
    return dv
  else:
    dv = digitos_somados

    while digitos_somados % 10 != 0:
      digitos_somados += 1

    dv = digitos_somados - dv

    return dv


def gera_codigo_gtin():
  ''' Retorna codigo com inicio '789' + quantidades de digitos digitado.'''

  quantidade_digitos = input("Digite a quantidade de digitos: ")

  digitos_aleatorios = [
    random.randrange(0, 9, 1) for i in range(int(quantidade_digitos) - 4)
  ]

  codigo_completo = ['7', '8', '9']

  for i in digitos_aleatorios:
    codigo_completo.append(str(i))

  codigo_completo = ''.join(codigo_completo)
  dv = calcula_dv(codigo_completo)
  codigo_completo = codigo_completo + str(dv)

  return codigo_completo


def gera_codigo_balanca():
  
  quantidade_digitos_validos = ['4', '5', '6']

  codigos_mascaras = {
  '4':'2CCCCQQQQQQQ0', 
  '5':'2CCCCCQQQQQQ0', 
  '6':'2CCCCCCQQQQQ0'}

  quantidade_digitos = input("Digite a quantidade de digitos(4-6): ")
  
  if quantidade_digitos not in quantidade_digitos_validos:
    print(f'\nQuantidade de digitos: {quantidade_digitos} invalido !!')
    return 0

  codigo_produto = input("Digite o codigo do produto: ")
  
  if len(codigo_produto) > int(quantidade_digitos):
      print(f'\nDigite um codigo de até: {quantidade_digitos} digitos')
      return 0

  quantidade_produto = input("Digite a quantidade/peso: ")

  codigo_mascara = codigos_mascaras[quantidade_digitos]

  #-Começa a Substituir o codigo do produto-
  while len(codigo_produto) != int(quantidade_digitos):
    codigo_produto = '0' + codigo_produto

  quantidade_de_C = len(codigo_produto) * 'C'

  codigo_barra = codigo_mascara.replace(quantidade_de_C, codigo_produto)

  codigo_barra = codigo_barra.replace('C', '0')  
  #-Finaliza a substituição do codigo do produto-

  #-Começa a substituir a quantidade do produto-'
  while len(quantidade_produto) != codigo_mascara.count('Q'):
    quantidade_produto = '0' + quantidade_produto
  quantidade_de_Q = len(quantidade_produto) * 'Q'

  codigo_barra = codigo_barra.replace(quantidade_de_Q, quantidade_produto)

  codigo_barra = codigo_barra.replace('Q', '0')
  #-Finaliza a substituição a quantidade do produto-'

  #-Começa calculo do dv-
  digito_dv = str(calcula_dv(codigo_barra[0:12]))
  codigo_barra = codigo_barra[:-1] + digito_dv 
  print(codigo_barra[0:12])
  #-finaliza calculo dv-

  return codigo_barra


while True:
	print('Selecione uma opção:')
	print('1.Calcula DV de um codigo de barras')
	print('2.Gera codigo de balança')
	print('3.Gera codigo Gtin')
	print('Digite "qq" para finalizar')
	escolhas_validas = ['1', '2', '3', 'qq']
	escolha = input('Escolha uma opção: ')
	
	if escolha not in escolhas_validas:
		print('\n== Escolha não é valida. ==\n')
		pass

	else:

		if escolha == '1':
			codigo_barras = input('\nDigite o codigo de barras sem o DV: ')
			dv_calculado = calcula_dv(codigo_barras)
			print(f'== DV calculado: {dv_calculado} ==\n')

		elif escolha == '2':
			codigo_gerado = gera_codigo_balanca()
			print(f'\n == Codigo gerado: {codigo_gerado} ==\n')

		elif escolha == '3':
			print('\n' + gera_codigo_gtin() + '\n')

		elif escolha == 'qq':
			break


