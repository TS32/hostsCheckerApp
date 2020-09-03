from pythonping import ping
from python_hosts import Hosts, HostsEntry
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree


ip_address_pattern = r"[1-9]\d{0,2}\.\d{1,3}\.\d{1,3}\.\d{1,3}[\s\t]*"
hostname_pattern = r'[\s|\t]+((?:[a-zA-Z0-9-_]+\.)+(?:[a-zA-Z])+)'

baseURL = r"https://www.ipaddress.com/search/"
Request_Header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
ServerNamesList =[
				'github.com',  #1
				'gist.github.com', #2
				'assets-cdn.github.com', #3
				'raw.githubusercontent.com', #4
				'github-cloud.s3.amazonaws.com', #5
				'github.global.ssl.fastly.net', #6
				'codeload.github.com', #7
				'nodeload.github.com', #8
				'gist.githubusercontent.com', #9
				'cloud.githubusercontent.com', #10
				'camo.githubusercontent.com', #11
				'avatars0.githubusercontent.com', #12
				'avatars1.githubusercontent.com', #13
				'avatars2.githubusercontent.com', #14
				'avatars3.githubusercontent.com', #15
				'avatars4.githubusercontent.com', #16
				'avatars5.githubusercontent.com', #17
				'avatars6.githubusercontent.com', #18
				'avatars7.githubusercontent.com', #19
				'avatars8.githubusercontent.com', #20
				'api.github.com', #21
				'training.github.com', #22
				'documentcloud.github.com', #23
				'help.github.com', #24
				'githubstatus.com', #25
				'raw.github.com', #26
				'marketplace-screenshots.githubusercontent.com', #27
				'repository-images.githubusercontent.com', #28
				'user-images.githubusercontent.com', #29
				'desktop.githubusercontent.com', #30
				]	

def checkHostsLatency(hostname_keyword=None):
	""" Read host and IP from system hosts config file, Ping the specific host IP to check the average latency in ms """
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
	""" Read host and IP from the input text file, similar format as system hosts config file.
	Ping the specific host IP to check the average latency in ms  """

	hostFile = open(hostFile,"r",encoding = "utf-8")
	filecontent = hostFile.readlines()
	hostFile.close()

	for i,line in enumerate(filecontent):
		ip_list = re.search(ip_address_pattern,line)
		hostname_list=re.search(hostname_pattern,line)
		if ip_list is not None and hostname_list is not None:
			ipaddr= ip_list.group().strip()
			hostname = hostname_list.group().strip()
			response = ping(ipaddr,size = 1000,verbose=False)
			print(f"{i+1:<3}  IP : {ipaddr:<15}\tLatency : {response.rtt_avg_ms:<7.2f}ms\tHost : {hostname}")

def GetIPAddressWithBS(ServerList=None):
	""" Get IPaddress of each server from Ipaddresss.com with beautifulsoap"""

	ServerIpAddressList=[]
	if ServerList is None:
		ServerList = sorted(ServerNamesList,key=len)

	width = max([len(k) for k in ServerList])+4

	for index,servername in enumerate(ServerList):		
		actionURL = baseURL + servername
		try:
			response = requests.get(actionURL, headers = Request_Header,timeout=(15,15))			
			if(response.status_code!=200):
				print(f"\nServer {servername} return status code {response.status_code} ( {response.reason} ), Abort!\n")
				continue  #if the ipadress.com dose not return a valid page, then switch to the enxt host

			soup = BeautifulSoup(response.text, features = 'lxml')		
			match_result = soup.find_all('ul', {'class': 'comma-separated'})

			serverIp = None
			i=None
			iplist=[]
			if(match_result is not None and len(match_result)):
				for i,ipstring in enumerate(match_result):
					serverIp = re.findall(ip_address_pattern,ipstring.text)  #note: findall always return a list if there is a match
					if serverIp is not None:	
						for j in range(len(serverIp)):					
							Ip = serverIp[j].strip()
							if Ip not in iplist:
								iplist.append(Ip)
						
				iplist.sort()
				for j in range(len(iplist)):
					ServerIpAddressList.append({"Ip":iplist[j],"Host":servername})
					latency=ping(iplist[j],size = 1000,verbose=False).rtt_avg_ms
					if(len(iplist)>1):
						index_str=f"{index+1}.{j+1}"
					else:
						index_str=f"{index+1}"
					print(f'{index_str:<6}:  {iplist[j]:<15}    {servername:<{width}}  Latency : {latency}ms')
			
			if len(iplist)==0:# no match result, something is wrong
				print(f'{index:<6}:  {"No IP found!   "}    {servername}')
						
		except Exception as e:
			print(e)
			print(f'{index:<6}:  {"Exception!     "}    {servername}')
	if(len(ServerIpAddressList)):
		return ServerIpAddressList
	else:
		return None

