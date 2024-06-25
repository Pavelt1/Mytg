import random
from aiogram import Router, types 
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext


from states import MyForm,MyQuiz
from texts import TEXTS
from db import Users,Сonversion,Quiz,Quiz_user, session_db, session_commit,reg_user_db, add_new_quiz, add_quiz_user, add_score_db

router1 = Router()


@router1.callback_query_handler(text='add_quiz')
async def add_new_quiz(callback_query: types.CallbackQuery):
    await callback_query.message.answer(TEXTS["add_quiz"][0])
    await MyQuiz.quiz.set()

@router1.message_handler(state = MyQuiz.quiz)
async def quiz_handler(message: types.Message, state: FSMContext):
    await state.update_data(quiz=message.text)
    await MyQuiz.next()
    await message.answer(TEXTS["add_quiz"][1])

@router1.message_handler(state = MyQuiz.round)
async def round_handler(message: types.Message, state: FSMContext):
    await state.update_data(round=message.text)
    await MyQuiz.next()
    await message.answer(TEXTS["add_quiz"][2])

@router1.message_handler(state = MyQuiz.answer)
async def answer_handler(message: types.Message, state: FSMContext):
    await state.update_data(answer=message.text)
    await MyQuiz.next()
    await message.answer(TEXTS["add_quiz"][3])


@router1.message_handler(state = MyQuiz.not_answer1)
async def not_answer1_handler(message: types.Message, state: FSMContext):
    await state.update_data(not_answer1=message.text)
    await MyQuiz.next()
    await message.answer(TEXTS["add_quiz"][4])

@router1.message_handler(state = MyQuiz.not_answer2)
async def not_answer2_handler(message: types.Message, state: FSMContext):
    await state.update_data(not_answer2=message.text)
    await MyQuiz.next()
    await message.answer(TEXTS["add_quiz"][5])

@router1.message_handler(state = MyQuiz.not_answer3)
async def not_answer3_handler(message: types.Message, state: FSMContext):
    await state.update_data(not_answer3=message.text)
    await message.answer(TEXTS["add_quiz"][6])
    quiz_data = await state.get_data()
    quiz = quiz_data.get("quiz")
    answer = quiz_data.get("answer")
    round = quiz_data.get("round")
    not_answer1 = quiz_data.get("not_answer1")
    not_answer2 = quiz_data.get("not_answer2")
    not_answer3 = quiz_data.get("not_answer3")
    await state.finish()
    add_new_quiz(quiz,round,answer,not_answer1,not_answer2,not_answer3)
    

@router1.callback_query_handler(text='reit_quiz')
async def reit_users(callback_query: types.CallbackQuery):
    await callback_query.message.answer(f"{TEXTS["reit"][1]}")
    with session_db() as session:
        results_quiz = session.query(Сonversion.POT, Сonversion.id_user).order_by(desc(Сonversion.POT)).all()
    for r,n in results_quiz:
        await callback_query.message.answer(f"Пользователь {n} - {r} баллов")