from typing import Optional, Dict, Any
from datetime import datetime
from app.models.schemas.auth import User

class AuthService:
    """
    Service class for authentication and user management
    """
    
    # Mock database for demonstration
    _users_db = [
        User(
            id=1,
            name="Admin User",
            email="admin@concreto.com",
            password="hashed_password_123",  # En producción usar bcrypt
            company="Constructora ABC",
            phone="+1234567890",
            role="admin",
            created_at=datetime.now(),
            active=True
        ),
        User(
            id=2,
            name="Operador Mixer",
            email="operador@concreto.com",
            password="hashed_password_456",
            company="Constructora ABC",
            phone="+1234567891",
            role="operator",
            created_at=datetime.now(),
            active=True
        )
    ]
    
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password
        """
        # En producción, aquí verificarías el hash de la contraseña
        user = next((user for user in AuthService._users_db 
                    if user.email == email and user.password == f"hashed_password_{password}"), None)
        
        if user and user.active:
            return user
        return None
    
    @staticmethod
    def register_user(name: str, email: str, password: str, company: str = None, phone: str = None) -> Optional[User]:
        """
        Register a new user
        """
        # Check if user already exists
        if any(user.email == email for user in AuthService._users_db):
            return None
        
        # Create new user
        new_user = User(
            id=len(AuthService._users_db) + 1,
            name=name,
            email=email,
            password=f"hashed_password_{password}",  # En producción usar bcrypt
            company=company,
            phone=phone,
            role="client",  # Default role
            created_at=datetime.now(),
            active=True
        )
        
        AuthService._users_db.append(new_user)
        return new_user
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """
        Get user by ID
        """
        return next((user for user in AuthService._users_db if user.id == user_id), None)
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """
        Get user by email
        """
        return next((user for user in AuthService._users_db if user.email == email), None)
    
    @staticmethod
    def get_all_users() -> list[User]:
        """
        Get all users
        """
        return AuthService._users_db
    
    @staticmethod
    def update_user_status(user_id: int, active: bool) -> bool:
        """
        Update user active status
        """
        user = AuthService.get_user_by_id(user_id)
        if user:
            user.active = active
            return True
        return False