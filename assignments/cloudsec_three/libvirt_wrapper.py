import libvirt
import libxml2
import sys

# dictionary to translate states of the virtual machine into short textual statuses
states = {
	libvirt.VIR_DOMAIN_NOSTATE: 'no state',
	libvirt.VIR_DOMAIN_RUNNING: 'running',
	libvirt.VIR_DOMAIN_BLOCKED: 'blocked',
	libvirt.VIR_DOMAIN_PAUSED: 'paused',
	libvirt.VIR_DOMAIN_SHUTDOWN: 'shutting down',
	libvirt.VIR_DOMAIN_SHUTOFF: 'off',
	libvirt.VIR_DOMAIN_CRASHED: 'crashed',
}

# function to get the value of a xml object given the context and the path
def get_xml_val(ctx, path):
	res = ctx.xpathEval(path)
	if res is None or len(res) == 0:
		val = "Unknown"
	else:
		val = res[0].content
	return val

# function to pretty print the section header
def print_section(title):
	print "\n%s" % title
	print "=" * 60

# function to pretty print the key-value pairs
def print_entry(key, value):
	print "%-10s %-10s" % (key, value)

# function to print all the info about a certain virtual machine
def print_info(dom):

	print_section("Machine Information")
	lst_info = dom.info()
	print_entry("State:", states.get(lst_info[0]))
	print_entry("MaxMem:", lst_info[1])
	print_entry("UsedMem:", lst_info[2])
	print_entry("VCPUs:", lst_info[3])
	if lst_info[0] != libvirt.VIR_DOMAIN_SHUTOFF:
		print_entry("Machine ID:", dom.ID())
	
	print_section("Kernel")
	dom_doc = libxml2.parseDoc(dom.XMLDesc(0))
	dom_ctx = dom_doc.xpathNewContext()
	print_entry("Type:", get_xml_val(dom_ctx, "/domain/os/type"))
	print_entry("Kernel:", get_xml_val(dom_ctx, "/domain/os/kernel"))
	print_entry("Initrd:", get_xml_val(dom_ctx, "/domain/os/initrd"))
	print_entry("Cmdline:", get_xml_val(dom_ctx, "/domain/os/cmdline"))

	print_section("Devices")
	dom_devs = dom_ctx.xpathEval("/domain/devices/*")
	for dev in dom_devs:
		dom_ctx.setContextNode(dev)
		type = get_xml_val(dom_ctx, "@type")
		print_entry("Device:", type)
		if type == "file":
			print_entry("    Source:", get_xml_val(dom_ctx, "source/@file"))
			print_entry("    Target:", get_xml_val(dom_ctx, "target/@dev"))
		elif type == "block":
			print_entry("    Source:", get_xml_val(dom_ctx, "source/@dev"))
			print_entry("    Target:", get_xml_val(dom_ctx, "target/@dev"))
		elif type == "bridge":
			print_xml("    Source:", get_xml_val(dom_ctx, "source/@bridge"))
			print_xml("    MAC Addr:", get_xml_val(dom_ctx, "mac/@address"))

# function to start a certain virtual machine
def vm_start():
	startable = conn.listDefinedDomains()
	if len(startable) == 0:
		print "There are no virtual machines that can be started."
		exit(0)
	for idx in xrange(len(startable)):
		print "\t%d\t%s" %(idx+1, startable[idx])
	chosen = input("Which one do you want to start? Enter the number: ")
	if chosen > 0 and chosen <= len(startable):
		chosen_start_dom = conn.lookupByName(startable[chosen-1])
		print "Starting", startable[chosen-1]
		chosen_start_dom.create()

# function to stop a certain virtual machine
def vm_stop():
	stoppable = conn.listDomainsID()
	if len(stoppable) == 0:
		print "No virtual machines are running."
		exit(0)
	for idx in xrange(len(stoppable)):
		stop_dom = conn.lookupByID(stoppable[idx])
		print "\t%d\t%s"%(stoppable[idx], stop_dom.name())
	chosen = input("Which one do you want to stop? Enter the number: ")
	chosen_stop_dom = conn.lookupByID(chosen)
	print "Stopping", chosen_stop_dom.name()
	chosen_stop_dom.shutdown()


# connect to the libvirt instance, in this case it'll be KVM (I think)
conn = libvirt.open(None)
if conn is None:
	print "Failed to open connection to the hypervisor."
	sys.exit(1)

# get all domains that aren't running
all_domains = conn.listDefinedDomains()
all_domains_info = map(conn.lookupByName, all_domains)

# get all domains that are running
running_domains = conn.listDomainsID()
running_domains_info = map(conn.lookupByID, running_domains)

# section to just print all the running and stopped virtual machines
if len(sys.argv) != 2:
	print "The defined domains are listed below:"
	for domain in all_domains:
		print domain
	print

	print "The running domains are listed below:"
	for domain in running_domains:
		print conn.lookupByID(domain).name()
	print
	print "Use", sys.argv[0], "with the domain name as argument to get the information about the domain."

# section to print the info of a specified virtual machine or start/stop a virtual machine
else:
	if sys.argv[1] == "start":
		vm_start()
	elif sys.argv[1] == "stop":
		vm_stop()
	else:
		print_info(conn.lookupByName(sys.argv[1]))
