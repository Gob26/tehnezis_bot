import os
from aiogram import Router,types, F
from aiogram.filters import Command, CommandStart
from core.use_cases.process_file import process_excel_file
import infrastructure.telegram_bot.keyboards as kb

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer("Привет, я бот обрабатывающий exel-файлы.", reply_markup=kb.main)

@router.message(F.text == "Загрузить файл")
async def process_document(message: types.Message)-> None:
    await message.answer("Пожалуйста, отправьте exel-файл.", reply_markup=kb.main)

@router.message(F.document)
async def process_document(message: types.Message)-> None:
    # Проверяем что формат и тип соответствуют нужным
    if (message.document and
    message.document.file_name.endswith(('.xlsx', '.xls', '.ods')) and
    message.document.mime_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                                  'application/vnd.ms-excel',
                                  'application/vnd.oasis.opendocument.spreadsheet']):
        
        file_id = message.document.file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path

        download_path = f"exel_file/{message.document.file_name}"
        os.makedirs("exel_file", exist_ok=True)
        
        await message.bot.download_file(file_path, download_path)
        await process_excel_file(message, download_path)
    else:
        await message.answer("Пожалуйста, отправьте файл в формате Excel (.xlsx, .xls или .ods).")
