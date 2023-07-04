import socket
import zlib
import threading

my_public_ip = ""

# def make_packets(data,packet_size):
#     packets = []
#     n_packets = int(len(data) / packet_size) + 1
#     for i in range(n_packets):
#         data_in_packet = data[i*packet_size:(i+1)*packet_size]
#         sequence_num = i
#         checksum = zlib.crc32(data_in_packet)
#         final_packet = f"{sequence_num}:{data_in_packet}:{checksum}"
#         packets.append(final_packet)
#     return packets
stop_sending = False

def send_con(src_port,target_addr,timeout):
    send_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    send_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    send_sock.bind(("192.168.0.105",src_port))
    send_sock.settimeout(timeout)
    print("Started sending connection requests...")
    global stop_sending
    while stop_sending != True:
        try:
            send_sock.sendto(f"Connection-req:{my_public_ip}:{src_port}:SYN".encode(),target_addr)
        except socket.timeout as T:
            continue

def recv_con(src_port,target_addr,connections,timeout):
    recv_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    recv_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    recv_sock.bind(("192.168.0.105",src_port))
    recv_sock.settimeout(timeout)
    try:
        print("Started trying to recieve some response from target...")
        data, client_addr = recv_sock.recvfrom(1024)
        print("Recieved something...")
    except socket.timeout as T:
        print("Connection request timeout. No response recieved from the host...")
        global stop_sending
        stop_sending = True
        return 0
    chunks = data.split(":")
    if chunks[0] == "Connection-req" and chunks[3] == "SYN":
        if target_addr == (chunks[1],chunks[2]):
            # sign the syn request
            recv_sock.sendto(f"Connection-req:{my_public_ip}:{src_port}:SYN-ACK".encode(),target_addr)
    elif chunks[0] == "Connection-req" and chunks[3] == "SYN-ACK":
        if target_addr == (chunks[1],chunks[2]):
            connections.append(target_addr)
            stop_sending = True
            print("Connection established")

class Transmission:
    def __init__(self,src_port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.src_port = src_port
        self.sock.bind(("192.168.0.105",src_port))
        self.connections = []

    def connect(self,target_addr,timeout):
        time_bw_send_connect_reqs = 1
        global stop_sending
        stop_sending = False
        threading.Thread(target=send_con,args=(self.src_port,target_addr,time_bw_send_connect_reqs)).start()
        threading.Thread(target=recv_con,args=(self.src_port,target_addr,self.connections,timeout)).start()
    # # run send and responses funcs simultanoesly
    # def send_packets(self,packets,target_addr):
    #     for packet in packets:
    #         self.sock.sendto(str(packet).encode(),target_addr)

    # def get_responses(self,target_addr):
    #     # if a packet is recieved successfullt we store it as ACK1 where 1 represents seq no of packet
    #     packet_status_recved = []
    #     packets_confirmed = []
    #     packets_corrupted = []
    #     packets_not_recved = []
    #     try:
    #         data, ret_addr = self.sock.recvfrom(1024)
    #         if ret_addr != target_addr:
    #             pass
    #         else:
    #             recved_status = str(data).split(":")
    #             for status in recved_status:
    #                 if status[0:3] == "ACK":
    #                     packet_num = status[3:]
    #                     packet_status_recved.append(packet_num)
    #                     packets_confirmed.append(packet_num)
    #                 elif status[0:3] == "NCK":
    #                     packet_num = status[3:]
    #                     packet_status_recved.append(packet_num)
    #                     packets_corrupted.append(packet_num)
    #                 else:
    #                     # packet maybe got corrupted during sending so asking the recver to resend its status again
    #                     packet_num = status[3:]
    #                     packets_corrupted.append(packet_num)
        


# src_port = 5000
# target_addr = ("129.219.129",6000)
