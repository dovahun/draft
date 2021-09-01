#!/bin/bash
REGISTRY=docker-v2.dcarttst201lv.region.vtb.ru
pushImage() {
  docker -H 192.168.255.5 push $new_tag
  if [[ ! $? -eq 0 ]]
  then
   echo "cant push "$1
   exit 1
  fi
}

retagImage() {
 domain=$(echo $1 | awk -F '/' '{print $1}')
 new_tag=$(echo $1 | sed "s/$domain/$REGISTRY/")
 docker -H 192.168.255.5 tag $1 $new_tag
 if [[ ! $? -eq 0 ]]
 then
  echo "cant tag image "$1 $new_tag
  exit 1
 fi
}

pullImage(){
  docker -H 192.168.255.5 pull $1
    if [[ ! $? -eq 0 ]]
    then
      echo "cant pull "$1
      exit 1
  fi
}


while read -r line;
do
  pullImage $line
  retagImage $line
  pushImage $line
done