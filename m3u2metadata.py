# m3u2metadata by magohole
# Copyright (C) 2021  magohole
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
from magic import from_buffer as mime
from os.path import isfile as pp
from os import rename as brr
from mutagen.id3 import ID3, TIT2, TRCK, TLEN
from mutagen.wave import WAVE
import riffp as rp

class track:
    grp=""
    alb=""
    art=""
    gn=""
    def __init__(self, l, n, p, i):
        self.l=l
        self.n=n
        self.p=p
        self.i=i
class globalinf:
    grp=""
    alb=""
    art=""
    genre=""

def snqdq(s, d, dq=False):
    if d == '"':
        raise ValueError
        return
    q=False
    r=[]
    i=0
    ii=0
    for c in s:
        if c == d and not q:
            r.append(s[ii:i])
            ii=i+1
        if c == '"':
            q=not q
        i+=1
    r.append(s[ii:i])
    if dq:
        r=[a.replace('"', '') for a in r]
    return r
        

def parse_extra(s, ts):
    it=snqdq(s, ' ', dq=True)
    tsl=it[0]
    if len(it) > 1:
        it=it[1:]
        for i in it:
            if "=" not in i:
                continue
            v=i.split("=", 1)
            if v[0] == "artist":
                ts.art=v[1]
            elif v[0] == "album":
                ts.alb=v[1]
            elif v[0] == "group":
                ts.grp=v[1]
            elif v[0] == "genere":
                ts.gn=v[1]
    return tsl

def get_tracks(fn, basepath, gi):
    f=open(fn, 'r', encoding='utf8')
    l=f.readline()
    l=l.strip()
    if not l == "#EXTM3U":
        sys.exit("Invalid m3u file!!1!")

    t = []
    ts=track("_Error","_Error","_Error", 0)
    i=1 # Track count
    extinf=False
    for l in f:
        l=l.strip()
        if l[0:8] == "#EXTINF:":
            ts.l, ts.n = l[8:].split(',',1)
            ts.l=parse_extra(ts.l, ts)
            ts.l=int(ts.l)
            ts.i=i
            extinf=True
        elif len(l)!=0:
            if extinf:
                if type(basepath) == str and basepath != None:
                    ts.p=basepath+l
                else:
                    ts.p=l
                t.append(ts)
                ts=track("_Error","_Error","_Error", 0)
                i+=1
                extinf=False
            elif l[:8] == "#EXTALB:":
                gi.alb=l[8:]
            elif l[:8] == "#EXTART:":
                gi.art=l[8:]
            elif l[:8] == "#EXTGENRE:":
                gi.genre=l[8:]
    return t

def print_tracks(ts):
    if len(ts) == 0:
        print("print_tracks list empty", file=sys.stderr)
        return
    elif type(ts[0]) != track:
        print("print_tracks list elements not of type 'track'", file=sys.stderr)
        return

    for t in ts:
        print("%i %s %s %i" % (t.i, t.n, t.p, t.l))


def set_metadata(ts, gi):
    for t in ts:
        if not pp(t.p):
            print("Error: File %s does not exist" % t.p, file=sys.stderr)
            continue
        f = open(t.p, "rb")
        mm= mime(f.read(), mime=True) 
        if mm != "audio/mpeg" and mm != "audio/x-wav":
            print("Error: Can't set file %s's metadata. file is of type %s" % (t.p, mm), file=sys.stderr)
            f.close()
            continue
        print("Changing metadata: %s" % t.p)
        f.close()
        if mm == "audio/mpeg":
            a=ID3(t.p, v2_version=3)
            a.add(TIT2(encoding=3, text=t.n))
            a.add(TRCK(encoding=3, text=str(t.i)))
            a.add(TLEN(encoding=3, text=str(t.l)))
            a.save(v2_version=3)
        elif mm == "audio/x-wav":
            wf=open(t.p, "rb")
            ck=rp.get_riff(wf)
            ckp=rp.riff_path(ck, [])
            mp=rp.path_to_metadata(ckp, new=True)
            mm=rp.get_metadata(wf, mp.ebl)
            mm[b'INAM'] = bytes(t.n, "utf-8")+b'\x00'
            mm[b'ITRK'] = bytes(str(t.i), "utf-8")+b'\x00'
            mm[b'TLEN'] = bytes(str(t.l), "utf-8")+b'\x00'
            if t.alb:
                mm[b'IPRD'] = bytes(str(t.alb), "utf-8")+b'\x00'
            elif gi.alb:
                mm[b'IPRD'] = bytes(str(gi.alb), "utf-8")+b'\x00'

            if t.art:
                mm[b'IART'] = bytes(str(t.art), "utf-8")+b'\x00'
            elif gi.art:
                mm[b'IART'] = bytes(str(gi.art), "utf-8")+b'\x00'

            if t.gn:
                mm[b'IGNR'] = bytes(str(t.gn), "utf-8")+b'\x00'
            elif gi.genre:
                mm[b'IGNR'] = bytes(str(gi.genre), "utf-8")+b'\x00'

            rp.set_metadata(mp, mm)
            wo=open(t.p+"._.wav", "wb")
            rp.save_riff(wo, wf, ck)
            wo.close()
            wf.close()
            brr(t.p, t.p+".old.wav")
            brr(t.p+"._.wav", t.p)

def __main__():
    if len(sys.argv) <= 1:
        sys.exit("Error: Missing filename")
    gi=globalinf()
    tt = get_tracks(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None, gi)
    #print_tracks(tt)
    set_metadata(tt, gi)

if __name__ == "__main__":
    __main__()
