#### Скрипт нужен для удаления каталогов RELEASE и HOTFIX в /ftp/ftp-user/ на инстансе 172.16.0.87
#### Работает в cron, находиться в папке opt.
### Запуск:
##### Для запуска скрипта надо указать флаги, пути до директории и количества дней, файлы которые старше заданного количества дней будут удалены.
```bash
Usage:
    ./ftp_cleaner.sh -p {path/to/dir} -d +{} -r {2} -n {2}

Flags:
    -h      Show information.
    -p      Path to directory.
    -d      Remove files, which older then a given number of days.
    -r      Count to save RELEASE.
    -n      Count to save HOTFIX.

Example:
    ./backupCleaner.sh -p /ftp/ftp-user/ -d +30 -r 3 -n 5 
```
