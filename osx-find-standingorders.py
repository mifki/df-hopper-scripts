f = open('/Users/vit/orders.txt', 'w')

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
	

def process(seg, s, a):	
	addr = seg.getReferencesOfAddress(a)[0]
	while addr > seg.getStartingAddress():
		addr = seg.instructionStart(addr-1)
		i = seg.getInstructionAtAddress(addr)
		if i.getInstructionString() == 'je':
			break

	addr = seg.instructionStart(addr-1)
	i = seg.getInstructionAtAddress(addr)
	if i.getInstructionString() != 'cmp':
		print 'can not find cmp instruction for %s' % s
		return

	reg = i.getFormattedArgument(0)[1:4]
	try:
		while addr > seg.getStartingAddress():
			addr = seg.instructionStart(addr-1)
			i = seg.getInstructionAtAddress(addr)
			if i.getInstructionString() == 'lea':
				if i.getFormattedArgument(0) == reg:
					gaddr = i.getFormattedArgument(1)[1:-1]
					gaddr = int(gaddr, 16)
					f.write ("<global-address name='standing_orders_%s' value='0x%08x'/>\n" % (s, gaddr))
					break
	except:
		print 'error finding', s



olist = {
    # standing order subscreen
    'Current Standing Orders': {
        # string in binary: name of global ('standing_orders_' prefix)
        ': Announce all job cancellations': 'job_cancel_announce',
        ' Gather Animals': 'gather_animals',
        ' Gather Food': 'gather_food',
        ' Gather Furniture': 'gather_furniture',
        ' Gather Bodies': 'gather_bodies',
        ' Gather Minerals': 'gather_minerals',
        ' Gather Wood': 'gather_wood',
        ' All Harvest': 'farmer_harvest',
        ': Mix Food': 'mix_food',
    },
    'Current Refuse Orders': {
        ' Gather Refuse': 'gather_refuse',
        '   From Outside': 'gather_refuse_outside',    # gather From Outside
        ': Gather Vermin Remains': 'gather_vermin_remains',
        ' Dump Corpses': 'dump_corpses',
        ' Dump Skulls': 'dump_skulls',
        ' Dump Bones': 'dump_bones',
        ' Dump Shells': 'dump_shells',
        ' Dump Skins': 'dump_skins',
        ' Dump Hair/Wool': 'dump_hair',
        ' Dump Other': 'dump_other',
    },

    'Current Forbid Orders': {
        ': Claim used ammunition': 'forbid_used_ammo',
        ': Claim your dead': 'forbid_own_dead',
        ': Claim your death items': 'forbid_own_dead_items',
        ': Claim other non-hunted': 'forbid_other_nohunt',
        ': Claim other death items': 'forbid_other_dead_items',
    },

    'Current Workshop Orders': {
        ': Auto Loom All Thread': 'auto_loom',
        ': Use Dyed Cloth': 'use_dyed_cloth',
        ': No Auto Collect Webs': 'auto_collect_webs',
        ': No Auto Slaughter': 'auto_slaughter',
        ': No Auto Butcher': 'auto_butcher',
        ': No Auto Fishery': 'auto_fishery',
        ': No Auto Kitchen': 'auto_kitchen',
        ': No Auto Tan': 'auto_tan',
        ': No Auto Kiln': 'auto_kiln',
        ': No Auto Smelter': 'auto_smelter',
        ': No Auto Other': 'auto_other',
    },
   
    'Current Zone Orders': {
        ': Prefer Zone Drinking': 'zoneonly_drink',
        ': Prefer Zone Fishing': 'zoneonly_fish',
    },
}



print '============================='

sec = doc.getSectionByName('__cstring')
addr = sec.getStartingAddress()
last = addr + sec.getLength()

while addr < last:
	s,ad = readAscii(seg,addr,last)

	if s[0:-1] in olist:
		strings = olist[s[0:-1]]

		addr2 = sec.getStartingAddress()
		while addr2 < last:
			s2,ad2 = readAscii(seg,addr2,last)

			if s2 in strings:
				process(seg, strings[s2], ad2)

			addr2 = ad2+len(s2)+1
			

	addr = ad+len(s)+1


f.close()

print 'DONE'
