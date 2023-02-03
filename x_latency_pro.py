import datetime
import argparse
import sys

from time import sleep

from ping3 import ping

# SET YOUR PING RESPONSE TIME THRESHOLD HERE, IN SECONDS
THRESHOLD = 0.25  # 250 milliseconds is the Comcast SLA threshold.

# SET YOUR PING INTERVAL HERE, IN SECONDS
INTERVAL = 1

# SET YOUR TIMES OF PINGS
PINGS = 3

# LOG TO WRITE TO WHEN PINGS TAKE LONGER THAN THE THRESHOLD SET ABOVE
i = datetime.datetime.now()
log_file = "x-latency-pro." + i.strftime("%Y.%m.%d.%H.%M.%S") + ".log"


def write_to_file(file_to_write, message):
    # os.makedirs(os.path.dirname(file_to_write), exist_ok=True)
    fh = open(file_to_write, "a")
    fh.write(message + "\n")
    fh.close()


def latency_test():
    try:
        with open('hosts.csv', 'r') as arquivo:
            hosts = arquivo.readlines()
            for host in hosts:
                host_detalhes = host.strip().split(',')

                ip_address = host_detalhes[0]
                host_name = host_detalhes[1]

                count = 0
                header = f"Pinging {host_name} - IP {ip_address} every {INTERVAL} secs; threshold: {THRESHOLD} secs."
                print(header)
                write_to_file(log_file, header)

                while count < PINGS:
                    count += 1
                    latency = ping(ip_address)

                    # Do we want to write it to the log?
                    if latency is None or latency > THRESHOLD:
                        write_log = "Yes"
                    else:
                        write_log = "No"

                    # Use better text is packet is dropped
                    if latency is None:
                        latency_text = "PACKET DROPPED"
                    else:
                        latency_text = f"{latency} secs"

                    line = f"{datetime.datetime.now()}: pinged {ip_address}; latency: {latency_text}"
                    print(f"{line}; logging: {write_log}")
                    write_to_file(log_file, line)

                    # if write_log == "Yes":
                    #    write_to_file(log_file, line)
                    sleep(INTERVAL)

                line = f" "  # PULA LINHA
                write_to_file(log_file, line)

    except FileNotFoundError:
        print('Error: File hosts.csv not found!')
    except Exception as error:
        print('Error:', error)


if __name__ == '__main__':
    print('Execution with default values, use x_latency_pro.exe -h to see a help!')

    parser = argparse.ArgumentParser(description='Xomano Tools Latency Test')
    parser.add_argument('--t', dest='thresold', type=float, help='Ping response time Threshold')
    parser.add_argument('--i', dest='interval', type=int, help='Ping interval in seconds')
    parser.add_argument('--p', dest='pings', type=int, help='Times to ping')

    args = parser.parse_args()

    if args.thresold is not None:
        THRESHOLD = args.thresold

    if args.interval is not None:
        INTERVAL = args.interval

    if args.pings is not None:
        PINGS = args.pings

    latency_test()

    argv = sys.argv[1:]
