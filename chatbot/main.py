import json
from flask import request
from chatbot import app

users = dict()


@app.route("/", methods=["GET", "POST"])
def index():
    global users
    req = request.json
    questions = [{
        "question": "Каким алгоритмом вы воспользуетесь для поиска объекта в упорядоченном массиве за log(n)?",
        "variants": ["Алгоритм Дейкстры",
                     "Алгоритм Форда-Беллмана",
                     "Бинарный поиск",
                     "Heavy-light decomposition"],
        "answer": "Бинарный поиск",
        "category": "Спортпрог"
        },
        {
            "question": "Что такое OSINT?",
            "variants": ["Разведка по открытым источникам",
                         "Исследование некоторого готового устройства или программы",
                         "Метод безопасного сокрытия информации",
                         ""],
            "answer": "Разведка по открытым источникам",
            "category": "Инфобез"
        },
        {
            "question": "Какое из перечисленных ниже слов не является зарезервированным словом в JavaScript?",
            "variants": ["default",
                         "throw",
                         "finally",
                         "undefined"],
            "answer": "undefined",
            "category": "JS"
        },
        {
            "question": "Что из этого в настоящее время не поддерживается в Kotlin ?",
            "variants": ["JVM",
                         "JavaScript",
                         "LLVM",
                         ".NET CLR"],
            "answer": ".NET CLR",
            "category": "Mobile"
        },
        {
            "question": "Какой пакетный менеджер есть в Python?",
            "variants": ["Jinja",
                         "manage.py",
                         "npm",
                         "pip"],
            "answer": "pip",
            "category": "Back-end"
        },
        {
            "question": "Как расшифровывается XR?",
            "variants": ["Extra Rush",
                         "Xor Reverse",
                         "Extended Reality",
                         "X-Ray"],
            "answer": "Extended Reality",
            "category": "Back-end"
        },
        {
            "question": "Какой формат файла поддерживает анимационные изображения?",
            "variants": ["psd",
                         "gif",
                         "jpg",
                         "png"],
            "answer": "gif",
            "category": "Дизайн"
        },
        {
            "question": "С помощью какого метода можно отправить сообщение от чат-бота?",
            "variants": ["send_message",
                         "write_to",
                         "println",
                         "cout"],
            "answer": "send_message",
            "category": "Чат-боты"
        }
    ]
    response = {"response": {
        "tts": "",
        "text": "",
        "buttons": [],
        "end_session": False
    },
        "session": req["session"],
        "version": req["version"]}
    buttons = list()
    if req["session"]["new"]:
        users[req["session"]["application"]["application_id"]] = {"quest_id": 0, "categories": []}
        response["response"]["text"] = "Приветствую! Это мини тест на то, какие категории вездекода тебe подходят. " \
                                       "Вот первый вопрос." + questions[0]["question"]
        response["response"]["tts"] = "Приветствую! Это мини тест на то, какие категории вездекода тебe подходят. " \
                                       "Вот первый вопрос." + questions[0]["question"]

        for variant in questions[0]["variants"]:
            buttons.append({"title": variant})
        response["response"]["buttons"] = buttons
        # response["response"]["card"] = {"type": "BigImage", "image_id": 457239017}
    else:
        q_id = users[req["session"]["application"]["application_id"]]["quest_id"]
        if req["request"]["original_utterance"] == questions[q_id]["answer"]:
            users[req["session"]["application"]["application_id"]]["categories"].append(questions[q_id]["category"])
            response["response"]["tts"] = "<speaker audio=marusia-sounds/game-win-1>"
        else:
            response["response"]["tts"] = "<speaker audio=marusia-sounds/game-loss-1>"
        users[req["session"]["application"]["application_id"]]["quest_id"] += 1
        q_id += 1
        if q_id == 8:
            text = f"Спасибо за участие в викторине! Тебе подходят следующие категории: " \
                   f"{', '.join(users[req['session']['application']['application_id']]['categories'])}. " \
                   f"Посетите наше мини-приложение! Удачи на Вездекоде! " \
                   f"Для повторного прохождения теста просто напиши мне что-нибудь."
            response["response"]["text"] = text
            response["response"]["tts"] += text
            # response["response"]["commands"] = [
            #                                     {"type": "MiniApp", "url": "[https://vk.com/app7543093]"}]
            response["response"]["end_session"] = True
        else:
            response["response"]["text"] = questions[q_id]["question"]
            response["response"]["tts"] += questions[q_id]["question"]
            for variant in questions[q_id]["variants"]:
                buttons.append({"title": variant})
            response["response"]["buttons"] = buttons
    return json.dumps(response)
