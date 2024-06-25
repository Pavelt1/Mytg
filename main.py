import logging
import random
from datetime import datetime

from aiogram import Bot, Dispatcher, types, Router, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from texts import TEXTS
from db import Users,Сonversion,Quiz,Quiz_user, session_db, session_commit,reg_user_db, add_new_quiz, add_quiz_user, add_score_db

from states import MyForm,MyQuiz,MyScore,MyScoretwo
from db import create_tables,engine

from admin import router1
from director import router2
from participant import router3

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot,storage=storage)
dp.include_router(router1,router2,router3)

create_tables(engine)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user = session.query(Users.id).filter(Users.id == message.id).first()
    if not user:
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Зарегестироваться", callback_data="register"))
        await message.reply(TEXTS["start"][0],reply_markup=markup)
    else:  
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Меню", callback_data='menu'))
        await message.reply(TEXTS["start"][1],reply_markup=markup)

@dp.callback_query_handler(text='register')
async def reg_new(callback_query: types.CallbackQuery):
    await callback_query.message.answer(TEXTS["reg"][0])
    await MyForm.name.set()

@dp.message_handler(state = MyForm.name)
async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await MyForm.next()
    await message.answer(TEXTS["reg"][1])

@dp.message_handler(state = MyForm.birthdate)
async def birthda_handler(message: types.Message, state: FSMContext):
    await state.update_data(birthdate=message.text)
    await MyForm.next()
    await message.answer(TEXTS["reg"][2])


@dp.message_handler(state = MyForm.phone)
async def phone_handler(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(TEXTS["reg"][5])
    await MyForm.next()


@dp.message_handler(state = MyForm.secret_admins)
async def phone_handler(message: types.Message, state: FSMContext):
    await state.update_data(secret_admins=message.text)
    await message.answer(TEXTS["reg"][3])
    user_data = await state.get_data()
    name = user_data.get("name")
    birthdate = user_data.get("birthdate")
    phone = user_data.get("phone")
    secret = user_data.get("secret_admins")
    await state.finish()
    if secret == "Админ":
        reg_user_db(message.from_user.id,name,birthdate,phone,message.from_user.username,"Администратор")
        await message.answer(TEXTS["reg"][6])
    elif secret == "Директор":
        reg_user_db(message.from_user.id,name,birthdate,phone,message.from_user.username,"Директор")
        await message.answer(TEXTS["reg"][7])
    else:
        await message.answer(f",{message.from_user}")
        reg_user_db(message.from_user.id,name,birthdate,phone,message.from_user.username)
        await message.answer(TEXTS["reg"][4])

@dp.message_handler(commands=['menu'])
async def menu_handler(message: types.Message):
    markup = InlineKeyboardMarkup()
    with session_db() as session:
        role = session.query(Users.role).filter(Users.id == message.from_user.id).scalar()
    await message.answer(role)    
    if role == "Участник":
        markup.row(InlineKeyboardButton(text="Мой турнирный рейтинг", callback_data="tur_reit"),
                    InlineKeyboardButton(text="Викторина", callback_data="quiz_go"),
                    InlineKeyboardButton(text="История викторин", callback_data="win_quiz"))
    if role == "Директор":
        markup.row(InlineKeyboardButton(text="Начислить", callback_data="add_scores"),
                    InlineKeyboardButton(text="Рейтинг", callback_data="reit"))
    if role == "Администратор":
        markup.row(InlineKeyboardButton(text="Добавить Викторину", callback_data="add_quiz"),
                    InlineKeyboardButton(text="Рейтинг Викторин", callback_data="reit_quiz"))

    await message.answer(TEXTS["menu"],reply_markup=markup)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)