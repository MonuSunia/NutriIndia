import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{st.secrets['DB_USER']}:"
    f"{st.secrets['DB_PASSWORD']}@"
    f"{st.secrets['DB_HOST']}:"
    f"{st.secrets['DB_PORT']}/"
    f"{st.secrets['DB_NAME']}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()