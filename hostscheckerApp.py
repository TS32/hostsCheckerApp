from pythonping import ping
from python_hosts import Hosts, HostsEntry

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



def getHosts(hostname_keyword=None):
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
			print(f"{i+1:<3}  IP : {ipaddr:<15}\tLatency:{response.rtt_avg_ms:<7.2f}ms\tHost: {hostname}")
	
if __name__ == '__main__':

	#hostFile = "hosts.txt"
	getHosts("github")

	
