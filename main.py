import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import time


def main():
    users = []
    phrases = ["Привет! Как дела с проектом?",
               "Приветствую! Посмотрел твой проект, перезвони мне, пожалуйста.",
               "Здравствуй! Поговорил с твоим заказчиком - тут не обойтись без графовых БД.",
               "Привет, ты что-нибудь слышал про клеточные автоматы?",
               "Я не думаю, что ты из любителей такой... Ну, старомодной музыки, но что ты думаешь о джазе?"]
    vk_session = vk_api.VkApi(
        token=
        'c3a549d526acda59616b81d2c8817c9ac50b57aefbc1304164df6c1377e8c1d1f676f77dc1fe9348fba77'
    )
    longpoll = VkBotLongPoll(vk_session, '195404075')  # id сообщества
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_chat:
                try:
                    if '!дайгиги' in event.obj.message['text'].lower():
                        vk.messages.send(
                            peer_id=event.obj.message['peer_id'],
                            message='Гиги за шаги',
                            random_id=random.randint(0, 2**64))
                    if 'клеточ' in event.obj.message['text'].lower() or 'автомат' in event.obj.message['text'].lower():
                        vk.messages.send(
                            peer_id=event.obj.message['peer_id'],
                            message='Мне послышалось, или кто-то сказал про клеточный автомат?',
                            random_id=random.randint(0, 2**64))
                    if 'гиглав' in event.obj.message['text'].lower() or 'александр' in event.obj.message['text'].lower() or 'владимирович' in event.obj.message['text'].lower():
                        vk.messages.send(
                            peer_id=event.obj.message['peer_id'],
                            message='Звали?',
                            random_id=random.randint(0, 2**64))
                    if 'alice' in event.obj.message['text'].lower() or 'алис' in event.obj.message['text'].lower():
                        vk.messages.send(
                            peer_id=event.obj.message['peer_id'],
                            message='Alice! А нет, не она. Ладно',
                            random_id=random.randint(0, 2**64))

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
                                random_id=random.randint(0, 2**64))
                except TypeError:
                    pass
                if len(users) > 1000:
                    users = []



if __name__ == '__main__':
    main()
