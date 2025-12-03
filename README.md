# CoAP IoT Protocol Lab

Lightweight IoT communication using CoAP protocol with Wireshark network analysis.

## 📋 Overview

Implementation of CoAP (Constrained Application Protocol) to replace HTTP in a Flask application, demonstrating efficient communication for resource-constrained IoT devices.

## 🛠️ Technologies

- **Protocol**: CoAP over UDP
- **Language**: Python
- **Tools**: Wireshark for packet analysis
- **Network**: WiFi

## 🔍 Key Results

**Wireshark Analysis:**
- Message size: 52 bytes (vs 200+ bytes for HTTP)
- Protocol stack: Ethernet → IP → UDP → CoAP
- Message type: Confirmable (CON) GET request
- Resource: /LED

**CoAP Message Structure:**
```
Version: 1
Type: Confirmable (CON)
Code: GET (0.01)
Message ID: 59112
Uri-Path: /LED
```

## 🚀 Quick Start
```bash
# Install dependencies
pip install aiocoap

# Run server
python coap_server.py

# Run client (in another terminal)
python coap_client.py

# Capture traffic in Wireshark with filter: coap
```

## 📁 Project Structure
```
├── coap_server.py          # CoAP server
├── coap_client.py          # CoAP client
├── wireshark_captures/     # .pcap files
└── README.md
```

## 💡 Applications

- Drone telemetry systems (low-latency UDP communication)
- Battery-powered IoT sensor networks
- Real-time embedded systems

## 👤 Author

**Your Name**  
GitHub: [@YOUR-USERNAME](https://github.com/YOUR-USERNAME)

## 📚 References

- [RFC 7252 - CoAP Protocol](https://datatracker.ietf.org/doc/html/rfc7252)