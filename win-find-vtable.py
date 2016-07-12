import re

f = open('/Users/vit/vtables.txt', 'w')

doc = Document.getCurrentDocument()
dataseg = doc.getSegmentByName('.data')
rdataseg = doc.getSegmentByName('.rdata')
textseg = doc.getSegmentByName('.text')
datasec = doc.getSectionByName('.data')
rdatasec = doc.getSectionByName('.rdata')
base = 0x140000000

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
		elif b != 0x2e:
				if not started:
					continue
		ret = ret + chr(b)
		if not started:
			started = addr-1

	return '',end
	
print '============================='

if True:
	addr1 = rdatasec.getStartingAddress()
	addr2 = rdatasec.getStartingAddress()
	end2 = rdatasec.getStartingAddress() + rdatasec.getLength()

	while addr2 < end2:
		q = doc.readUInt64LE(addr2)
		if q > addr1 and q < end2:
			rdataseg.setTypeAtAddress(addr2, 8, Segment.TYPE_LONG)

		addr2 = addr2 + 4


print 'PREPARE DONE'


addr2 = rdatasec.getStartingAddress()
end2 = rdatasec.getStartingAddress() + rdatasec.getLength()
addr3 = datasec.getStartingAddress()
end3 = datasec.getStartingAddress() + datasec.getLength()

while addr2 < end2:
	d = doc.readUInt32LE(addr2) + base
	if d > addr3 and d < end3 and doc.readByte(d+16) == 0x2e and doc.readByte(addr2-12) == 0x01:
		s,ad = readAscii(dataseg, d, d+0x100)
		m = re.match("(..[A-Z]+)([a-z_]+st)", s)
		if m and m.group(2) != 'bad_cast':
			classname = m.group(2)
			refs = rdataseg.getReferencesOfAddress(addr2-12)
			if len(refs) == 0:
				print 'can not find refs for %s 0x%x' % (classname, addr2-12)
			else:
				vtable = refs[0] + 8
				f.write ("<vtable-address name='%s' value='0x%08x'/>\n" % (classname, vtable))

	addr2 = addr2 + 4
			
f.close()

print 'DONE'
