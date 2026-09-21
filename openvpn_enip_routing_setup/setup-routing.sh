#!/bin/bash
# Replace tun0 with your VPN interface name if different

# Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# Flush existing rules
sudo iptables -t mangle -F

# Mark ENIP traffic (port 44818) to VM-X
sudo iptables -t mangle -A OUTPUT -p tcp --dport 44818 -j MARK --set-mark 10
# For modbus, use the following
# sudo iptables -t mangle -A OUTPUT -p tcp --dport 502 -j MARK --set-mark 10


# Add routing rule to use table 100 for marked packets
sudo ip rule add fwmark 10 table 100

# Add route to table 100 via VPN tunnel interface (e.g., tun0)
sudo ip route add <VM-X-PRIVATE-IP> via <TUNNEL-GATEWAY> dev tun0 table 100
# e.g. sudo ip route add 10.0.0.5 via 10.8.0.1 dev tun0 (10.0.0.5 = scada's AWS private IP, 10.8.0.1 = VPN router IP (VPN-Private))
