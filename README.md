# NetworkNAPALM
Exploring NAPALM library

### Prerequisites
- Docker and docker-compose installed 
- python3

### Environment Set Up
1. In the NetworkNAPALM project directory run `$ python3 -m venv env` to create a fresh python environment called `env`
2. From the project directory source the environment `$ . env/bin/activate`
3. From the project directory install the python dependencies for the project `$ pip install -r requirements.txt`
4. Your environment is all set

To exit the environment `$ deactivate`  
To activate the environment, source the environment `$ . env/bin/activate`


### How to Run
Make sure to be connected to the Cybera VPN for all challenges

#### Q1)
Make sure to activate your environment  
In this challenge we wrote a python script `q1/parsing_ports.py` that takes as input: the IP address, user name and password associated to the port. 

    usage: parsing_ports.py [-h] [-v] host_name username password

    positional arguments:
      host_name      Provide IP address or host name of switch
      username       Provide username of switch
      password       Provide password of switch

    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  Run the program in verbose mode.

To run the script execute  
`python3 q1/parsing_ports.py <address> <username> <password>`

The python script will return: a list of ports associated with the switch, along with information on the switch such as the vendor and model. 

#### Q2)
Make sure to activate the environment

In the ansible inventory file `q2/inventory.yml`, manually set the path to your environments python interpreter 
```
ansible_python_interpreter=<path/to/project/directory>/NetworkNAPALM/env/bin/python3
```

In the ansible config file `q2/ansible.cfg`, manually set the path to your environments napalm packages
```
[defaults]
library = <path/to/project/directory>/NetworkNAPALM/env/lib/python3.8/site-packages/napalm_ansible/modules
action_plugins = <path/to/project/directory>/NetworkNAPALM/env/lib/python3.8/site-packages/napalm_ansible/plugins/action
```

Set the environment variable `$ export ANSIBLE_HOST_KEY_CHECKING=False`

Enter the `q2` directory and run `$ ansible-playbook -i inventory.yml facts-demo.yml --extra-vars "ansible_user=<username> ansible_password=<password>"`

#### Q3)
##### How to set up and acess NetBox:  

We will use a Docker image for NetBox 
1. `$ git clone https://github.com/netbox-community/netbox-docker.git` to download the netbox-docker files
2. `cd netbox-docker`
3. `$ vim env/netbox.env`  
set the values required for Napalm
```
NAPALM_USERNAME=<username>
NAPALM_PASSWORD=<password>
NAPALM_ARGS={'secret': NAPALM_PASSWORD}
```
4. `$ docker-compose pull` and `$ docker-compose up -d`  
It will take Netbox a few minutes to be prepared
5. Url to access netbox at - `$ echo "http://$(docker-compose port nginx 8080)/"`  
If Netbox is not ready yet, you'll receive a `502 Bad Gateway` error

##### How to Connect Netbox to a Remote Device
1. Log into netbox as the default admin user
2. Create a `Device Role` and give it a name
3. Create a `Manufacturer` and give it a name
4. Create a `Device Type` and give it a name
5. Create a `Site` and give it a name
6. Create a `Platform` give it a name and set the field "NAPALM driver" to `IOS`
7. Create a `Device` and give it a name
8. Create a interface
9. Create a `IP Address` using the the remote devices address. Under the "Interface Assignment" header, make sure to select the Device and Interface you created earlier
10. Edit your existing device and update it with a primary ip address
11. Query 
`http://0.0.0.0:<PORT>/api/dcim/devices/<DEVICE_NUM>/napalm/?X-NAPALM-Username=<USERNAME>&X-NAPALM-Password=<PASSWORD>method=get_facts`

