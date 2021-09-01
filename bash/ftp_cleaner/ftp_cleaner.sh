#!/usr/bin/env bash

day=
path_to_dir=
number_hotfix=
number_release=
path_to_logs=
#Вывод информации если задан неверный флаг
function usage {
        echo "Usage: $(basename $0) [-d,-p,-n,-r, -l]" 2>&1
        echo '   -h   Show information'
        echo '   -p   Path to directory'
        echo '   -d   Days after create'
        echo '   -n   Amount of latest Hotfixes to exclude'
        echo '   -r   Amount of latest Releases to exclude'
        exit 1
}

if [[ ${#} -eq 0  ]]; then
  usage
fi

#Создание флагов
while getopts ":p:d:r:n:h" arg; do
  case "${arg}" in
    d) day="${OPTARG}" ;;
    p) path_to_dir="${OPTARG}" ;;
    r) number_release="${OPTARG}";;
    n) number_hotfix="${OPTARG}";;
    h) usage; exit 1 ;;
    ?)
      echo "Invalid option: -${OPTARG}."
      usage
      ;;
  esac
done
#function receives search template, days and amount of folders to exclude from deletion
Remove() {
 find $1 -type d -name "$2-*" -mtime +$3  -printf "%T+\t%p\n" | sort -r | tail -n +$4 | cut -f 2 | xargs rm -rf 
}
#Запуск функций
Remove $path_to_dir HOTFIX $day $number_hotfix
Remove $path_to_dir RELEASE $day $number_release
