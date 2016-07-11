f = open('/Users/vit/keydisplay.txt', 'w')

doc = Document.getCurrentDocument()
seg = doc.getSegmentByName('__TEXT')

def readAscii(seg,addr,end):
	start = seg
	ret = ''
	started = 0
	while addr < end:
		b = seg.readByte(addr)
		addr = addr + 1
		if not b:
			if started:
				return ret, started
			else:
				continue
		ret = ret + chr(b)
		if not started:
			started = addr-1
	

def process(seg, a):	
	refs = seg.getReferencesOfAddress(a)
	for j in range(0,len(refs)):
		addr = refs[j]
		start = addr
		while addr < start + 100:
			i = seg.getInstructionAtAddress(addr)
			if i.getInstructionString() == 'jmp':
				addr = int(i.getFormattedArgument(0), 16)
				start = addr
				while addr < start + 100:
					i = seg.getInstructionAtAddress(addr)
					if i.getInstructionString() == 'lea' and i.getFormattedArgument(0) == 'rdi':
						gaddr = i.getFormattedArgument(1)[1:-1]
						gaddr = int(gaddr, 16)
						f.write("<global-address name='keydisplay' value='0x%08x'/>\n" % gaddr)
						return
		
					addr = addr + i.getInstructionLength()
				return

			addr = addr + i.getInstructionLength()


print '============================='

sec = doc.getSectionByName('__cstring')
addr = sec.getStartingAddress()
last = addr + sec.getLength()

while addr < last:
	s,ad = readAscii(seg,addr,last)

	if s == 'Tab':
		process(seg,ad)
		break

	addr = ad+len(s)+1


print 'DONE'
