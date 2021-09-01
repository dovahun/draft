# Описание playbook
### Конфигурация playbook
| Имя переменной | Путь к переменной | Описание |
| --------------:|:-----------------:|:---------|
|    book      | Локальная переменная в playbook | Выводит надпись на экран "vars from playbook" используется в файле web.yml |
|    vars_not_book         | vars/nginx_vars.yml | Выводит надпись на экран "vars not from playbook", находится в файле vars/nginx_vars.yml |
|     vars_cycle   | vars/nginx_vars.yml | Выводит на экран переменные циклом,находится в файле vars/nginx_vars.yml |

### Как запустить playbook:
 Вводите команду `ansible-playbook web.yml -i inventory/hosts.ini `
