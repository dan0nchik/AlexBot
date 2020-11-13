import csv
import random
from datetime import datetime

import pandas as pd
import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

now = datetime.now()
cur_time = now.strftime("%H%M")
vk_session = vk_api.VkApi(
    token=
    'c3a549d526acda59616b81d2c8817c9ac50b57aefbc1304164df6c1377e8c1d1f676f77dc1fe9348fba77'
)
longpoll = VkBotLongPoll(vk_session, '195404075')  # id сообщества
vk = vk_session.get_api()


def stat():
    r = requests.get('https://vote-cat.temocenter.ru/api/vote')
    votes = r.json()["votes"]
    s = "Всего голосов: {0}\n".format(votes)
    items = r.json()["items"]
    for i in items:
        s += i["name"] + ": " + str(round((i["votes"] / 100) * votes)) + " голосов ({0}%)\n".format(i["votes"])
    return s


def graph():
    now = datetime.now()
    cur_time = now.strftime("%H%M")
    print(cur_time)
    r = requests.get("https://vote-cat.temocenter.ru/api/vote")
    data = r.json()["items"]
    votes = r.json()["votes"]

    f = open('data.csv', 'a', newline='')
    with f:
        writer = csv.writer(f)
        writer.writerow(
            [int(cur_time) / 100, round(votes * data[0]["votes"] / 100), round(votes * data[1]["votes"] / 100),
             round(votes * data[2]["votes"] / 100), round(votes * data[3]["votes"] / 100),
             round(votes * data[4]["votes"] / 100)])
    df = pd.read_csv('data.csv')
    plot = df.plot(x="Time", y=["Gig", "Mashik", "Masharik", "Mashonok", "Smartcat"], kind="bar")
    fig = plot.get_figure()
    fig.savefig("output.png")


def main():
    users = []
    graph_img = ''
    phrases = ["Привет! Как дела с проектом?",
               "Приветствую! Посмотрел твой проект, перезвони мне, пожалуйста.",
               "Здравствуй! Поговорил с твоим заказчиком - тут не обойтись без графовых БД.",
               "Привет, ты что-нибудь слышал про клеточные автоматы?",
               "Я не думаю, что ты из любителей такой... Ну, старомодной музыки, но что ты думаешь о джазе?",
               "Alice! А нет, не она. Ладно.",
               "Welcome to based department. Перевод, конечно, убогий, но суть понятна.",
               "Привет, не подскажешь, как выйти из этого чата?",
               "Привет, ты можешь мне сейчас позвонить в дискорде?"]

    if int(cur_time) % 10 == 0:
        # перестраиваем график каждые 10 минут
        graph()

    # не мой код для отправки фото
    a = vk_session.method('photos.getMessagesUploadServer')
    b = requests.post(a['upload_url'], files={'photo': open('output.png', 'rb')}).json()
    c = vk_session.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[
        0]
    graph_img = 'photo{}_{}'.format(c['owner_id'], c['id'])

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_chat:
                try:

                    if '!дайгиги' in event.obj.message['text'].lower():
                        vk.messages.send(
                            peer_id=event.obj.message['peer_id'],
                            message='Гиги за шаги \nОтдай свой голос Родине! https://school.moscow/mesh_voting',
                            random_id=random.randint(0, 2 ** 64))
                    if 'клеточ' in event.obj.message['text'].lower() or 'автомат' in event.obj.message['text'].lower():
                        vk.messages.send(
                            peer_id=event.obj.message['peer_id'],
                            message='Мне послышалось, или кто-то сказал про клеточный автомат?',
                            random_id=random.randint(0, 2 ** 64))
                    if 'гиглав' in event.obj.message['text'].lower() or 'александр владимирович' in event.obj.message[
                        'text'].lower():
                        vk.messages.send(
                            peer_id=event.obj.message['peer_id'],
                            message='Да-да, я тут',
                            random_id=random.randint(0, 2 ** 64))
                    if 'скинь сотку' in event.obj.message['text'].lower() or 'биткоин' in event.obj.message[
                        'text'].lower() or 'дай сотку' in event.obj.message['text'].lower() or 'скиньте сотку' in \
                            event.obj.message['text'].lower() or 'сотк' in event.obj.message['text'].lower():
                        vk.messages.send(
                            peer_id=event.obj.message['peer_id'],
                            message='Кстати о деньгах. Мы недавно провели исследование: что больше всего гуглили в '
                                    'этом году? Ну, это было сложное исследование, в ходе которого мы хотели понять, '
                                    'что нужно народу. В итоге оказалось, что самое простое и, так сказать, '
                                    'банальное, и вместе с этим непонятное для народа - это просто слово блокчейн.',
                            random_id=random.randint(0, 2 ** 64))
                    if 'поджопник' in event.obj.message['text'].lower():
                        vk.messages.send(
                            peer_id=event.obj.message['peer_id'],
                            message='Да, ну согласен я',
                            random_id=random.randint(0, 2 ** 64))
                    if '!stats' in event.obj.message['text'].lower():
                        vk.messages.send(
                            peer_id=event.obj.message['peer_id'],
                            message=stat(),
                            random_id=random.randint(0, 2 ** 64),
                            attachment=graph_img)


                except TypeError:
                    pass
                try:
                    users.append(vk.messages.getConversationMembers(
                        peer_id=event.obj.message['peer_id'])["count"])
                    if len(users) > 2:
                        if users[-1] > users[-2]:
                            print("NEW!!!!!")
                            vk.messages.send(
                                peer_id=event.obj.message['peer_id'],
                                message=random.choice(phrases),
                                random_id=random.randint(0, 2 ** 64))
                except TypeError:
                    pass
                if len(users) > 1000:
                    users = []


if __name__ == '__main__':
    main()
