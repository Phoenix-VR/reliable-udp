import main
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--from_port",type=int)
parser.add_argument("--to_port",type=int)
args = parser.parse_args()

sock = main.Transmission(src_port=args.from_port)

sock.connect(target_addr=("192.168.0.105",args.to_port),timeout=10)
