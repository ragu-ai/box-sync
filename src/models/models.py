from sqlalchemy import ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from src.settings import Settings

# Create a base class for declarative class definitions
Base = declarative_base()


# Define a sample model
class DataSources(Base):
    """
    DataSources model
    """

    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True)
    external_id = Column(String(50), nullable=True)
    account_id = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    service = Column(String(50), nullable=False)
    credentials = Column(String(50), nullable=True)
    active = Column(Integer, nullable=False)
    folders = relationship(
        "Folders", back_populates="data_source", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<DataSources(external_id={self.external_id}, account_id={self.account_id}, name={self.name}, type={self.type}, service={self.service}, credentials={self.credentials}, active={self.active})>"


class Folders(Base):
    """
    Folders model
    """

    __tablename__ = "folders"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    data_source_id = Column(
        Integer, ForeignKey("data_sources.id", ondelete="CASCADE"), nullable=False
    )
    active = Column(Integer, nullable=False)
    data_source = relationship("DataSources", back_populates="folders")

    def __repr__(self):
        return f"<Folders(external_id={self.external_id}, account_id={self.account_id}, name={self.name}, parent_id={self.data_source_id}, active={self.active})>"


class AssistantFolders(Base):
    """
    AssistantFolders model
    """

    __tablename__ = "assistant_folders"

    assistant_id = Column(Integer, primary_key=True)
    folder_id = Column(
        Integer, ForeignKey("folders.id", ondelete="CASCADE"), nullable=False
    )


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine(
    f"mysql+pymysql://{Settings.database_user}:{Settings.database_password}@{Settings.database_host}/{Settings.database_name}"
)

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session()

# Create a new user
new_user = User(name="John Doe", email="john@example.com")
session.add(new_user)
session.commit()

# Query users
users = session.query(User).all()
for user in users:
    print(user)

# Close the session
session.close()
