# ICS-Sniper ENIP-C Software Testbed

**SWaT software testbed (Connected ENIP version)**

This repository contains the SWaT software testbed used by ICS-Sniper in Connected EtherNet/IP (ENIP) mode. Six simulated PLCs run on one Linux host and communicate with the SCADA application through an OpenVPN router.

Replace every value in angle brackets, such as `<router-public-ip>`, with a value from your environment. Generate new VPN credentials for every deployment.

## Architecture

```text
Software PLC host                OpenVPN router                 SCADA host
OpenVPN: 10.8.0.5/24  <------->  OpenVPN: 10.8.0.1/24  <----> OpenVPN: 10.8.0.4/24
PLC1-PLC6: localhost:44818-44823                            SCADA: 10.8.0.4:44818
```

The six PLC servers bind only to loopback addresses on the software PLC host. The PLC processes reach SCADA through the VPN.

## Requirements

The testbed uses three Linux instances. The table lists the configuration used for the original deployment; increase storage when collecting long packet captures.

| Instance | Quantity | Operating system | Configuration used | Network and access requirements |
| --- | ---: | --- | --- | --- |
| OpenVPN router | 1 | Ubuntu 22.04 | 1 vCPU, 1 GiB RAM, 32 GiB storage | Publicly reachable TCP 1194; SSH access; IP forwarding; a public IP or DNS name |
| SCADA | 1 | Ubuntu 22.04 | 4 vCPUs, 16 GiB RAM, 32 GiB storage | SSH access; outbound TCP access to the router; TCP 44818 available on `10.8.0.4` |
| Software PLC host | 1 | Ubuntu 22.04 | 8 vCPUs, 32 GiB RAM, 32 GiB storage | SSH access; outbound TCP access to the router; TCP 44818-44823 available on loopback |

The router firewall or cloud security group must allow TCP 1194 from both VPN clients.

## Clone the Repository

Clone the public repository on the SCADA and software PLC hosts.

```bash
cd /home/ubuntu
git clone https://github.com/ICS-Sniper/ENIP-C-software-testbed.git
cd ENIP-C-software-testbed
```

## One-Time Setup

### 1. Configure the OpenVPN router

Log in to the router and install OpenVPN and Easy-RSA:

```bash
sudo apt update
sudo apt install -y easy-rsa openvpn
mkdir -p ~/openvpn-ca
cd ~/openvpn-ca
```

Create the certificate authority and server material:

```bash
/usr/share/easy-rsa/easyrsa init-pki
/usr/share/easy-rsa/easyrsa build-ca
/usr/share/easy-rsa/easyrsa gen-req server nopass
/usr/share/easy-rsa/easyrsa sign-req server server
/usr/share/easy-rsa/easyrsa gen-dh
openvpn --genkey tls-crypt-v2-server ta.key
```

Create separate credentials for the software PLC and SCADA clients:

```bash
/usr/share/easy-rsa/easyrsa gen-req plc nopass
/usr/share/easy-rsa/easyrsa sign-req client plc
openvpn --tls-crypt-v2 ./ta.key \
  --genkey tls-crypt-v2-client ./pki/private/plc-tc.key

/usr/share/easy-rsa/easyrsa gen-req scada nopass
/usr/share/easy-rsa/easyrsa sign-req client scada
openvpn --tls-crypt-v2 ./ta.key \
  --genkey tls-crypt-v2-client ./pki/private/scada-tc.key
```

Install the server material:

```bash
sudo install -d -m 0755 /etc/openvpn/ccd
sudo install -m 0644 ~/openvpn-ca/pki/ca.crt /etc/openvpn/ca.crt
sudo install -m 0644 ~/openvpn-ca/pki/dh.pem /etc/openvpn/dh.pem
sudo install -m 0644 ~/openvpn-ca/pki/issued/server.crt /etc/openvpn/server.crt
sudo install -m 0600 ~/openvpn-ca/pki/private/server.key /etc/openvpn/server.key
sudo install -m 0600 ~/openvpn-ca/ta.key /etc/openvpn/ta.key
```

Create `/etc/openvpn/server.conf`:

