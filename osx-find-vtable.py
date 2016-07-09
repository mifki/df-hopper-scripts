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
		ret = ret + chr(b)
		if not started:
			started = addr-1

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

	vtable = refs[0] + 8
	f.write ("<vtable-address name='%s' value='0x%016x'/>\n" % (classname, vtable))
	

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
######################################################

print '============================='

######################################################
for s in textseg.getSectionsList():
	if s.getName() == '__const':
		sec = s
		break

addr = sec.getStartingAddress()
end = addr + sec.getLength()

ss = -1
while addr < end:
	s,ad = readAscii(textseg,addr,end)
	textseg.setTypeAtAddress(ad, len(s)+1, Segment.TYPE_ASCII)
	if re.match("[0-9]+[a-z_]+.+st", s):
		classname = s[2:]
		process(classname, ad, end)
	addr = ad+len(s)+1
#######################################################
			
f.close()

print 'DONE'
