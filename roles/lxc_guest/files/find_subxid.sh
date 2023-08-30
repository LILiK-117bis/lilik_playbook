#!/bin/bash

## Detect the first available continuous allocation of subuids/subgids
## of a given size.
##
## Returns output in idmap format:
## <starting_sub[ug]id> <allocation_length>
## Author: Lorenzo Zolfanelli <zolfa@lilik.it>

required_length=65536

function find_interval {
  if [ ! -f "$1" ]; then
    echo "100000 ${required_length}"
    return 0
  fi
  min_id_list=(100000 $(sed -n -e 's/^[^:]\+:\([0-9]\+\):\([0-9]\+\)/\1/p' $1))
  inc_id_list=(0 $(sed -n -e 's/^[^:]\+:\([0-9]\+\):\([0-9]\+\)/\2/p' $1))
  rows=$(( ${#min_id_list[*]} - 1 ))
  if [ $rows -lt 1 ]; then
    echo "100000 ${required_length}"
    return 0
  fi
  for i in $(seq 0 $rows); do
    c_start=$(( ${min_id_list[i]} + ${inc_id_list[i]} ))
    c_end=$(( ${c_start} + ${required_length} - 1 ))
    overlap=0
    for j in $(seq 0 $rows); do
      j_start=${min_id_list[j]}
      j_end=$(( ${min_id_list[j]} + ${inc_id_list[j]} - 1 ))
      if ([ "${c_start}" -ge "${j_start}" ] && [ "${c_start}" -le "${j_end}" ]) || ([ "${c_end}" -ge "${j_start}" ] && [ "${c_end}" -le "${j_end}" ]); then
        overlap=1
        break
      fi
    done
    if [ "${overlap}" -eq "0" ]; then
      echo "${c_start} ${required_length}"
      return 0
    fi
  done
}

find_interval /etc/subuid
find_interval /etc/subgid