```conf
port 1194
proto tcp
dev tun

ca ca.crt
cert server.crt
key server.key
dh dh.pem
tls-crypt-v2 /etc/openvpn/ta.key

server 10.8.0.0 255.255.255.0
topology subnet
client-config-dir /etc/openvpn/ccd
ifconfig-pool-persist ipp.txt
push "route 10.8.0.0 255.255.255.0"

keepalive 10 120
persist-key
persist-tun
cipher AES-256-GCM
auth SHA256
auth-nocache
user nobody
group nogroup
status openvpn-status.log
verb 3
```

Assign stable VPN addresses. The CCD filenames must match the certificate common names:

```bash
echo "ifconfig-push 10.8.0.5 255.255.255.0" | \
  sudo tee /etc/openvpn/ccd/plc >/dev/null
echo "ifconfig-push 10.8.0.4 255.255.255.0" | \
  sudo tee /etc/openvpn/ccd/scada >/dev/null
```

To run the testbed only on demand, disable automatic OpenVPN startup:

```bash
sudo systemctl disable openvpn
sudo systemctl disable openvpn@server
```

### 2. Configure the Linux VPN clients

Run the following on both the SCADA and software PLC hosts:

```bash
sudo apt update
sudo apt install -y openvpn
mkdir -p ~/openvpn-ca
chmod 700 ~/openvpn-ca
```

Securely copy the following files from the router. Never transfer private keys through a public repository or shared public storage.

| Client | Router source | Client destination |
| --- | --- | --- |
| PLC | `pki/ca.crt` | `ca.crt` |
| PLC | `pki/issued/plc.crt` | `plc.crt` |
| PLC | `pki/private/plc.key` | `plc.key` |
| PLC | `pki/private/plc-tc.key` | `plc-tc.key` |
| SCADA | `pki/ca.crt` | `ca.crt` |
| SCADA | `pki/issued/scada.crt` | `scada.crt` |
| SCADA | `pki/private/scada.key` | `scada.key` |
| SCADA | `pki/private/scada-tc.key` | `scada-tc.key` |

Protect the client private keys:

```bash
chmod 600 ~/openvpn-ca/*.key
```

On the software PLC host, create `~/openvpn-ca/client.conf`:

```conf
client
dev tun
proto tcp
remote <router-public-ip-or-dns> 1194
resolv-retry infinite
nobind
persist-key
persist-tun

ca ca.crt
cert plc.crt
key plc.key
remote-cert-tls server
tls-crypt-v2 plc-tc.key

pull
cipher AES-256-GCM
auth SHA256
auth-nocache
verb 3
```

On the SCADA host, create the same profile but use the SCADA credentials:

```conf
ca ca.crt
cert scada.crt
key scada.key
remote-cert-tls server
tls-crypt-v2 scada-tc.key
```

### 3. Install Python 2.7 and the ENIP dependencies

Run these commands on both the SCADA and software PLC hosts:

```bash
sudo apt update
sudo apt install -y software-properties-common curl
sudo add-apt-repository -y universe
sudo apt update
sudo apt install -y python2.7
curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
sudo python2.7 get-pip.py
sudo python2.7 -m pip install \
  cpppo==4.3.0 \
  pymodbus==2.5.3 \
  numpy==1.16.6
```

Verify the imports:

```bash
python2.7 -c 'import cpppo, pymodbus, numpy; print("ENIP dependencies imported successfully")'
```

Create the log directory on both hosts:

```bash
mkdir -p ~/test-setup/scadalogs
```

## Start the Testbed

Start the components in this order. Do not start the PLC process until SCADA prints `SCADA main loop starts here`.

### 1. Start the router

```bash
ssh -i <ssh-key> ubuntu@<router-public-ip>
cd /etc/openvpn
sudo openvpn --config /etc/openvpn/server.conf --daemon
sudo sysctl -w net.ipv4.ip_forward=1
sudo ss -ltnp | grep 1194
```

### 2. Start SCADA

