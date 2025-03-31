import sqlite3
from typing import Optional

def create_connection():
    """Cria conexão com o banco de dados"""
    return sqlite3.connect("database.db")

class UserProfile:
    def __init__(self, user_id: int, username: str, full_name: str, 
                 birth_date: str, email: str,  # Adicionado email como obrigatório
                 avatar_url: Optional[str] = None,
                 name: Optional[str] = None):
        """
        Inicializa um perfil de usuário completo.
        
        Args:
            user_id: ID do usuário
            username: Nome de usuário único
            full_name: Nome completo
            birth_date: Data de nascimento (YYYY-MM-DD)
            email: Endereço de email (obrigatório)
            avatar_url: URL da foto de perfil
            name: Nome alternativo (se diferente de full_name)
        """
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.birth_date = birth_date
        self.email = email  # Campo obrigatório adicionado
        self.avatar_url = avatar_url
        self.name = name if name else full_name  # Usa full_name se name não for fornecido

    @classmethod
    def get_by_user_id(cls, user_id) -> Optional['UserProfile']:
        """
        Busca perfil completo com JOIN entre users e profiles
        
        Args:
            user_id: ID do usuário (str ou int)
            
        Returns:
            Instância de UserProfile ou None se não encontrado
        """
        try:
            user_id = int(user_id) if isinstance(user_id, str) else user_id
            if not isinstance(user_id, int) or user_id <= 0:
                raise ValueError("ID de usuário inválido")
                
            conn = create_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                '''SELECT p.username, p.full_name, p.birth_date, p.avatar_url,
                          u.name, u.email 
                   FROM profiles p
                   JOIN users u ON p.user_id = u.id
                   WHERE p.user_id = ?''',
                (user_id,)
            )

            profile_data = cursor.fetchone()
            conn.close()

            if profile_data:
                return cls(
                    user_id=user_id,
                    username=profile_data[0],
                    full_name=profile_data[1],
                    birth_date=profile_data[2],
                    avatar_url=profile_data[3],
                    name=profile_data[4],  # name da tabela users
                    email=profile_data[5]  # email da tabela users
                )
            return None
            
        except sqlite3.Error as e:
            print(f"Erro de banco de dados: {e}")
            raise
        except Exception as e:
            print(f"Erro inesperado: {e}")
            raise