import random
from aiogram import Router, types 
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from texts import TEXTS
from db import Users,Сonversion,Quiz,Quiz_user, session_db, session_commit

from states import MyForm,MyQuiz
from texts import TEXTS
from db import Users,Сonversion,Quiz,Quiz_user, session_db, session_commit, reg_user_db, add_new_quiz, add_quiz_user, add_score_db

router3 = Router()

@router3.callback_query_handler(text='tur_reit')
async def reg_new(callback_query: types.CallbackQuery):
    dicter = {}
    tur = session.query(Conversion.id_user, Conversion.tournament).order_by(desc(Сonversion.tournament)).all()
    for q,e in tur:
        if e in dicter:
            dicter[q] += e
            await callback_query.message.answer(f"{q} - {dicter[q]}")
        else:
            dicter[q] = e
            await callback_query.message.answer(f"{q} - {dicter[q]}")



@router3.callback_query_handler(text='quiz_go')
async def quizz(callback_query: types.CallbackQuery):
    idd = callback_query.from_user.id
    await callback_query.message.answer(TEXTS["quiz_go"][0])
    with session_db() as session:
        quiz = session.query(Quiz.round, Quiz.quiz, Quiz.answer, Quiz.not_answer1, Quiz.not_answer2, Quiz.not_answer3).join
        (Quiz_user,Quiz.round == Quiz_user.numer_round).filter
        (Quiz_user.id_user != idd).one()

    await callback_query.message.answer(f"{TEXTS["quiz_go"][1]}  {quiz.round}")
    await callback_query.message.answer(f"{quiz.quiz} \n{TEXTS["quiz_go"][2]}")
    but = [quiz.answer, quiz.not_answer1, quiz.not_answer2, quiz.not_answer3]
    random.shuffle(but)
    for n,i in enumerate(but):
        await callback_query.message.answer(f"№{n} - {i}") 
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text=but[0], callback_data="answer1",adjust_width=True),
                InlineKeyboardButton(text=but[1], callback_data="answer2",adjust_width=True),
                InlineKeyboardButton(text=but[2], callback_data="answer3",adjust_width=True),
                InlineKeyboardButton(text=but[4], callback_data="answer4",adjust_width=True))
    await callback_query.message.answer(reply_markup=markup)
    
@router3.callback_query_handler(text=['answer1', 'answer2', 'answer3', 'answer4'])
async def handle_answer(callback_query: types.CallbackQuery):
    selected_answer = callback_query.data
    idd = callback_query.from_user.id
    with session_db() as session:
        quiz = session.query(Quiz.round,Quiz.answer).join
        (Quiz_user,Quiz.round == Quiz_user.numer_round).filter
        (Quiz_user.id_user != idd).one()
    if selected_answer == quiz.answer:
        await callback_query.message.answer(TEXTS["quiz_go"][3])
        add_quiz_user(Quiz.round, idd)

    else:
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton(text="Еще раз", callback_data="quiz_go"))
        await callback_query.message.answer(TEXTS["quiz_go"][4],reply_markup=markup)
    


@router3.callback_query_handler(text='win_quiz')
async def you_reit(callback_query: types.CallbackQuery):
    await callback_query.message.answer(f"{TEXTS["reit"][1]}")
    with session_db() as session:
        results_quiz = session.query(Сonversion.POT, Сonversion.id_user).order_by(desc(Сonversion.POT)).all()
    for q,r,n in enumerate(results_quiz):
        if n == callback_query.from_user.id :
            await callback_query.message.answer(f"Ваше место {q} у вас {r} баллов")
        else:    
            await callback_query.message.answer(f"Пользователь {n} - {r} баллов. Место {q}")
