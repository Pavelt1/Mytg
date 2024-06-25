from aiogram import Router
from aiogram.dispatcher.filters.state import State, StatesGroup

router = Router()

class MyForm(StatesGroup):
    name = State()
    birthdate = State()
    phone = State()
    secret_admins = State()

class MyQuiz(StatesGroup):
    quiz = State()
    round = State()
    answer = State()
    not_answer1 = State()
    not_answer2 = State()
    not_answer3 = State()

class MyScore(StatesGroup):
    score = State()

class MyScoretwo(StatesGroup):
    score1 = State()
    name1 = State()