import mordor_api

cookies = {
    "xf_user": "your",
    "cf_clearance": "your",
    "xf_session": "your",
    "xf_csrf": "your",
}
user_agents = "your"

api = mordor_api.MordorAPI(user_agent=user_agents, cookie=cookies)

getuserthread = api.get_member_thread(14678)
print(getuserthread)

getuserthread = api.get_member_threads(14678, 1)
for i in getuserthread:
    print(api.get_thread(i)['title'])