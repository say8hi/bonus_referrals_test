import datetime
from typing import Annotated
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from .database import Base


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[
    datetime.datetime, mapped_column(default=datetime.datetime.now())
]


# Tables
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    referal_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    created_at: Mapped[created_at]

    referrals = relationship("User", backref=backref("inviter", remote_side=id), foreign_keys=[referal_id])

    purchases = relationship("Purchase", back_populates="user")


class Package(Base):
    __tablename__ = "packages"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    purchases = relationship("Purchase", back_populates="package")


class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    package_id: Mapped[int] = mapped_column(ForeignKey('packages.id'), nullable=False)
    purchase_date: Mapped[created_at]

    user = relationship("User", back_populates="purchases")
    package = relationship("Package", back_populates="purchases")
