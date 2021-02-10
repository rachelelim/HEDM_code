"""Parse CHESS spec files to find scan information

QUESTIONS/COMMENTS:
* This only processes "slew_omega" type scans. Do we need "tseries" too?
"""
from collections import namedtuple
import os
import re

import numpy as np

from hexrd import imageseries
from hexrd.imageseries.process import ProcessedImageSeries as Pims

fs_root = '/nfs/chess/raw'
re_scan = re.compile('^#S ')
re_eff = re.compile('effectively slew_ome')

flip_dflt = "h"
darkframes_dflt = 120
save_fmt = "frame-cache"
raw_fmt = "hdf5"

class ScanTypes:
    omega = 'slew_ome'
    tseries = 'tseries'

RunInfo = namedtuple('RunInfo', ['cycle', 'station', 'user', 'name'])

_fields = ['id', 'type', 'ome0', 'ome1', 'steps', 'exposure']
ScanRequest = namedtuple('ScanRequest', _fields)
del _fields

# Image Series Options: panels = list of strings, number from spec.log
ImageSeriesOpts = namedtuple('ImageSeriesOpts', ['flip'])


def _get_raw_dir(info):
    raw_tmpl = fs_root + '/%(cycle)s/%(station)s/%(user)s/%(name)s'
    return raw_tmpl % info._asdict()


def _make_dark(ims):
    """build dark"""
    return imageseries.stats.median(ims, nframes=darkframes_dflt)


class Parser(object):

    def __init__(self, runinfo):
        self.runinfo = runinfo
        self.requests = []
        self.effective = []
        self._get_requests()
        self.scans = []
        self._get_scans()

    @property
    def rawdir(self):
        return _get_raw_dir(self.runinfo)

    def scandir(self, scanid):
        return os.path.join(self.rawdir, str(scanid))

    def _get_scans(self):
        """Break log file into text for each scan"""
        speclog = os.path.join(self.rawdir, 'spec.log')

        with open(speclog, "r") as f:
            scantext = []
            for l in f:
                if re_scan.match(l):
                    # start new scan
                    self.scans.append(scantext)
                    scantext = []
                scantext.append(l)
            self.scans.append(scantext)


    def _get_requests(self):
        """List of available scan numbers"""
        speclog = os.path.join(self.rawdir, 'spec.log')
        with open(speclog, "r") as f:
            needs_eff = False
            for l in f:
                if re_scan.match(l):
                    if needs_eff:
                        # No matching effective request, scan probably terminated
                        self.effective.append(None)
                    needs_eff = True

                    # New scan, waiting for response
                    flds = l.split()
                    scanid = int(flds[1])
                    scantype = flds[2]
                    if scantype == ScanTypes.omega:
                        ome0 = float(flds[3]),
                        ome1 = float(flds[4]),
                        steps = int(flds[5]),
                        exposure = float(flds[6])
                    else:
                        ome0 = None
                        ome1 = None
                        steps = None
                        exposure = None

                    req = ScanRequest(
                        id=scanid,
                        type=scantype,
                        ome0=ome0,
                        ome1=ome1,
                        steps=steps,
                        exposure=exposure
                    )
                    self.requests.append(req)

                if re_eff.search(l):
                    # Got Response: assumes exposure not changed
                    flds = l.split()
                    effreq = ScanRequest(
                        id=scanid,
                        type=flds[8],
                        ome0=float(flds[9]),
                        ome1=float(flds[10]),
                        steps=int(flds[11]),
                        exposure=req.exposure
                    )
                    self.effective.append(effreq)
                    needs_eff = False
        if needs_eff:
            self.effective.append(None)

        nr, ne = len(self.requests), len(self.effective)
        amsg = "Request and response lists do not have same length: %d, %d" % (nr, ne)
        assert nr == ne, amsg

    def _find_imagefiles(self, scanid):
        """Walk the filesystem to locate """
        raw = self.rawdir
        imgdir = os.path.join(self.scandir(scanid), 'ff')

        return os.listdir(imgdir)


    def imagefiles_dict(self, scanid):
        imfdict = dict()
        sdir = self.scandir(scanid)
        imgfiles = self._find_imagefiles(scanid)
        for fname in imgfiles:
            panel = fname.split('_')[0]
            imfdict[panel] = os.path.join(sdir, 'ff', fname)

        return imfdict

    def raw_imageseries_dict(self, scanid):
        ims_dict = dict()
        imf_dict = self.imagefiles_dict(scanid)
        for p in imf_dict:
            ims_dict[p] = imageseries.open(imf_dict[p], raw_fmt, path='imageseries')

        return ims_dict

    def imageseries_dict(self, scanid, opts_dict):
        ims_dict = dict()
        raw_dict = self.raw_imageseries_dict(scanid)
        for p in raw_dict:
            ims = raw_dict[p]
            opts = opts_dict[p]
            omega = self.get_omega(scanid)
            ops = [('flip', opts.flip), ('dark', _make_dark(ims))]
            pims = Pims(ims, ops)
            pims.metadata['omega'] = omega
            ims_dict[p] = pims

        return ims_dict

    def write_fc(self, ims, fname, threshold):
        imageseries.write(ims, fname, save_fmt,
                          cache_file=fname,
                          threshold=threshold
        )

    def get_omega(self, scanid):
        # Find omegas
        raw_ims = self.raw_imageseries_dict(scanid)
        key = list(raw_ims.keys())[0]
        req = self.effective[scanid - 1]  # FIXME
        nsteps = len(raw_ims[key])
        domega = (req.ome1 - req.ome0)/req.steps
        ome0 = req.ome0
        ome1 = ome0 + nsteps*domega
        w = imageseries.omega.OmegaWedges(nsteps)
        w.addwedge(ome0, ome1, nsteps)

        return w.omegas
