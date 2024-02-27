from sqlalchemy import create_engine, String, Boolean,select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash


pasta_atual = Path(__file__).parent
PATH_TO_BD = pasta_atual / 'bd_usuario.sqlite'


class base(DeclarativeBase):
    pass

class Usuario(base):
    __tablename__ = 'usuario'

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(40))
    senha: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(40))
    acesso_gestao: Mapped[bool] = mapped_column(Boolean(), default=False)


    def __repr__(self):
        return f"Usuario({self.id}, {self.nome})"
    
    def define_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verifica_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
engine = create_engine(f'sqlite:///{PATH_TO_BD}')
base.metadata.create_all(bind=engine)


#CRUD
def criar_usuarios(
        nome,
        senha,
        email,
        **kwargs
):
    with Session(bind=engine) as s:
         usuario = Usuario(
             nome=nome,
             email=email,
             **kwargs
         )
         usuario.define_senha(senha)
         s.add(usuario)
         s.commit()
        

def ler_usuarios():
    with Session(bind=engine) as s:
        comando_sql = select(Usuario)
        usuarios = s.execute(comando_sql).fetchall()
        usuarios = [user[0] for user in usuarios]
        return usuarios
    
def  buscar_usuario_por_id(id):
    with Session(bind=engine) as s:
        comando_sql = select(Usuario).where(Usuario.id == id)
        usuarios = s.execute(comando_sql).fetchall()
        return usuarios[0][0]
    
def  modificar_usuario(id, nome=None, senha=None, email=None, acesso_gestao=None):
    with Session(bind=engine) as s:
        comando_sql =  select(Usuario).where(Usuario.id == id)
        usuarios = s.execute(comando_sql).fetchall()
        for usuario in usuarios:
            if nome is not None:
                usuario[0].nome = nome
            if senha is not None:
                usuario[0].define_senha(senha)
            if email is not None:
                usuario[0].email = email
            if acesso_gestao is not None:
                usuario[0].acesso_gestao = acesso_gestao
        s.commit()

def  deletar_usuario(id):
    with Session(bind=engine) as s:
        comando_sql = select(Usuario).where(Usuario.id == id)
        usuarios = s.execute(comando_sql).fetchall()
        for  u in usuarios:
            s.delete(u[0])
        s.commit()


# criar_usuarios(
#     'Gabriel Souza',
#     senha='Confesso',
#     email= "gabrielguitta93@gmail.com"
# )