��          <               \   �  ]   3   D  3   x  �  �  �  �  e   i  Y   �   Commands list:
/start - start bot
/help - show this message
/search - search among user's friends or groups' subs

The search is performed step by step, starting from user_id and continuing with a set of modificators:
* friends (add current users' friends to next step),
* subs (add current users' groups subs to next step),
* name (filter current users by name part, both first and last),
* bdate (filter current users by bdate part).

Example:
/search 168768958 friends name("Azimov") Enter a user id and a set of modifications to start Found more than 100 users, try to narrow the search Project-Id-Version: PROJECT VERSION
Report-Msgid-Bugs-To: EMAIL@ADDRESS
POT-Creation-Date: 2023-06-13 10:00+0300
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: ru
Language-Team: ru <LL@li.org>
Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.9.1
 Список команд:
/start - начать работу с ботом
/help - вывести это сообщение
/search - поиск среди друзей и подписчиков групп пользователя

Подробнее о поиске. Поиск осуществляется пошагово, начиная с user_id и с применением последующих модификаторов:
* friends - добавляет на следующий шаг друзей текущих пользователей
* subs - добавляет на следующий шаг подписчиков групп, где состоят текущие пользователи
* name - фильтрует текущих пользователей по части имени (без пробелов)
* bdate - фильтрует текущих пользователей по части дня рождения.

Пример:
/search 168768958 friends name("Azimov") Укажите аккаунт для старта и набор расширений/фильтров Найдено больше 100 пользователей, уточните запрос 