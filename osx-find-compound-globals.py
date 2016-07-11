f = open('/Users/vit/ctors.txt', 'w')

atexit = 'imp___symbol_stub1____cxa_atexit'

doc = Document.getCurrentDocument()
seg = doc.getSegmentByName('__TEXT')

atexitaddr = doc.getAddressForName(atexit)

refs = seg.getReferencesOfAddress(atexitaddr)

globals = []
gprocs = {}

for addr in refs:
	i = seg.getInstructionAtAddress(addr)
	if i.getInstructionString() == 'call':	
		addr2 = addr
		while addr2 > seg.getStartingAddress():
			addr2 = seg.instructionStart(addr2-1)
			i = seg.getInstructionAtAddress(addr2)
			if i.getInstructionString() == 'lea' and i.getFormattedArgument(0) == 'rsi':
				gaddr = i.getFormattedArgument(1)[1:-1]
				gaddr = int(gaddr, 16)
				globals.append(gaddr)
				gprocs[gaddr] = addr #doc.getNameAtAddress(p.getEntryPoint())
				break

globals.sort()

print '============================='

for i in range(0,len(globals)-1):
	offset = globals[i]
	size = globals[i+1]-globals[i]
	callsite = gprocs[offset]
	p = seg.getProcedureAtAddress(callsite)
	ctorlist = 'sub_'+("%x" % p.getEntryPoint())

	f.write('<global-object name="?" offset="0x%x" size="%d">\n' % (offset, size))
	f.write('    <comment>ctorlist="%s" callsite="0x%x" </comment>\n' % (ctorlist, callsite))
	f.write('</global-object>\n')

f.close()

print 'DONE'
