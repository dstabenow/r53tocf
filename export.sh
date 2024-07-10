#!/bin/bash
read -p "Enter domain name: " domain
if [[ -z "$domain" ]]; then
  echo "Error: Please enter a domain name."
  exit 1
fi

command="cli53 export --full --debug $domain > $domain.txt 2> $domain.err.log"
eval "$command"
if [[ $? -ne 0 ]]; then
  echo "Error: cli53 command failed. See $domain.err.log for details."
fi
echo "Domain information exported to $domain.txt"
echo "Debug log exported to $domain.err.log"

removelines="python3 modify.py $domain.txt"
eval "$removelines"
if [[ $? -ne 0 ]]; then
  echo "Error: remove_lines.py script failed."
fi
echo "NS and SOA records removed from $domain.txt"

echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo ""
echo "copy the below to your clipboard and Download using the Actions bar in the upper right corner"
echo ""
echo "$PWD/$domain.txt"
echo ""
echo ""
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
