
# This file was generated by 'versioneer.py' (0.18) from
# revision-control system data, or from the parent directory name of an
# unpacked source archive. Distribution tarballs contain a pre-generated copy
# of this file.

import json

version_json = '''
{
 "date": "2022-05-30T03:50:44+0000",
 "dirty": false,
 "error": null,
 "full-revisionid": "5619eb7010d7434bc2608e4f791bf39cb6a2d2be",
 "version": "1.16.0.post.dev560"
}
'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)
