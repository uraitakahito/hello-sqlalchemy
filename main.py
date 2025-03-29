from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

# Database setup
DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# 1. Definition of POD class (Plain Old Data)
class UserData:
    def __init__(self, id: int, name: str, age: int):
        self.id = id
        self.name = name
        self.age = age

    def __repr__(self):
        return f"UserData(id={self.id}, name={self.name}, age={self.age})"


# 2. Definition of SQLAlchemy ORM class
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    # Conversion from POD to ORM
    @classmethod
    def from_pod(cls, pod: UserData):
        return cls(id=pod.id, name=pod.name, age=pod.age)

    # Conversion from ORM to POD
    def to_pod(self) -> UserData:
        return UserData(id=self.id, name=self.name, age=self.age)


# 3. Create tables in the database
Base.metadata.create_all(bind=engine)

# 4. Add data & perform conversions
session = SessionLocal()

# Create a POD instance
user_data = UserData(id=1, name="Alice", age=30)

# Convert POD to ORM and save to the database
user_orm = User.from_pod(user_data)
session.add(user_orm)
session.commit()

# Retrieve ORM from the database and convert to POD
retrieved_user = session.query(User).filter(User.id == 1).first()
if retrieved_user is None:
    raise ValueError("User not found in the database")
user_pod = retrieved_user.to_pod()
print(user_pod)  # Output: UserData(id=1, name=Alice, age=30)

# Close the session
session.close()
