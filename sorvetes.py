import pymysql
from db_config import connect_db
from flask import jsonify, request, Blueprint

sorvete_bp = Blueprint("sorvetes", __name__)

@sorvete_bp.route("/sorvetes")
def listar_sorvetes():
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM sorvetes")
        rows = cursor.fetchall()

        for row in rows:
            row["disponivel"] = "Sim" if row["disponivel"] == 1 else "Não"

        return jsonify(rows)
    except Exception as e:
        print(e)
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@sorvete_bp.route("/sorvetes/<id>")
def sorvete_by_id(id):
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM sorvetes WHERE id=%s", (id,))
        row = cursor.fetchone()

        if row:
            row["disponivel"] = "Sim" if row["disponivel"] == 1 else "Não"

        return jsonify(row)
    except Exception as e:
        print(e)
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@sorvete_bp.route("/sorvetes", methods=["POST"])
def novo_sorvete():
    try:
        dados = request.json
        disponivel = 1 if dados["disponivel"] == "Sim" else 0

        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            INSERT INTO sorvetes (sabor, preco, tipo, disponivel, descricao)
            VALUES (%s, %s, %s, %s, %s)
        """, (dados["sabor"], dados["preco"], dados["tipo"], disponivel, dados["descricao"]))
        conn.commit()
        return jsonify({"message": "inserido"})
    except Exception as e:
        print(e)
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@sorvete_bp.route("/sorvetes", methods=["PUT"])
def atualizar_sorvete():
    try:
        dados = request.json
        disponivel = 1 if dados["disponivel"] == "Sim" else 0

        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("""
            UPDATE sorvetes
            SET sabor=%s, preco=%s, tipo=%s, disponivel=%s, descricao=%s
            WHERE id=%s
        """, (dados["sabor"], dados["preco"], dados["tipo"], disponivel, dados["descricao"], dados["id"]))
        conn.commit()
        return jsonify({"message": "alterado"})
    except Exception as e:
        print(e)
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@sorvete_bp.route("/sorvetes/<id>", methods=["DELETE"])
def deletar_sorvete(id):
    try:
        conn = connect_db()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("DELETE FROM sorvetes WHERE id=%s", (id,))
        conn.commit()
        return jsonify({"message": "excluido"})
    except Exception as e:
        print(e)
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
