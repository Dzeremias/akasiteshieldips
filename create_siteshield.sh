#!/bin/bash
name="akamai_siteshield"
name_stage="akamai_siteshield_stage"

echo "Removing IPtable rules"
iptables -D INPUT -p tcp --dport 80 -m set --match-set $name src -j ACCEPT
iptables -D INPUT -p tcp --dport 80 -m set --match-set $name_stage src -j ACCEPT
iptables -D INPUT -p tcp --dport 443 -m set --match-set $name src -j ACCEPT
iptables -D INPUT -p tcp --dport 443 -m set --match-set $name_stage src -j ACCEPT
echo "Removing the old ipsets $name and $name_stage"
ipset destroy $name
ipset destroy $name_stage
echo "Creating a new version of $name and $name_stage"
ipset create $name hash:net
ipset create $name_stage hash:net
while read line; do
	echo "Adding $line to $name"
	ipset add $name $line;
done < siteshield.txt

while read line; do
	echo "Adding $line to $name_stage"
	ipset add $name_stage $line;
done < staging_siteshield.txt

iptables -I INPUT 1 -p tcp --dport 80 -m set --match-set akamai_siteshield_stage src -j ACCEPT
iptables -I INPUT 1 -p tcp --dport 443 -m set --match-set akamai_siteshield_stage src -j ACCEPT
iptables -I INPUT 1 -p tcp --dport 80 -m set --match-set akamai_siteshield src -j ACCEPT
iptables -I INPUT 1 -p tcp --dport 443 -m set --match-set akamai_siteshield src -j ACCEPT
