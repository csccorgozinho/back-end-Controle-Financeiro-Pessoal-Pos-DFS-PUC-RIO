
from flask import Blueprint, request, jsonify
from models import get_connection
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():
    """
    Cadastrar novo usuário
    ---
    tags:
      - Usuário
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: João da Silva
            email:
              type: string
              example: joao@email.com
            senha:
              type: string
              example: 123456
    responses:
      201:
        description: Usuário cadastrado com sucesso
      400:
        description: Erro no cadastro
    """
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", 
                       (data['nome'], data['email'], data['senha']))
        conn.commit()
        return jsonify({'message': 'Usuário cadastrado com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

@api.route('/login_usuario', methods=['POST'])
def login_usuario():
    """
    Login de usuário
    ---
    tags:
      - Usuário
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: joao@email.com
            senha:
              type: string
              example: 123456
    responses:
      200:
        description: Login realizado com sucesso
      401:
        description: Credenciais inválidas
    """
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", 
                   (data['email'], data['senha']))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({'id': user[0], 'nome': user[1]}), 200
    return jsonify({'error': 'Credenciais inválidas'}), 401

@api.route('/deletar_usuario/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    """
    Deletar usuário pelo ID
    ---
    tags:
      - Usuário
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Usuário deletado com sucesso
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Usuário deletado com sucesso'}), 200

@api.route('/gastos/<int:id_usuario>', methods=['GET'])
def gastos(id_usuario):
    """
    Listar gastos do usuário
    ---
    tags:
      - Gastos
    parameters:
      - name: id_usuario
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Lista de gastos retornada
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT categoria, valor, data FROM gastos WHERE id_usuario=?", (id_usuario,))
    gastos = cursor.fetchall()
    conn.close()
    return jsonify(gastos), 200

@api.route('/adicionar_gasto/<int:id_usuario>', methods=['POST'])
def adicionar_gasto(id_usuario):
    """
    Adicionar um gasto para o usuário
    ---
    tags:
      - Gastos
    consumes:
      - application/json
    parameters:
      - name: id_usuario
        in: path
        type: integer
        required: true
        description: ID do usuário
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            categoria:
              type: string
              example: Transporte
            valor:
              type: number
              example: 25.75
            data:
              type: string
              example: 2025-07-01
    responses:
      201:
        description: Gasto adicionado com sucesso
      400:
        description: Erro ao adicionar gasto
    """
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO gastos (id_usuario, categoria, valor, data) VALUES (?, ?, ?, ?)",
                       (id_usuario, data['categoria'], data['valor'], data['data']))
        conn.commit()
        return jsonify({'message': 'Gasto adicionado com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()
        
@api.route('/comparar_gastos/<int:id_usuario>', methods=['GET'])
def comparar_gastos(id_usuario):
    """
    Comparar gastos do mês atual com o mês anterior
    ---
    tags:
      - Gastos
    parameters:
      - name: id_usuario
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Totais dos meses atual e anterior
    """
    conn = get_connection()
    cursor = conn.cursor()
    data = datetime.now()
    mes_atual = f"{data.year}-{data.month:02}"
    mes_anterior = f"{data.year if data.month > 1 else data.year - 1}-{(data.month - 1) if data.month > 1 else 12:02}"

    def total_mes(mes):
        cursor.execute("SELECT SUM(valor) FROM gastos WHERE id_usuario=? AND substr(data, 1, 7)=?", (id_usuario, mes))
        return cursor.fetchone()[0] or 0.0

    total_atual = total_mes(mes_atual)
    total_anterior = total_mes(mes_anterior)
    conn.close()

    return jsonify({
        'mes_atual': mes_atual,
        'total_atual': total_atual,
        'mes_anterior': mes_anterior,
        'total_anterior': total_anterior,
        'diferenca': total_atual - total_anterior
    }), 200
