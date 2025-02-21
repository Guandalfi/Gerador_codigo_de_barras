Utilitário de Código de Barras

Este script em Python oferece funcionalidades para manipulação de códigos de barras, incluindo cálculo de dígitos verificadores, geração de códigos de barras GTIN e para balanças, além da correção de dígitos verificadores em registros armazenados em um banco de dados MySQL.

Funcionalidades

1. Cálculo de Dígitos Verificadores (Opção 1)

Entrada: Um código de barras sem o dígito verificador.

Saída: O dígito verificador calculado.

Uso: Permite validar ou corrigir códigos de barras gerados manualmente.

2. Geração de Códigos de Barras para Balanças (Opção 2)

Entrada:

Quantidade de dígitos (4 a 6)

Código do produto

Quantidade ou peso do produto

Saída: Um código de barras formatado corretamente para uso em balanças.

Uso: Adequado para sistemas que precisam gerar etiquetas de produtos pesáveis.

3. Geração de Códigos de Barras GTIN (Opção 3)

Entrada: Quantidade de dígitos desejada.

Saída: Um código de barras GTIN válido com dígito verificador calculado.

Uso: Para gerar códigos de produtos de acordo com padrões comerciais.

4. Correção de Dígitos Verificadores no MySQL (Opção 4)

Entrada: Credenciais do banco de dados (host, porta, senha, banco).

Processo:

Conecta ao banco de dados MySQL.

Identifica os registros da tabela arqbar com códigos de barras inválidos.

Calcula novos dígitos verificadores e insere os códigos corrigidos.

Saída: Atualização dos registros com códigos de barras corrigidos.

Uso: Para corrigir erros em bases de dados e garantir a integridade dos códigos armazenados.

Como Usar

Execute o script Python.

Escolha a opção desejada no menu interativo.

Insira as informações conforme solicitado.

O resultado será exibido no console ou salvo no banco de dados (para a opção 4).

Requisitos

Python 3.x

Biblioteca mysql-connector-python

Para instalar dependências, execute:

pip install mysql-connector-python

Contribuição

Sinta-se à vontade para contribuir para este projeto fazendo um fork do repositório e criando pull requests. Relatórios de bugs e sugestões de melhorias são bem-vindos.

Licença

Este projeto está licenciado sob a Licença MIT.

