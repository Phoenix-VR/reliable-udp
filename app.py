import main
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--from_port",type=int)
parser.add_argument("--send",type=str)
args = parser.parse_args()

sock = main.Transmission(src_port=args.from_port)
ip,port = str(args.send).split(":")
sock.connect(target_addr=(ip,int(port)),timeout=10)

