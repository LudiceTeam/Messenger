from sqlalchemy import Table,Column,String,Boolean,MetaData


metadata_obj = MetaData()

main_table = Table(
    "messenger_main_table",
    Column("username",String,primary_key=True),
    Column("password",String),
    Column("avatar",String),
    Column("state",String)
)