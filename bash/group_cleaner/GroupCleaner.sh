#!/usr/bin/env bash

#Создание флагов
while test $# -gt 0; do
  case "$1" in
    -dir) #путь до ддиректории с нужными файлами
    shift
    path_to_dir=$1
    shift
    ;;

    -dg) # Группу которую нужно удалить
    shift
    group_delete=$1
    shift
    ;;

    -fg) #Группа по которой отбираем полльзователей
    shift
    group_find=$1
    shift
    ;;

    -e) #расширение файлов
    shift
    extension=$1
    shift
    ;;

    *)
    echo "$1 is not a recognized flag!"
    return 1;
    ;;
    esac
done

#Удаление групп
deleteGroup(){
  for file in $(find $path_to_dir -type f -name "*.$extension")
  do
    GET_USER_LOGIN=$(yq e '.login' $file)
    PARAMS=$(yq e '.params.state' $file )
    FIND_GROUP_DELETE=$(yq e '.groups' $file | grep "$group_delete")
    FIND_GROUP=$(yq e '.groups' $file | grep "$group_find")
    if [[ $PARAMS != 'absent'  && $FIND_GROUP_DELETE  ]]
      then
        if [[ -z $FIND_GROUP ]]
        then
          echo "Delete group: $FIND_GROUP_DELETE  user: " $GET_USER_LOGIN
          sed -i '' 's/- '$group_delete'//' $file && sed -i '' '/^[[:space:]]*$/d' $file
        fi
    fi
  done
}

deleteGroup

