🤖 Automação de Consulta Cadastral - SUFRAMA (SIMNAC)
Este projeto é um robô de automação desenvolvido em Python utilizando Selenium para realizar consultas em massa da situação cadastral de destinatários no sistema SIMNAC (Suframa). O script automatiza o processo de login, navegação, consulta de CNPJs via planilha Excel e retorno dos resultados estruturados.
<img width="1916" height="901" alt="image" src="https://github.com/user-attachments/assets/0ce7a907-a03e-4df6-b239-610b5bbea386" />

🚀 Funcionalidades
Login Automatizado: Gerenciamento seguro de credenciais através de variáveis de ambiente.

Processamento em Lote: Lê uma lista de CNPJs diretamente de um arquivo .xlsx.

Tratamento de Erros Dinâmico: Identifica e trata modais de "CNPJ não encontrado", evitando a interrupção do fluxo.

Coleta de Dados Inteligente: Captura a situação cadastral e registra a data/hora exata da consulta.

Persistência de Dados: Salva os resultados automaticamente na planilha original ao final da execução.

🛠️ Tecnologias Utilizadas
Python 3.x

Selenium WebDriver: Para automação de interface web.

Pandas & Openpyxl: Para manipulação de dados em Excel.

Python-dotenv: Para segurança de dados sensíveis.

📋 Pré-requisitos
Google Chrome instalado.

ChromeDriver compatível com a versão do seu navegador.

Bibliotecas necessárias:

Bash

pip install selenium pandas openpyxl python-dotenv
⚙️ Configuração
1. Variáveis de Ambiente
Crie um arquivo chamado .env na raiz do projeto e adicione suas credenciais:

Snippet de código

CNPJ_SUFRAMA=seu_cnpj_aqui
SENHA_SUFRAMA=sua_senha_aqui
2. Planilha de Dados
Certifique-se de que o arquivo Suframa.xlsx possua as seguintes colunas:

CNPJ: Lista dos CNPJs para consulta.

Status Suframa: Onde o robô gravará o resultado.

DATA: Onde o robô gravará o timestamp.

📂 Estrutura do Código
wait.until(...): Utilizado para garantir a sincronização e evitar erros de elementos não carregados.

Lógica de Navegação: O script acessa o menu "Remetente" e segue para "Consultar Situação Cadastral Destinatário".

Tratamento de Modais: Se um CNPJ for inválido, o robô clica em "Fechar" no modal de erro e continua para o próximo item da lista.

⚠️ Observações Técnicas
O código utiliza EC.presence_of_element_located e EC.element_to_be_clickable para maximizar a estabilidade em conexões lentas ou sistemas single-page (SPA). O uso de time.sleep foi mantido pontualmente para garantir transições suaves de tela onde o JavaScript do site demanda tempo de processamento.
