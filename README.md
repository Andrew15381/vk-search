# vk-search

## Постановка задачи
Бот для расширенного поиска друзей ВКонтакте. Допускается пошаговое расширение области поиска подписчиками групп (sub) и друзьями (friend) уже найденных людей и, наоборот, фильтрация по значениям полей "имя" (name), "дата рождения" (bday).

Пример команды:
/search 1 friend sub name("Андрей") bday("1997") sub

## Используемые библиотеки:
 * aiogram
 * vkbottle

## Вспомогательные библиотеки:
 * pydocstyle
 * flake8
 * sphinx
 * pybabel
 * pytest
 * doit
 * setuptools
 * build
