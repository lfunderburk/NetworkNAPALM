# Authors: Vuk Radovic, Laura Gutierrez Funderburk, Lisa Cao
# Created on: Nov 8 2020
# Last modified on: Nov 25 2020

"""This script obtains a list of ports from a Cisco switch"""

from napalm import get_network_driver
import json
import pandas as pd
import argparse                 


def getArguments():
    # Set up the command line parser
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=""
    )

    # Host name of Cisco switch
    parser.add_argument(
        "host_name",
        help="Provide IP address or host name of switch"
    )
    
    # Username
    parser.add_argument(
        "username",
        help="Provide username of switch"
    )
    
    # Password
    parser.add_argument(
        "password",
        help="Provide password of switch"
    )

    # Verbosity flag
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Run the program in verbose mode.")

    # Parse the command line arguements.
    options = parser.parse_args()
    return options

if __name__ == "__main__":
    
    # Input reading
    options = getArguments()
    host_name = options.host_name
    username = options.username
    password = options.password
    
    try:
        print("Getting drivers")
        driver = get_network_driver("ios")
        print("Set up device")
        device = driver(hostname=str(host_name),username=str(username),password=password)
        print("Open device")
        device.open()
    
        # Use open device to get facts, interface counters and interfaces
        # Dump and then load using JSON format
        # Gathering some information
        print("Get information")
        json_facts = json.loads(json.dumps(device.get_facts(), sort_keys=True))
        json_interface_counters = json.loads(json.dumps(device.get_interfaces_counters(), sort_keys=True))
        json_devices = json.loads(json.dumps(device.get_interfaces(), sort_keys=True))
        json_interfaces = json.loads(json.dumps(device.get_interfaces(),sort_keys=True))
        interface_ip_json = json.loads(json.dumps(device.get_interfaces_ip(), sort_keys=True))
        json_env = json.loads(json.dumps(device.get_environment(),sort_keys=True))
        json_net_instances = json.loads(json.dumps(device.get_network_instances(),sort_keys=True))
        users = device.get_users()
        ntp_peers = device.get_ntp_peers()
        ntp_servers = device.get_ntp_servers()
        json_vlan = json.loads(json.dumps(device.get_vlans(),sort_keys=True))

        # Close device
        device.close()
    
        # Generate dataframes 
        interfaces_df = pd.DataFrame.from_dict(json_interfaces)
        transp_inter = interfaces_df.T
        devices_df = pd.DataFrame.from_dict(json_devices)
        facts_df = pd.DataFrame.from_dict(json_facts)
        
        # Get list of ports
        print("------------------------------------------------")
        print("List of ports:")
        for item in interfaces_df.T.index:
            print(item)

        print("------------------------------------------------")
        print("Model, vendor for each port")
        display(facts_df[['model','vendor','interface_list']])
        
        print("------------------------------------------------")
        print("Other info:")
        print("Ports enabled and up")
        display(transp_inter[(transp_inter['is_enabled']==True) & (transp_inter['is_up']==True)])
        
        print("------------------------------------------------")
        print("Ports not enabled or")    
        display(transp_inter[(transp_inter['is_enabled']!=True) | (transp_inter['is_up']!=True)])
        
        print("Users")
        if not(users):
            print("No users found")
        else:
            for item in users:
                print(item)
        
    except:
        
        print("WARNING:\nEnsure you are connected to Cybera VPN.\n\
        Ensure you provided the correct credentials. ")
