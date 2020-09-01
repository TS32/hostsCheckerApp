from ssl import match_hostname
from pythonping import ping
from python_hosts import Hosts, HostsEntry
import requests
from bs4 import BeautifulSoup
import re

"""

Use PythonPing to check the host reachable and connectivity.


PythonPing Parameters
+==========================================================================================================
| Parameter   | Type         | Description  
+-------------------------------------------------------------------------------------------------------                                                                                                                                                                                                                    |
| target      | str          | The remote device to ping. This is the only mandatory parameter.                                                                                                                                                                 |
| timeout     | int          | How long before considering a non-received response lost, in seconds.                                                                                                                                                            |
| count       | int          | How many ICMP packets to send in sequence.                                                                                                                                                                                       |
| size        | int          | The size of the entire ICMP packet we want to send. You can leave it to 0, the default value, to adapt the size to the payload and not the other way around.                                                                     |
| payload     | str or bytes | The payload of the packet. If you provide also the size of the payload, this will be cut or repeated to match the desired size.                                                                                                  |
| sweep_start | int          | To be used together with sweep_end. It ignores the size and sends each subsequent packet by incrementing payload size by one byte, starting from sweep_start size all the way to sweep_end size. Useful when trying to find MTU. |
| sweep_end   | int          | When doing a ping sweep (with sweep_start), maximum payload size to reach.                                                                                                                                                       |
| df          | bool         | Value for the Don’t Fragment flag of the IP header.                                                                                                                                                                              |
| verbose     | bool         | True if you wish to write output to the screen.                                                                                                                                                                                  |
| out         | file         | Where to direct the output, by default sys.stdout.   
+==============================================================================================================      
PythonPing return values:
Since a Response is an object, you can get its properties from its members.

error_message contains a string describing the error this response represents. For example, an error could be “Network Unreachable” or “Fragmentation Required”. If you got a successful response, this property is None.
success is a bool indicating if the response is successful
time_elapsed and time_elapsed_ms indicate how long it took to receive this response, respectively in seconds and milliseconds.
You can access individual responses by accessing the _responses property of your ResponseList object, returned from ping(). In this case, _responses is simply a list. However, _responses are not meant to be accessed from outside the ResponseList, you should work with ResponseList directly. On top of that, ResponseList adds some intelligence you can access from its own members. The fields are self-explanatory:

rtt_min and rtt_min_ms
rtt_max and rtt_max_ms
rtt_avg and rtt_avg_ms
                                                                                                                                                                    |
"""

def checkHostsLatency(hostname_keyword=None):
	my_hosts = Hosts()
	print(my_hosts.determine_hosts_path())
	print("Host config entries : ", my_hosts.count())

	entry=0

	for host in my_hosts.entries:		
		if(host.entry_type=="ipv4"):
			if(hostname_keyword is None): #by default print all entries
				print(host)
			else: #print entries with keyword
				hostString ="".join(host.names)
				hostString = hostString.strip().lower()
				if(hostname_keyword.strip().lower() in hostString):
					ipaddr=host.address
					latency=ping(ipaddr,size = 1000,verbose=False).rtt_avg_ms
					print(entry,f"  Latency {latency:<7.2f}ms " , host)
					entry+=1
	
	if(entry==0):
		print(hostname_keyword, " Not found in the host file!\n")


def checkLatency(hostFile):
	hostFile = open(hostFile,"r",encoding = "utf-8")

	filecontent = hostFile.readlines()

	hostFile.close()

	ip_address_pattern = r"[1-9]\d{0,2}\.\d{1,3}\.\d{1,3}\.\d{1,3}[\s\t]+"
	hostname_pattern = r'[\s|\t]+((?:[a-zA-Z0-9-_]+\.)+(?:[a-zA-Z])+)'

	for i,line in enumerate(filecontent):
		ip_list = re.search(ip_address_pattern,line)
		hostname_list=re.search(hostname_pattern,line)
		if ip_list is not None and hostname_list is not None:
			ipaddr= ip_list.group().strip()
			hostname = hostname_list.group().strip()
			response = ping(ipaddr,size = 1000,verbose=False)
			print(f"{i+1:<3}  IP : {ipaddr:<15}\tLatency : {response.rtt_avg_ms:<7.2f}ms\tHost : {hostname}")

