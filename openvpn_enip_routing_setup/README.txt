# OpenVPN Routing Setup for ENIP Traffic

## Files
- client-laptop.conf: Laptop's OpenVPN client config
- client-vmx.conf: VM-X's OpenVPN client config
- setup-routing.sh: Routing script to route ENIP traffic via VPN

## Instructions
1. Replace `VM-Y-IP`, `<VM-X-PRIVATE-IP>`, and `<TUNNEL-GATEWAY>` with actual IPs.
2. Place certificates (`ca.crt`, `client.crt`, `client.key`) alongside each config file.
3. Use `sudo openvpn --config client-laptop.conf` to connect from laptop.
4. Use `sudo openvpn --config client-vmx.conf` to connect from VM-X.
5. Run `setup-routing.sh` after VPN is up to route ENIP traffic through VM-Y.


## At the compromised router, enable IP forwarding
sysctl -w net.ipv4.ip_forward=1
Check with: sysctl net.ipv4.ip_forward
