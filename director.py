import random
from aiogram import Router, types 
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext


from states import MyForm,MyQuiz,MyScore,MyScoretwo
from texts import TEXTS
from db import Users,Сonversion,Quiz,Quiz_user, session_db, session_commit,session_reload,reg_user_db, add_new_quiz, add_quiz_user, add_score_db

router2 = Router()


@router2.callback_query_handler(text='add_scores')
async def tt_new(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text="Всем баллы за викторины", callback_data="add_score_quiz"),
               InlineKeyboardButton(text="Доп баллы", callback_data="Additional_score_go"),)
    await callback_query.message.answer(TEXTS["add_scores"][0],reply_markup=markup)

@router2.callback_query_handler(text='add_score_quiz')
async def new(callback_query: types.CallbackQuery):
    await callback_query.message.answer(TEXTS["add_scores"][2])
    await MyScore.score.set()

@router2.message_handler(state = MyScore.score)
async def add_score1(message: types.Message, state: FSMContext):
    await state.update_data(score=message.text)
    score_data = await state.get_data()
    score = score_data.get("score")
    await state.finish()
    await message.answer(f"{TEXTS["add_scores"][3]}")
    with session_db() as session:
        results_quiz = session.query(Quiz_user.numer_round,Quiz_user.id_user).filter
        (Quiz_user.estimation == False).all()
    
    session.query(Quiz_user).filter(Quiz_user.estimation == False).update
    ({Quiz_user.estimation: True})
    session_reload()
    dickter = {}
    for r,n in results_quiz:
        if n in dickter:
            dickter[n].append(r)
        else:
            dickter[n] = [r]
    for i in dickter:
        ssum = score*(len(dickter[i]))
        add_score_db(ssum,message.from_user.id,(ssum/50))
        await message.answer(f"{i} - {TEXTS["add_scores"][3]} - {ssum} ")



@router2.callback_query_handler(text='Additional_score_go')
async def reg_newww(callback_query: types.CallbackQuery):
    await callback_query.message.answer(TEXTS["add_scores"][4])
    await MyScoretwo.score1.set()

@router2.message_handler(state = MyScoretwo.score1)
async def add_score2(message: types.Message, state: FSMContext):
    await state.update_data(score1=message.text)
    await message.answer(TEXTS["add_scores"][5])
    await MyScoretwo.next()

@router2.message_handler(state = MyScoretwo.name1)
async def add_score3(message: types.Message, state: FSMContext):
    await state.update_data(score=message.text)
    score_data = await state.get_data()
    score = score_data.get("score1")
    name = score_data.get("name1")
    await state.finish()
    session.query(Сonversion).filter(Сonversion.id_user == name).update
    ({Сonversion.resultbonus : score})
    session_reload()
    await message.answer(TEXTS["add_scores"][6])
    



@router2.callback_query_handler(text='reit')
async def reg_neww(callback_query: types.CallbackQuery):
    await callback_query.message.answer(f"{TEXTS["reit"][0]}/n{TEXTS["reit"][1]}")
    with session_db() as session:
        results_quiz = session.query(Сonversion.POT,Сonversion.id_user).all()
    for r,n in results_quiz:
        await callback_query.message.answer(f"Пользователь {n} - {r} баллов")

