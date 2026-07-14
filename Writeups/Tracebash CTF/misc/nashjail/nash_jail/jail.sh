#!/bin/bash
# Welcome to Nash! (Not A Shell).

export PATH=""
unalias -a
unset $(env | cut -d= -f1)
hash -r

echo "======================================"
echo "          Welcome to Nash!          "
echo "======================================"
echo "No alphanumeric characters allowed."
echo "Some symbols are restricted."
echo "Can you read flag ?"
echo "======================================"

while true; do
    if ! read -p "Nash> " input; then
        break
    fi

    if [[ "$input" =~ [a-zA-Z0-9/!\&\"\'%().*\<\>@] ]]; then
        echo "Illegal characters detected! Try again."
        continue
    fi
    
    eval "$input"
done
