#!/usr/bin/env bash

PATH_TO_DIR=$1

validate(){
  for file in $(find $PATH_TO_DIR -name "*.yaml")
  do
    cat $file | yq .
    if [[ `echo $?` = 1 ]]; then
      echo "Файл: $file не прошел валидацию"
      exit 1
    fi
  done
}
validate