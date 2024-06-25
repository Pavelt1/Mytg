import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker

metadata = sq.MetaData()
Base = declarative_base(metadata=metadata)

DSN = "sqlite:///test.db"  # Тестовая БД
engine = sq.create_engine(DSN, echo=True)

def session_db():
    Session = sessionmaker(bind=engine)
    return Session()

def session_commit(user):
    session = session_db()
    session.add(user)
    session.commit()
    session.close()
    
def session_reload():
    session = session_db()
    session.commit()
    session.close()

class Users(Base):
    __tablename__ = "users"
        
    id = sq.Column(sq.BigInteger,primary_key=True)
    time = sq.Column(sq.Date,nullable=False)
    name = sq.Column(sq.String(length=80),nullable=False)
    birthday = sq.Column(sq.String,nullable=False)
    number_phone = sq.Column(sq.BigInteger,nullable=False)
    log_tg = sq.Column(sq.String,nullable=False)
    role = sq.Column(sq.String,nullable=False)

    
class Сonversion(Base):
    __tablename__ = "conversion"

    time_enrollment = sq.Column(sq.Date,primary_key=True)
    tournament = sq.Column(sq.INTEGER)
    POT = sq.Column(sq.INTEGER)
    resultbonus = sq.Column(sq.INTEGER)
    time_conversion = sq.Column(sq.Date)
    id_user = sq.Column(sq.BigInteger)
    id_admin = sq.Column(sq.BigInteger)


class Quiz(Base):
    __tablename__ = "quiz"

    time_quiz = sq.Column(sq.Date,primary_key=True)
    round = sq.Column(sq.INTEGER,nullable=False)
    quiz = sq.Column(sq.Text)
    answer = sq.Column(sq.Text)
    not_answer1 = sq.Column(sq.Text)
    not_answer2 = sq.Column(sq.Text) 
    not_answer3 = sq.Column(sq.Text)

class Quiz_user(Base):
    __tablename__ = "quiz_user"

    id = sq.Column(sq.INTEGER,primary_key=True)
    numer_round = sq.Column(sq.Integer,sq.ForeignKey("quiz.round"),nullable=False)
    id_user = sq.Column(sq.BigInteger,sq.ForeignKey("user.id"),nullable=False)
    estimation = sq.Column(sq.Boolean,default=False)

    quiz = relationship(Quiz,backref="quiz_user")
    users = relationship(Users,backref="quiz_user")
    

async def reg_user_db(uid,name,birth_day,number,nametg,roles= "Участник"):
    now = datetime.now()
    format_time = now.strftime("%Y-%m-%d-%H-%M")
    birth_day = datetime.strptime(birth_day, "%Y, %m, %d")
    age = now.year - birth_day.year
    user = Users(id = uid, time = format_time, name = name, birthday = f"{birth_day},{age}",
                 number_phone = number, log_tg = nametg, role = roles)
    session_commit(user)

async def add_new_quiz(quizz,roundd,answerr,not_answer11,not_answer22,not_answer33):
    now = datetime.now()
    format_time = now.strftime("%Y-%m-%d-%H-%M")
    quiz = Quiz(time_quiz = format_time, quiz = quizz, round = roundd, answer = answerr,
                 not_answer1 = not_answer11, not_answer2 = not_answer22, not_answer3 = not_answer33)
    session_commit(quiz)

async def add_quiz_user(roundd, id_userr):
    new = Quiz(numer_round = roundd, id_user = id_userr)
    session_commit(new)

async def add_score_db(score,id_admin,id_user,tour=0):
    now = datetime.now()
    format_time = now.strftime("%Y-%m-%d-%H-%M")
    score_user = Сonversion(time_enrollment = format_time,tournament = tour, POT = score, id_admin = id_admin, id_user = id_user)
    session_commit(score_user)

 

def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Creating database")