def getGitHubLatestIpAddress():
	""" Get IPaddress of each server from Ipaddresss.com """
	ServerNamesList =[
				'github.com',
				'gist.github.com',
				'assets-cdn.github.com',
				'raw.githubusercontent.com',
				'github-cloud.s3.amazonaws.com',
				'github.global.ssl.fastly.net',
				'codeload.github.com',
				'gist.githubusercontent.com',
				'cloud.githubusercontent.com',
				'camo.githubusercontent.com',
				'avatars0.githubusercontent.com',
				'avatars1.githubusercontent.com',
				'avatars2.githubusercontent.com',
				'avatars3.githubusercontent.com',
				'avatars4.githubusercontent.com',
				'avatars5.githubusercontent.com',
				'avatars6.githubusercontent.com',
				'avatars7.githubusercontent.com',
				'avatars8.githubusercontent.com'
				]	
	ServerLinksList =[
				'https://github.com.ipaddress.com/', # github.com
				'https://github.com.ipaddress.com/gist.github.com', # gist.github.com
				'https://github.com.ipaddress.com/assets-cdn.github.com', # assets-cdn.github.com	
				'https://githubusercontent.com.ipaddress.com/raw.githubusercontent.com',# raw.githubusercontent.com
				'https://amazonaws.com.ipaddress.com/github-cloud.s3.amazonaws.com',# github-cloud.s3.amazonaws.com
				'https://fastly.net.ipaddress.com/github.global.ssl.fastly.net', #github.global.ssl.fastly.net
				'https://github.com.ipaddress.com/codeload.github.com',#codeload.github.com
				'https://githubusercontent.com.ipaddress.com/gist.githubusercontent.com',#gist.githubusercontent.com
				'https://githubusercontent.com.ipaddress.com/cloud.githubusercontent.com',#cloud.githubusercontent.com
				'https://githubusercontent.com.ipaddress.com/camo.githubusercontent.com',#camo.githubusercontent.com
				'https://githubusercontent.com.ipaddress.com/avatars0.githubusercontent.com',#avatars0.githubusercontent.com
				'https://githubusercontent.com.ipaddress.com/avatars1.githubusercontent.com',#avatars1.githubusercontent.com
				'https://githubusercontent.com.ipaddress.com/avatars2.githubusercontent.com',#avatars2.githubusercontent.com
				'https://githubusercontent.com.ipaddress.com/avatars3.githubusercontent.com',#avatars3.githubusercontent.com
				'https://githubusercontent.com.ipaddress.com/avatars4.githubusercontent.com',#avatars4.githubusercontent.com
				'https://githubusercontent.com.ipaddress.com/avatars5.githubusercontent.com',#avatars5.githubusercontent.com
				'https://githubusercontent.com.ipaddress.com/avatars6.githubusercontent.com',#avatars6.githubusercontent.com
				'https://githubusercontent.com.ipaddress.com/avatars7.githubusercontent.com',#avatars7.githubusercontent.com
				'https://githubusercontent.com.ipaddress.com/avatars8.githubusercontent.com' #avatars8.githubusercontent.com
				
				
				]	
	ServerIpAddressList=[]
	Request_Header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
	
	ip_address_pattern = r"[1-9]\d{0,2}\.\d{1,3}\.\d{1,3}\.\d{1,3}[\s\t]*"

	width = max([len(k) for k in ServerNamesList])+4

	for index,serverLinks in enumerate(ServerLinksList):
		servername = ServerNamesList[index]		
		try:
			response = requests.get(serverLinks, Request_Header,timeout=(15,15))
			soup = BeautifulSoup(response.text, features = 'lxml')		
			match_result = soup.find_all('ul', {'class': 'comma-separated'})
			match_result_backup = soup.find_all('li')	
			# print(f"{servername:<{width}}\n \
			# 		{'None' if match_result is None else match_result[0].text[0:15]}\n \
			# 		{'None' if match_result_backup is None else match_result_backup[0].text[0:15]}\n \
			# 	 ")

			serverIp = None
			
			if(match_result is not None and len(match_result)):
				serverIp = re.search(ip_address_pattern,match_result[0].text)
				if serverIp is not None:
					serverIp = serverIp.group().strip()
					ServerIpAddressList.append({"Ip":serverIp,"Host":servername})
					latency=ping(serverIp,size = 1000,verbose=False).rtt_avg_ms
					print(f'{index:<6}:  {serverIp:<15}    {servername:<{width}}  Latency : {latency}ms')				

			if(match_result_backup is not None):# There is no match, then check if there is other matches				
				if match_result_backup is not None and len(match_result_backup):
					iplist=[]					
					for i in range(len(match_result_backup)):
						ip = re.search(ip_address_pattern,match_result_backup[i].text) 
						if ip is not None:
							ip = ip.group().strip()
						else:
							continue  # does not contain IP, skip

						if(ip not in iplist) and ((serverIp is not None ) and (ip!=serverIp) or (serverIp is None)):	
							iplist.append(ip)
							latency=ping(ip,size = 1000,verbose=False).rtt_avg_ms
							print(f'{index:<3}.{i:<2}:  {ip:<15}    {servername:<{width}}  Latency : {latency}ms')
							ServerIpAddressList.append({"Ip":ip,"Host":servername})
			if(match_result_backup is None and match_result is None):
				print(f'{index:<6}:  {"IP Not Found!  "}    {servername}')	
		except Exception as e:
			print(e)
			print(f'{index:<3}:  {"Exception!     "}    {servername}')
	if(len(ServerIpAddressList)):
		return ServerIpAddressList
	else:
		return None

def updateHostsConfigFile(newEntriesList):
	my_hosts = Hosts()
	print("Locate the hosts config from : ", my_hosts.determine_hosts_path())
	print("Host config entries number : ", my_hosts.count())
	
	#step 1, remove all the entries with the same name
	for entry in newEntriesList:
		my_hosts.remove_all_matching(name=entry['Host'])
	
	#step 2, add the entry from the new entry list
	for entry in newEntriesList:
		new_entry = HostsEntry(entry_type='ipv4', address=entry['Ip'], names=entry['Host'])
		ret=my_hosts.add([new_entry],allow_address_duplication=True)
		print(f"Add ipv4 entry for:  {new_entry}\n\tOperation result : {ret}")
	
	#step 3, write the host file
	result = my_hosts.write()
	print(f"Done! new host file saved!\n{result}")

if __name__ == '__main__':

	#hostFile = "hosts.txt"
	#checkLatency(hostFile)
	#checkHostsLatency("github")

	entryList = getGitHubLatestIpAddress()
	if(entryList is not None):
		updateHostsConfigFile(entryList)
	else:
		print("Nothing updated for the hosts file! ")



