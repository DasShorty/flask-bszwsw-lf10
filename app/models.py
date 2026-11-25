from datetime import datetime
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import DATETIME

from .extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))

    def __repr__(self):
        return f"<User {self.id}>"



class MixingPlant(db.Model):
    __tablename__ = "Mischanlage"

    id: Mapped[int] = mapped_column("ID", primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        "Datum_Uhrzeit",
        DATETIME(fsp=6),
        nullable=False,
        server_default=func.current_timestamp(6),
    )
    temperature: Mapped[Decimal | None] = mapped_column("Temperatur", db.Numeric(6, 2))
    humidity: Mapped[Decimal | None] = mapped_column("Luftfeuchtigkeit", db.Numeric(5, 2))
    fill_level: Mapped[Decimal | None] = mapped_column("Fuellstand", db.Numeric(5, 2))