from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.repositories.users import UserRepository
from app.schemas.auth import CurrentUser, LoginResponse


class AuthService:
    def __init__(self, db: Session) -> None:
        self.repository = UserRepository(db)

    def login(self, username: str, password: str) -> LoginResponse:
        user = self.repository.get_by_username(username)
        if not user or user.password != password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="아이디 또는 비밀번호가 올바르지 않습니다.")

        return LoginResponse(
            access_token=create_access_token(subject=user.username, role=user.role),
            user=CurrentUser.model_validate(user),
        )
