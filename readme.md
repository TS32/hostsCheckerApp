# Modify hosts config file to speedup access to github.com #

## Purpose ##

This script file provide a way to lookup the ip address of a given server name. and add the <IP> <Servername> pair to hosts config file.


## Requirements ##

In order to run this scripts, Python3.6+ is needed. and use the requirements.txt to install the requested libraries.
Only tested in Window10 (with python3.7)

pip3 install -r requirements.txt


## How to use it ##

GetIPAddressWithXpath : Get IP address from ipaddress.com and scrape it with XPath

GetIPAddressWithBS    : Get IP address from ipaddress.com and scrape it with BeautifulSoup

checkHostsLatency     : Read host and IP from system hosts config file, Ping the specific host IP to check the average latency in ms

updateHostsConfigFile : write the latest IP address for the hosts to the system config file

## How to use it ##

``` Console output
hostsCheckerApp> python hostscheckerApp.py
Outut as following :

1     :  140.82.112.3       github.com                                         Latency : 244.27ms
2     :  140.82.112.5       api.github.com                                     Latency : 244.36ms
3     :  199.232.68.133     raw.github.com                                     Latency : 230.36ms
4     :  140.82.114.3       gist.github.com                                    Latency : 240.75ms
5.1   :  185.199.108.154    help.github.com                                    Latency : 32.17ms
5.2   :  185.199.109.154    help.github.com                                    Latency : 32.11ms
5.3   :  185.199.110.154    help.github.com                                    Latency : 32.18ms
5.4   :  185.199.111.154    help.github.com                                    Latency : 32.4ms
6.1   :  185.199.108.153    githubstatus.com                                   Latency : 31.93ms
6.2   :  185.199.109.153    githubstatus.com                                   Latency : 31.8ms
6.3   :  185.199.110.153    githubstatus.com                                   Latency : 31.84ms
6.4   :  185.199.111.153    githubstatus.com                                   Latency : 32.79ms
7     :  140.82.113.10      codeload.github.com                                Latency : 241.35ms
8     :  140.82.112.9       nodeload.github.com                                Latency : 255.07ms
9     :  140.82.113.17      training.github.com                                Latency : 243.68ms
10.1  :  185.199.108.153    assets-cdn.github.com                              Latency : 32.2ms
10.2  :  185.199.109.153    assets-cdn.github.com                              Latency : 31.97ms
10.3  :  185.199.110.153    assets-cdn.github.com                              Latency : 31.86ms
10.4  :  185.199.111.153    assets-cdn.github.com                              Latency : 31.94ms
11.1  :  185.199.108.153    documentcloud.github.com                           Latency : 32.95ms
11.2  :  185.199.109.153    documentcloud.github.com                           Latency : 32.4ms
11.3  :  185.199.110.153    documentcloud.github.com                           Latency : 32.07ms
11.4  :  185.199.111.153    documentcloud.github.com                           Latency : 32.23ms
12    :  199.232.68.133     raw.githubusercontent.com                          Latency : 230.26ms
13    :  199.232.68.133     gist.githubusercontent.com                         Latency : 230.43ms
14    :  199.232.68.133     camo.githubusercontent.com                         Latency : 230.37ms
15    :  199.232.68.133     cloud.githubusercontent.com                        Latency : 230.27ms
16    :  199.232.69.194     github.global.ssl.fastly.net                       Latency : 262.01ms
17    :  52.216.107.212     github-cloud.s3.amazonaws.com                      Latency : 263.62ms
18    :  199.232.68.133     desktop.githubusercontent.com                      Latency : 230.18ms
19    :  199.232.68.133     avatars0.githubusercontent.com                     Latency : 230.17ms
20    :  199.232.68.133     avatars1.githubusercontent.com                     Latency : 230.22ms
21    :  199.232.68.133     avatars2.githubusercontent.com                     Latency : 230.38ms
22    :  199.232.68.133     avatars3.githubusercontent.com                     Latency : 230.33ms
23    :  199.232.68.133     avatars4.githubusercontent.com                     Latency : 233.79ms
24    :  199.232.68.133     avatars5.githubusercontent.com                     Latency : 230.29ms
25    :  199.232.68.133     avatars6.githubusercontent.com                     Latency : 230.34ms
26    :  199.232.68.133     avatars7.githubusercontent.com                     Latency : 230.35ms
27    :  199.232.68.133     avatars8.githubusercontent.com                     Latency : 230.31ms
28    :  199.232.68.133     user-images.githubusercontent.com                  Latency : 230.21ms
29    :  199.232.68.133     repository-images.githubusercontent.com            Latency : 230.29ms
30    :  199.232.68.133     marketplace-screenshots.githubusercontent.com      Latency : 230.23ms
Locate the hosts config from :  c:\windows\system32\drivers\etc\hosts
Host config entries number :  71
Done! new host file saved! result :

blanks_written : 8
comments_written : 24
ipv4_entries_written : 39
ipv6_entries_written : 0
total_written : 71

```
