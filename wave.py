#!/usr/bin/env python
#
#!/usr/bin/python2.4
#
# Copyright 2009 Google Inc. All Rights Reserved.
"""grauniady - a Guardian robot for Wave

gives you the ten most recent items from The Guardian for text in a blip
"""

__author__ = 'chris.thorpe@guardian.co.uk (Chris Thorpe)'

from waveapi import events
from waveapi import robot

from guardianapi import Client


def OnBlipSubmitted(properties, context):
	blip = context.GetBlipById(properties['blipId'])
	contents = blip.GetDocument().GetText()
	if '?guardian' in contents:
		search = '"%s"' % contents.replace('?guardian', '').replace('"', ' ').replace('\n', '')
		items = Client('API_KEY_GOES_IN_HERE').search(q = search, count = '10', order_by_date = 'desc')
		content = "\n\nLatest items from The Guardian for " + search + "\n"
		for item in items:
			standfirst = ""
			try:
				standfirst = item['standfirst'] + "\n"
			except:
				standfirst = ""
			content = content + item['headline'] + ", by "+ item['byline'] +"\n" + standfirst + item['webUrl'] + "\n\n"
		blip.GetDocument().SetText(content)



if __name__ == '__main__':
  grauniady = robot.Robot('grauniady',
                         image_url='http://grauniady.appspot.com/public/grauniady.jpg',
                         profile_url='http://www.google.com')
  grauniady.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
  grauniady.Run(debug=True)
