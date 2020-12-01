# NetworkNAPALM
Exploring NAPALM library

### Environment Set Up
1. In the NetworkNAPALM project directory run `$ python3 -m venv env` to create a fresh python environment called `env`
2. From the project directory source the environment `$ . env/bin/activate`
3. From the project directory install the python dependencies for the project `$ pip install -r requirements.txt`
4. Your environment is all set

To exit the environment `$ deactivate`  
To activate the environment, source the environment `$ . env/bin/activate`


### How to Run
Make sure to be connected to the Cybera VPN

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
