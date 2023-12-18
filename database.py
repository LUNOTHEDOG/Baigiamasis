from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,  relationship


Base = declarative_base()
metadata = MetaData()

# tarpine studentu skolu lentele
studentai_skolos = Table(
    'studentai_skolos',
    metadata,
    Column('studentas_id', Integer, ForeignKey('Studentai.id')),
    Column('mok_dalyko_skola_id', Integer, ForeignKey('MokomojiDalykoSkola.id'))
)

Base = declarative_base(metadata=metadata)


class DuomenuBaze(Base):
    __tablename__ = 'Studentai'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column("Vardas", String, nullable=False)
    last_name = Column('Pavarde', String, nullable=False)
    birth_date = Column('Gimimo data', Date, nullable=False)
    student_since = Column('Studentas nuo', Date, nullable=False)
    division = Column('Padalinys', String, nullable=False)
    study = Column('Studijos', String, nullable=False)
    member = Column('Tarybos narys', String, nullable=False)
    password = Column('Slaptazodis', String, nullable=False)

    skolos = relationship('MokomojiDalykoSkola', secondary=studentai_skolos, back_populates='studentai',
                          primaryjoin="DuomenuBaze.id == studentai_skolos.c.studentas_id",
                          secondaryjoin="MokomojiDalykoSkola.id == studentai_skolos.c.mok_dalyko_skola_id")

    def __init__(self, name, last_name, birth_date, student_since, division, study,  member, password):

        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date
        self.student_since = student_since
        self.division = division
        self.study = study
        self.member = member
        self.password = password

    def __str__(self):
        separator = '*' * 40
        return (f"ID #{self.id} {self.name} {self.last_name}\n"
                f"Gimimo data: {self.birth_date}\n"
                f"Studentas nuo: {self.student_since}\n"
                f"Padalinys: {self.division}\n"
                f"Studijos: {self.study}\n"
                f"Tarybos narys: {self.member}\n"
                f"Slaptazodis: {self.password}\n"
                f"{separator}")


class MokomojiDalykoSkola(Base):
    __tablename__ = 'MokomojiDalykoSkola'
    id = Column('id', Integer, primary_key=True)
    debt_name = Column('Skolos pavadinimas', String, nullable=False)
    has_debt = Column('Ar turi skola', String, nullable=False)

    studentai = relationship('DuomenuBaze', secondary=studentai_skolos, back_populates='skolos',
                             primaryjoin="MokomojiDalykoSkola.id == studentai_skolos.c.mok_dalyko_skola_id",
                             secondaryjoin="DuomenuBaze.id == studentai_skolos.c.studentas_id")


engine = create_engine('sqlite:///Centralized_College.db', echo=True)
Base.metadata.bind = engine
Base.metadata.create_all()

Session = sessionmaker(bind=engine)
