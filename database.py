from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str] = mapped_column()
    completed: Mapped[bool] = mapped_column(default=False)


Base.metadata.create_all(bind=engine)
