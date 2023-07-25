import mordor_api

cookies = {
    "xf_user": "your",
    "cf_clearance": "your",
    "xf_session": "your",
    "xf_csrf": "your",
}
user_agents = "your"

api = mordor_api.MordorAPI(user_agent=user_agents, cookie=cookies)

user = api.current_member()
print(f"Имя: {user['username']} | Подпись: {user['user_title']} | Аватар: {user['avatar']} | Сообщения: {user['messages_count']} | Симпатий: {user['reactions_count']} | Дата рег: {user['data_registration']}")

member = api.get_member(14678)
print(f"Имя: {member['username']} | Подпись: {member['user_title']} | Аватар: {member['avatar']} | Сообщения: {member['messages_count']} | Симпатий: {member['reactions_count']} | Дата рег: {member['data_registration']}")

category = api.get_category(78)
print(f"Название: {category['title']} ({category['id']}) | Страниц: {category['pages_count']}")

thread = api.get_thread(16607)
print(f"Название: {thread['title']} ({thread['id']})| Автор темы: {thread['creator']['username']} Категория: {thread['category']['title']} ({thread['category']['id']}) | Дата создания: {thread['create_date']} | Закрыто: {thread['is_closed']}")

statistic = api.get_forum_statistic()
print(f"Количество тем: {statistic['threads_count']} | Количество сообщение: {statistic['posts_count']} | Всего пользователей: {statistic['users_count']} | Последний чел: {statistic['last_register_member']}")

post = api.get_post(4599861)
print(f"Автор: {post['creator']['username']}({post['creator']['id']}) | ID: {post['id']} | Дата создания: {post['create_date']} | Размещено в теме {post['thread']['title']} | {post['bb_content']}")

profile_post = api.get_profile_post(224876)
print(f"Автор: {profile_post['creator']['username']} ({profile_post['creator']['id']}) | Создано в {profile_post['create_date']} у пользователя {profile_post['profile']['username']} ({profile_post['profile']['id']}) | {profile_post['bb_content']}")
