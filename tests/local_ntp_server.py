# my_ntp_project/local_ntp_server.py
import socket
import time
import struct

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Python NTP server listening on {HOST}:{PORT}...")
print("Press Ctrl+C to stop.")

try:
    while True:
        data, client_address = server_socket.recvfrom(1024)
        print(f"\n-> Received request from {client_address}")

        # Mode 4 = Server, Version 4, LI 0 (no leap warning)
        li_vn_mode = 0b00100100  # LI=0, VN=4, Mode=4 packed into one byte
        stratum = 2             
        poll = 6                 # A common poll interval
        precision = -20          # A common precision value

        NTP_DELTA = 2208988800
        current_time = time.time()
        
        # Timestamps are 64-bit fixed-point numbers.
        # The first 32 bits are seconds, the last 32 are fractions of a second.
        transmit_timestamp = current_time + NTP_DELTA
        tx_secs = int(transmit_timestamp)
        tx_frac = int((transmit_timestamp - tx_secs) * 2**32)

        # Pack the data into a 48-byte NTP packet.
        # We are only filling in the essential fields for a valid response.
        ntp_packet = struct.pack('!BBBbII4sIIQQQQ',
                                 li_vn_mode, stratum, poll, precision,
                                 0, 0, b'LOCL', 0, 0, 0, 0, # Root Delay, Dispersion, Ref ID, etc.
                                 tx_secs, tx_frac) # Transmit Timestamp

        server_socket.sendto(ntp_packet, client_address)
        print(f"<- Sent realistic NTP response to {client_address}")

except KeyboardInterrupt:
    print("\nServer is shutting down.")
finally:
    server_socket.close()