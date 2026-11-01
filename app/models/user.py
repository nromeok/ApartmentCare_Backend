from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    house_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #Relationships
    issues =  db.relationship("Issue", back_populates = "user", lazy = True)#Lazy is used to load issues only when accessed.
    announcements = db.relationship("Announcement", back_populates = "author", lazy = True)#author is used to name admin who created the announcement.

    def set_password(self,password:str)-> None:
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password:str)-> bool:
        return check_password_hash(self.password_hash,password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "house_number": self.house_number,
            "role": self.role,
            "created_at": self.created_at.isoformat()
        }
    
    def __repr__(self) -> str:
        return f"<User self.house_number={self.house_number} self.email={self.email} self.role={self.role}>"