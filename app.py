import logging
from flask import Flask
from flask_cors import CORS
from routes.webhook import webhook_bp
from utils.statistics_manager import StatisticsManager
import schedule
import time
from threading import Thread
from config import Config
from utils.openai_client import OpenAIClient

app = Flask(__name__)
CORS(app)

# Регистрация маршрутов
app.register_blueprint(webhook_bp)

# Инициализация статистики
stats_manager = StatisticsManager()

# Инициализация клиента OpenAI
openai_client = OpenAIClient()


# Загрузка знаний из файлов при запуске
def load_knowledge_on_start():
    knowledge_files = [
        ("7ya_data.json", "7ya_data"),
        ("Argument_data.json", "Argument_data"),
        ("Dneprovskiy_data.json", "Dneprovskiy_data"),
        ("Filosofia_data.json", "Filosofia_data"),
        ("Gorizont_data.json", "Gorizont_data"),
        ("Klubniy_data.json", "Klubniy_data"),
        ("Novozhilovo_data.json", "Novozhilovo_data"),
        ("Akvatoriya_data.json", "Akvatoriya_data"),
        ("Amurskiy_data.json", "Amurskiy_data"),
        ("Andersen_data.json", "Andersen_data"),
        ("Ayaks_data.json", "Ayaks_data"),
        ("Brusnika_data.json", "Brusnika_data"),
        ("CentralPark Dom1_data.json", "CentralPark Dom1_data"),
        ("CentralPark Dom2_data.json", "CentralPark Dom2_data"),
        ("Dns_city_data.json", "Dns_city_data"),
        ("Eco_city_data.json", "Eco_city_data"),
        ("Edelweiss_data.json", "Edelweiss_data"),
        ("Flagman_data.json", "Flagman_data"),
        ("Format_data.json", "Format_data"),
        ("Futurist1_data.json", "Futurist1_data"),
        ("Futurist2_data.json", "Futurist2_data"),
        ("Futurist3_data.json", "Futurist3_data"),
        ("Fyord_data.json", "Fyord_data"),
        ("Garmoniya_data.json", "Garmoniya_data"),
        ("Gavan_data.json", "Gavan_data"),
        ("Greenhills_data.json", "Greenhills_data"),
        ("Greenwood_data.json", "Greenwood_data"),
        ("Istorichesky_data.json", "Istorichesky_data"),
        ("Kaleidoscop_data.json", "Kaleidoscop_data"),
        ("Kashtanoviy_data.json", "Kashtanoviy_data"),
        ("Kurortniy1_data.json", "Kurortniy1_data"),
        ("Kvartal_neibuta_data.json", "Kvartal_neibuta_data"),
        ("Lisapark_data.json", "Lisapark_data"),
        ("Meridiany_ulissa_data.json", "Meridiany_ulissa_data"),
        ("More_data.json", "More_data"),
        ("Nahodka_data.json", "Nahodka_data"),
        ("Nebopark2_data.json", "Nebopark2_data"),
        ("Novyegorizonty_data.json", "Novyegorizonty_data"),
        ("Ostrogornyi_data.json", "Ostrogornyi_data"),
        ("Pobeda_data.json", "Pobeda_data"),
        ("Poseidoniya_data.json", "Poseidoniya_data"),
        ("Pribrezhniy_data.json", "Pribrezhniy_data"),
        ("Sabaneeva125_data.json", "Sabaneeva125_data"),
        ("Sady_makovskogo_data.json", "Sady_makovskogo_data"),
        ("Serdce_kvartala_data.json", "Serdce_kvartala_data"),
        ("Singapur_data.json", "Singapur_data"),
        ("Solnechniygorod_data.json", "Solnechniygorod_data"),
        ("Solyaris_data.json", "Solyaris_data"),
        ("Supreme_data.json", "Supreme_data"),
        ("Tihvinskiy_data.json", "Tihvinskiy_data"),
        ("Vesna4_data.json", "Vesna4_data"),
        ("Vostochnyi_Dom102-103_data.json", "Vostochnyi_Dom102-103_data"),
        ("Vostochnyi_Dom108_data.json", "Vostochnyi_Dom108_data"),
        ("Yuzhniy_data.json", "Yuzhniy_data"),
        ("Zaliv_data.json", "Zaliv_data"),
        ("Zhuravli_data.json", "Zhuravli_data"),
        ("Zolotaya_dolina_data.json", "Zolotaya_dolina_data"),
        ("Сhaika_data.json", "Сhaika_data"),
        ("Сhernyahovskogo_data.json", "Сhernyahovskogo_data"),

    ]
    openai_client.load_knowledge_files(knowledge_files)


def reset_statistics():
    stats_manager.reset_statistics()


def check_and_reset():
    today = time.localtime()
    if today.tm_mday == 1:
        reset_statistics()


def schedule_monthly_reset():
    # Задача будет запускаться каждый день в 00:00
    schedule.every().day.at("00:00").do(check_and_reset)

    while True:
        schedule.run_pending()
        time.sleep(60)


def start_scheduler():
    scheduler_thread = Thread(target=schedule_monthly_reset)
    scheduler_thread.daemon = True  # Этот поток будет завершаться при закрытии основного приложения
    scheduler_thread.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

    # Загружаем файлы знаний при старте приложения
    load_knowledge_on_start()

    # Запускаем планировщик задач
    start_scheduler()

    # Запуск приложения
    app.run(port=Config.PORT)
