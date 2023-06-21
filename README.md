# akasiteshieldips
Quick and dirty script which fetches Siteshield CIDR ranges from Akamai's api and uses that in firewall rules. 

This is a standalone version, no package install needed. Akamai's Edge authentication
is included locally. The library is taken from the official repository:
https://github.com/akamai/AkamaiOPEN-edgegrid-python

You need to include a file called apiclient.txt in the scripts folder, which
will contain your api client credentials in the format:

client_secret
https://base_url
access_token
client_token

Api client needs to have read access to Siteshield and Firewall notifications.

Use sudo run.sh to automatically run all the scripts, generate the necessary data
and apply it to IPtables configuration.
