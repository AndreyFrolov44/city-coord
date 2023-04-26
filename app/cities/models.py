import sqlalchemy


from app.database import metadata

cities = sqlalchemy.Table(
    "cities",
    metadata,
    sqlalchemy.Column("lat", sqlalchemy.DECIMAL(10, 8), primary_key=True),
    sqlalchemy.Column("lon", sqlalchemy.DECIMAL(11, 8), primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
)
