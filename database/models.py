from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    ForeignKey,
    BigInteger,
    TIMESTAMP,
    func,
    UniqueConstraint,
    Index,
)

from sqlalchemy.orm import relationship
from database.database import Base


class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, autoincrement=True)

    food_code = Column(String(20), unique=True, nullable=False)

    food_name = Column(String(255), nullable=False)

    scientific_name = Column(String(255))

    food_group = Column(String(100))

    created_at = Column(TIMESTAMP, server_default=func.now())

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
    )

    nutrients = relationship(
        "FoodNutrient",
        back_populates="food",
        cascade="all, delete-orphan",
    )


class Nutrient(Base):
    __tablename__ = "nutrients"

    id = Column(Integer, primary_key=True, autoincrement=True)

    nutrient_code = Column(String(50), unique=True)

    nutrient_name = Column(String(255), nullable=False)

    display_name = Column(String(255))

    unit = Column(String(20))

    created_at = Column(TIMESTAMP, server_default=func.now())

    foods = relationship(
        "FoodNutrient",
        back_populates="nutrient",
    )


class FoodNutrient(Base):
    __tablename__ = "food_nutrients"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    food_id = Column(
        Integer,
        ForeignKey("foods.id", ondelete="CASCADE"),
        nullable=False,
    )

    nutrient_id = Column(
        Integer,
        ForeignKey("nutrients.id", ondelete="CASCADE"),
        nullable=False,
    )

    nutrient_value = Column(DECIMAL(12, 4))

    food = relationship("Food", back_populates="nutrients")

    nutrient = relationship("Nutrient", back_populates="foods")

    __table_args__ = (
        UniqueConstraint(
            "food_id",
            "nutrient_id",
            name="uq_food_nutrient",
        ),
        Index("idx_food", "food_id"),
        Index("idx_nutrient", "nutrient_id"),
    )