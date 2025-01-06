# schemas.py
import strawberry
from typing import List
from ..crud import users as usersCrud


@strawberry.type
class UserType:
    id: int
    name: str
    email: str


def resolve_users() -> List[UserType]:
    users = usersCrud.get_users()
    return [
        UserType(
            **{
                key: value
                for key, value in vars(user).items()
                if key in UserType.__annotations__
            }
        )
        for user in users
    ]


@strawberry.type
class Query:
    users: List[UserType] = strawberry.field(resolver=resolve_users)


# @strawberry.type
# class Mutation:
#     @strawberry.mutation
#     def create_user(self, name: str, email: str) -> UserType:
#         session = SessionLocal()
#         new_user = User(name=name, email=email)
#         session.add(new_user)
#         session.commit()
#         session.refresh(new_user)
#         return UserType(id=new_user.id, name=new_user.name, email=new_user.email)


schema = strawberry.Schema(query=Query)
# schema = strawberry.Schema(query=Query, mutation=Mutation)
