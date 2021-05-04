# Cipher

__author__ = "Григорьева, Задворная, Сырова"

  Создать виртуально окружение и сразу запустить его:
python -m venv venv
venv\Scripts\activate
  Установить все нужные пакеты:
pip install -r requirements.txt
  Указать основной файл:
set FLASK_APP=chess.py
  Оживить БД:
flask db upgrade
  Запуск:
flask run
