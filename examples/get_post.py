import mordor_api

cookies = {
    "xf_user": "your",
    "cf_clearance": "your",
    "xf_session": "your",
    "xf_csrf": "your",
}
user_agents = "your"

api = mordor_api.MordorAPI(user_agent=user_agents, cookie=cookies)

#Получить все посты в теме
getthreadpost = api.get_thread_posts(567391)
for i in getthreadpost:
    print(api.get_post(i)['text_content'])

#Получить все сообщение в профиле пользовителя
getprofilemsg = api.get_profile_messages(7325, 1)
for i in getprofilemsg:
    print(i)