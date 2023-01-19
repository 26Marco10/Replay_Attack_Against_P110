# Replay_Attack_Against_P110
In this repository you'll find a simple python code to perform replay attacks against Tapo P110

## How it works
To make the attack succes you first must create a pcap file with inside the POST request that you want replicate. Use Wireshark to create pcap files and Ettercap for MITM.

In replay_attack.py several libraries have been used, such as pyshark, request, sys and json. You can install these using:
```console
   pip install pyshark
   pip install request
   pip install sys
   pip install json
```
To use this python script you must input the path of the pcap file and the number of the POST request to be replicate. 
```console
   python replay_attack.py pcap_path request_number
```

