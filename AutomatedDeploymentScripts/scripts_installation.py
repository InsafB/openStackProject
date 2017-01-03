import os_client_config
import os
import paramiko
import credentials
from neutronclient.v2_0 import client
from swiftclient.client import Connection, ClientException
from credentials import *
from utils import *

def createNetwork(network_name):
    credentials = get_credentials()
    neutron = client.Client(**credentials)
	try:	
		body_create_network = {'network': {'name': network_name,'admin_state_up': True}}
		network = neutron.create_network(body=body_create_network)
		network_dict = network['network']
		network_id = network_dict['id']
		print('Network %s has been successfuly created' % network_id)
		body_create_subnet = {'subnets': [{'cidr': '192.168.0.0/24','ip_version': 4, 'network_id': network_id}]}
		subnet = neutron.create_subnet(body=body_create_subnet)
		print('SubNetwork %s has been successfuly created' % subnet)
	finally:
		print("Create Network: Execution completed")
	return network_id 

def createRouter(router_name):
	neutron = client.Client(**credentials)
	neutron.format = 'json'
	request = {'router': {'name': router_name,'admin_state_up': True}}
	router = neutron.create_router(request)
	router_id = router['router']['id']
	print("Create Router: Execution Completed")
	return router_id

def createPort(port_name,router_id,network_id)
	body_create_port = {'port': {'admin_state_up': True,'device_id': router_id,'name': port_name,'network_id': network_id}}
	response = neutron.create_port(body=body_create_port)
	print(response)
	print("Add Port to Network: Execution Completed")

def exec_commands(commands,server):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server)    
    for cmd in commands:
        print "executing command : ",cmd
        client_stdin, client_stdout, client_stderr = client.exec_command(cmd);
        exit_status = client_stdout.channel.recv_exit_status()
        print "exit status for command '",cmd," is : ",exit_status

def appendHost(ip,ServerName):
    command = "echo '"+ip+"    "+ServerName+"' >> /etc/hosts"
    commands = [command]
    exec_commands(commands,ServerName)

def install_mysql(server):
    commands=["sudo apt-get update","sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password othmane'","sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password othmane'","sudo apt-get -y install mysql-server"]
    exec_commands(commands,server)

def getNovaClient():
    ## Nova Client
    credentials = get_nova_credentials_v2()
    nova_client = os_client_config.make_client('compute',**credentials)
    return nova_client

def getSwiftConn():
    return Connection(**get_session_credentials())

def createVM(name,network_id):
    novaclient = getNovaClient()
    ## Initiate VM parameters 
    image = nova_client.images.find(name="ubuntu1404")
    flavor = nova_client.flavors.find(name="m1.small")
    net = nova_client.networks.find(id=network_id)
    nics = [{'net-id': net.id}]
    ## Create VM
    ServerName = "Server"+name
    instance = nova_client.servers.create(name=ServerName, image=image,flavor=flavor, key_name="key_mac", nics=nics)
    appendHost(instance.to_dict()['addresses']['private'][0]['addr'],ServerName)
    return instance,ServerName

def link_VM_FloatingIP(network_id,ServerName):
    nova_client = getNovaClient()
    ##Ask for a floating IP
    #floating_ip = nova_client.floating_ips.create(nova_client.floating_ip_pools.list()[0].name)
    #link with an existing ip ( already created)
    floating_ip = nova_client.floating_ips.find(id=network_id)
    instance = nova_client.servers.find(name=ServerName)
    instance.add_floating_ip(floating_ip)

def createVM_Master(network_id):
    instance , ServerName = createVM("Master")
    link_VM_FloatingIP(network_id,ServerName)

def createVM_I():
    instance , ServerName =createVM("I")
    install_mysql(ServerName)

def createVM_S():
    instance , ServerName =createVM("S")
    install_mysql(ServerName)

def createVM_B():
    instance , ServerName = createVM("B")

def createVM_P():
    instance , ServerName = createVM("P")

def createVM_W():
    instance , ServerName = createVM("W")
       
## Main 
network_id = createNetwork('private_network1')
router_id = createRouter('router1')
createPort('port1',router_id, network_id)

createVM_Master(network_id)
createVM_I()
createVM_S()
createVM_B()
createVM_P()
createVM_W()

createSwift_store()
