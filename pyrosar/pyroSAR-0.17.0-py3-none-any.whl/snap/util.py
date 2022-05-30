###############################################################################
# Convenience functions for SAR image batch processing with ESA SNAP

# Copyright (c) 2016-2022, the pyroSAR Developers.

# This file is part of the pyroSAR Project. It is subject to the
# license terms in the LICENSE.txt file found in the top-level
# directory of this distribution and at
# https://github.com/johntruckenbrodt/pyroSAR/blob/master/LICENSE.txt.
# No part of the pyroSAR project, including this file, may be
# copied, modified, propagated, or distributed except according
# to the terms contained in the LICENSE.txt file.
###############################################################################
import os
import re
import shutil
from ..drivers import identify, identify_many, ID
from ..ancillary import multilook_factors
from ..auxdata import get_egm_lookup
from .auxil import parse_recipe, parse_node, gpt, groupbyWorkers, writer, windows_fileprefix, orb_parametrize

from spatialist import crsConvert, Vector, Raster, bbox, intersect
from spatialist.ancillary import dissolve

import logging

log = logging.getLogger(__name__)


def geocode(infile, outdir, t_srs=4326, spacing=20, polarizations='all', shapefile=None, scaling='dB',
            geocoding_type='Range-Doppler', removeS1BorderNoise=True, removeS1BorderNoiseMethod='pyroSAR',
            removeS1ThermalNoise=True, offset=None, allow_RES_OSV=False, demName='SRTM 1Sec HGT',
            externalDEMFile=None, externalDEMNoDataValue=None, externalDEMApplyEGM=True, terrainFlattening=True,
            basename_extensions=None, test=False, export_extra=None, groupsize=1, cleanup=True, tmpdir=None,
            gpt_exceptions=None, gpt_args=None, returnWF=False, nodataValueAtSea=True,
            demResamplingMethod='BILINEAR_INTERPOLATION', imgResamplingMethod='BILINEAR_INTERPOLATION',
            alignToStandardGrid=False, standardGridOriginX=0, standardGridOriginY=0,
            speckleFilter=False, refarea='gamma0', clean_edges=False, clean_edges_npixels=1,
            rlks=None, azlks=None):
    """
    general function for geocoding of SAR backscatter images with SNAP.
    
    This function performs the following steps:
    
    - (if necessary) identify the SAR scene(s) passed via argument `infile` (:func:`pyroSAR.drivers.identify`)
    - (if necessary) create the directories defined via `outdir` and `tmpdir`
    - (if necessary) download Sentinel-1 OSV files
    - parse a SNAP workflow (:class:`pyroSAR.snap.auxil.Workflow`)
    - write the workflow to an XML file in `outdir`
    - execute the workflow (:func:`pyroSAR.snap.auxil.gpt`)

    Note
    ----
    The function may create workflows with multiple `Write` nodes. All nodes are parametrized to write data in ENVI format,
    in which case the node parameter `file` is going to be a directory. All nodes will use the same temporary directory,
    which will be created in `tmpdir`.
    Its name is created from the basename of the `infile` (:meth:`pyroSAR.drivers.ID.outname_base`)
    and a suffix identifying each processing node of the workflow (:meth:`pyroSAR.snap.auxil.Workflow.suffix`).
    
    For example: `S1A__IW___A_20180101T170648_NR_Orb_Cal_ML_TF_TC`.
    
    Parameters
    ----------
    infile: str or ~pyroSAR.drivers.ID or list
        The SAR scene(s) to be processed; multiple scenes are treated as consecutive acquisitions, which will be
        mosaicked with SNAP's SliceAssembly operator.
    outdir: str
        The directory to write the final files to.
    t_srs: int, str or osr.SpatialReference
        A target geographic reference system in WKT, EPSG, PROJ4 or OPENGIS format.
        See function :func:`spatialist.auxil.crsConvert()` for details.
        Default: `4326 <https://spatialreference.org/ref/epsg/4326/>`_.
    spacing: int or float, optional
        The target pixel spacing in meters. Default is 20
    polarizations: list[str] or str
        The polarizations to be processed; can be a string for a single polarization, e.g. 'VV', or a list of several
        polarizations, e.g. ['VV', 'VH']. With the special value 'all' (default) all available polarizations are
        processed.
    shapefile: str or :py:class:`~spatialist.vector.Vector` or dict, optional
        A vector geometry for subsetting the SAR scene to a test site. Default is None.
    scaling: {'dB', 'db', 'linear'}, optional
        Should the output be in linear or decibel scaling? Default is 'dB'.
    geocoding_type: {'Range-Doppler', 'SAR simulation cross correlation'}, optional
        The type of geocoding applied; can be either 'Range-Doppler' (default) or 'SAR simulation cross correlation'
    removeS1BorderNoise: bool, optional
        Enables removal of S1 GRD border noise (default). Will be ignored if SLC scenes are processed.
    removeS1BorderNoiseMethod: str, optional
        The border noise removal method to be applied if `removeS1BorderNoise` is True.
        See :func:`pyroSAR.S1.removeGRDBorderNoise` for details. One of the following:
        
         - 'ESA': the pure implementation as described by ESA
         - 'pyroSAR': the ESA method plus the custom pyroSAR refinement (default)
    removeS1ThermalNoise: bool, optional
        Enables removal of S1 thermal noise (default).
    offset: tuple, optional
        A tuple defining offsets for left, right, top and bottom in pixels, e.g. (100, 100, 0, 0); this variable is
        overridden if a shapefile is defined. Default is None.
    allow_RES_OSV: bool
        (only applies to Sentinel-1) Also allow the less accurate RES orbit files to be used?
        The function first tries to download a POE file for the scene.
        If this fails and RES files are allowed, it will download the RES file.
        The selected OSV type is written to the workflow XML file.
        Processing is aborted if the correction fails (Apply-Orbit-File parameter continueOnFail set to false).
    demName: str
        The name of the auto-download DEM. Default is 'SRTM 1Sec HGT'. Is ignored when `externalDEMFile` is not None.
        Supported options:
        
         - ACE2_5Min
         - ACE30
         - ASTER 1sec GDEM
         - CDEM
         - Copernicus 30m Global DEM
         - Copernicus 90m Global DEM
         - GETASSE30
         - SRTM 1Sec Grid
         - SRTM 1Sec HGT
         - SRTM 3Sec
    externalDEMFile: str or None, optional
        The absolute path to an external DEM file. Default is None. Overrides `demName`.
    externalDEMNoDataValue: int, float or None, optional
        The no data value of the external DEM. If not specified (default) the function will try to read it from the
        specified external DEM.
    externalDEMApplyEGM: bool, optional
        Apply Earth Gravitational Model to external DEM? Default is True.
    terrainFlattening: bool
        Apply topographic normalization on the data?
    basename_extensions: list of str or None
        Names of additional parameters to append to the basename, e.g. ['orbitNumber_rel'].
    test: bool, optional
        If set to True the workflow xml file is only written and not executed. Default is False.
    export_extra: list or None
        A list of image file IDs to be exported to outdir. The following IDs are currently supported:
        
         - incidenceAngleFromEllipsoid
         - localIncidenceAngle
         - projectedLocalIncidenceAngle
         - DEM
         - layoverShadowMask
         - scatteringArea (requires ``terrainFlattening=True``)
         - gammaSigmaRatio (requires ``terrainFlattening=True`` and ``refarea=['sigma0', 'gamma0']``)
    groupsize: int
        The number of workers executed together in one gpt call.
    cleanup: bool
        Should all files written to the temporary directory during function execution be deleted after processing?
        Default is True.
    tmpdir: str or None
        Path of custom temporary directory, useful to separate output folder and temp folder. If `None`, the `outdir`
        location will be used. The created subdirectory will be deleted after processing if ``cleanup=True``.
    gpt_exceptions: dict or None
        A dictionary to override the configured GPT executable for certain operators;
        each (sub-)workflow containing this operator will be executed with the define executable;
        
         - e.g. ``{'Terrain-Flattening': '/home/user/snap/bin/gpt'}``
    gpt_args: list or None
        A list of additional arguments to be passed to the gpt call.
        
        - e.g. ``['-x', '-c', '2048M']`` for increased tile cache size and intermediate clearing
    returnWF: bool
        Return the full name of the written workflow XML file?
    nodataValueAtSea: bool
        Mask pixels acquired over sea? The sea mask depends on the selected DEM.
    demResamplingMethod: str
        One of the following:
        
         - 'NEAREST_NEIGHBOUR'
         - 'BILINEAR_INTERPOLATION'
         - 'CUBIC_CONVOLUTION'
         - 'BISINC_5_POINT_INTERPOLATION'
         - 'BISINC_11_POINT_INTERPOLATION'
         - 'BISINC_21_POINT_INTERPOLATION'
         - 'BICUBIC_INTERPOLATION'
    imgResamplingMethod: str
        The resampling method for geocoding the SAR image; the options are identical to demResamplingMethod.
    alignToStandardGrid: bool
        Align all processed images to a common grid?
    standardGridOriginX: int or float
        The x origin value for grid alignment
    standardGridOriginY: int or float
        The y origin value for grid alignment
    speckleFilter: str
        One of the following:
        
         - 'Boxcar'
         - 'Median'
         - 'Frost'
         - 'Gamma Map'
         - 'Refined Lee'
         - 'Lee'
         - 'Lee Sigma'
    refarea: str or list
        'sigma0', 'gamma0' or a list of both
    clean_edges: bool
        erode noisy image edges? See :func:`pyroSAR.snap.auxil.erode_edges`.
        Does not apply to layover-shadow mask.
    clean_edges_npixels: int
        the number of pixels to erode.
    rlks: int or None
        the number of range looks. If not None, overrides the computation done by function
        :func:`pyroSAR.ancillary.multilook_factors` based on the image pixel spacing and the target spacing.
    azlks: int or None
        the number of azimuth looks. Like `rlks`.
    
    Returns
    -------
    str or None
        Either the name of the workflow file if ``returnWF == True`` or None otherwise
    
    
    .. figure:: figures/snap_geocode.svg
        :align: center
        
        Function geocode workflow diagram for processing Sentinel-1 scenes.
        Dashed lines depict optional steps. The output is sigma or gamma nought
        backscatter with ellipsoid or radiometric terrain correction (suffix elp/rtc)
        as well as several optional ancillary datasets (controlled via argument `export_extra`).

    Examples
    --------
    geocode a Sentinel-1 scene and export the local incidence angle map with it

    >>> from pyroSAR.snap import geocode
    >>> filename = 'S1A_IW_GRDH_1SDV_20180829T170656_20180829T170721_023464_028DE0_F7BD.zip'
    >>> geocode(infile=filename, outdir='outdir', tr=20, scaling='dB',
    >>>         export_extra=['DEM', 'localIncidenceAngle'], t_srs=4326)

    See Also
    --------
    :class:`pyroSAR.drivers.ID`,
    :class:`spatialist.vector.Vector`,
    :func:`spatialist.auxil.crsConvert()`
    """
    if clean_edges:
        try:
            import scipy
        except ImportError:
            raise RuntimeError('please install scipy to clean edges')
    
    if isinstance(infile, ID):
        id = infile
        ids = [id]
    elif isinstance(infile, str):
        id = identify(infile)
        ids = [id]
    elif isinstance(infile, list):
        ids = identify_many(infile, sortkey='start')
        id = ids[0]
    else:
        raise TypeError("'infile' must be of type str, list or pyroSAR.ID")
    
    if id.is_processed(outdir):
        log.info('scene {} already processed'.format(id.outname_base()))
        return
    
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    ############################################
    # general setup
    process_S1_SLC = False
    
    if id.sensor in ['ASAR', 'ERS1', 'ERS2']:
        formatName = 'ENVISAT'
    elif id.sensor in ['S1A', 'S1B']:
        if id.product == 'SLC':
            removeS1BorderNoise = False
            process_S1_SLC = True
        formatName = 'SENTINEL-1'
    else:
        raise RuntimeError('sensor not supported (yet)')
    
    # several options like resampling are modified globally for the whole workflow at the end of this function
    # this list gathers IDs of nodes for which this should not be done because they are configured individually
    resampling_exceptions = []
    ######################
    if isinstance(polarizations, str):
        if polarizations == 'all':
            polarizations = id.polarizations
        else:
            if polarizations in id.polarizations:
                polarizations = [polarizations]
            else:
                raise RuntimeError('polarization {} does not exists in the source product'.format(polarizations))
    elif isinstance(polarizations, list):
        polarizations = [x for x in polarizations if x in id.polarizations]
    else:
        raise RuntimeError('polarizations must be of type str or list')
    
    swaths = None
    if process_S1_SLC:
        if id.acquisition_mode == 'IW':
            swaths = ['IW1', 'IW2', 'IW3']
        elif id.acquisition_mode == 'EW':
            swaths = ['EW1', 'EW2', 'EW3', 'EW4', 'EW5']
        elif re.search('S[1-6]', id.acquisition_mode):
            pass
        else:
            raise RuntimeError('acquisition mode {} not supported'.format(id.acquisition_mode))
    
    bandnames = dict()
    bandnames['beta0'] = ['Beta0_' + x for x in polarizations]
    bandnames['gamma0'] = ['Gamma0_' + x for x in polarizations]
    bandnames['sigma0'] = ['Sigma0_' + x for x in polarizations]
    bandnames['int'] = ['Intensity_' + x for x in polarizations]
    ############################################
    ############################################
    # parse base workflow
    workflow = parse_recipe('blank')
    ############################################
    if not isinstance(infile, list):
        infile = [infile]
    
    last = None
    collect = []
    for i in range(0, len(infile)):
        ############################################
        # Read node configuration
        read = parse_node('Read')
        workflow.insert_node(read)
        read.parameters['file'] = ids[i].scene
        read.parameters['formatName'] = formatName
        last = read
        ############################################
        # Remove-GRD-Border-Noise node configuration
        if id.sensor in ['S1A', 'S1B'] and id.product == 'GRD' and removeS1BorderNoise:
            bn = parse_node('Remove-GRD-Border-Noise')
            workflow.insert_node(bn, before=last.id)
            bn.parameters['selectedPolarisations'] = polarizations
            last = bn
        ############################################
        # Calibration node configuration
        cal = parse_node('Calibration')
        workflow.insert_node(cal, before=last.id)
        cal.parameters['selectedPolarisations'] = polarizations
        if isinstance(refarea, str):
            refarea = [refarea]
        for item in refarea:
            if item not in ['sigma0', 'gamma0']:
                raise ValueError('unsupported value for refarea: {}'.format(item))
        if terrainFlattening:
            cal.parameters['outputBetaBand'] = True
            cal.parameters['outputSigmaBand'] = False
        else:
            for opt in refarea:
                cal.parameters['output{}Band'.format(opt[:-1].capitalize())] = True
        last = cal
        ############################################
        # ThermalNoiseRemoval node configuration
        if id.sensor in ['S1A', 'S1B'] and removeS1ThermalNoise:
            if re.search('S[1-6]', id.acquisition_mode) and id.product == 'SLC':
                raise RuntimeError('thermal noise removal is currently not supported '
                                   'for Sentinel-1 Stripmap SLCs.\nsee here: '
                                   'https://forum.step.esa.int/t/stripmap-slc-error-during-thermal-noise-removal/32688')
            tn = parse_node('ThermalNoiseRemoval')
            workflow.insert_node(tn, before=last.id)
            tn.parameters['selectedPolarisations'] = polarizations
            last = tn
        collect.append(last.id)
    ############################################
    # SliceAssembly node configuration
    if len(collect) > 1:
        sliceAssembly = parse_node('SliceAssembly')
        sliceAssembly.parameters['selectedPolarisations'] = polarizations
        workflow.insert_node(sliceAssembly, before=collect)
        last = sliceAssembly
    ############################################
    # TOPSAR-Deburst node configuration
    if process_S1_SLC and swaths is not None:
        deb = parse_node('TOPSAR-Deburst')
        workflow.insert_node(deb, before=last.id)
        deb.parameters['selectedPolarisations'] = polarizations
        last = deb
    ############################################
    # Apply-Orbit-File node configuration
    orb = orb_parametrize(scene=id, workflow=workflow, before=last.id,
                          formatName=formatName, allow_RES_OSV=allow_RES_OSV)
    last = orb
    ############################################
    # Subset node configuration
    #######################
    # (optionally) add subset node and add bounding box coordinates of defined shapefile
    if shapefile:
        if isinstance(shapefile, dict):
            ext = shapefile
        else:
            if isinstance(shapefile, Vector):
                shp = shapefile.clone()
            elif isinstance(shapefile, str):
                shp = Vector(shapefile)
            else:
                raise TypeError("argument 'shapefile' must be either a dictionary, a Vector object or a string.")
            # reproject the geometry to WGS 84 latlon
            shp.reproject(4326)
            ext = shp.extent
            shp.close()
        # add an extra buffer of 0.01 degrees
        buffer = 0.01
        ext['xmin'] -= buffer
        ext['ymin'] -= buffer
        ext['xmax'] += buffer
        ext['ymax'] += buffer
        with bbox(ext, 4326) as bounds:
            inter = intersect(id.bbox(), bounds)
            if not inter:
                raise RuntimeError('no bounding box intersection between shapefile and scene')
            inter.close()
            wkt = bounds.convert2wkt()[0]
        
        subset = parse_node('Subset')
        workflow.insert_node(subset, before=last.id)
        subset.parameters['region'] = [0, 0, id.samples, id.lines]
        subset.parameters['geoRegion'] = wkt
        subset.parameters['copyMetadata'] = True
        last = subset
    #######################
    # (optionally) configure Subset node for pixel offsets
    if offset and not shapefile:
        subset = parse_node('Subset')
        workflow.insert_node(subset, before=last.id)
        
        # left, right, top and bottom offset in pixels
        l, r, t, b = offset
        
        subset_values = [l, t, id.samples - l - r, id.lines - t - b]
        subset.parameters['region'] = subset_values
        subset.parameters['geoRegion'] = ''
        last = subset
    ############################################
    # Multilook node configuration
    try:
        image_geometry = id.meta['image_geometry']
        incidence = id.meta['incidence']
    except KeyError:
        raise RuntimeError('This function does not yet support sensor {}'.format(id.sensor))
    
    if rlks is None and azlks is None:
        rlks, azlks = multilook_factors(source_rg=id.spacing[0],
                                        source_az=id.spacing[1],
                                        target=spacing,
                                        geometry=image_geometry,
                                        incidence=incidence)
    if [rlks, azlks].count(None) > 0:
        raise RuntimeError("'rlks' and 'azlks' must either both be integers or None")
    
    if azlks > 1 or rlks > 1:
        workflow.insert_node(parse_node('Multilook'), before=last.id)
        ml = workflow['Multilook']
        ml.parameters['nAzLooks'] = azlks
        ml.parameters['nRgLooks'] = rlks
        ml.parameters['sourceBands'] = None
        last = ml
    ############################################
    # Terrain-Flattening node configuration
    tf = None
    if terrainFlattening:
        tf = parse_node('Terrain-Flattening')
        workflow.insert_node(tf, before=last.id)
        if id.sensor in ['ERS1', 'ERS2'] or (id.sensor == 'ASAR' and id.acquisition_mode != 'APP'):
            tf.parameters['sourceBands'] = 'Beta0'
        else:
            tf.parameters['sourceBands'] = bandnames['beta0']
        if 'reGridMethod' in tf.parameters.keys():
            if externalDEMFile is None:
                tf.parameters['reGridMethod'] = True
            else:
                tf.parameters['reGridMethod'] = False
        if 'sigma0' in refarea:
            try:
                tf.parameters['outputSigma0'] = True
            except KeyError:
                raise RuntimeError("The Terrain-Flattening node does not accept "
                                   "parameter 'outputSigma0'. Please update S1TBX.")
        last = tf
    ############################################
    # merge bands to pass them to Terrain-Correction
    bm_tc = None
    bands = dissolve([bandnames[opt] for opt in refarea])
    if len(refarea) > 1 and terrainFlattening and 'scatteringArea' in export_extra:
        bm_tc = parse_node('BandMerge')
        workflow.insert_node(bm_tc, before=[last.source, last.id])
        sources = bm_tc.source
        gamma_index = sources.index('Terrain-Flattening')
        sigma_index = abs(gamma_index - 1)
        s1_id = os.path.basename(os.path.splitext(id.scene)[0])
        bands_long = []
        for band in bands:
            comp = [band + '::']
            if shapefile is not None:
                comp.append('Subset_')
            comp.append(s1_id)
            if band.startswith('Gamma'):
                comp.append('_' + workflow.suffix(stop=sources[gamma_index]))
            else:
                comp.append('_' + workflow.suffix(stop=sources[sigma_index]))
            bands_long.append(''.join(comp))
        bm_tc.parameters['sourceBands'] = bands_long
        last = bm_tc
    ############################################
    # Speckle-Filter node configuration
    speckleFilter_options = ['Boxcar',
                             'Median',
                             'Frost',
                             'Gamma Map',
                             'Refined Lee',
                             'Lee',
                             'Lee Sigma']
    
    if speckleFilter:
        message = '{0} must be one of the following:\n- {1}'
        if speckleFilter not in speckleFilter_options:
            raise ValueError(message.format('speckleFilter', '\n- '.join(speckleFilter_options)))
        sf = parse_node('Speckle-Filter')
        workflow.insert_node(sf, before=last.id)
        sf.parameters['sourceBands'] = None
        sf.parameters['filter'] = speckleFilter
        last = sf
    ############################################
    # configuration of node sequence for specific geocoding approaches
    if geocoding_type == 'Range-Doppler':
        tc = parse_node('Terrain-Correction')
        workflow.insert_node(tc, before=last.id)
        tc.parameters['sourceBands'] = bands
    elif geocoding_type == 'SAR simulation cross correlation':
        sarsim = parse_node('SAR-Simulation')
        workflow.insert_node(sarsim, before=last.id)
        sarsim.parameters['sourceBands'] = bands
        
        workflow.insert_node(parse_node('Cross-Correlation'), before='SAR-Simulation')
        
        tc = parse_node('SARSim-Terrain-Correction')
        workflow.insert_node(tc, before='Cross-Correlation')
    else:
        raise RuntimeError('geocode_type not recognized')
    
    tc.parameters['alignToStandardGrid'] = alignToStandardGrid
    tc.parameters['standardGridOriginX'] = standardGridOriginX
    tc.parameters['standardGridOriginY'] = standardGridOriginY
    last = tc
    #######################
    # specify spatial resolution and coordinate reference system of the output dataset
    tc.parameters['pixelSpacingInMeter'] = spacing
    
    try:
        # try to convert the CRS into EPSG code (for readability in the workflow XML)
        t_srs = crsConvert(t_srs, 'epsg')
    except TypeError:
        raise RuntimeError("format of parameter 't_srs' not recognized")
    except RuntimeError:
        # this error can occur when the CRS does not have a corresponding EPSG code
        # in this case the original CRS representation is written to the workflow
        pass
    
    # the EPSG code 4326 is not supported by SNAP and thus the WKT string has to be defined;
    # in all other cases defining EPSG:{code} will do
    if t_srs == 4326:
        t_srs = 'GEOGCS["WGS84(DD)",' \
                'DATUM["WGS84",' \
                'SPHEROID["WGS84", 6378137.0, 298.257223563]],' \
                'PRIMEM["Greenwich", 0.0],' \
                'UNIT["degree", 0.017453292519943295],' \
                'AXIS["Geodetic longitude", EAST],' \
                'AXIS["Geodetic latitude", NORTH]]'
    
    if isinstance(t_srs, int):
        t_srs = 'EPSG:{}'.format(t_srs)
    
    tc.parameters['mapProjection'] = t_srs
    ############################################
    # (optionally) add node for conversion from linear to db scaling
    if scaling not in ['dB', 'db', 'linear']:
        raise RuntimeError('scaling must be  a string of either "dB", "db" or "linear"')
    
    if scaling in ['dB', 'db']:
        lin2db = parse_node('LinearToFromdB')
        workflow.insert_node(lin2db, before=last.id)
        lin2db.parameters['sourceBands'] = bands
        last = lin2db
    ############################################
    # parametrize write node
    # create a suffix for the output file to identify processing steps performed in the workflow
    suffix = workflow.suffix()
    if tmpdir is None:
        tmpdir = outdir
    basename = os.path.join(tmpdir, id.outname_base(basename_extensions))
    outname = basename + '_' + suffix
    
    write = parse_node('Write')
    workflow.insert_node(write, before=last.id)
    write.parameters['file'] = outname
    write.parameters['formatName'] = 'ENVI'
    ############################################
    ############################################
    if export_extra is not None:
        tc_options = ['incidenceAngleFromEllipsoid',
                      'localIncidenceAngle',
                      'projectedLocalIncidenceAngle',
                      'DEM',
                      'layoverShadowMask']
        tc_selection = []
        for item in export_extra:
            if item in tc_options:
                key = 'save{}{}'.format(item[0].upper(), item[1:])
                tc.parameters[key] = True
                if item == 'DEM':
                    tc_selection.append('elevation')
                else:
                    tc_selection.append(item)
            elif item == 'scatteringArea':
                if not terrainFlattening:
                    raise RuntimeError('scatteringArea can only be created if terrain flattening is performed')
                area_select = parse_node('BandSelect')
                workflow.insert_node(area_select, before=tf.source, resetSuccessorSource=False)
                area_select.parameters['sourceBands'] = bandnames['beta0']
                
                area_merge1 = parse_node('BandMerge')
                workflow.insert_node(area_merge1, before=[tf.id, area_select.id], resetSuccessorSource=False)
                
                math = parse_node('BandMaths')
                workflow.insert_node(math, before=area_merge1.id, resetSuccessorSource=False)
                
                pol = polarizations[0]  # the result will be the same for each polarization
                area = 'scatteringArea_{0}'.format(pol)
                expression = 'Beta0_{0} / Gamma0_{0}'.format(pol)
                
                math.parameters.clear_variables()
                exp = math.parameters['targetBands'][0]
                exp['name'] = area
                exp['type'] = 'float32'
                exp['expression'] = expression
                exp['noDataValue'] = 0.0
                
                if len(refarea) > 1:
                    bm_tc.source = bm_tc.source + [math.id]
                else:
                    bm_tc = parse_node('BandMerge')
                    workflow.insert_node(bm_tc, before=[tf.id, math.id], resetSuccessorSource=False)
                    tc.source = bm_tc.id
                
                # modify Terrain-Correction source bands
                tc_bands = tc.parameters['sourceBands'] + ',' + area
                tc.parameters['sourceBands'] = tc_bands
                
                # add scattering Area to list of band directly written from Terrain-Correction
                tc_selection.append(area)
            elif item == 'gammaSigmaRatio':
                if not terrainFlattening:
                    raise RuntimeError('gammaSigmaRatio can only be created if terrain flattening is performed')
                if sorted(refarea) != ['gamma0', 'sigma0']:
                    raise ValueError("For export_extra layer 'gammaSigmaRatio' 'refarea' "
                                     "must contain both sigma0 and gamma0")
                math = parse_node('BandMaths')
                workflow.insert_node(math, before=tf.id, resetSuccessorSource=False)
                
                pol = polarizations[0]  # the result will be the same for each polarization
                ratio = 'gammaSigmaRatio_{0}'.format(pol)
                expression = 'Sigma0_{0} / Gamma0_{0}'.format(pol)
                
                math.parameters.clear_variables()
                exp = math.parameters['targetBands'][0]
                exp['name'] = ratio
                exp['type'] = 'float32'
                exp['expression'] = expression
                exp['noDataValue'] = 0.0
                
                if len(refarea) > 1:
                    bm_tc.source = bm_tc.source + [math.id]
                else:
                    bm_tc = parse_node('BandMerge')
                    workflow.insert_node(bm_tc, before=[tf.id, math.id], resetSuccessorSource=False)
                    tc.source = bm_tc.id
                
                # modify Terrain-Correction source bands
                tc_bands = tc.parameters['sourceBands'] + ',' + ratio
                tc.parameters['sourceBands'] = tc_bands
                
                # add scattering Area to list of band directly written from Terrain-Correction
                tc_selection.append(ratio)
            else:
                raise RuntimeError("ID '{}' not valid for argument 'export_extra'".format(item))
        # directly write export_extra layers to avoid dB scaling
        if scaling in ['db', 'dB'] and len(tc_selection) > 0:
            tc_write = parse_node('Write')
            workflow.insert_node(tc_write, before=tc.id, resetSuccessorSource=False)
            tc_write.parameters['file'] = outname
            tc_write.parameters['formatName'] = 'ENVI'
            tc_select = parse_node('BandSelect')
            workflow.insert_node(tc_select, after=tc_write.id)
            tc_select.parameters['sourceBands'] = tc_selection
    ############################################
    ############################################
    # select DEM type
    dempar = {'externalDEMFile': externalDEMFile,
              'externalDEMApplyEGM': externalDEMApplyEGM}
    if externalDEMFile is not None:
        if os.path.isfile(externalDEMFile):
            if externalDEMNoDataValue is None:
                with Raster(externalDEMFile) as dem:
                    dempar['externalDEMNoDataValue'] = dem.nodata
                if dempar['externalDEMNoDataValue'] is None:
                    raise RuntimeError('Cannot read NoData value from DEM file. '
                                       'Please specify externalDEMNoDataValue')
            else:
                dempar['externalDEMNoDataValue'] = externalDEMNoDataValue
            dempar['reGridMethod'] = False
        else:
            raise RuntimeError('specified externalDEMFile does not exist')
        dempar['demName'] = 'External DEM'
    else:
        dempar['demName'] = demName
        dempar['externalDEMFile'] = None
        dempar['externalDEMNoDataValue'] = 0
    
    for key, value in dempar.items():
        workflow.set_par(key, value)
    
    # download the EGM lookup table if necessary
    if dempar['externalDEMApplyEGM']:
        get_egm_lookup(geoid='EGM96', software='SNAP')
    ############################################
    ############################################
    # configure the resampling methods
    
    options = ['NEAREST_NEIGHBOUR',
               'BILINEAR_INTERPOLATION',
               'CUBIC_CONVOLUTION',
               'BISINC_5_POINT_INTERPOLATION',
               'BISINC_11_POINT_INTERPOLATION',
               'BISINC_21_POINT_INTERPOLATION',
               'BICUBIC_INTERPOLATION']
    
    message = '{0} must be one of the following:\n- {1}'
    if demResamplingMethod not in options:
        raise ValueError(message.format('demResamplingMethod', '\n- '.join(options)))
    if imgResamplingMethod not in options:
        raise ValueError(message.format('imgResamplingMethod', '\n- '.join(options)))
    
    workflow.set_par('demResamplingMethod', demResamplingMethod)
    workflow.set_par('imgResamplingMethod', imgResamplingMethod,
                     exceptions=resampling_exceptions)
    ############################################
    ############################################
    # additional parameter settings applied to the whole workflow
    
    workflow.set_par('nodataValueAtSea', nodataValueAtSea)
    ############################################
    ############################################
    # write workflow to file and optionally execute it
    log.debug('writing workflow to file')
    
    wf_name = outname.replace(tmpdir, outdir) + '_proc.xml'
    workflow.write(wf_name)
    
    # execute the newly written workflow
    if not test:
        try:
            groups = groupbyWorkers(wf_name, groupsize)
            gpt(wf_name, groups=groups, cleanup=cleanup, tmpdir=outname,
                gpt_exceptions=gpt_exceptions, gpt_args=gpt_args,
                removeS1BorderNoiseMethod=removeS1BorderNoiseMethod)
            writer(xmlfile=wf_name, outdir=outdir, basename_extensions=basename_extensions,
                   clean_edges=clean_edges, clean_edges_npixels=clean_edges_npixels)
        except Exception as e:
            log.info(str(e))
            with open(wf_name.replace('_proc.xml', '_error.log'), 'w') as logfile:
                logfile.write(str(e))
        finally:
            if cleanup and os.path.isdir(outname):
                log.info('deleting temporary files')
                shutil.rmtree(outname, onerror=windows_fileprefix)
        log.info('done')
    if returnWF:
        return wf_name


