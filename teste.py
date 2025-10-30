from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://lucasino:abcdcba123*@localhost:5432/projects"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))  # <- usa text()
        print("Conectado com sucesso ao PostgreSQL:")
        for row in result:
            print(row)
except Exception as e:
    print("Erro ao conectar:", e)
