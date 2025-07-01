🧠 Controle Financeiro Pessoal - Back-End
Este é o repositório da API (back-end) do sistema de controle financeiro pessoal, desenvolvido como MVP para a disciplina de Desenvolvimento Full Stack Básico.

🚀 Objetivo
A API permite o cadastro de usuários, inserção e consulta de gastos, comparação de despesas mensais e gerenciamento completo dos dados via requisições HTTP. É integrada a um banco de dados SQLite.

🛠️ Tecnologias Utilizadas
Python 3.x
Flask
Flasgger (Swagger)
SQLite
📦 Instalação e Execução
Clone o repositório:
git clone https://github.com/seu-usuario/back-end.git
cd back-end
pip install -r requirements.txt
python app.py

Acesse a documentação Swagger:

Abra o navegador e vá para: http://localhost:5000/apidocs

📚 Rotas Principais

POST /cadastrar_usuario

POST /adicionar_gasto/{id_usuario}

GET /gastos/{id_usuario}

GET /comparar_gastos/{id_usuario}

DELETE /deletar_usuario/{id}

POST /login_usuario
