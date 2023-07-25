<p align="center">
  <a href="http://mordor.ratmir.fun/docs/"><img alt="apimordor" src="http://mordor.ratmir.fun/docs/logo1.png" width="500" height="200" /></a>
  <br><br>
  <a href="http://mordor.ratmir.fun/docs/index.html"><img height="20" alt="apimordor documentation" src="https://img.shields.io/badge/docs-ratmir.fun-%20"></a>
  <img alt="Version" src="https://img.shields.io/badge/version-beta-blue" />
  <img alt="Python 3.7+" src="https://img.shields.io/badge/Python-3.7+-%23FFD242" />
  <img alt="code-style" src="https://img.shields.io/badge/code--style-black-%23000000" />
  <img alt="The Unlicense" src="https://img.shields.io/badge/license-The%20Unlicense-blue" />
  <img alt="mordor Badge" src="https://img.shields.io/badge/samp-Mordor%20RP-%20?color=%23fc2323">
</p>

<h1 align="center">  Mordor API </h1>
<p align="center">Готовый api для форума Mordor RP</p>

* [Документация](http://mordor.ratmir.fun/docs/)
* [Примеры](./examples)
* [Официальная тема на форуме](https://github.com/python273/vk_api/issues/356) (асинхронность; боты)

#Подключение и работа с биоблиотекой
```python
import mordor_api

cookies = {
    "xf_user": "your",
    "cf_clearance": "your",
    "xf_session": "your",
    "xf_csrf": "your",
}
user_agents = "your"

api = mordor_api.MordorAPI(user_agent=user_agents, cookie=cookies)
```
