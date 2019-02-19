tshark -r ReconCase.pcap -2 -T fields -e ip.src -e ip.dst | sort -n | uniq -c | sort -n 
tshark -r ReconCase.pcap -2 -T fields -e ip.dst | sort -n | uniq -c | sort -n 
tshark -r ReconCase.pcap -R "ip.src==10.42.42.253" -T fields -e ip.dst | sort -n | uniq -c | sort -n 
tshark -r ReconCase.pcap -2 -R "ip.src==10.42.42.253" -T fields -e ip.dst | sort -n | uniq -c | sort -n 
tshark -r ReconCase.pcap -2 -T fields -e eth.addr | sort -n | uniq -c | sort -n
tshark -r ReconCase.pcap -2 -T fields -e eth.dst_resolved | sort -n | uniq -c | sort -n | grep "Apple"
tshark -r ReconCase.pcap -2 -T fields -e eth.dst_resolved -e ip.src | sort -n | uniq -c | sort -n
tshark -r ReconCase.pcap -2 -T fields -e eth.dst_resolved -e ip.dst | sort -n | uniq -c | sort -n
tshark -r ReconCase.pcap -2 -T fields -e eth.dst_resolved -e ip.dst | sort -n | uniq -c | sort -n | grep "Apple"
tshark -r ReconCase.pcap -2 -R "ip.src_host==10.42.42.253" -T fields -e eth.dst_resolved -e ip.dst | sort -n | uniq -c | sort -n
tshark -r ReconCase.pcap -2 -R "ip.src_host==10.42.42.253" -T fields -e eth.dst_resolved -e ip.dst | sort -n | uniq -c | sort -n | grep "Apple"
tshark -r ReconCase.pcap -2 -T fields -R "ip.src_host==10.42.42.253" -e eth.dst_resolved -e ip.dst | sort -n | uniq -c | sort -n
tshark -r ReconCase.pcap -2 -T fields -R "ip.src_host==10.42.42.253" -e ip.dst | sort -n | uniq -c | sort -n
tshark -r ReconCase.pcap -2 -T fields -R "nbns" -e ip.src -e ip.dst | sort -n | uniq -c | sort -n
tshark -r ReconCase.pcap -2 -T fields -R "nbns.flags.response == 1" -e ip.src -e ip.dst | sort -n | uniq -c | sort -n
tshark -r ReconCase.pcap -2 -T fields -R "nbns.flags.response == 1" -e ip.src | sort -n | uniq -c | sort -n
tshark -r ReconCase.pcap -2 -T fields -R "tcp.flags == 0x012 && ip.src == 10.42.42.50" -e tcp.srcport 
tshark -r ReconCase.pcap -2 -T fields -R "tcp.flags == 0x012 && ip.src == 10.42.42.50" -e tcp.srcport | sort -n | uniq -c | sort -n
tshark -r ReconCase.pcap -2 -T fields -R "tcp.flags == 0x012 && ip.src == 10.42.42.50" -e tcp.srcport | sort -n | uniq | sort -n
tshark -r ReconCase.pcap -2 -T fields -e data
tshark -r ReconCase.pcap -2 -T fields -e data | sort -n | uniq | sort -n
tshark -r ReconCase.pcap -2 -T fields -e ip.dst_host | sort -n | uniq -c | sort -n
tshark -r ReconCase.pcap -2 -R "ip.src_host==10.42.42.253" -T fields -e eth.dst_resolved -e ip.dst | sort -n | uniq -c | sort -n | grep "Apple"
tshark -r ReconCase.pcap -2 -R "ip.src_host==10.42.42.253" -T fields -e eth.dst_resolved -e ip.dst | sort -n | uniq -c | sort -n
tshark -r ReconCase.pcap -2 -R "ip.src_host==10.42.42.253" -T fields -e eth.dst -e ip.dst | sort -n | uniq -c | sort -n