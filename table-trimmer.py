import sqlite3
import os

def encontrar_arquivos_db():
    """ Encontra todos os arquivos .db no diretório atual. """
    arquivos_db = [arq for arq in os.listdir('.') if arq.endswith('.db')]
    return arquivos_db

def escolher_arquivo_db(arquivos_db):
    """ Permite ao usuário escolher um arquivo de banco de dados para investigar. """
    if not arquivos_db:
        print("Não foram encontrados arquivos .db neste diretório.")
        return None
    for idx, arquivo in enumerate(arquivos_db, start=1):
        print(f"{idx}. {arquivo}")
    escolha = int(input("Escolha um arquivo pelo número: "))
    return arquivos_db[escolha - 1]

def listar_tabelas(db_path):
    """ Lista todas as tabelas no banco de dados SQLite. """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    conn.close()
    return [tabela[0] for tabela in tabelas]

def escolher_tabela(tabelas):
    """ Permite ao usuário escolher uma tabela para investigar. """
    for idx, tabela in enumerate(tabelas, start=1):
        print(f"{idx}. {tabela}")
    escolha = int(input("Escolha uma tabela pelo número: "))
    return tabelas[escolha - 1]

def listar_colunas(db_path, tabela_escolhida):
    """ Lista todas as colunas de uma tabela selecionada, tratando corretamente os nomes. """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({tabela_escolhida})")
    colunas = cursor.fetchall()
    conn.close()
    return [f"{coluna[1]}" for coluna in colunas]

def criar_nova_tabela(db_path, tabela_origem, nova_tabela, colunas):
    """ Cria uma nova tabela apenas com as colunas selecionadas, delimitando nomes de colunas. """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Adiciona aspas duplas ao redor dos nomes das colunas para lidar com espaços e caracteres especiais
    colunas_str = ", ".join([f'"{coluna}"' for coluna in colunas])
    cursor.execute(f"CREATE TABLE {nova_tabela} AS SELECT {colunas_str} FROM {tabela_origem}")
    conn.commit()
    conn.close()

def main():
    arquivos_db = encontrar_arquivos_db()
    db_path = escolher_arquivo_db(arquivos_db)
    if db_path is None:
        return
    
    tabelas = listar_tabelas(db_path)
    if not tabelas:
        print("Não foram encontradas tabelas no banco de dados.")
        return

    print("\nTabelas encontradas no banco de dados:")
    tabela_escolhida = escolher_tabela(tabelas)
    colunas = listar_colunas(db_path, tabela_escolhida)

    print("\nColunas encontradas na tabela:")
    for idx, coluna in enumerate(colunas, start=1):
        print(f"{idx}. {coluna}")

    colunas_selecionadas = input("\nDigite os números das colunas que deseja manter, separados por vírgula (ex: 1, 3, 4): ")
    indices = [int(x.strip()) - 1 for x in colunas_selecionadas.split(',')]
    colunas_escolhidas = [colunas[i] for i in indices]

    print("\nColunas selecionadas: " + ", ".join(colunas_escolhidas))
    confirmacao = input("Deseja criar uma nova tabela com essas colunas? (s/n): ")
    if confirmacao.lower() == 's':
        nova_tabela = input("Digite o nome da nova tabela: ")
        criar_nova_tabela(db_path, tabela_escolhida, nova_tabela, colunas_escolhidas)
        print(f"\nNova tabela '{nova_tabela}' criada com sucesso.")
    else:
        print("\nOperação cancelada.")

if __name__ == "__main__":
    main()
