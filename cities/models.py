import sqlalchemy


from database import metadata

cities = sqlalchemy.Table(
    "cities",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("lat", sqlalchemy.DECIMAL(10, 8)),
    sqlalchemy.Column("lon", sqlalchemy.DECIMAL(11, 8)),
)
