import mordor_api

cookies = {
    "xf_user": "your",
    "cf_clearance": "your",
    "xf_session": "your",
    "xf_csrf": "your",
}
user_agents = "your"

api = mordor_api.MordorAPI(user_agent=user_agents, cookie=cookies)

#Изменить аватарку
uploadnewphoto = api.edit_avatar("photo.jpg")
print(uploadnewphoto)

#Удалить аватарку
deleteavatar = api.delete_avatar()
print(deleteavatar)