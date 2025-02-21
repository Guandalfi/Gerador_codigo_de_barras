import random
import mysql.connector
from random import randint

def inverte_codigo(codigo):
  return codigo[::-1]


import mysql.connector
import re  # Biblioteca para expressões regulares

def corrige_dv():
    host = str(input("Host.: "))
    porta = str(input("Port.: "))
    senha = str(input("Senha: "))
    banco = str(input("Banco: "))
    
    try:
        # Conectar ao banco de dados MySQL
        conexao = mysql.connector.connect(
            host=host,
            user='root',
            port=porta,
            password=senha,
            database=banco,
            auth_plugin='mysql_native_password'
        )
        cursor = conexao.cursor()

        # Selecionar todos os registros da tabela 'arqbar'
        cursor.execute("SELECT codpro, codbarra, qtdeembal FROM arqbar ORDER BY codpro")
        registros = cursor.fetchall()

        maior_codigobarra_valido = None

        # Verificar qual o maior código de barras válido no banco de dados
        for registro in registros:
            codigobarra = str(registro[1])

            # Filtrar apenas os dígitos numéricos no código de barras
            codigobarra = re.sub(r'\D', '', codigobarra)  # Remove qualquer caractere que não seja número

            if len(codigobarra) < 9:  # Certifica-se de que o código tenha pelo menos 8 dígitos
                codigobarra_sem_dv = codigobarra[:-1]  # Código de barras sem o DV
                dv_existente = int(codigobarra[-1])  # Último dígito é o DV existente

                # Verificar se o DV existente é válido
                if calcular_digito_verificador(codigobarra_sem_dv) == dv_existente:
                    if maior_codigobarra_valido is None or int(codigobarra) > int(maior_codigobarra_valido):
                        maior_codigobarra_valido = codigobarra[:-1]

        if maior_codigobarra_valido is None:
            print("Nenhum código de barras válido foi encontrado.")
            return
        print(f"O maior codigo é: {maior_codigobarra_valido}")

        # Ponto de partida: incrementar o maior código de barras válido
        codigobarra_ean = str(int(maior_codigobarra_valido) + 1)
        incremento = 2

        print("Maior código de barras válido encontrado:", maior_codigobarra_valido)

        for registro in registros:
            id_registro, codigobarra, qtdembal = registro

            codigobarra = str(codigobarra)            

            # Filtrar apenas os dígitos numéricos
            codigobarra = re.sub(r'\D', '', codigobarra)

            if len(codigobarra) < 14:  # Trabalhar com códigos de barras com menos 14 dígitos
                codigobarra_ean = str(int(maior_codigobarra_valido) + incremento)
                incremento += 1
                #codigobarra_ean = f"{int(codigobarra):012d}"  # Formatar com 12 dígitos

                # Gerar o novo código de barras a partir do maior código encontrado
                dv_calculado = calcular_digito_verificador(codigobarra_ean)
                novo_codigobarra = f"{codigobarra_ean}{dv_calculado}"
                print(f"Novo codigo gerado para o produto {id_registro}: {novo_codigobarra}")

                # Atualizar o registro no banco de dados com o DV corrigido
                cursor.execute(
                    "INSERT INTO arqbar (codpro, codbarra, qtdeembal) VALUES (%s, %s, %s)",
                    (id_registro, novo_codigobarra, qtdembal)
                )
                conexao.commit()
        cursor.close()
        conexao.close()

    except mysql.connector.Error as err:
        print(f"\nErro: {err}")
        print(f"==Não foi possivel conectar no banco de dados==\n")
        return
    else:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
            print("Conexão com o banco de dados encerrada.")
            return


def calcular_digito_verificador(ean):
    soma = 0
    for i, digito in enumerate(reversed(ean)):
        soma += int(digito) * 3 if i % 2 == 0 else int(digito)
    return (10 - (soma % 10)) % 10


def calcula_dv(digitos_separados):

  digitos_multiplicados = []

  contador = 1
  for digito in digitos_separados:
    if contador % 2 == 0 or len(digitos_separados) == 1:
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
  print('1. Calcula DV de um código de barras')
  print('2. Gera código de balança')
  print('3. Gera código Gtin')
  print('4. Corrige DV codigobarra MySQL')
  print('Digite "qq" para finalizar')

  escolhas_validas = ['1', '2', '3', '4', 'qq']
  escolha = input('Escolha uma opção: ')

  match escolha:
    case '1':
      codigo_barras = input('\nDigite o codigo de barras sem o DV: ')
      dv_calculado = calcular_digito_verificador(codigo_barras)
      print(f'== DV calculado: {dv_calculado} ==\n')

    case '2':
      codigo_gerado = gera_codigo_balanca()
      print(f'\n == Codigo gerado: {codigo_gerado} ==\n')

    case '3':
      print('\n' + gera_codigo_gtin() + '\n')

    case '4':
      print("\n\n")
      corrige_dv()

    case 'qq':
      input("Finalizando programa...")
      break

    case _:
      print("\n== Opcao não é válida==\n")



