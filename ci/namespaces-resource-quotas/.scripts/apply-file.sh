#!/usr/bin/env bash

PATH_TO_DIR=$1

apply(){
  for file in $(find $PATH_TO_DIR -name "*.yaml")
  do
    echo $file
    kubectl apply -f $file
  done
}
apply
