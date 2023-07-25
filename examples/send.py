import mordor_api

cookies = {
    "xf_user": "your",
    "cf_clearance": "your",
    "xf_session": "your",
    "xf_csrf": "your",
}
user_agents = "your"

api = mordor_api.MordorAPI(user_agent=user_agents, cookie=cookies)

#Создать тему
createthread = api.create_thread(560, "test", "это тема была создана с помощью api")
print(createthread)

#Устоновить статус прочитанный
readcat = api.set_read_category(560)
print(readcat)

#Подписка/отписка от пользовителя
followmem = api.follow_member(101190)
print(followmem)

#Изменить статус игнора пользовителя
ignoremem = api.ignore_member(101190)
print(ignoremem)

#Поставить/убрать лайк на пост
reactpost = api.react_post(5075104)
print(reactpost)

#Редактировать пост
editpost = api.edit_post(5075112, "я крут")
print(editpost)

#Удалить пост
deletepost = api.delete_post(5075118, "хз")
print(deletepost)

#Поставить лайк на пост в профиле пользовителя
reactprofilepost = api.react_profile_post(224017)
print(reactprofilepost)

#Удалить пост в профиле пользовителя
deleteprofilepost = api.delete_profile_post(224649, "нет")
print(deleteprofilepost)

#Редактировать пост в профиле пользовителя
editprofilepost = api.edit_profile_post(224650, "нет")
print(editprofilepost)

#Ответить в теме
answermsg = api.answer_thread(567391, "ого")
print(answermsg)

#Изменить отслеживание в теме
watchthread = api.watch_thread(567391, False)
print(watchthread)

#Удалить тему
deletethread = api.delete_thread(567418, "хз")
print(deletethread)
