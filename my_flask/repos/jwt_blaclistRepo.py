"Defines Jwt_BlacklistRepo class"
from models import storage
from models.jwt_blacklist import Jwt_Blacklist



class Jwt_BlacklistRepo:
    """
    Defines a repository for Jwt_Blacklist model
    provides methods for querying its table in the db
    """

    session = None

    def __init__(self):
        self.session = storage.get_session()

    def findByJwt(self, token: str) -> Jwt_Blacklist:
        return self.session.query(Jwt_Blacklist).filter(Jwt_Blacklist.jwt == token).first()
    
Jwt_Blacklist_repo = Jwt_Blacklist()