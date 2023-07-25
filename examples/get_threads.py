import mordor_api

cookies = {
    "xf_user": "your",
    "cf_clearance": "your",
    "xf_session": "your",
    "xf_csrf": "your",
}
user_agents = "your"

api = mordor_api.MordorAPI(user_agent=user_agents, cookie=cookies)

threads = api.get_threads(78)
print('Закрепленные темы:')
for i in threads["pins"]:
    thread = api.get_thread(i)
    print(f"{thread['title']} by {thread['creator']['username']}")

print('\n____________________\nНезакрепленные темы:')
for i in threads["unpins"]:
    thread = api.get_thread(i)
    print(f"{thread['title']} by {thread['creator']['username']}")