def GetIPAddressWithXpath(ServerList=None):
	""" Get IPaddress of each server from Ipaddresss.com with xpath"""

	if ServerList is None:
		ServerList = sorted(ServerNamesList,key=len)

	ServerIpAddressList=[]

	width = max([len(k) for k in ServerList])+4
	for index, host in enumerate(ServerList):
		try:
			actionURL = baseURL + host
			response = requests.get(actionURL,headers = Request_Header)
			if(response.status_code!=200):			
				print(f"\n{host} : {actionURL} returns error, status_code ={response.status_code}( {response.reason} )\n")

			html = response.content		

			elements_selector = etree.HTML(html)

			ip_list = elements_selector.xpath('/html/body/div/main/section/table/tbody/tr/td/ul[@class="comma-separated"]/li/text()')

			if ip_list is not None and len(ip_list):	
				ip_list.sort()
				for j,ipstring in enumerate(ip_list):	
					serverIp = re.findall(ip_address_pattern,ipstring.strip())	
					if serverIp is not None:
						serverIp=serverIp[0]
						ServerIpAddressList.append({"Ip":serverIp,"Host":host})
						latency=ping(serverIp,size = 1000,verbose=False).rtt_avg_ms
						if(len(ip_list)>1):
							index_str=f"{index+1}.{j+1}"
						else:
							index_str=f"{index+1}"
						print(f'{index_str:<6}:  {serverIp:<15}    {host:<{width}}  Latency : {latency}ms')
			else:
				print(f'{index:<6}:  {"No IP found!   "}    {host}')
		
		except Exception as e:
			print(e)
			print(f'{index:<6}:  {"Exception!     "}    {host}')
	if(len(ServerIpAddressList)):
		return ServerIpAddressList
	else:
		return None
		
def updateHostsConfigFile(newEntriesList):
	""" write the latest IP address for the hosts to the system config file """
	my_hosts = Hosts()
	print("Locate the hosts config from : ", my_hosts.determine_hosts_path())
	print("Host config entries number : ", my_hosts.count())
	
	#step 1, remove all the entries with the same name
	for entry in newEntriesList:
		my_hosts.remove_all_matching(name=entry['Host'])
	
	#step 2, add the entry from the new entry list
	for entry in newEntriesList:
		new_entry = HostsEntry(entry_type='ipv4', address=entry['Ip'], names= [entry['Host']])
		ret=my_hosts.add([new_entry],allow_address_duplication=True,)
		#print(f"Add ipv4 entry for:  {new_entry}\n\tOperation result : {ret}\n")
	
	#step 3, write the host file
	result = my_hosts.write()
	if(result is not None):
		print("Done! new host file saved! result : \n")
		print('\n'.join(f'{k} : {v}' for k,v in sorted(result.items())))
	else:
		print("Error! update host file failed! \n")

if __name__ == '__main__':

    #test 1
	#hostFile = "hosts.txt"
	#checkLatency(hostFile)
	#checkHostsLatency("github")
	#	
	#test 2
	#hostIPList = GetIPAddressWithXpath()

	hostIPList = GetIPAddressWithBS()
	if(hostIPList is not None):
		updateHostsConfigFile(hostIPList)
	else:
		print("Nothing updated for the hosts file! ")

	
	
	


