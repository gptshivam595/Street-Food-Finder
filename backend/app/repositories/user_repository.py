from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.user import User, UserRole


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_or_create_demo_user(db: Session, email: str) -> User:
    user = get_by_email(db, email)
    if user:
        return user
    user = User(name="Demo User", email=email, role=UserRole.CUSTOMER)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