```bash
ssh -i <ssh-key> ubuntu@<scada-host>
cd ~/openvpn-ca
sudo openvpn --config client.conf --daemon
sudo sysctl -w net.ipv4.ip_forward=1
ip -brief -4 addr
ping -c 3 10.8.0.1
ping -c 3 10.8.0.5
cd /home/ubuntu/ENIP-C-software-testbed
sudo python2.7 SCADA_1.py
```

Wait for:

```text
SCADA main loop starts here
```

### 3. Start the software PLCs

In another terminal:

```bash
ssh -i <ssh-key> ubuntu@<software-plc-host>
cd ~/openvpn-ca
sudo openvpn --config client.conf --daemon
sudo sysctl -w net.ipv4.ip_forward=1
ip -brief -4 addr
ping -c 3 10.8.0.1
ping -c 3 10.8.0.4
cd /home/ubuntu/ENIP-C-software-testbed
sudo python2.7 plc_main.py
```

Keep both Python processes in the foreground so initialization and communication errors remain visible.

## Optional Packet Capture

Install TShark on the router and create a trace directory:

```bash
sudo apt install -y tshark
mkdir -p ~/traces
```

Capture public-side and tunnel-side traffic in separate sessions:

```bash
sudo tshark -i <public-interface> -w ~/traces/public-side.pcap
```

```bash
sudo tshark -i tun0 -w ~/traces/tunnel-side.pcap
```

Use `ip link` to identify the public interface. Packet captures can contain sensitive traffic and should not be committed.

## Stop the Testbed

1. Stop `plc_main.py` with `Ctrl+C`.
2. Stop `SCADA_1.py` with `Ctrl+C`.
3. Stop OpenVPN on each Linux client with `sudo pkill openvpn`.
4. Stop OpenVPN on the router with `sudo pkill openvpn`.
5. Copy required logs or packet captures before terminating ephemeral instances.

## Troubleshooting

| Symptom | Likely cause | Check or fix |
| --- | --- | --- |
| VPN client reports `Connection refused` | Router OpenVPN process or TCP 1194 firewall rule is missing | Start the router service and check `sudo ss -ltnp \| grep 1194` |
| SCADA cannot bind `10.8.0.4:44818` | The SCADA VPN is disconnected, has the wrong CCD address, or another server owns the port | Check `ip -brief -4 addr` and `sudo ss -ltnp \| grep ':44818'` |
| A PLC cannot reach SCADA | SCADA is not initialized or a VPN client is disconnected | Wait for `SCADA main loop starts here`, then test `ping -c 3 10.8.0.4` from the PLC host |
| A PLC server cannot bind a local ENIP port | Another process owns one of TCP 44818-44823 | Check `sudo ss -ltnp \| grep -E ':4481[8-9]\|:4482[0-3]'` |
| SCADA cannot create its CSV log | The log directory is missing or not writable | Create `/home/ubuntu/test-setup/scadalogs` and check its permissions |
| Python reports a missing package | A dependency was installed for Python 3 or a different Python 2 installation | Run `sudo python2.7 -m pip install cpppo==4.3.0 pymodbus==2.5.3 numpy==1.16.6` |
| OpenVPN assigns an unexpected client address | A certificate common name does not match its CCD filename | Use the `plc` and `scada` certificate names shown above |

## Repository Layout

| Path | Purpose |
| --- | --- |
| `SCADA_1.py` | Connected ENIP SCADA process |
| `plc_main.py` | Launcher for all six simulated PLCs |
| `utils.py` | ENIP addresses, ports, tag definitions, and shared testbed configuration |
| `protocols.py` | ENIP protocol process and client integration |
| `enip-main-scada/main.py` | Customized `cpppo` ENIP server used by the testbed |
| `HMI/`, `real_plc/`, `plant/`, `controlblock/`, `logicblock/` | SWaT process, PLC, HMI, and control simulation |

## Licensing

The repository's original code is covered by the repository-level `LICENSE`. The customized `enip-main-scada/main.py` is derived from `cpppo`, retains its upstream copyright and license header, and remains subject to the GNU General Public License version 3 or later. The repository-level MIT license does not replace the upstream licensing terms that apply to that file.
