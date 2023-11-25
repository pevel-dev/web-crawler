## Веб-краулер

### Основные Критерии:
* [x] Не используется scrapy
* [x] Парсинг с помощью html.parser
* [ ] Сохранение html страниц, не скачивать повторно
* [ ] Фильтры для ссылок (переход в рамках указанных доменнов)
* [ ] Поддержка robots.txt (Only allow/disallow for user-agent: *)
* [x] Многопоточность
* [x] Возможность докачки (С новыми фильтрами, нужно указать точку входа)

### Некоторые фичи:
* [ ] Кастомное количество retry
* [ ] Кастомный таймаут
* [ ] Поддержка/Запрет redirect (http status 301)

