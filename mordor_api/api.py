from requests import session
import re
from bs4 import BeautifulSoup
import urllib.parse

MAIN_URL = "https://forum.mordor-rp.com/index.php" 

class MordorAPI:
    #Основаная чат входа и выхода
    def __init__(self, user_agent: str, cookie: dict):
        self.user_agent = user_agent
        self.cookie = cookie
        self.session = session()
        self.session.headers = {"user-agent": user_agent}
        self.session.cookies.update(cookie)
        if BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('html')['data-logged-in'] == "false":
            return "Вы ввели неверные cookie!"

    
    def logout(self):
        """• Закрыть сессию •"""
        self.session.close()

    def current_member(self):
        """
        • Объект текущего пользователя •
        ➤ Возвращает массив:
        {
            "user_id": int,
            "username": str,
            "user_title": str, 
            "avatar": str,
            "messages_count": int,
            "reactions_count": int,
            "data_registration": date
        }
        """

        content = BeautifulSoup(self.session.get(f"{MAIN_URL}?account/account-details").content, 'html.parser')
        user_id = content.find('span', {'class': 'avatar avatar--xxs avatar--default avatar--default--dynamic'})
        if user_id:
            user_id = int(content.find('span', {'class': 'avatar avatar--xxs avatar--default avatar--default--dynamic'})['data-user-id'])
        else:
            user_id = int(content.find('span', {'class': 'avatar avatar--xxs'})['data-user-id'])
        member_info = self.get_member(user_id)
        return {"user_id": member_info['user_id'], "username": member_info['username'], "user_title": member_info['user_title'], "avatar": member_info['avatar'], "messages_count": member_info['messages_count'], "reactions_count": member_info['reactions_count'], "data_registration": member_info['data_registration']}
    
    def get_member(self, user_id: int):
        """
        • Найти пользователя по ID •
        ➤ Принимает параметры:
            user_id - ID пользователя
        ➤ Возвращает массив:
        {
            "user_id": int,
            "username": str,
            "user_title": str, 
            "avatar": str,
            "messages_count": int,
            "reactions_count": int,
            "data_registration": date
        }
        """

        content = BeautifulSoup(self.session.get(f"{MAIN_URL}?members/{user_id}").content, 'html.parser')
        username = content.find('h1', class_='memberHeader-name').text.strip()
        user_title = content.find('span', {'class': 'userTitle'}).text
        avatar = content.find('span', class_='avatar avatar--l avatar--default avatar--default--dynamic')
        if avatar:
            avatar = "Нету аватарки"
        else:
            avatar = content.find('span', class_='avatar avatar--l avatar--updateLink avatar--default avatar--default--dynamic')
            if avatar:
                avatar = "Нету аватарки"
            else:
                avatar = content.find('span', class_='avatar avatar--l avatar--updateLink')
                if avatar:
                    avatar = content.find('span', class_='avatar avatar--l avatar--updateLink').find('img')['src']
                else:
                    avatar = content.find('span', class_='avatar avatar--l').find('img')['src']
        messages_count = int(content.find('a', {'href': f'/index.php?search/member&user_id={user_id}'}).text.strip().replace(' ', ''))
        dl_elements = content.find_all('dl', class_='pairs pairs--rows pairs--rows--centered')
        data_registration = dl_elements[0].dd.get_text().replace(" ", "")
        reactions_count = int(dl_elements[1].dd.get_text().replace(" ", ""))
        return {"user_id": user_id, "username": username, "user_title": user_title, "avatar": avatar, "messages_count": messages_count, "reactions_count": reactions_count, "data_registration": data_registration}
    
    def get_forum_statistic(self):
        """
        • Получить статистику форума •
        ➤ Возвращает массив:
        {
            "threads_count": int,
            "posts_count": int,
            "users_count": int,
            "last_register_member": 
            {
                "user_id": int,
                "username": str,
                "user_title": str, 
                "avatar": str,
                "messages_count": int,
                "reactions_count": int,
                "data_registration": date
            }
        }
        """

        content = BeautifulSoup(self.session.get(MAIN_URL).content, 'html.parser')
        dl_elements = content.find_all('dl', class_='pairs--justified')
        threads_count = dl_elements[0].dd.get_text().replace(" ", "")
        posts_count = dl_elements[1].dd.get_text().replace(" ", "")
        users_count = dl_elements[2].dd.get_text().replace(" ", "")
        last_register_member = self.get_member(dl_elements[3].find('a')['data-user-id'])
        return {"threads_count": threads_count, "posts_count": posts_count, "users_count": users_count, "last_register_member": last_register_member}
    
    def get_category(self, category_id: int):
        """
        • Найти раздел по ID •
        ➤ Принимает параметры:
            category_id - ID раздела
        ➤ Возвращает массив:
        {
            "category_id": int,
            "title": str,
            "pages_count": int
        }
        """

        content = BeautifulSoup(self.session.get(f"{MAIN_URL}?forums/{category_id}").content, 'html.parser')
        title = content.find('h1', {'class': 'p-title-value'}).text
        try: pages_count = int(content.find_all('li', {'class': 'pageNav-page'})[-1].text)
        except IndexError: pages_count = 1
        try: parent_category_id = int(content.find('html')['data-container-key'].strip('node-'))
        except: parent_category_id = None 
        return {"category_id": category_id, "title": title, "pages_count": pages_count}

    def get_thread(self, thread_id: int):
        """
        • Найти тему по ID •
        ➤  Принимает параметры:
            thread_id - ID темы
        ➤ Возвращает массив:
        {
            "thread_id": int,
            "creator":
            {
                "user_id": int,
                "username": str,
                "user_title": str, 
                "avatar": str,
                "messages_count": int,
                "reactions_count": int,
                "data_registration": date
            }
            "category":
            {
                "category_id": int,
                "title": str,
                "pages_count": int
            }
            "create_date": int,
            "title": str,
            "prefix": str,
            "thread_content_html": str,
            "thread_content": str,
            "pages_count": int,
            "is_closed": bool,
            "thread_post_id": int
        }
        """

        content = BeautifulSoup(self.session.get(f"{MAIN_URL}?threads/{thread_id}/page-1").content, 'html.parser')
        creator = self.get_member(int(content.find('a', {'class': 'username'})['data-user-id']))
        category = self.get_category(int(content.find('html')['data-container-key'].strip('node-')))
        create_date = int(content.find('time')['data-time'])
        try: title = [i for i in content.find('h1', {'class': 'p-title-value'}).strings][-1]
        except: title = ""
        try: prefix = content.find('h1', {'class': 'p-title-value'}).find('span', {'class': 'label'}).text
        except: prefix = ""
        thread_content_html = content.find('div', {'class': 'bbWrapper'})
        thread_content = thread_content_html.text
        try: pages_count = int(content.find_all('li', {'class': 'pageNav-page'})[-1].text)
        except IndexError: pages_count = 1
        is_closed = False
        if content.find('dl', {'class': 'blockStatus'}): is_closed = True
        thread_post_id = content.find('article', {'id': re.compile('js-post-*')})['id'].strip('js-post-')
        return {"thread_id": thread_id, "creator": creator, "category": category, "create_date": create_date, "title": title, "prefix": prefix, "thread_content_html": thread_content_html, "thread_content": thread_content, "pages_count": pages_count, "is_closed": is_closed, "thread_post_id": thread_post_id}
    
    def get_post(self, post_id: int):
        """
        • Найти пост по ID •
        ➤ Принимает параметры:
            post_id - ID поста в теме
        ➤ Возвращает массив:
        {
            "post_id": id,
            "creator":
            {
                "user_id": int,
                "username": str,
                "user_title": str, 
                "avatar": str,
                "messages_count": int,
                "reactions_count": int,
                "data_registration": date
            }
            "thread":
            {
                "thread_id": int,
                "creator":
                {
                    "user_id": int,
                    "username": str,
                    "user_title": str, 
                    "avatar": str,
                    "messages_count": int,
                    "reactions_count": int,
                    "data_registration": date
                }
                "category":
                {
                    "category_id": int,
                    "title": str,
                    "pages_count": int
                }
                "create_date": int,
                "title": str,
                "prefix": str,
                "thread_content_html": str,
                "thread_content": str,
                "pages_count": int,
                "is_closed": bool,
                "thread_post_id": int
            }
            "create_date": int,
            "bb_content": str,
            "text_content": str
        }
        """

        content = BeautifulSoup(self.session.get(f"{MAIN_URL}?posts/{post_id}").content, 'html.parser')
        post = content.find('article', {'id': f'js-post-{post_id}'})
        creator = self.get_member(int(post.find('a', {'data-xf-init': 'member-tooltip'})['data-user-id']))
        thread = self.get_thread(int(content.find('html')['data-content-key'].strip('thread-')))
        create_date = int(post.find('time', {'class': 'u-dt'})['data-time'])
        bb_content = post.find('div', {'class': 'bbWrapper'})
        text_content = bb_content.text
        return {"post_id": post_id, "creator": creator, "thread": thread, "create_date": create_date, "bb_content": bb_content, "text_content": text_content}
    
    def get_profile_post(self, post_id):
        """
        • Найти сообщение профиля по ID •
        ➤ Принимает параметры:
            post_id - ID поста
        ➤ Возвращает массив:
        {
           "post_id": int,
           creator: 
           {
                "user_id": int,
                "username": str,
                "user_title": str, 
                "avatar": str,
                "messages_count": int,
                "reactions_count": int,
                "data_registration": date
            }
            profile:
            {
                "user_id": int,
                "username": str,
                "user_title": str, 
                "avatar": str,
                "messages_count": int,
                "reactions_count": int,
                "data_registration": date
            }
            "create_date": int,
            "bb_content": str,
            "text_content": str
        }
        """

        content = BeautifulSoup(self.session.get(f"{MAIN_URL}?profile-posts/{post_id}").content, 'html.parser')
        post = content.find('article', {'id': f'js-profilePost-{post_id}'})
        creator = self.get_member(int(post.find('a', {'class': 'username'})['data-user-id']))
        profile = self.get_member(int(content.find('span', {'class': 'username'})['data-user-id']))
        create_date = int(post.find('time')['data-time'])
        bb_content = post.find('article', class_='message-body')
        text_content = bb_content.text.strip()
        return {"post_id": post_id, "creator": creator, "profile": profile, "create_date": create_date, "bb_content": bb_content, "text_content": text_content}

    #-------------================ МЕТОДЫ ОБЪЕКТОВ ====================--------------------

    def create_thread(self, category_id: int, title: str, message_html: str):
        """
        • Создать тему в категории •
        ➤ Принимает параметры:
            category_id - ID раздела
            title - Название темы
            message_html - текст темы
        """

        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        return self.session.post(f"{MAIN_URL}?forums/{category_id}/post-thread", {'_xfToken': token, 'title': title, 'message_html': message_html, 'watch_thread': 1, "watch_thread_email": 1})
    
    def set_read_category(self, category_id: int):
        """
        • Отметить тему как прочитанную •
        ➤ Принимает параметры:
            category_id - ID раздела
        """

        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        return self.session.post(f"{MAIN_URL}?forums/{category_id}/mark-read", {'_xfToken': token})
    
    def get_threads(self, category_id: int, page: int = 1):
        """
        • Возвращает ID всех тем из раздела •
        ➤Принимает параметры:
            category_id - ID раздела
            page - номер страницы
        ➤ Возвращает массив:
        {
            pins: {}
            unpins: {}
        }
        """

        soup = BeautifulSoup(self.session.get(f"{MAIN_URL}?forums/{category_id}/page-{page}").content, "html.parser")
        result = {'pins': [], 'unpins': []}
        for thread in soup.find_all('div', re.compile('structItem structItem--thread.*')):
            link = thread.find_all('div', "structItem-title")[0].find_all("a")[-1]
            if len(re.findall(r'\d+', link['href'])) < 1: continue
            if len(thread.find_all('i', {'title': 'Закреплено'})) > 0: result['pins'].append(int(re.findall(r'\d+', urllib.parse.unquote(link['href']))[-1]))
            else: result['unpins'].append(int(re.findall(r'\d+', urllib.parse.unquote(link['href']))[-1]))
        return result
    
    def get_categories(self, category_id: int):
        """
        • Возращаеь ID всех дочерных категории из раздела •
        ➤ Принимает параметры: 
            category_id - ID раздела
        ➤ Вовзвращает массив
        """

        soup = BeautifulSoup(self.session.get(f"{MAIN_URL}?forums/{category_id}").content, "html.parser")
        result = []
        for category in soup.find_all('div', re.compile('.*node--depth2 node--forum.*')): 
            result.append(int(re.findall(r'\d+', urllib.parse.unquote(category.find("a")['href']))[-1]))
        return result
    
    # MEMBER
    def follow_member(self, member_id: int):
        """
        • Изменить статус подписки на пользователя •
        ➤ Принимает параметры: 
            member_id - ID пользователя
        """

        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        return self.session.post(f"{MAIN_URL}?members/{member_id}/follow", {'_xfToken': token})
    
    def ignore_member(self, member_id: int):
        """
        • Изменить статус игнора пользователя •
        ➤ Принимает параметры: 
            member_id - ID пользователя
        """

        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        return self.session.post(f"{MAIN_URL}?members/{member_id}/ignore", {'_xfToken': token})
    
    def get_profile_messages(self, member_id: int, page: int = 1):
        """
        Возвращает ID всех сообщений со стенки пользователя
        ➤ Принимает параметры:
            member_id - ID пользователя
            page - номер страницы
        ➤ Возвращает массив
        """

        soup = BeautifulSoup(self.session.get(f"{MAIN_URL}?members/{member_id}/page-{page}").content, "html.parser")
        result = []
        for post in soup.find_all('article', {'id': re.compile('js-profilePost-*')}):
            result.append(int(post['id'].strip('js-profilePost-')))
        return result
    
    # POST
    def react_post(self, post_id: int):
        """
        • Поставить реакцию на пост •
        ➤ Принимает параметры: 
            post_id - ID поста
        """

        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        return self.session.post(f'{MAIN_URL}?posts/{post_id}/like', {'_xfToken': token})
    
    def edit_post(self, post_id: int, html_message: str):
        """
        • Отредактировать пост •
        ➤ Принимает параметры:
            post_id - ID поста
            html_message - новый текст сообщения
        """

        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        return self.session.post(f"{MAIN_URL}?posts/{post_id}/edit", {"message_html": html_message, "message": html_message, "_xfToken": token})
    
    def delete_post(self, post_id: int, reason: str, hard_delete: int = 0):
        """
        • Удалить пост •
        ➤ Принимает параметры:
            post_id - ID поста
            reason - причина удаление
        """

        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        return self.session.post(f"{MAIN_URL}?posts/{post_id}/delete", {"reason": reason, "hard_delete": hard_delete, "_xfToken": token})
    
    # PROFILE POST
    def react_profile_post(self, post_id: int):
        """
        • Поставить реакцию на сообщение профиля •
        ➤ Принимает параметры:
            post_id - ID поста
        """

        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        return self.session.post(f'{MAIN_URL}?profile-posts/{post_id}/like', {'_xfToken': token})
    
    def delete_profile_post(self, post_id: int, reason: str, hard_delete: int = 0):
        """
        • Удалить сообщение профиля •
        ➤ Принимает параметры:
            post_id - ID поста
            reason - причина удаление
        """

        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        return self.session.post(f"{MAIN_URL}?profile-posts/{post_id}/delete", {"reason": reason, "hard_delete": hard_delete, "_xfToken": token})
    
    def edit_profile_post(self, post_id: int, html_message: str):
        """
        • Отредактировать сообщение профиля •
        ➤ Принимает параметры:
            post_id - ID поста
            html_message - новый текст сообщения
        """

        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        return self.session.post(f"{MAIN_URL}?profile-posts/{post_id}/edit", {"message_html": html_message, "message": html_message, "_xfToken": token})
    
    # THREAD
    def answer_thread(self, thread_id: int, html_message: str):
        """
        • Оставить ответ в теме •
        ➤ Принимает параметры:
            thread_id - ID темы
            html_message - текст сообщение
        """

        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        return self.session.post(f"{MAIN_URL}?threads/{thread_id}/add-reply", {'_xfToken': token, 'message_html': html_message})
    
    def watch_thread(self, thread_id: int, stop: bool, email_subscribe: bool = False):
        """
        • Отслеживание темы •
        ➤ Принимает параметры:
            thread_id - ID темы
            stop - (true - остоновить отслеживание, false - начать отслеживание)
        """

        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        return self.session.post(f"{MAIN_URL}?threads/{thread_id}/watch", {'_xfToken': token, 'stop': int(stop), 'email_subscribe': int(email_subscribe)})
    
    def delete_thread(self, thread_id: int, reason: str, hard_delete: int = 0):
        """
        • Удалить тему •
        ➤Принимает параметры:
            thread_id - ID темы
            reason - причина удаление
        """

        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        return self.session.post(f"{MAIN_URL}?threads/{thread_id}/delete", {"reason": reason, "hard_delete": hard_delete, "_xfToken": token})
    
    def get_thread_posts(self, thread_id: int, page: int = 1):
        """
        • Получить все посты из темы •
        ➤ Принимает параметры: 
            thread_id - ID темы
            page - номер страницы
            Возвращает массив
        """
        soup = BeautifulSoup(self.session.get(f"{MAIN_URL}?threads/{thread_id}/page-{page}").content, 'lxml')
        return_data = []
        for i in soup.find_all('article', {'id': re.compile('js-post-*')}):
            if i['id'].startswith('js-post-') == False: continue
            return_data.append(i['id'].strip('js-post-'))
        return return_data
    
    # OTHER
    def edit_avatar(self, upload_photo):
        """
        • Поставить новую аватарку •
        ➤ Принимает параметры: 
            upload_photo - путь до фото
        """
        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        with open(upload_photo, 'rb') as image:
            file_dict = {'upload': (upload_photo, image.read())}
        data = {
            "avatar_crop_x": 0, 
            "avatar_crop_y": 0,
            "_xfToken": token, 
            "use_custom": 1,
        }
        return self.session.post(f"{MAIN_URL}?account/avatar", files=file_dict, data=data)
    
    def delete_avatar(self):
        """
        • Удалить аватарку •
        """
        token = BeautifulSoup(self.session.get(f"{MAIN_URL}").content, 'html.parser').find('input', {'name': '_xfToken'})['value']
        file_dict = {'upload': ("", "")}
        data = {
            "avatar_crop_x": 0, 
            "avatar_crop_y": 0,
            "_xfToken": token, 
            "use_custom": 1,
            "delete_avatar": 1
        }
        return self.session.post(f"{MAIN_URL}?account/avatar", files=file_dict, data=data)

    def get_member_thread(self, member_id: int):
        """
        • Получить темы пользовителя •
        ➤Принимает параметры:
            member_id - ID пользовителя
        ➤ Возвращает массив:
        {
            "member_id": int,
            "pages_count": int
        }
        """
        content = BeautifulSoup(self.session.get(f"{MAIN_URL}?search/member&user_id={member_id}&content=thread").content, 'html.parser')
        try: pages_count = int(content.find_all('li', {'class': 'pageNav-page'})[-1].text)
        except IndexError: pages_count = 1
        return {"member_id": member_id, "pages_count": pages_count}
    
    def get_member_threads(self, member_id: int, page: int = 1):
        """
        • Возвращает ID всех тем пользовителя •
        ➤Принимает параметры:
            member_id - ID пользовителя
            page - номер страницы
        Возвращает массив:
        """

        soup = BeautifulSoup(self.session.get(f"{MAIN_URL}?search/member&user_id={member_id}&content=thread").content, "html.parser")
        url = soup.find('meta', attrs={'property': 'og:url'}).get('content', '')
        soupcontent = BeautifulSoup(self.session.get(f"{url}&page={page}").content, "html.parser")
        result = []
        for thread in soupcontent.find_all('li', class_='block-row--separated'):
            link = thread.find('h3', class_='contentRow-title').find('a')['href']
            result.append(int(re.findall(r'\d+', urllib.parse.unquote(link))[-1]))
        return result
