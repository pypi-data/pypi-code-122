#!/usr/bin/env python
# -*- encoding: utf-8 -*-

nsmap = {
    "D": "DAV:",
    "C": "urn:ietf:params:xml:ns:caldav",
}

## silly thing with this one ... but quite many caldav libraries,
## caldav clients and caldav servers supports this namespace and the
## calendar-color and calendar-order properties.  However, those
## attributes aren't described anywhere, and the I-URL even gives a
## 404!  I don't want to ship it in the namespace list of every request.
nsmap2 = nsmap.copy()
nsmap2["I"] = "http://apple.com/ns/ical/",

def ns(prefix, tag=None):
    name = "{%s}" % nsmap2[prefix]
    if tag is not None:
        name = "%s%s" % (name, tag)
    return name
