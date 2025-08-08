# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import HTTPException

# from app.models.model_definitions import Users
# from app.schemas.user import UserCreate

# def create_user(session: AsyncSession, user: UserCreate) -> Users:
#     db_user = Users(**user.model_dump())
#     session.add(db_user)
#     session.commit()
#     session.refresh(db_user)
#     return db_user

"""I'm thinking let a third party handle the user auth stuff and let
me just get the token to get user id at least for now.
"""
