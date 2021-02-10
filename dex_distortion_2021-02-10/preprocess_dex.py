"""Init file for CHESS users"""

from importlib import reload

import multiprocessing
import numpy as np

from hexrd.imageseries import stats
from hexrd.imageseries.process import ProcessedImageSeries
from hexrd import imageseries

import chess

# chess.darkframes_dflt = 10 # testing

ncpus = int(np.round(0.5*multiprocessing.cpu_count()))
nrows = 3888
ncols = 3072
rectangles = {
    '0_0': np.array([[0, nrows//2], [0, ncols//2]]),
    '1_0': np.array([[nrows//2, nrows], [0, ncols//2]]),
    '0_1': np.array([[0, nrows//2], [ncols//2, ncols]]),
    '1_1': np.array([[nrows//2, nrows], [ncols//2, ncols]])
}

cycle = '2021-1'
station = 'id3a'
user = 'pagan-1108-2'


'''
sample_info = {
    'fd1-q-1' :np.arange(12, 68),
    'fd1-a-1':np.arange(4, 98),
    'fd2-q-1':np.hstack([2, np.arange(10, 87)]),
    'fd2-a-1':np.hstack([3, np.arange(11, 25), np.arange(26, 40), np.arange(54, 79)])
}

sample_info = {
    'mruby-0129':[4, ]
}
'''

sample_info = {
    'mruby-0120a':np.arange(1,2)
}

do_subpanels = False

save_fmt = 'frame-cache'

ims_options_dict = dict(
    ff1=chess.ImageSeriesOpts(flip='v'),
    ff2=chess.ImageSeriesOpts(flip='h')
)

# %% functions

def process_raw_mp_init(params):
    global paramMP
    paramMP = params


def process_raw_mp(scan_id):
    threshold = paramMP['threshold']
    opts_dict = paramMP['ims_options']
    parser = paramMP['parser']
    do_subpanels = paramMP['do_subpanels']

    fname_tmpl = "%s_%04d-%s.npz"
    imsd = parser.imageseries_dict(scan_id, opts_dict)
    for panel_id, ims in imsd.items():
        if do_subpanels:
            for subpanel_id, rect in rectangles.items():
                pims = ProcessedImageSeries(
                    ims,
                    [('rectangle', rect), ]
                )
                output_fname = fname_tmpl % (
                    parser.runinfo.name,
                    scan_id,
                    '_'.join([panel_id, subpanel_id])
                )
                if save_fmt == 'frame-cache':
                    parser.write_fc(pims, output_fname, threshold)
                elif save_fmt == 'hdf5':
                    imageseries.write(pims, output_fname, format='hdf5', path='/imageseries')
        else:
            output_fname = fname_tmpl % (
                parser.runinfo.name,
                scan_id,
                panel_id
            )
            if save_fmt == 'frame-cache':
                parser.write_fc(ims, output_fname, threshold)
            elif save_fmt == 'hdf5':
                imageseries.write(ims, output_fname, format='hdf5', path='/imageseries')

# run

for sample_name, scan_ids in sample_info.items():
    runinfo = chess.RunInfo(
        cycle=cycle,
        station=station,
        user=user,
        name=sample_name
    )

    '''
    p = chess.Parser(runinfo)
    imf_dict = p.imagefiles_dict(scanid)
    raw_dict = p.raw_imageseries_dict(scanid)
    '''

    params = dict(
        threshold=250,
        ims_options=ims_options_dict,
        parser=chess.Parser(runinfo),
        do_subpanels=do_subpanels
    )

    # import pdb;pdb.set_trace()

    print("INFO:\tprocessing '%s'" % sample_name)
    pool = multiprocessing.Pool(
        min(ncpus, len(scan_ids)),
        process_raw_mp_init, (params, )
    )
    result = pool.map(process_raw_mp, scan_ids)
    pool.close()
