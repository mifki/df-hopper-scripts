f = open('/Users/vit/next_ids.txt', 'w')

doc = Document.getCurrentDocument()
textseg = doc.getSegmentByName('.text')
dataseg = doc.getSegmentByName('.rdata')

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
	

def process(seg, s, a):	
	refs = dataseg.getReferencesOfAddress(a)
	if len(refs) == 0:
		print 'can not find refs for %s' % s
		return

	addr = refs[0]
	while addr > seg.getStartingAddress():
		addr = seg.instructionStart(addr-1)
		i = seg.getInstructionAtAddress(addr)
		if i.getInstructionString() == 'jl':
			break

	addr = seg.instructionStart(addr-1)
	i = seg.getInstructionAtAddress(addr)
	if i.getInstructionString() != 'cmp':
		print 'can not find cmp instruction for %s' % s
		return

	if i.getFormattedArgument(1)[0] == '[':
		gaddr = i.getFormattedArgument(1)[1:-1]
		gaddr = int(gaddr, 16)
		f.write("<global-address name='%s_next_id' value='0x%08x'/>\n" % (s, gaddr))
	else:
		reg = i.getFormattedArgument(1)
		while addr > seg.getStartingAddress():
			addr = seg.instructionStart(addr-1)
			i = seg.getInstructionAtAddress(addr)
			if i.getInstructionString() == 'mov':
				if i.getFormattedArgument(0) == reg:
					gaddr = i.getFormattedArgument(1)[1:-1]
					gaddr = int(gaddr, 16)
					f.write("<global-address name='%s_next_id' value='0x%08x'/>\n" % (s, gaddr))
					break

print '============================='

sec = doc.getSectionByName('.rdata')
addr = sec.getStartingAddress()
last = addr + sec.getLength()
while addr < last:
	s,ad = readAscii(dataseg,addr,last)
	if s.find('Load Game: Invalid') != -1:
		j = s.find('ID Number')
		s = s[19:j-1].lower().replace(' ', '_')
		process(textseg,s,ad)

	addr = ad+len(s)+1


f.close()

print 'DONE'