def noise_power(infile, outdir, polarizations, spacing, t_srs, refarea='sigma0', tmpdir=None, test=False, cleanup=True,
                demName='SRTM 1Sec HGT', externalDEMFile=None, externalDEMNoDataValue=None, externalDEMApplyEGM=True,
                alignToStandardGrid=False, standardGridOriginX=0, standardGridOriginY=0, groupsize=1,
                clean_edges=False, clean_edges_npixels=1, rlks=None, azlks=None):
    """
    Generate Sentinel-1 noise power images for each polarization, calibrated to either beta, sigma or gamma nought.
    The written GeoTIFF files will carry the suffix NEBZ, NESZ or NEGZ respectively.

    Parameters
    ----------
    infile: str
        The SAR scene(s) to be processed
    outdir: str
        The directory to write the final files to.
    polarizations: list[str]
        The polarizations to be processed, e.g. ['VV', 'VH'].
    spacing: int or float
        The target pixel spacing in meters.
    t_srs: int or str or osr.SpatialReference
        A target geographic reference system in WKT, EPSG, PROJ4 or OPENGIS format.
    refarea: str
        either 'beta0', 'gamma0' or 'sigma0'.
    tmpdir: str
        Path of custom temporary directory, useful to separate output folder and temp folder. If `None`, the `outdir`
        location will be used. The created subdirectory will be deleted after processing if ``cleanup=True``.
    test: bool
        If set to True the workflow xml file is only written and not executed. Default is False.
    cleanup: bool
        Should all files written to the temporary directory during function execution be deleted after processing?
        Default is True.
    demName: str
        The name of the auto-download DEM. Default is 'SRTM 1Sec HGT'. Is ignored when `externalDEMFile` is not None.
        Supported options:
        
         - ACE2_5Min
         - ACE30
         - ASTER 1sec GDEM
         - CDEM
         - Copernicus 30m Global DEM
         - Copernicus 90m Global DEM
         - GETASSE30
         - SRTM 1Sec Grid
         - SRTM 1Sec HGT
         - SRTM 3Sec
    externalDEMFile: str or None, optional
        The absolute path to an external DEM file. Default is None. Overrides `demName`.
    externalDEMNoDataValue: int, float or None, optional
        The no data value of the external DEM. If not specified (default) the function will try to read it from the
        specified external DEM.
    externalDEMApplyEGM: bool, optional
        Apply Earth Gravitational Model to external DEM? Default is True.
    alignToStandardGrid: bool
        Align all processed images to a common grid?
    standardGridOriginX: int or float
        The x origin value for grid alignment
    standardGridOriginY: int or float
        The y origin value for grid alignment
    groupsize: int
        The number of workers executed together in one gpt call.
    clean_edges: bool
        erode noisy image edges? See :func:`pyroSAR.snap.auxil.erode_edges`.
        Does not apply to layover-shadow mask.
    clean_edges_npixels: int
        the number of pixels to erode.
    rlks: int or None
        the number of range looks. If not None, overrides the computation done by function
        :func:`pyroSAR.ancillary.multilook_factors` based on the image pixel spacing and the target spacing.
    azlks: int or None
        the number of azimuth looks. Like `rlks`.
    
    Returns
    -------

    """
    if clean_edges:
        try:
            import scipy
        except ImportError:
            raise RuntimeError('please install scipy to clean edges')
    
    if refarea not in ['beta0', 'sigma0', 'gamma0']:
        raise ValueError('refarea not supported')
    
    id = identify(infile)
    
    if id.sensor not in ['S1A', 'S1B']:
        raise RuntimeError('this function is for Sentinel-1 only')
    
    os.makedirs(outdir, exist_ok=True)
    if tmpdir is not None:
        os.makedirs(tmpdir, exist_ok=True)
    
    wf = parse_recipe('blank')
    
    read = parse_node('Read')
    read.parameters['file'] = infile
    wf.insert_node(read)
    ############################################
    orb = orb_parametrize(scene=id, workflow=wf, before=read.id,
                          formatName='SENTINEL-1', allow_RES_OSV=True)
    ############################################
    cal = parse_node('Calibration')
    wf.insert_node(cal, before=orb.id)
    cal.parameters['selectedPolarisations'] = polarizations
    cal.parameters['outputBetaBand'] = False
    cal.parameters['outputSigmaBand'] = False
    cal.parameters['outputGammaBand'] = False
    
    inband = refarea.capitalize()
    cal.parameters['output{}Band'.format(inband[:-1])] = True
    
    tnr = parse_node('ThermalNoiseRemoval')
    wf.insert_node(tnr, before=cal.id)
    last = tnr
    ############################################
    if id.product == 'SLC':
        deb = parse_node('TOPSAR-Deburst')
        wf.insert_node(deb, before=tnr.id)
        last = deb
    ############################################
    select = parse_node('BandSelect')
    wf.insert_node(select, before=last.id)
    measure = 'NE{}Z'.format(refarea.capitalize()[0])
    bands = ['{}_{}'.format(measure, pol) for pol in polarizations]
    select.parameters['sourceBands'] = bands
    last = select
    ############################################
    # Multilook node configuration
    
    try:
        image_geometry = id.meta['image_geometry']
        incidence = id.meta['incidence']
    except KeyError:
        raise RuntimeError('This function does not yet support sensor {}'.format(id.sensor))
    
    if rlks is None and azlks is None:
        rlks, azlks = multilook_factors(source_rg=id.spacing[0],
                                        source_az=id.spacing[1],
                                        target=spacing,
                                        geometry=image_geometry,
                                        incidence=incidence)
    if [rlks, azlks].count(None) > 0:
        raise RuntimeError("'rlks' and 'azlks' must either both be integers or None")
    
    if azlks > 1 or rlks > 1:
        wf.insert_node(parse_node('Multilook'), before=last.id)
        ml = wf['Multilook']
        ml.parameters['nAzLooks'] = azlks
        ml.parameters['nRgLooks'] = rlks
        ml.parameters['sourceBands'] = None
        last = ml
    ############################################
    tc = parse_node('Terrain-Correction')
    wf.insert_node(tc, before=last.id)
    last = tc
    
    tc.parameters['demResamplingMethod'] = 'BILINEAR_INTERPOLATION'
    tc.parameters['imgResamplingMethod'] = 'BILINEAR_INTERPOLATION'
    tc.parameters['alignToStandardGrid'] = alignToStandardGrid
    tc.parameters['standardGridOriginX'] = standardGridOriginX
    tc.parameters['standardGridOriginY'] = standardGridOriginY
    
    # specify spatial resolution and coordinate reference system of the output dataset
    tc.parameters['pixelSpacingInMeter'] = spacing
    
    try:
        # try to convert the CRS into EPSG code (for readability in the workflow XML)
        t_srs = crsConvert(t_srs, 'epsg')
    except TypeError:
        raise RuntimeError("format of parameter 't_srs' not recognized")
    except RuntimeError:
        # this error can occur when the CRS does not have a corresponding EPSG code
        # in this case the original CRS representation is written to the workflow
        pass
    
    # the EPSG code 4326 is not supported by SNAP and thus the WKT string has to be defined;
    # in all other cases defining EPSG:{code} will do
    if t_srs == 4326:
        t_srs = 'GEOGCS["WGS84(DD)",' \
                'DATUM["WGS84",' \
                'SPHEROID["WGS84", 6378137.0, 298.257223563]],' \
                'PRIMEM["Greenwich", 0.0],' \
                'UNIT["degree", 0.017453292519943295],' \
                'AXIS["Geodetic longitude", EAST],' \
                'AXIS["Geodetic latitude", NORTH]]'
    
    if isinstance(t_srs, int):
        t_srs = 'EPSG:{}'.format(t_srs)
    
    tc.parameters['mapProjection'] = t_srs
    
    # select DEM type
    dempar = {'externalDEMFile': externalDEMFile,
              'externalDEMApplyEGM': externalDEMApplyEGM}
    if externalDEMFile is not None:
        if os.path.isfile(externalDEMFile):
            if externalDEMNoDataValue is None:
                with Raster(externalDEMFile) as dem:
                    dempar['externalDEMNoDataValue'] = dem.nodata
                if dempar['externalDEMNoDataValue'] is None:
                    raise RuntimeError('Cannot read NoData value from DEM file. '
                                       'Please specify externalDEMNoDataValue')
            else:
                dempar['externalDEMNoDataValue'] = externalDEMNoDataValue
            dempar['reGridMethod'] = False
        else:
            raise RuntimeError('specified externalDEMFile does not exist')
        dempar['demName'] = 'External DEM'
    else:
        dempar['demName'] = demName
        dempar['externalDEMFile'] = None
        dempar['externalDEMNoDataValue'] = 0
    
    for key, value in dempar.items():
        wf.set_par(key, value)
    
    # download the EGM lookup table if necessary
    if dempar['externalDEMApplyEGM']:
        get_egm_lookup(geoid='EGM96', software='SNAP')
    ############################################
    
    suffix = wf.suffix()
    if tmpdir is None:
        tmpdir = outdir
    basename = id.outname_base() + '_' + suffix
    procdir = os.path.join(tmpdir, basename)
    outname = os.path.join(procdir, basename + '.dim')
    
    write = parse_node('Write')
    wf.insert_node(write, before=last.id)
    write.parameters['file'] = outname
    write.parameters['formatName'] = 'BEAM-DIMAP'
    
    wf_name = os.path.join(outdir, basename + '_proc.xml')
    wf.write(wf_name)
    
    if not test:
        groups = groupbyWorkers(wf_name, groupsize)
        gpt(xmlfile=wf_name, tmpdir=procdir, groups=groups, cleanup=cleanup)
        writer(xmlfile=wf_name, outdir=outdir, clean_edges=clean_edges,
               clean_edges_npixels=clean_edges_npixels)
        if cleanup:
            if os.path.isdir(procdir):
                shutil.rmtree(procdir, onerror=windows_fileprefix)
