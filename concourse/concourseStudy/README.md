# Pipeline
### Как запустить  pipeline
####  шаг-1
1) Аутентификация(Используется один раз для одной комманды ):\
`fly -t playground login --concourse-url=https://ci.fabric8.ru -n playground`
#### Где:
```
1. -t - это опция названия целевого сервера (название моего таргета "playground")
2. -login - это команда логина
3. --concourse-url - задаёте УРЛ где находится ваш кластер ConcourseCI; Указывается только в первый раз.
4. -n - это имя комманды  
```
#### шаг-2
2) Создание pipeline:\
`fly -t playground sp -c pipeline.yml -p playground `
#### Где:
```
1. -t - название целевого сервера где мы запускаем пайплайн
2. sp(set-pipeline)-команда для создания конвейера 
3. -с - имя файла конфигурации конвейера 
4. -p - даем имя ковейеру с которым он отобразится на вэб странице
```
#### шаг-3 
3) Запуск pipeline:\
`fly -t playground unpause-pipeline -p playground `
#### Где:
````
 unpause-pipeline - это команда для запуска pipeline
````
 или:\
`fly -t playground sp -c pipeline.yml -p playground --load-vars-from vars.yml `
#### Где:
````
--load-vars-from - это параметр для секретных значений 
````
