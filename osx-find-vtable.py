import re

f = open('/Users/vit/vtables.txt', 'w')

doc = Document.getCurrentDocument()
dataseg = doc.getSegmentByName('__DATA')
textseg = doc.getSegmentByName('__TEXT')

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
		elif b < ord('0') or b > ord('9'):
				if not started:
					continue
		ret = ret + chr(b)
		if not started:
			started = addr-1

	return '',end

def process(classname,addr,end):
	refs = textseg.getReferencesOfAddress(addr)
	if len(refs) == 0:
		print 'can not find refs for', classname
		return
	a = refs[0]
	if a < textseg.getStartingAddress():
		a = refs[1]
	a = a - 8

	refs = dataseg.getReferencesOfAddress(a)
	if len(refs) == 0:
		print 'can not find more refs for', classname
		return

	for i in range(0,len(refs)):
		vtable = refs[i] + 8
		if doc.readUInt64LE(vtable):
			f.write ("<vtable-address name='%s' value='0x%08x'/>\n" % (classname, vtable))
			break
	

#######################################################
for s in dataseg.getSectionsList():
	if s.getName() == '__const':
		sec = s
		break
i = sec.getStartingAddress()
end = i + sec.getLength()

while i < end:
	dataseg.setTypeAtAddress(i, 8, Segment.TYPE_LONG)
	i = i + 8
#######################################################
for s in dataseg.getSectionsList():
	if s.getName() == '__const_coal':
		sec = s
		break
i = sec.getStartingAddress()
end = i + sec.getLength()

while i < end:
	dataseg.setTypeAtAddress(i, 8, Segment.TYPE_LONG)
	i = i + 8
######################################################

print '============================='

######################################################
for s in textseg.getSectionsList():
	if s.getName() == '__const':
		sec = s
		break
addr = sec.getStartingAddress()

# __const_coal is right after __const
for s in textseg.getSectionsList():
	if s.getName() == '__const_coal':
		sec = s
		break
end = sec.getStartingAddress() + sec.getLength()

ss = -1
while addr < end:
	s,ad = readAscii(textseg,addr,end)
	textseg.setTypeAtAddress(ad, len(s)+1, Segment.TYPE_ASCII)
	m = re.match("([0-9]+)([a-z_]+.+st)", s)
	if m:
		classname = m.group(2)
		process(classname, ad, end)
	addr = ad+len(s)+1
#######################################################
			
f.close()

print 'DONE'
