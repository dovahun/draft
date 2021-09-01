#!/usr/bin/env bash
path=$1
fly -t main sync
GETTEAMS=($(fly -t main teams))
manageTeam(){
  for file in $(find $path -name "*.yaml")
  do
    NAME=$(cat $file | yq r - name)
    STATE=$(cat $file | yq r - state)
    case $STATE in
      "present")
        fly -t main set-team -c $file -n $NAME --non-interactive
        ;;
      "absent")
        # shellcheck disable=SC2068
        for team in ${GETTEAMS[@]}
        do
          if [ "$team" == "$NAME" ]; then
            fly -t main destroy-team -n $NAME --non-interactive
          fi
        done
        ;;
    esac
  done
}
manageTeam
