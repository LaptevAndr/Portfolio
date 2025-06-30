from aiogram import F, Router #фильтровать событие 
from aiogram.filters import CommandStart
from aiogram.types import Message# с помощью этого Типизировать
from aiogram.fsm.state import State, StatesGroup# выдавать пользователюмсостояние и делать антифлуд систему
from aiogram.fsm.context import FSMContext
from app.generate import ai_generate

router = Router()

class Gen(StatesGroup):
    wait = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать, напиште ваш запрос!')

@router.message(Gen.wait)
async def stop_flood(message: Message):
    await message.answer('Подождите, ваш запрос генерируется!')

@router.message()
async def generating(message: Message, state: FSMContext):
    await state.set_state(Gen.wait)
    respons = await ai_generate(message.text)
    await message.answer(respons)
    await state.clear()