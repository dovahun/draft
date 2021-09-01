# Файловая структура 
| Название файла | Путь | Описание |
|----------------|:------|:--------|
|main.yml|defaults/main.yml|Указывает путь к каталогу переменных |
|handlers.yml|handlers/handlers.yml|Файл в котором хранятся хендлеры|
|main.yml|meta/main.yml|Файл в которм хранится мета-информация|
|main.yml|tasks/main.yml|Файл в котром хранятся таски|
|index.html.j2| templates/index.html.j2|Файл в котром написан html-код для стартовой страницы|
|localhost.j2| templates/localhost.j2| Конфиг файл Nginx|
|main.yml| vars/main.yml| Файл с переменными | 