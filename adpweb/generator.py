
import sys
import pprint
import os
import jinja2
import webbrowser


current_dir = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(current_dir, 'templates')

env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))
template = env.get_template('report.html')

datasets_test = [{'input_data': 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor.fits',
  'status': 'error',
  'softwares': [{'software_id': 'SoFiA-2',
                 'mode': 'absorption',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_logfile.log',
                 'log_content': '____________________________________________________________________________\n'
                                '\n'
                                ' Pipeline started\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Software:  Source Finding Application (SoFiA)\n'
                                '  Version:   2.6.14 (2025-05-14)\n'
                                '  CPU:       12 threads available\n'
                                '  Memory:    12.7 GB total / 6.6 GB free\n'
                                '  Date:      2025-09-04\n'
                                '  Time:      08:16:58 h\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading parameter settings\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Activating SoFiA default parameter settings.\n'
                                '  Loading user-specified parameters.\n'
                                '  - Loading user parameter file: '
                                '/home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID5619.par\n'
                                '  Using 3 out of 12 available CPU threads.\n'
                                '\n'
                                'WARNING: '
                                '┌──────────────────────────────────────────────────────────┐\n'
                                '         │ You have set parameter.physical = true. SoFiA will '
                                'try   │\n'
                                '         │ to convert some parameters to physical units under '
                                'the   │\n'
                                '         │ following fundamental '
                                'assumptions:                       │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The beam information in the FITS header (BMAJ, '
                                'BMIN)  │\n'
                                '         │    is correct and accurate across the entire data '
                                'cube.  │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The spectral channels of the data cube are '
                                'uncorrela- │\n'
                                '         │    ted, i.e. spectral resolution equals channel '
                                'width.   │\n'
                                '         '
                                '│                                                          │\n'
                                '         │ Should any of these assumptions be incorrect then '
                                'the    │\n'
                                '         │ measurement of \n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading data cube\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Opening FITS file '
                                "'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor.fits'.\n"
                                '  Reading FITS data with the following specifications:\n'
                                '    Data type:    -32\n'
                                '    No. of axes:  4\n'
                                '    Axis sizes:   350, 350, 118\n'
                                '    Region:       0-349, 0-349, 0-117\n'
                                '    Memory used:  55.1 MB\n'
                                '  Searching for values of infinity.\n'
                                '    No infinite data values found.\n'
                                '  Inverting data cube\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring global noise level\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Global RMS:  3.947e-04  (using stride of 14)\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running S+C finder\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using the following parameters:\n'
                                '  - Kernels\n'
                                '    - spatial:        0, 3, 6, 9\n'
                                '    - spectral:       0, 3, 7, 15\n'
                                '  - Flux threshold:   3.8 * rms\n'
                                '  - Noise statistic:  median absolute deviation\n'
                                '  - Flux range:       negative\n'
                                '\n'
                                '  Using a stride of 14 in noise measurement.\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [0]\n'
                                '  Noise level:       3.947e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [3]\n'
                                '  Noise level:       3.165e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [7]\n'
                                '  Noise level:       2.140e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [15]\n'
                                '  Noise level:       1.374e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [0]\n'
                                '  Noise level:       2.875e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [3]\n'
                                '  Noise level:       2.296e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:03 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [7]\n'
                                '  Noise level:       1.549e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:03 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [15]\n'
                                '  Noise level:       9.927e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [0]\n'
                                '  Noise level:       1.949e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [3]\n'
                                '  Noise level:       1.560e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [7]\n'
                                '  Noise level:       1.064e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [15]\n'
                                '  Noise level:       6.777e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [0]\n'
                                '  Noise level:       1.200e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [3]\n'
                                '  Noise level:       9.727e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [7]\n'
                                '  Noise level:       6.659e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [15]\n'
                                '  Noise level:       4.286e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating source mask\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  340062 pixels detected by source finder (2.353%).\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running Linker\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Linker settings:\n'
                                '   - Merging radii:   2, 2, 3\n'
                                '   - Minimum size:    5 x 5 x 5\n'
                                '   - Min/max fill:    5.0%, 0.0%\n'
                                '   - Keep negative:   yes\n'
                                '\n'
                                '  Linker status:\n'
                                '   - No. of objects:  335\n'
                                '   - Memory usage:    44.82 kB\n'
                                '\n'
                                '\n'
                                '  Elapsed time: 00:00:05 h\n'
                                '  CPU time:     00:00:08 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring reliability\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using 3D parameter space:\n'
                                '   - peak\n'
                                '   - sum\n'
                                '   - mean\n'
                                '  Found 164 positive and 171 negative sources.\n'
                                '  Retaining all negative detections.\n'
                                '  Using auto-kernel feature.\n'
                                '    Iter.  1: kernel = 0.100, median = 1.000\n'
                                '    Iter.  2: kernel = 0.200, median = 0.860\n'
                                '    Iter.  3: kernel = 0.300, median = 0.655\n'
                                '    Iter.  4: kernel = 0.400, median = 0.585\n'
                                '    Iter.  5: kernel = 0.500, median = 0.438\n'
                                '    Iter.  6: kernel = 0.540, median = 0.382\n'
                                '    Iter.  7: kernel = 0.580, median = 0.340\n'
                                '    Iter.  8: kernel = 0.620, median = 0.288\n'
                                '    Iter.  9: kernel = 0.660, median = 0.250\n'
                                '    Iter. 10: kernel = 0.700, median = 0.224\n'
                                '    Iter. 11: kernel = 0.740, median = 0.171\n'
                                '    Iter. 12: kernel = 0.780, median = 0.144\n'
                                '    Iter. 13: kernel = 0.820, median = 0.121\n'
                                '    Iter. 14: kernel = 0.860, median = 0.093\n'
                                '    Iter. 15: kernel = 0.900, median = 0.078\n'
                                '    Iter. 16: kernel = 0.940, median = 0.069\n'
                                '    Iter. 17: kernel = 0.980, median = 0.062\n'
                                '    Iter. 18: kernel = 1.020, median = 0.057\n'
                                '    Iter. 19: kernel = 1.060, median = 0.042\n'
                                '  Converged to scale_kernel = 1.060 after 19 iterations.\n'
                                '  \n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_rel.eps\n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_skellam.eps\n'
                                '\n'
                                'ERROR: No reliable sources found. Terminating pipeline.\n'
                                '       Terminating with error code 8.\n'
                                '\n',
                 'error': "Command '['sofia', "
                          "'/home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID5619.par']' "
                          'returned non-zero exit status 8.',
                 'sw_status': 'error',
                 'sofia_par_changes': {'pipeline.threads': '3',
                                       'input.data': 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor.fits',
                                       'input.invert': 'true',
                                       'output.directory': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption'},
                 'sofia_parfile': '# SoFiA 2 parameter file for the official SoFiA test datacube\n'
                                  '\n'
                                  '\n'
                                  '# Global settings\n'
                                  '\n'
                                  'pipeline.verbose           =  false\n'
                                  'pipeline.pedantic          =  true\n'
                                  'pipeline.threads           =  0\n'
                                  '\n'
                                  '\n'
                                  '# Input\n'
                                  '\n'
                                  'input.data                 =  sofia_test_datacube.test\n'
                                  'input.primaryBeam          =  \n'
                                  'input.region               =  \n'
                                  'input.gain                 =  \n'
                                  'input.noise                =  \n'
                                  'input.weights              =  \n'
                                  'input.mask                 =  \n'
                                  'input.invert               =  falseee\n'
                                  '\n'
                                  '\n'
                                  '# Flagging\n'
                                  '\n'
                                  'flag.region                =  \n'
                                  'flag.catalog               =  \n'
                                  'flag.radius                =  5\n'
                                  'flag.auto                  =  false\n'
                                  'flag.threshold             =  5.0\n'
                                  'flag.log                   =  false\n'
                                  'flag.cube                  =  \n'
                                  '\n'
                                  '\n'
                                  '# Continuum subtraction\n'
                                  '\n'
                                  'contsub.enable             =  false\n'
                                  'contsub.order              =  0\n'
                                  'contsub.threshold          =  2.0\n'
                                  'contsub.shift              =  4\n'
                                  'contsub.padding            =  3\n'
                                  '\n'
                                  '\n'
                                  '# Noise scaling\n'
                                  '\n'
                                  'scaleNoise.enable          =  false\n'
                                  'scaleNoise.mode            =  local\n'
                                  'scaleNoise.statistic       =  mad\n'
                                  'scaleNoise.fluxRange       =  negative\n'
                                  'scaleNoise.windowXY        =  31\n'
                                  'scaleNoise.windowZ         =  31\n'
                                  'scaleNoise.gridXY          =  0\n'
                                  'scaleNoise.gridZ           =  0\n'
                                  'scaleNoise.interpolate     =  false\n'
                                  'scaleNoise.scfind          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Ripple filter\n'
                                  '\n'
                                  'rippleFilter.enable        =  false\n'
                                  'rippleFilter.statistic     =  median\n'
                                  'rippleFilter.windowXY      =  31\n'
                                  'rippleFilter.windowZ       =  15\n'
                                  'rippleFilter.gridXY        =  0\n'
                                  'rippleFilter.gridZ         =  0\n'
                                  'rippleFilter.interpolate   =  false\n'
                                  '\n'
                                  '\n'
                                  '# S+C finder\n'
                                  '\n'
                                  'scfind.enable              =  true\n'
                                  'scfind.kernelsXY           =  0, 3, 6, 9\n'
                                  'scfind.kernelsZ            =  0, 3, 7, 15\n'
                                  'scfind.threshold           =  3.8\n'
                                  'scfind.replacement         =  2.0\n'
                                  'scfind.statistic           =  mad\n'
                                  'scfind.fluxRange           =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Threshold finder\n'
                                  '\n'
                                  'threshold.enable           =  false\n'
                                  'threshold.threshold        =  5.0\n'
                                  'threshold.mode             =  relative\n'
                                  'threshold.statistic        =  mad\n'
                                  'threshold.fluxRange        =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Linker\n'
                                  '\n'
                                  'linker.enable              =  true\n'
                                  'linker.radiusXY            =  2\n'
                                  'linker.radiusZ             =  3\n'
                                  'linker.minSizeXY           =  5\n'
                                  'linker.minSizeZ            =  5\n'
                                  'linker.maxSizeXY           =  0\n'
                                  'linker.maxSizeZ            =  0\n'
                                  'linker.minPixels           =  0\n'
                                  'linker.maxPixels           =  0\n'
                                  'linker.minFill             =  0.05\n'
                                  'linker.maxFill             =  0.0\n'
                                  'linker.positivity          =  false\n'
                                  'linker.keepNegative        =  false\n'
                                  '\n'
                                  '\n'
                                  '# Reliability\n'
                                  '\n'
                                  'reliability.enable         =  true\n'
                                  'reliability.parameters     =  peak, sum, mean\n'
                                  'reliability.threshold      =  0.9\n'
                                  'reliability.scaleKernel    =  0.3\n'
                                  'reliability.minSNR         =  6.0\n'
                                  'reliability.minPixels      =  150\n'
                                  'reliability.autoKernel     =  true\n'
                                  'reliability.iterations     =  50\n'
                                  'reliability.tolerance      =  0.05\n'
                                  'reliability.catalog        =  \n'
                                  'reliability.plot           =  true\n'
                                  'reliability.plotExtra      =  false\n'
                                  'reliability.debug          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Mask dilation\n'
                                  '\n'
                                  'dilation.enable            =  false\n'
                                  'dilation.iterationsXY      =  10\n'
                                  'dilation.iterationsZ       =  5\n'
                                  'dilation.threshold         =  0.001\n'
                                  '\n'
                                  '\n'
                                  '# Parameterisation\n'
                                  '\n'
                                  'parameter.enable           =  true\n'
                                  'parameter.wcs              =  true\n'
                                  'parameter.physical         =  true\n'
                                  'parameter.prefix           =  SoFiA\n'
                                  'parameter.offset           =  false\n'
                                  '\n'
                                  '\n'
                                  '# Output\n'
                                  '\n'
                                  'output.directory           =  \n'
                                  'output.filename            =  \n'
                                  'output.writeCatASCII       =  true\n'
                                  'output.writeCatXML         =  true\n'
                                  'output.writeCatSQL         =  false\n'
                                  'output.writeKarma          =  false\n'
                                  'output.writeNoise          =  false\n'
                                  'output.writeFiltered       =  false\n'
                                  'output.writeMask           =  true\n'
                                  'output.writeMask2d         =  true\n'
                                  'output.writeRawMask        =  false\n'
                                  'output.writeMoments        =  true\n'
                                  'output.writeCubelets       =  true\n'
                                  'output.writePV             =  true\n'
                                  'output.marginAperSpec      =  10\n'
                                  'output.marginCubelets      =  10\n'
                                  'output.thresholdMom12      =  0.0\n'
                                  'output.overwrite           =  true\n',
                 'command': ''},
                {'software_id': 'SoFiA-2',
                 'mode': 'emission',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_logfile.log',
                 'log_content': '____________________________________________________________________________\n'
                                '\n'
                                ' Pipeline started\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Software:  Source Finding Application (SoFiA)\n'
                                '  Version:   2.6.14 (2025-05-14)\n'
                                '  CPU:       12 threads available\n'
                                '  Memory:    12.7 GB total / 5.0 GB free\n'
                                '  Date:      2025-09-04\n'
                                '  Time:      08:17:03 h\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading parameter settings\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Activating SoFiA default parameter settings.\n'
                                '  Loading user-specified parameters.\n'
                                '  - Loading user parameter file: '
                                '/home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID5619.par\n'
                                '  Using 3 out of 12 available CPU threads.\n'
                                '\n'
                                'WARNING: '
                                '┌──────────────────────────────────────────────────────────┐\n'
                                '         │ You have set parameter.physical = true. SoFiA will '
                                'try   │\n'
                                '         │ to convert some parameters to physical units under '
                                'the   │\n'
                                '         │ following fundamental '
                                'assumptions:                       │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The beam information in the FITS header (BMAJ, '
                                'BMIN)  │\n'
                                '         │    is correct and accurate across the entire data '
                                'cube.  │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The spectral channels of the data cube are '
                                'uncorrela- │\n'
                                '         │    ted, i.e. spectral resolution equals channel '
                                'width.   │\n'
                                '         '
                                '│                                                          │\n'
                                '         │ Should any of these assumptions be incorrect then '
                                'the    │\n'
                                '         │ measurement of \n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading data cube\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Opening FITS file '
                                "'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor.fits'.\n"
                                '  Reading FITS data with the following specifications:\n'
                                '    Data type:    -32\n'
                                '    No. of axes:  4\n'
                                '    Axis sizes:   350, 350, 118\n'
                                '    Region:       0-349, 0-349, 0-117\n'
                                '    Memory used:  55.1 MB\n'
                                '  Searching for values of infinity.\n'
                                '    No infinite data values found.\n'
                                '\n'
                                '  Elapsed time: 00:00:00 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring global noise level\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Global RMS:  3.933e-04  (using stride of 14)\n'
                                '\n'
                                '  Elapsed time: 00:00:00 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running S+C finder\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using the following parameters:\n'
                                '  - Kernels\n'
                                '    - spatial:        0, 3, 6, 9\n'
                                '    - spectral:       0, 3, 7, 15\n'
                                '  - Flux threshold:   3.8 * rms\n'
                                '  - Noise statistic:  median absolute deviation\n'
                                '  - Flux range:       negative\n'
                                '\n'
                                '  Using a stride of 14 in noise measurement.\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [0]\n'
                                '  Noise level:       3.933e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:00 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [3]\n'
                                '  Noise level:       3.149e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:00 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [7]\n'
                                '  Noise level:       2.152e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [15]\n'
                                '  Noise level:       1.380e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [0]\n'
                                '  Noise level:       2.868e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [3]\n'
                                '  Noise level:       2.289e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [7]\n'
                                '  Noise level:       1.556e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:03 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [15]\n'
                                '  Noise level:       1.001e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [0]\n'
                                '  Noise level:       1.947e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [3]\n'
                                '  Noise level:       1.561e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [7]\n'
                                '  Noise level:       1.053e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [15]\n'
                                '  Noise level:       6.792e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [0]\n'
                                '  Noise level:       1.206e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [3]\n'
                                '  Noise level:       9.713e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [7]\n'
                                '  Noise level:       6.576e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:08 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [15]\n'
                                '  Noise level:       4.225e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:08 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating source mask\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  340830 pixels detected by source finder (2.358%).\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:08 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running Linker\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Linker settings:\n'
                                '   - Merging radii:   2, 2, 3\n'
                                '   - Minimum size:    5 x 5 x 5\n'
                                '   - Min/max fill:    5.0%, 0.0%\n'
                                '   - Keep negative:   yes\n'
                                '\n'
                                '  Linker status:\n'
                                '   - No. of objects:  338\n'
                                '   - Memory usage:    45.22 kB\n'
                                '\n'
                                '\n'
                                '  Elapsed time: 00:00:05 h\n'
                                '  CPU time:     00:00:09 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring reliability\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using 3D parameter space:\n'
                                '   - peak\n'
                                '   - sum\n'
                                '   - mean\n'
                                '  Found 173 positive and 165 negative sources.\n'
                                '  Retaining all negative detections.\n'
                                '  Using auto-kernel feature.\n'
                                '    Iter.  1: kernel = 0.100, median = 0.990\n'
                                '    Iter.  2: kernel = 0.200, median = 0.749\n'
                                '    Iter.  3: kernel = 0.300, median = 0.563\n'
                                '    Iter.  4: kernel = 0.400, median = 0.459\n'
                                '    Iter.  5: kernel = 0.440, median = 0.396\n'
                                '    Iter.  6: kernel = 0.480, median = 0.323\n'
                                '    Iter.  7: kernel = 0.520, median = 0.284\n'
                                '    Iter.  8: kernel = 0.560, median = 0.232\n'
                                '    Iter.  9: kernel = 0.600, median = 0.204\n'
                                '    Iter. 10: kernel = 0.640, median = 0.169\n'
                                '    Iter. 11: kernel = 0.680, median = 0.163\n'
                                '    Iter. 12: kernel = 0.720, median = 0.146\n'
                                '    Iter. 13: kernel = 0.760, median = 0.130\n'
                                '    Iter. 14: kernel = 0.800, median = 0.128\n'
                                '    Iter. 15: kernel = 0.840, median = 0.111\n'
                                '    Iter. 16: kernel = 0.880, median = 0.091\n'
                                '    Iter. 17: kernel = 0.920, median = 0.083\n'
                                '    Iter. 18: kernel = 0.960, median = 0.072\n'
                                '    Iter. 19: kernel = 1.000, median = 0.062\n'
                                '    Iter. 20: kernel = 1.040, median = 0.049\n'
                                '  Converged to scale_kernel = 1.040 after 20 iterations.\n'
                                '  \n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_rel.eps\n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_skellam.eps\n'
                                '\n'
                                'ERROR: No reliable sources found. Terminating pipeline.\n'
                                '       Terminating with error code 8.\n'
                                '\n',
                 'error': "Command '['sofia', "
                          "'/home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID5619.par']' "
                          'returned non-zero exit status 8.',
                 'sw_status': 'error',
                 'sofia_par_changes': {'pipeline.threads': '3',
                                       'input.invert': 'false',
                                       'output.directory': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission',
                                       'input.data': 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor.fits'},
                 'sofia_parfile': '# SoFiA 2 parameter file for the official SoFiA test datacube\n'
                                  '\n'
                                  '\n'
                                  '# Global settings\n'
                                  '\n'
                                  'pipeline.verbose           =  false\n'
                                  'pipeline.pedantic          =  true\n'
                                  'pipeline.threads           =  0\n'
                                  '\n'
                                  '\n'
                                  '# Input\n'
                                  '\n'
                                  '#input.data                 =  sofia_test_datacube.test\n'
                                  '#input.primaryBeam          =  \n'
                                  'input.region               =  \n'
                                  'input.gain                 =  \n'
                                  'input.noise                =  \n'
                                  'input.weights              =  \n'
                                  'input.mask                 =  \n'
                                  'input.invert               =   \n'
                                  '\n'
                                  '\n'
                                  '# Flagging\n'
                                  '\n'
                                  'flag.region                =  \n'
                                  'flag.catalog               =  \n'
                                  'flag.radius                =  5\n'
                                  'flag.auto                  =  false\n'
                                  'flag.threshold             =  5.0\n'
                                  'flag.log                   =  false\n'
                                  'flag.cube                  =  \n'
                                  '\n'
                                  '\n'
                                  '# Continuum subtraction\n'
                                  '\n'
                                  'contsub.enable             =  false\n'
                                  'contsub.order              =  0\n'
                                  'contsub.threshold          =  2.0\n'
                                  'contsub.shift              =  4\n'
                                  'contsub.padding            =  3\n'
                                  '\n'
                                  '\n'
                                  '# Noise scaling\n'
                                  '\n'
                                  'scaleNoise.enable          =  false\n'
                                  'scaleNoise.mode            =  local\n'
                                  'scaleNoise.statistic       =  mad\n'
                                  'scaleNoise.fluxRange       =  negative\n'
                                  'scaleNoise.windowXY        =  31\n'
                                  'scaleNoise.windowZ         =  31\n'
                                  'scaleNoise.gridXY          =  0\n'
                                  'scaleNoise.gridZ           =  0\n'
                                  'scaleNoise.interpolate     =  false\n'
                                  'scaleNoise.scfind          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Ripple filter\n'
                                  '\n'
                                  'rippleFilter.enable        =  false\n'
                                  'rippleFilter.statistic     =  median\n'
                                  'rippleFilter.windowXY      =  31\n'
                                  'rippleFilter.windowZ       =  15\n'
                                  'rippleFilter.gridXY        =  0\n'
                                  'rippleFilter.gridZ         =  0\n'
                                  'rippleFilter.interpolate   =  false\n'
                                  '\n'
                                  '\n'
                                  '# S+C finder\n'
                                  '\n'
                                  'scfind.enable              =  true\n'
                                  'scfind.kernelsXY           =  0, 3, 6, 9\n'
                                  'scfind.kernelsZ            =  0, 3, 7, 15\n'
                                  'scfind.threshold           =  3.8\n'
                                  'scfind.replacement         =  2.0\n'
                                  'scfind.statistic           =  mad\n'
                                  'scfind.fluxRange           =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Threshold finder\n'
                                  '\n'
                                  'threshold.enable           =  false\n'
                                  'threshold.threshold        =  5.0\n'
                                  'threshold.mode             =  relative\n'
                                  'threshold.statistic        =  mad\n'
                                  'threshold.fluxRange        =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Linker\n'
                                  '\n'
                                  'linker.enable              =  true\n'
                                  'linker.radiusXY            =  2\n'
                                  'linker.radiusZ             =  3\n'
                                  'linker.minSizeXY           =  5\n'
                                  'linker.minSizeZ            =  5\n'
                                  'linker.maxSizeXY           =  0\n'
                                  'linker.maxSizeZ            =  0\n'
                                  'linker.minPixels           =  0\n'
                                  'linker.maxPixels           =  0\n'
                                  'linker.minFill             =  0.05\n'
                                  'linker.maxFill             =  0.0\n'
                                  'linker.positivity          =  false\n'
                                  'linker.keepNegative        =  false\n'
                                  '\n'
                                  '\n'
                                  '# Reliability\n'
                                  '\n'
                                  'reliability.enable         =  true\n'
                                  'reliability.parameters     =  peak, sum, mean\n'
                                  'reliability.threshold      =  0.9\n'
                                  'reliability.scaleKernel    =  0.3\n'
                                  'reliability.minSNR         =  6.0\n'
                                  'reliability.minPixels      =  150\n'
                                  'reliability.autoKernel     =  true\n'
                                  'reliability.iterations     =  50\n'
                                  'reliability.tolerance      =  0.05\n'
                                  'reliability.catalog        =  \n'
                                  'reliability.plot           =  true\n'
                                  'reliability.plotExtra      =  false\n'
                                  'reliability.debug          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Mask dilation\n'
                                  '\n'
                                  'dilation.enable            =  false\n'
                                  'dilation.iterationsXY      =  10\n'
                                  'dilation.iterationsZ       =  5\n'
                                  'dilation.threshold         =  0.001\n'
                                  '\n'
                                  '\n'
                                  '# Parameterisation\n'
                                  '\n'
                                  'parameter.enable           =  true\n'
                                  'parameter.wcs              =  true\n'
                                  'parameter.physical         =  true\n'
                                  'parameter.prefix           =  SoFiA\n'
                                  'parameter.offset           =  false\n'
                                  '\n'
                                  '\n'
                                  '# Output\n'
                                  '\n'
                                  'output.directory           =  \n'
                                  'output.filename            =  \n'
                                  'output.writeCatASCII       =  true\n'
                                  'output.writeCatXML         =  true\n'
                                  'output.writeCatSQL         =  false\n'
                                  'output.writeKarma          =  false\n'
                                  'output.writeNoise          =  false\n'
                                  'output.writeFiltered       =  false\n'
                                  'output.writeMask           =  true\n'
                                  'output.writeMask2d         =  true\n'
                                  'output.writeRawMask        =  false\n'
                                  'output.writeMoments        =  true\n'
                                  'output.writeCubelets       =  true\n'
                                  'output.writePV             =  true\n'
                                  'output.marginAperSpec      =  10\n'
                                  'output.marginCubelets      =  10\n'
                                  'output.thresholdMom12      =  0.0\n'
                                  'output.overwrite           =  true\n',
                 'command': ''},
                {'software_id': 'SIP',
                 'mode': 'absorption',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_sip.log',
                 'log_content': 'No log file available: '
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_sip.log',
                 'error': 'No valid .txt or .xml catalog for SIP found within the  '
                          '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption  directory.',
                 'sw_status': 'error',
                 'sofia_par_changes': {},
                 'sofia_parfile': 'No log file available: ',
                 'command': ''},
                {'software_id': 'SIP',
                 'mode': 'emission',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_sip.log',
                 'log_content': 'No log file available: '
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_sip.log',
                 'error': 'No valid .txt or .xml catalog for SIP found within the  '
                          '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission  directory.',
                 'sw_status': 'error',
                 'sofia_par_changes': {},
                 'sofia_parfile': 'No log file available: ',
                 'command': ''}],
  'images': [],
  'images_grouped': {'sofia': {'absorption': [], 'emission': []},
                     'sip': {'absorption': {}, 'emission': {}},
                     'qa': []}},
 {'input_data': 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor.fits',
  'status': 'error',
  'softwares': [{'software_id': 'SoFiA-2',
                 'mode': 'absorption',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_logfile.log',
                 'log_content': '____________________________________________________________________________\n'
                                '\n'
                                ' Pipeline started\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Software:  Source Finding Application (SoFiA)\n'
                                '  Version:   2.6.14 (2025-05-14)\n'
                                '  CPU:       12 threads available\n'
                                '  Memory:    12.7 GB total / 6.6 GB free\n'
                                '  Date:      2025-09-04\n'
                                '  Time:      08:16:58 h\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading parameter settings\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Activating SoFiA default parameter settings.\n'
                                '  Loading user-specified parameters.\n'
                                '  - Loading user parameter file: '
                                '/home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID5620.par\n'
                                '  Using 3 out of 12 available CPU threads.\n'
                                '\n'
                                'WARNING: '
                                '┌──────────────────────────────────────────────────────────┐\n'
                                '         │ You have set parameter.physical = true. SoFiA will '
                                'try   │\n'
                                '         │ to convert some parameters to physical units under '
                                'the   │\n'
                                '         │ following fundamental '
                                'assumptions:                       │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The beam information in the FITS header (BMAJ, '
                                'BMIN)  │\n'
                                '         │    is correct and accurate across the entire data '
                                'cube.  │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The spectral channels of the data cube are '
                                'uncorrela- │\n'
                                '         │    ted, i.e. spectral resolution equals channel '
                                'width.   │\n'
                                '         '
                                '│                                                          │\n'
                                '         │ Should any of these assumptions be incorrect then '
                                'the    │\n'
                                '         │ measurement of \n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading data cube\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Opening FITS file '
                                "'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor.fits'.\n"
                                '  Reading FITS data with the following specifications:\n'
                                '    Data type:    -32\n'
                                '    No. of axes:  4\n'
                                '    Axis sizes:   350, 350, 118\n'
                                '    Region:       0-349, 0-349, 0-117\n'
                                '    Memory used:  55.1 MB\n'
                                '  Searching for values of infinity.\n'
                                '    No infinite data values found.\n'
                                '  Inverting data cube\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring global noise level\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Global RMS:  4.146e-04  (using stride of 14)\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running S+C finder\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using the following parameters:\n'
                                '  - Kernels\n'
                                '    - spatial:        0, 3, 6, 9\n'
                                '    - spectral:       0, 3, 7, 15\n'
                                '  - Flux threshold:   3.8 * rms\n'
                                '  - Noise statistic:  median absolute deviation\n'
                                '  - Flux range:       negative\n'
                                '\n'
                                '  Using a stride of 14 in noise measurement.\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [0]\n'
                                '  Noise level:       4.146e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [3]\n'
                                '  Noise level:       3.304e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [7]\n'
                                '  Noise level:       2.238e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [15]\n'
                                '  Noise level:       1.431e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [0]\n'
                                '  Noise level:       3.036e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [3]\n'
                                '  Noise level:       2.415e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [7]\n'
                                '  Noise level:       1.627e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:03 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [15]\n'
                                '  Noise level:       1.044e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:03 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [0]\n'
                                '  Noise level:       2.065e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [3]\n'
                                '  Noise level:       1.644e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [7]\n'
                                '  Noise level:       1.105e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [15]\n'
                                '  Noise level:       7.082e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [0]\n'
                                '  Noise level:       1.287e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [3]\n'
                                '  Noise level:       1.032e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [7]\n'
                                '  Noise level:       6.898e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [15]\n'
                                '  Noise level:       4.467e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating source mask\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  362741 pixels detected by source finder (2.509%).\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running Linker\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Linker settings:\n'
                                '   - Merging radii:   2, 2, 3\n'
                                '   - Minimum size:    5 x 5 x 5\n'
                                '   - Min/max fill:    5.0%, 0.0%\n'
                                '   - Keep negative:   yes\n'
                                '\n'
                                '  Linker status:\n'
                                '   - No. of objects:  368\n'
                                '   - Memory usage:    49.23 kB\n'
                                '\n'
                                '\n'
                                '  Elapsed time: 00:00:05 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring reliability\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using 3D parameter space:\n'
                                '   - peak\n'
                                '   - sum\n'
                                '   - mean\n'
                                '  Found 184 positive and 184 negative sources.\n'
                                '  Retaining all negative detections.\n'
                                '  Using auto-kernel feature.\n'
                                '    Iter.  1: kernel = 0.100, median = 0.999\n'
                                '    Iter.  2: kernel = 0.200, median = 0.738\n'
                                '    Iter.  3: kernel = 0.300, median = 0.460\n'
                                '    Iter.  4: kernel = 0.340, median = 0.425\n'
                                '    Iter.  5: kernel = 0.380, median = 0.374\n'
                                '    Iter.  6: kernel = 0.420, median = 0.343\n'
                                '    Iter.  7: kernel = 0.460, median = 0.331\n'
                                '    Iter.  8: kernel = 0.500, median = 0.287\n'
                                '    Iter.  9: kernel = 0.540, median = 0.311\n'
                                '    Iter. 10: kernel = 0.580, median = 0.286\n'
                                '    Iter. 11: kernel = 0.620, median = 0.275\n'
                                '    Iter. 12: kernel = 0.660, median = 0.254\n'
                                '    Iter. 13: kernel = 0.700, median = 0.232\n'
                                '    Iter. 14: kernel = 0.740, median = 0.217\n'
                                '    Iter. 15: kernel = 0.780, median = 0.179\n'
                                '    Iter. 16: kernel = 0.820, median = 0.173\n'
                                '    Iter. 17: kernel = 0.860, median = 0.183\n'
                                '    Iter. 18: kernel = 0.900, median = 0.174\n'
                                '    Iter. 19: kernel = 0.940, median = 0.159\n'
                                '    Iter. 20: kernel = 0.980, median = 0.153\n'
                                '    Iter. 21: kernel = 1.020, median = 0.130\n'
                                '    Iter. 22: kernel = 1.060, median = 0.109\n'
                                '    Iter. 23: kernel = 1.100, median = 0.101\n'
                                '    Iter. 24: kernel = 1.140, median = 0.091\n'
                                '    Iter. 25: kernel = 1.180, median = 0.088\n'
                                '    Iter. 26: kernel = 1.220, median = 0.085\n'
                                '    Iter. 27: kernel = 1.260, median = 0.082\n'
                                '    Iter. 28: kernel = 1.300, median = 0.075\n'
                                '    Iter. 29: kernel = 1.340, median = 0.069\n'
                                '    Iter. 30: kernel = 1.380, median = 0.067\n'
                                '    Iter. 31: kernel = 1.420, median = 0.064\n'
                                '    Iter. 32: kernel = 1.460, median = 0.058\n'
                                '    Iter. 33: kernel = 1.500, median = 0.053\n'
                                '    Iter. 34: kernel = 1.540, median = 0.049\n'
                                '  Converged to scale_kernel = 1.540 after 34 iterations.\n'
                                '  \n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_rel.eps\n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_skellam.eps\n'
                                '\n'
                                'ERROR: No reliable sources found. Terminating pipeline.\n'
                                '       Terminating with error code 8.\n'
                                '\n',
                 'error': "Command '['sofia', "
                          "'/home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID5620.par']' "
                          'returned non-zero exit status 8.',
                 'sw_status': 'error',
                 'sofia_par_changes': {'pipeline.threads': '3',
                                       'input.data': 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor.fits',
                                       'input.invert': 'true',
                                       'output.directory': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption'},
                 'sofia_parfile': '# SoFiA 2 parameter file for the official SoFiA test datacube\n'
                                  '\n'
                                  '\n'
                                  '# Global settings\n'
                                  '\n'
                                  'pipeline.verbose           =  false\n'
                                  'pipeline.pedantic          =  true\n'
                                  'pipeline.threads           =  0\n'
                                  '\n'
                                  '\n'
                                  '# Input\n'
                                  '\n'
                                  'input.data                 =  sofia_test_datacube.test\n'
                                  'input.primaryBeam          =  \n'
                                  'input.region               =  \n'
                                  'input.gain                 =  \n'
                                  'input.noise                =  \n'
                                  'input.weights              =  \n'
                                  'input.mask                 =  \n'
                                  'input.invert               =  falseee\n'
                                  '\n'
                                  '\n'
                                  '# Flagging\n'
                                  '\n'
                                  'flag.region                =  \n'
                                  'flag.catalog               =  \n'
                                  'flag.radius                =  5\n'
                                  'flag.auto                  =  false\n'
                                  'flag.threshold             =  5.0\n'
                                  'flag.log                   =  false\n'
                                  'flag.cube                  =  \n'
                                  '\n'
                                  '\n'
                                  '# Continuum subtraction\n'
                                  '\n'
                                  'contsub.enable             =  false\n'
                                  'contsub.order              =  0\n'
                                  'contsub.threshold          =  2.0\n'
                                  'contsub.shift              =  4\n'
                                  'contsub.padding            =  3\n'
                                  '\n'
                                  '\n'
                                  '# Noise scaling\n'
                                  '\n'
                                  'scaleNoise.enable          =  false\n'
                                  'scaleNoise.mode            =  local\n'
                                  'scaleNoise.statistic       =  mad\n'
                                  'scaleNoise.fluxRange       =  negative\n'
                                  'scaleNoise.windowXY        =  31\n'
                                  'scaleNoise.windowZ         =  31\n'
                                  'scaleNoise.gridXY          =  0\n'
                                  'scaleNoise.gridZ           =  0\n'
                                  'scaleNoise.interpolate     =  false\n'
                                  'scaleNoise.scfind          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Ripple filter\n'
                                  '\n'
                                  'rippleFilter.enable        =  false\n'
                                  'rippleFilter.statistic     =  median\n'
                                  'rippleFilter.windowXY      =  31\n'
                                  'rippleFilter.windowZ       =  15\n'
                                  'rippleFilter.gridXY        =  0\n'
                                  'rippleFilter.gridZ         =  0\n'
                                  'rippleFilter.interpolate   =  false\n'
                                  '\n'
                                  '\n'
                                  '# S+C finder\n'
                                  '\n'
                                  'scfind.enable              =  true\n'
                                  'scfind.kernelsXY           =  0, 3, 6, 9\n'
                                  'scfind.kernelsZ            =  0, 3, 7, 15\n'
                                  'scfind.threshold           =  3.8\n'
                                  'scfind.replacement         =  2.0\n'
                                  'scfind.statistic           =  mad\n'
                                  'scfind.fluxRange           =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Threshold finder\n'
                                  '\n'
                                  'threshold.enable           =  false\n'
                                  'threshold.threshold        =  5.0\n'
                                  'threshold.mode             =  relative\n'
                                  'threshold.statistic        =  mad\n'
                                  'threshold.fluxRange        =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Linker\n'
                                  '\n'
                                  'linker.enable              =  true\n'
                                  'linker.radiusXY            =  2\n'
                                  'linker.radiusZ             =  3\n'
                                  'linker.minSizeXY           =  5\n'
                                  'linker.minSizeZ            =  5\n'
                                  'linker.maxSizeXY           =  0\n'
                                  'linker.maxSizeZ            =  0\n'
                                  'linker.minPixels           =  0\n'
                                  'linker.maxPixels           =  0\n'
                                  'linker.minFill             =  0.05\n'
                                  'linker.maxFill             =  0.0\n'
                                  'linker.positivity          =  false\n'
                                  'linker.keepNegative        =  false\n'
                                  '\n'
                                  '\n'
                                  '# Reliability\n'
                                  '\n'
                                  'reliability.enable         =  true\n'
                                  'reliability.parameters     =  peak, sum, mean\n'
                                  'reliability.threshold      =  0.9\n'
                                  'reliability.scaleKernel    =  0.3\n'
                                  'reliability.minSNR         =  6.0\n'
                                  'reliability.minPixels      =  150\n'
                                  'reliability.autoKernel     =  true\n'
                                  'reliability.iterations     =  50\n'
                                  'reliability.tolerance      =  0.05\n'
                                  'reliability.catalog        =  \n'
                                  'reliability.plot           =  true\n'
                                  'reliability.plotExtra      =  false\n'
                                  'reliability.debug          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Mask dilation\n'
                                  '\n'
                                  'dilation.enable            =  false\n'
                                  'dilation.iterationsXY      =  10\n'
                                  'dilation.iterationsZ       =  5\n'
                                  'dilation.threshold         =  0.001\n'
                                  '\n'
                                  '\n'
                                  '# Parameterisation\n'
                                  '\n'
                                  'parameter.enable           =  true\n'
                                  'parameter.wcs              =  true\n'
                                  'parameter.physical         =  true\n'
                                  'parameter.prefix           =  SoFiA\n'
                                  'parameter.offset           =  false\n'
                                  '\n'
                                  '\n'
                                  '# Output\n'
                                  '\n'
                                  'output.directory           =  \n'
                                  'output.filename            =  \n'
                                  'output.writeCatASCII       =  true\n'
                                  'output.writeCatXML         =  true\n'
                                  'output.writeCatSQL         =  false\n'
                                  'output.writeKarma          =  false\n'
                                  'output.writeNoise          =  false\n'
                                  'output.writeFiltered       =  false\n'
                                  'output.writeMask           =  true\n'
                                  'output.writeMask2d         =  true\n'
                                  'output.writeRawMask        =  false\n'
                                  'output.writeMoments        =  true\n'
                                  'output.writeCubelets       =  true\n'
                                  'output.writePV             =  true\n'
                                  'output.marginAperSpec      =  10\n'
                                  'output.marginCubelets      =  10\n'
                                  'output.thresholdMom12      =  0.0\n'
                                  'output.overwrite           =  true\n',
                 'command': ''},
                {'software_id': 'SoFiA-2',
                 'mode': 'emission',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_logfile.log',
                 'log_content': '____________________________________________________________________________\n'
                                '\n'
                                ' Pipeline started\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Software:  Source Finding Application (SoFiA)\n'
                                '  Version:   2.6.14 (2025-05-14)\n'
                                '  CPU:       12 threads available\n'
                                '  Memory:    12.7 GB total / 5.0 GB free\n'
                                '  Date:      2025-09-04\n'
                                '  Time:      08:17:03 h\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading parameter settings\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Activating SoFiA default parameter settings.\n'
                                '  Loading user-specified parameters.\n'
                                '  - Loading user parameter file: '
                                '/home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID5620.par\n'
                                '  Using 3 out of 12 available CPU threads.\n'
                                '\n'
                                'WARNING: '
                                '┌──────────────────────────────────────────────────────────┐\n'
                                '         │ You have set parameter.physical = true. SoFiA will '
                                'try   │\n'
                                '         │ to convert some parameters to physical units under '
                                'the   │\n'
                                '         │ following fundamental '
                                'assumptions:                       │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The beam information in the FITS header (BMAJ, '
                                'BMIN)  │\n'
                                '         │    is correct and accurate across the entire data '
                                'cube.  │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The spectral channels of the data cube are '
                                'uncorrela- │\n'
                                '         │    ted, i.e. spectral resolution equals channel '
                                'width.   │\n'
                                '         '
                                '│                                                          │\n'
                                '         │ Should any of these assumptions be incorrect then '
                                'the    │\n'
                                '         │ measurement of \n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading data cube\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Opening FITS file '
                                "'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor.fits'.\n"
                                '  Reading FITS data with the following specifications:\n'
                                '    Data type:    -32\n'
                                '    No. of axes:  4\n'
                                '    Axis sizes:   350, 350, 118\n'
                                '    Region:       0-349, 0-349, 0-117\n'
                                '    Memory used:  55.1 MB\n'
                                '  Searching for values of infinity.\n'
                                '    No infinite data values found.\n'
                                '\n'
                                '  Elapsed time: 00:00:00 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring global noise level\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Global RMS:  4.166e-04  (using stride of 14)\n'
                                '\n'
                                '  Elapsed time: 00:00:00 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running S+C finder\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using the following parameters:\n'
                                '  - Kernels\n'
                                '    - spatial:        0, 3, 6, 9\n'
                                '    - spectral:       0, 3, 7, 15\n'
                                '  - Flux threshold:   3.8 * rms\n'
                                '  - Noise statistic:  median absolute deviation\n'
                                '  - Flux range:       negative\n'
                                '\n'
                                '  Using a stride of 14 in noise measurement.\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [0]\n'
                                '  Noise level:       4.166e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:00 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [3]\n'
                                '  Noise level:       3.324e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [7]\n'
                                '  Noise level:       2.250e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [15]\n'
                                '  Noise level:       1.445e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [0]\n'
                                '  Noise level:       3.062e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [3]\n'
                                '  Noise level:       2.428e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:03 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [7]\n'
                                '  Noise level:       1.644e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [15]\n'
                                '  Noise level:       1.058e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [0]\n'
                                '  Noise level:       2.090e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [3]\n'
                                '  Noise level:       1.657e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [7]\n'
                                '  Noise level:       1.121e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [15]\n'
                                '  Noise level:       7.195e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [0]\n'
                                '  Noise level:       1.280e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [3]\n'
                                '  Noise level:       1.017e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [7]\n'
                                '  Noise level:       6.962e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:08 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [15]\n'
                                '  Noise level:       4.450e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:05 h\n'
                                '  CPU time:     00:00:09 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating source mask\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  356422 pixels detected by source finder (2.466%).\n'
                                '\n'
                                '  Elapsed time: 00:00:05 h\n'
                                '  CPU time:     00:00:09 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running Linker\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Linker settings:\n'
                                '   - Merging radii:   2, 2, 3\n'
                                '   - Minimum size:    5 x 5 x 5\n'
                                '   - Min/max fill:    5.0%, 0.0%\n'
                                '   - Keep negative:   yes\n'
                                '\n'
                                '  Linker status:\n'
                                '   - No. of objects:  359\n'
                                '   - Memory usage:    48.03 kB\n'
                                '\n'
                                '\n'
                                '  Elapsed time: 00:00:05 h\n'
                                '  CPU time:     00:00:09 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring reliability\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using 3D parameter space:\n'
                                '   - peak\n'
                                '   - sum\n'
                                '   - mean\n'
                                '  Found 184 positive and 175 negative sources.\n'
                                '  Retaining all negative detections.\n'
                                '  Using auto-kernel feature.\n'
                                '    Iter.  1: kernel = 0.100, median = 1.000\n'
                                '    Iter.  2: kernel = 0.200, median = 0.842\n'
                                '    Iter.  3: kernel = 0.300, median = 0.673\n'
                                '    Iter.  4: kernel = 0.400, median = 0.527\n'
                                '    Iter.  5: kernel = 0.500, median = 0.448\n'
                                '    Iter.  6: kernel = 0.540, median = 0.415\n'
                                '    Iter.  7: kernel = 0.580, median = 0.393\n'
                                '    Iter.  8: kernel = 0.620, median = 0.394\n'
                                '    Iter.  9: kernel = 0.660, median = 0.381\n'
                                '    Iter. 10: kernel = 0.700, median = 0.332\n'
                                '    Iter. 11: kernel = 0.740, median = 0.304\n'
                                '    Iter. 12: kernel = 0.780, median = 0.216\n'
                                '    Iter. 13: kernel = 0.820, median = 0.199\n'
                                '    Iter. 14: kernel = 0.860, median = 0.160\n'
                                '    Iter. 15: kernel = 0.900, median = 0.134\n'
                                '    Iter. 16: kernel = 0.940, median = 0.126\n'
                                '    Iter. 17: kernel = 0.980, median = 0.111\n'
                                '    Iter. 18: kernel = 1.020, median = 0.111\n'
                                '    Iter. 19: kernel = 1.060, median = 0.103\n'
                                '    Iter. 20: kernel = 1.100, median = 0.089\n'
                                '    Iter. 21: kernel = 1.140, median = 0.073\n'
                                '    Iter. 22: kernel = 1.180, median = 0.066\n'
                                '    Iter. 23: kernel = 1.220, median = 0.057\n'
                                '    Iter. 24: kernel = 1.260, median = 0.047\n'
                                '  Converged to scale_kernel = 1.260 after 24 iterations.\n'
                                '  \n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_rel.eps\n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_skellam.eps\n'
                                '\n'
                                'ERROR: No reliable sources found. Terminating pipeline.\n'
                                '       Terminating with error code 8.\n'
                                '\n',
                 'error': "Command '['sofia', "
                          "'/home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID5620.par']' "
                          'returned non-zero exit status 8.',
                 'sw_status': 'error',
                 'sofia_par_changes': {'pipeline.threads': '3',
                                       'input.invert': 'false',
                                       'output.directory': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission',
                                       'input.data': 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor.fits'},
                 'sofia_parfile': '# SoFiA 2 parameter file for the official SoFiA test datacube\n'
                                  '\n'
                                  '\n'
                                  '# Global settings\n'
                                  '\n'
                                  'pipeline.verbose           =  false\n'
                                  'pipeline.pedantic          =  true\n'
                                  'pipeline.threads           =  0\n'
                                  '\n'
                                  '\n'
                                  '# Input\n'
                                  '\n'
                                  '#input.data                 =  sofia_test_datacube.test\n'
                                  '#input.primaryBeam          =  \n'
                                  'input.region               =  \n'
                                  'input.gain                 =  \n'
                                  'input.noise                =  \n'
                                  'input.weights              =  \n'
                                  'input.mask                 =  \n'
                                  'input.invert               =   \n'
                                  '\n'
                                  '\n'
                                  '# Flagging\n'
                                  '\n'
                                  'flag.region                =  \n'
                                  'flag.catalog               =  \n'
                                  'flag.radius                =  5\n'
                                  'flag.auto                  =  false\n'
                                  'flag.threshold             =  5.0\n'
                                  'flag.log                   =  false\n'
                                  'flag.cube                  =  \n'
                                  '\n'
                                  '\n'
                                  '# Continuum subtraction\n'
                                  '\n'
                                  'contsub.enable             =  false\n'
                                  'contsub.order              =  0\n'
                                  'contsub.threshold          =  2.0\n'
                                  'contsub.shift              =  4\n'
                                  'contsub.padding            =  3\n'
                                  '\n'
                                  '\n'
                                  '# Noise scaling\n'
                                  '\n'
                                  'scaleNoise.enable          =  false\n'
                                  'scaleNoise.mode            =  local\n'
                                  'scaleNoise.statistic       =  mad\n'
                                  'scaleNoise.fluxRange       =  negative\n'
                                  'scaleNoise.windowXY        =  31\n'
                                  'scaleNoise.windowZ         =  31\n'
                                  'scaleNoise.gridXY          =  0\n'
                                  'scaleNoise.gridZ           =  0\n'
                                  'scaleNoise.interpolate     =  false\n'
                                  'scaleNoise.scfind          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Ripple filter\n'
                                  '\n'
                                  'rippleFilter.enable        =  false\n'
                                  'rippleFilter.statistic     =  median\n'
                                  'rippleFilter.windowXY      =  31\n'
                                  'rippleFilter.windowZ       =  15\n'
                                  'rippleFilter.gridXY        =  0\n'
                                  'rippleFilter.gridZ         =  0\n'
                                  'rippleFilter.interpolate   =  false\n'
                                  '\n'
                                  '\n'
                                  '# S+C finder\n'
                                  '\n'
                                  'scfind.enable              =  true\n'
                                  'scfind.kernelsXY           =  0, 3, 6, 9\n'
                                  'scfind.kernelsZ            =  0, 3, 7, 15\n'
                                  'scfind.threshold           =  3.8\n'
                                  'scfind.replacement         =  2.0\n'
                                  'scfind.statistic           =  mad\n'
                                  'scfind.fluxRange           =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Threshold finder\n'
                                  '\n'
                                  'threshold.enable           =  false\n'
                                  'threshold.threshold        =  5.0\n'
                                  'threshold.mode             =  relative\n'
                                  'threshold.statistic        =  mad\n'
                                  'threshold.fluxRange        =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Linker\n'
                                  '\n'
                                  'linker.enable              =  true\n'
                                  'linker.radiusXY            =  2\n'
                                  'linker.radiusZ             =  3\n'
                                  'linker.minSizeXY           =  5\n'
                                  'linker.minSizeZ            =  5\n'
                                  'linker.maxSizeXY           =  0\n'
                                  'linker.maxSizeZ            =  0\n'
                                  'linker.minPixels           =  0\n'
                                  'linker.maxPixels           =  0\n'
                                  'linker.minFill             =  0.05\n'
                                  'linker.maxFill             =  0.0\n'
                                  'linker.positivity          =  false\n'
                                  'linker.keepNegative        =  false\n'
                                  '\n'
                                  '\n'
                                  '# Reliability\n'
                                  '\n'
                                  'reliability.enable         =  true\n'
                                  'reliability.parameters     =  peak, sum, mean\n'
                                  'reliability.threshold      =  0.9\n'
                                  'reliability.scaleKernel    =  0.3\n'
                                  'reliability.minSNR         =  6.0\n'
                                  'reliability.minPixels      =  150\n'
                                  'reliability.autoKernel     =  true\n'
                                  'reliability.iterations     =  50\n'
                                  'reliability.tolerance      =  0.05\n'
                                  'reliability.catalog        =  \n'
                                  'reliability.plot           =  true\n'
                                  'reliability.plotExtra      =  false\n'
                                  'reliability.debug          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Mask dilation\n'
                                  '\n'
                                  'dilation.enable            =  false\n'
                                  'dilation.iterationsXY      =  10\n'
                                  'dilation.iterationsZ       =  5\n'
                                  'dilation.threshold         =  0.001\n'
                                  '\n'
                                  '\n'
                                  '# Parameterisation\n'
                                  '\n'
                                  'parameter.enable           =  true\n'
                                  'parameter.wcs              =  true\n'
                                  'parameter.physical         =  true\n'
                                  'parameter.prefix           =  SoFiA\n'
                                  'parameter.offset           =  false\n'
                                  '\n'
                                  '\n'
                                  '# Output\n'
                                  '\n'
                                  'output.directory           =  \n'
                                  'output.filename            =  \n'
                                  'output.writeCatASCII       =  true\n'
                                  'output.writeCatXML         =  true\n'
                                  'output.writeCatSQL         =  false\n'
                                  'output.writeKarma          =  false\n'
                                  'output.writeNoise          =  false\n'
                                  'output.writeFiltered       =  false\n'
                                  'output.writeMask           =  true\n'
                                  'output.writeMask2d         =  true\n'
                                  'output.writeRawMask        =  false\n'
                                  'output.writeMoments        =  true\n'
                                  'output.writeCubelets       =  true\n'
                                  'output.writePV             =  true\n'
                                  'output.marginAperSpec      =  10\n'
                                  'output.marginCubelets      =  10\n'
                                  'output.thresholdMom12      =  0.0\n'
                                  'output.overwrite           =  true\n',
                 'command': ''},
                {'software_id': 'SIP',
                 'mode': 'absorption',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_sip.log',
                 'log_content': 'No log file available: '
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_sip.log',
                 'error': 'No valid .txt or .xml catalog for SIP found within the  '
                          '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption  directory.',
                 'sw_status': 'error',
                 'sofia_par_changes': {},
                 'sofia_parfile': 'No log file available: ',
                 'command': ''},
                {'software_id': 'SIP',
                 'mode': 'emission',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_sip.log',
                 'log_content': 'No log file available: '
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_sip.log',
                 'error': 'No valid .txt or .xml catalog for SIP found within the  '
                          '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission  directory.',
                 'sw_status': 'error',
                 'sofia_par_changes': {},
                 'sofia_parfile': 'No log file available: ',
                 'command': ''}],
  'images': [],
  'images_grouped': {'sofia': {'absorption': [], 'emission': []},
                     'sip': {'absorption': {}, 'emission': {}},
                     'qa': []}},
 {'input_data': 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor.fits',
  'status': 'error',
  'softwares': [{'software_id': 'SoFiA-2',
                 'mode': 'absorption',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_logfile.log',
                 'log_content': '____________________________________________________________________________\n'
                                '\n'
                                ' Pipeline started\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Software:  Source Finding Application (SoFiA)\n'
                                '  Version:   2.6.14 (2025-05-14)\n'
                                '  CPU:       12 threads available\n'
                                '  Memory:    12.7 GB total / 6.6 GB free\n'
                                '  Date:      2025-09-04\n'
                                '  Time:      08:16:58 h\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading parameter settings\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Activating SoFiA default parameter settings.\n'
                                '  Loading user-specified parameters.\n'
                                '  - Loading user parameter file: '
                                '/home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID5618.par\n'
                                '  Using 3 out of 12 available CPU threads.\n'
                                '\n'
                                'WARNING: '
                                '┌──────────────────────────────────────────────────────────┐\n'
                                '         │ You have set parameter.physical = true. SoFiA will '
                                'try   │\n'
                                '         │ to convert some parameters to physical units under '
                                'the   │\n'
                                '         │ following fundamental '
                                'assumptions:                       │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The beam information in the FITS header (BMAJ, '
                                'BMIN)  │\n'
                                '         │    is correct and accurate across the entire data '
                                'cube.  │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The spectral channels of the data cube are '
                                'uncorrela- │\n'
                                '         │    ted, i.e. spectral resolution equals channel '
                                'width.   │\n'
                                '         '
                                '│                                                          │\n'
                                '         │ Should any of these assumptions be incorrect then '
                                'the    │\n'
                                '         │ measurement of \n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading data cube\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Opening FITS file '
                                "'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor.fits'.\n"
                                '  Reading FITS data with the following specifications:\n'
                                '    Data type:    -32\n'
                                '    No. of axes:  4\n'
                                '    Axis sizes:   350, 350, 118\n'
                                '    Region:       0-349, 0-349, 0-117\n'
                                '    Memory used:  55.1 MB\n'
                                '  Searching for values of infinity.\n'
                                '    No infinite data values found.\n'
                                '  Inverting data cube\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring global noise level\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Global RMS:  4.042e-04  (using stride of 14)\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running S+C finder\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using the following parameters:\n'
                                '  - Kernels\n'
                                '    - spatial:        0, 3, 6, 9\n'
                                '    - spectral:       0, 3, 7, 15\n'
                                '  - Flux threshold:   3.8 * rms\n'
                                '  - Noise statistic:  median absolute deviation\n'
                                '  - Flux range:       negative\n'
                                '\n'
                                '  Using a stride of 14 in noise measurement.\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [0]\n'
                                '  Noise level:       4.042e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [3]\n'
                                '  Noise level:       3.201e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [7]\n'
                                '  Noise level:       2.194e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [15]\n'
                                '  Noise level:       1.412e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [0]\n'
                                '  Noise level:       2.781e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [3]\n'
                                '  Noise level:       2.208e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [7]\n'
                                '  Noise level:       1.507e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:03 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [15]\n'
                                '  Noise level:       9.642e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:03 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [0]\n'
                                '  Noise level:       1.824e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [3]\n'
                                '  Noise level:       1.455e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [7]\n'
                                '  Noise level:       9.892e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [15]\n'
                                '  Noise level:       6.316e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [0]\n'
                                '  Noise level:       1.118e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [3]\n'
                                '  Noise level:       8.925e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [7]\n'
                                '  Noise level:       6.031e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [15]\n'
                                '  Noise level:       3.899e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating source mask\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  284523 pixels detected by source finder (1.968%).\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running Linker\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Linker settings:\n'
                                '   - Merging radii:   2, 2, 3\n'
                                '   - Minimum size:    5 x 5 x 5\n'
                                '   - Min/max fill:    5.0%, 0.0%\n'
                                '   - Keep negative:   yes\n'
                                '\n'
                                '  Linker status:\n'
                                '   - No. of objects:  246\n'
                                '   - Memory usage:    32.91 kB\n'
                                '\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring reliability\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using 3D parameter space:\n'
                                '   - peak\n'
                                '   - sum\n'
                                '   - mean\n'
                                '  Found 134 positive and 112 negative sources.\n'
                                '  Retaining all negative detections.\n'
                                '  Using auto-kernel feature.\n'
                                '    Iter.  1: kernel = 0.100, median = 1.000\n'
                                '    Iter.  2: kernel = 0.200, median = 0.896\n'
                                '    Iter.  3: kernel = 0.300, median = 0.645\n'
                                '    Iter.  4: kernel = 0.400, median = 0.393\n'
                                '    Iter.  5: kernel = 0.440, median = 0.296\n'
                                '    Iter.  6: kernel = 0.480, median = 0.273\n'
                                '    Iter.  7: kernel = 0.520, median = 0.239\n'
                                '    Iter.  8: kernel = 0.560, median = 0.175\n'
                                '    Iter.  9: kernel = 0.600, median = 0.115\n'
                                '    Iter. 10: kernel = 0.640, median = 0.069\n'
                                '    Iter. 11: kernel = 0.680, median = 0.032\n'
                                '  Converged to scale_kernel = 0.680 after 11 iterations.\n'
                                '  \n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_rel.eps\n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_skellam.eps\n'
                                '  1 reliable source found.\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating initial catalogue\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Initial source catalogue created.\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring source parameters\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Found 1 source in need of parameterisation.\n'
                                '  Assuming beam size of 6.6 x 5.1 pixels.\n'
                                '\n'
                                '  Attempting to measure parameters in physical units.\n'
                                '\n'
                                '  Elapsed time: 00:00:05 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating cubelets\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Flux threshold (moment 1 and 2): 0.00e+00\n'
                                '  Assuming beam size of 6.6 x 5.1 pixels.\n'
                                '\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_cube.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mask.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom0.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom1.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom2.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_chan.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_snr.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv_min.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv_mask.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv_min_mask.fits\n'
                                '  Creating text file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_spec.txt\n'
                                '  Creating text file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_spec_aperture.txt\n'
                                '\n'
                                '  Elapsed time: 00:00:05 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating moment maps\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mom0.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mom1.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mom2.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_chan.fits\n'
                                '\n'
                                '  Elapsed time: 00:00:05 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Writing mask cube\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mask-2d.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mask.fits\n'
                                '\n'
                                '  Elapsed time: 00:00:07 h\n'
                                '  CPU time:     00:00:15 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Writing source catalogue\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Writing ASCII file:   '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_cat.txt\n'
                                '  Writing VOTable file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_cat.xml\n'
                                '\n'
                                '  Elapsed time: 00:00:07 h\n'
                                '  CPU time:     00:00:15 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Pipeline finished\n'
                                '____________________________________________________________________________\n'
                                '\n',
                 'error': '',
                 'sw_status': 'ok',
                 'sofia_par_changes': {'pipeline.threads': '3',
                                       'input.data': 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor.fits',
                                       'input.invert': 'true',
                                       'output.directory': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption'},
                 'sofia_parfile': '# SoFiA 2 parameter file for the official SoFiA test datacube\n'
                                  '\n'
                                  '\n'
                                  '# Global settings\n'
                                  '\n'
                                  'pipeline.verbose           =  false\n'
                                  'pipeline.pedantic          =  true\n'
                                  'pipeline.threads           =  0\n'
                                  '\n'
                                  '\n'
                                  '# Input\n'
                                  '\n'
                                  'input.data                 =  sofia_test_datacube.test\n'
                                  'input.primaryBeam          =  \n'
                                  'input.region               =  \n'
                                  'input.gain                 =  \n'
                                  'input.noise                =  \n'
                                  'input.weights              =  \n'
                                  'input.mask                 =  \n'
                                  'input.invert               =  falseee\n'
                                  '\n'
                                  '\n'
                                  '# Flagging\n'
                                  '\n'
                                  'flag.region                =  \n'
                                  'flag.catalog               =  \n'
                                  'flag.radius                =  5\n'
                                  'flag.auto                  =  false\n'
                                  'flag.threshold             =  5.0\n'
                                  'flag.log                   =  false\n'
                                  'flag.cube                  =  \n'
                                  '\n'
                                  '\n'
                                  '# Continuum subtraction\n'
                                  '\n'
                                  'contsub.enable             =  false\n'
                                  'contsub.order              =  0\n'
                                  'contsub.threshold          =  2.0\n'
                                  'contsub.shift              =  4\n'
                                  'contsub.padding            =  3\n'
                                  '\n'
                                  '\n'
                                  '# Noise scaling\n'
                                  '\n'
                                  'scaleNoise.enable          =  false\n'
                                  'scaleNoise.mode            =  local\n'
                                  'scaleNoise.statistic       =  mad\n'
                                  'scaleNoise.fluxRange       =  negative\n'
                                  'scaleNoise.windowXY        =  31\n'
                                  'scaleNoise.windowZ         =  31\n'
                                  'scaleNoise.gridXY          =  0\n'
                                  'scaleNoise.gridZ           =  0\n'
                                  'scaleNoise.interpolate     =  false\n'
                                  'scaleNoise.scfind          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Ripple filter\n'
                                  '\n'
                                  'rippleFilter.enable        =  false\n'
                                  'rippleFilter.statistic     =  median\n'
                                  'rippleFilter.windowXY      =  31\n'
                                  'rippleFilter.windowZ       =  15\n'
                                  'rippleFilter.gridXY        =  0\n'
                                  'rippleFilter.gridZ         =  0\n'
                                  'rippleFilter.interpolate   =  false\n'
                                  '\n'
                                  '\n'
                                  '# S+C finder\n'
                                  '\n'
                                  'scfind.enable              =  true\n'
                                  'scfind.kernelsXY           =  0, 3, 6, 9\n'
                                  'scfind.kernelsZ            =  0, 3, 7, 15\n'
                                  'scfind.threshold           =  3.8\n'
                                  'scfind.replacement         =  2.0\n'
                                  'scfind.statistic           =  mad\n'
                                  'scfind.fluxRange           =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Threshold finder\n'
                                  '\n'
                                  'threshold.enable           =  false\n'
                                  'threshold.threshold        =  5.0\n'
                                  'threshold.mode             =  relative\n'
                                  'threshold.statistic        =  mad\n'
                                  'threshold.fluxRange        =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Linker\n'
                                  '\n'
                                  'linker.enable              =  true\n'
                                  'linker.radiusXY            =  2\n'
                                  'linker.radiusZ             =  3\n'
                                  'linker.minSizeXY           =  5\n'
                                  'linker.minSizeZ            =  5\n'
                                  'linker.maxSizeXY           =  0\n'
                                  'linker.maxSizeZ            =  0\n'
                                  'linker.minPixels           =  0\n'
                                  'linker.maxPixels           =  0\n'
                                  'linker.minFill             =  0.05\n'
                                  'linker.maxFill             =  0.0\n'
                                  'linker.positivity          =  false\n'
                                  'linker.keepNegative        =  false\n'
                                  '\n'
                                  '\n'
                                  '# Reliability\n'
                                  '\n'
                                  'reliability.enable         =  true\n'
                                  'reliability.parameters     =  peak, sum, mean\n'
                                  'reliability.threshold      =  0.9\n'
                                  'reliability.scaleKernel    =  0.3\n'
                                  'reliability.minSNR         =  6.0\n'
                                  'reliability.minPixels      =  150\n'
                                  'reliability.autoKernel     =  true\n'
                                  'reliability.iterations     =  50\n'
                                  'reliability.tolerance      =  0.05\n'
                                  'reliability.catalog        =  \n'
                                  'reliability.plot           =  true\n'
                                  'reliability.plotExtra      =  false\n'
                                  'reliability.debug          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Mask dilation\n'
                                  '\n'
                                  'dilation.enable            =  false\n'
                                  'dilation.iterationsXY      =  10\n'
                                  'dilation.iterationsZ       =  5\n'
                                  'dilation.threshold         =  0.001\n'
                                  '\n'
                                  '\n'
                                  '# Parameterisation\n'
                                  '\n'
                                  'parameter.enable           =  true\n'
                                  'parameter.wcs              =  true\n'
                                  'parameter.physical         =  true\n'
                                  'parameter.prefix           =  SoFiA\n'
                                  'parameter.offset           =  false\n'
                                  '\n'
                                  '\n'
                                  '# Output\n'
                                  '\n'
                                  'output.directory           =  \n'
                                  'output.filename            =  \n'
                                  'output.writeCatASCII       =  true\n'
                                  'output.writeCatXML         =  true\n'
                                  'output.writeCatSQL         =  false\n'
                                  'output.writeKarma          =  false\n'
                                  'output.writeNoise          =  false\n'
                                  'output.writeFiltered       =  false\n'
                                  'output.writeMask           =  true\n'
                                  'output.writeMask2d         =  true\n'
                                  'output.writeRawMask        =  false\n'
                                  'output.writeMoments        =  true\n'
                                  'output.writeCubelets       =  true\n'
                                  'output.writePV             =  true\n'
                                  'output.marginAperSpec      =  10\n'
                                  'output.marginCubelets      =  10\n'
                                  'output.thresholdMom12      =  0.0\n'
                                  'output.overwrite           =  true\n',
                 'command': ''},
                {'software_id': 'SoFiA-2',
                 'mode': 'emission',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_logfile.log',
                 'log_content': '____________________________________________________________________________\n'
                                '\n'
                                ' Pipeline started\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Software:  Source Finding Application (SoFiA)\n'
                                '  Version:   2.6.14 (2025-05-14)\n'
                                '  CPU:       12 threads available\n'
                                '  Memory:    12.7 GB total / 3.7 GB free\n'
                                '  Date:      2025-09-04\n'
                                '  Time:      08:17:09 h\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading parameter settings\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Activating SoFiA default parameter settings.\n'
                                '  Loading user-specified parameters.\n'
                                '  - Loading user parameter file: '
                                '/home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID5618.par\n'
                                '  Using 3 out of 12 available CPU threads.\n'
                                '\n'
                                'WARNING: '
                                '┌──────────────────────────────────────────────────────────┐\n'
                                '         │ You have set parameter.physical = true. SoFiA will '
                                'try   │\n'
                                '         │ to convert some parameters to physical units under '
                                'the   │\n'
                                '         │ following fundamental '
                                'assumptions:                       │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The beam information in the FITS header (BMAJ, '
                                'BMIN)  │\n'
                                '         │    is correct and accurate across the entire data '
                                'cube.  │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The spectral channels of the data cube are '
                                'uncorrela- │\n'
                                '         │    ted, i.e. spectral resolution equals channel '
                                'width.   │\n'
                                '         '
                                '│                                                          │\n'
                                '         │ Should any of these assumptions be incorrect then '
                                'the    │\n'
                                '         │ measurement of \n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading data cube\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Opening FITS file '
                                "'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor.fits'.\n"
                                '  Reading FITS data with the following specifications:\n'
                                '    Data type:    -32\n'
                                '    No. of axes:  4\n'
                                '    Axis sizes:   350, 350, 118\n'
                                '    Region:       0-349, 0-349, 0-117\n'
                                '    Memory used:  55.1 MB\n'
                                '  Searching for values of infinity.\n'
                                '    No infinite data values found.\n'
                                '\n'
                                '  Elapsed time: 00:00:00 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading and applying flag cube\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Opening FITS file '
                                "'/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mask.fits'.\n"
                                '  Reading FITS data with the following specifications:\n'
                                '    Data type:    32\n'
                                '    No. of axes:  3\n'
                                '    Axis sizes:   350, 350, 118\n'
                                '    Region:       0-349, 0-349, 0-117\n'
                                '    Memory used:  55.1 MB\n'
                                '\n'
                                '  Elapsed time: 00:00:00 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring global noise level\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Global RMS:  4.033e-04  (using stride of 14)\n'
                                '\n'
                                '  Elapsed time: 00:00:00 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running S+C finder\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using the following parameters:\n'
                                '  - Kernels\n'
                                '    - spatial:        0, 3, 6, 9\n'
                                '    - spectral:       0, 3, 7, 15\n'
                                '  - Flux threshold:   3.8 * rms\n'
                                '  - Noise statistic:  median absolute deviation\n'
                                '  - Flux range:       negative\n'
                                '\n'
                                '  Using a stride of 14 in noise measurement.\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [0]\n'
                                '  Noise level:       4.033e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:00 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [3]\n'
                                '  Noise level:       3.229e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:00 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [7]\n'
                                '  Noise level:       2.181e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [15]\n'
                                '  Noise level:       1.401e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [0]\n'
                                '  Noise level:       2.779e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [3]\n'
                                '  Noise level:       2.210e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:02 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [7]\n'
                                '  Noise level:       1.500e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:03 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [15]\n'
                                '  Noise level:       9.592e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:03 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [0]\n'
                                '  Noise level:       1.823e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:03 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [3]\n'
                                '  Noise level:       1.451e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [7]\n'
                                '  Noise level:       9.905e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [15]\n'
                                '  Noise level:       6.325e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [0]\n'
                                '  Noise level:       1.107e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [3]\n'
                                '  Noise level:       8.805e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:05 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [7]\n'
                                '  Noise level:       6.040e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [15]\n'
                                '  Noise level:       3.853e-05\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating source mask\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  289654 pixels detected by source finder (2.004%).\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running Linker\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Linker settings:\n'
                                '   - Merging radii:   2, 2, 3\n'
                                '   - Minimum size:    5 x 5 x 5\n'
                                '   - Min/max fill:    5.0%, 0.0%\n'
                                '   - Keep negative:   yes\n'
                                '\n'
                                '  Linker status:\n'
                                '   - No. of objects:  236\n'
                                '   - Memory usage:    31.57 kB\n'
                                '\n'
                                '\n'
                                '  Elapsed time: 00:00:03 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring reliability\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using 3D parameter space:\n'
                                '   - peak\n'
                                '   - sum\n'
                                '   - mean\n'
                                '  Found 107 positive and 129 negative sources.\n'
                                '  Retaining all negative detections.\n'
                                '  Using auto-kernel feature.\n'
                                '    Iter.  1: kernel = 0.100, median = 1.000\n'
                                '    Iter.  2: kernel = 0.200, median = 0.900\n'
                                '    Iter.  3: kernel = 0.300, median = 0.679\n'
                                '    Iter.  4: kernel = 0.400, median = 0.570\n'
                                '    Iter.  5: kernel = 0.500, median = 0.491\n'
                                '    Iter.  6: kernel = 0.540, median = 0.470\n'
                                '    Iter.  7: kernel = 0.580, median = 0.459\n'
                                '    Iter.  8: kernel = 0.620, median = 0.450\n'
                                '    Iter.  9: kernel = 0.660, median = 0.430\n'
                                '    Iter. 10: kernel = 0.700, median = 0.415\n'
                                '    Iter. 11: kernel = 0.740, median = 0.415\n'
                                '    Iter. 12: kernel = 0.780, median = 0.402\n'
                                '    Iter. 13: kernel = 0.820, median = 0.405\n'
                                '    Iter. 14: kernel = 0.860, median = 0.417\n'
                                '    Iter. 15: kernel = 0.900, median = 0.433\n'
                                '    Iter. 16: kernel = 0.940, median = 0.450\n'
                                '    Iter. 17: kernel = 0.980, median = 0.469\n'
                                '    Iter. 18: kernel = 1.020, median = 0.478\n'
                                '    Iter. 19: kernel = 1.060, median = 0.483\n'
                                '    Iter. 20: kernel = 1.100, median = 0.496\n'
                                '    Iter. 21: kernel = 1.140, median = 0.515\n'
                                '    Iter. 22: kernel = 1.240, median = 0.542\n'
                                '    Iter. 23: kernel = 1.340, median = 0.583\n'
                                '    Iter. 24: kernel = 1.440, median = 0.633\n'
                                '    Iter. 25: kernel = 1.540, median = 0.671\n'
                                '    Iter. 26: kernel = 1.640, median = 0.719\n'
                                '    Iter. 27: kernel = 1.740, median = 0.760\n'
                                '    Iter. 28: kernel = 1.840, median = 0.798\n'
                                '    Iter. 29: kernel = 1.940, median = 0.831\n'
                                '    Iter. 30: kernel = 2.040, median = 0.864\n'
                                '    Iter. 31: kernel = 2.140, median = 0.896\n'
                                '    Iter. 32: kernel = 2.240, median = 0.924\n'
                                '    Iter. 33: kernel = 2.340, median = 0.945\n'
                                '    Iter. 34: kernel = 2.440, median = 0.972\n'
                                '    Iter. 35: kernel = 2.540, median = 0.996\n'
                                '    Iter. 36: kernel = 2.640, median = 1.017\n'
                                '    Iter. 37: kernel = 2.740, median = 1.039\n'
                                '    Iter. 38: kernel = 2.840, median = 1.061\n'
                                '    Iter. 39: kernel = 2.940, median = 1.082\n'
                                '    Iter. 40: kernel = 3.040, median = 1.101\n'
                                '    Iter. 41: kernel = 3.140, median = 1.119\n'
                                '    Iter. 42: kernel = 3.240, median = 1.135\n'
                                '    Iter. 43: kernel = 3.340, median = 1.147\n'
                                '    Iter. 44: kernel = 3.440, median = 1.162\n'
                                '    Iter. 45: kernel = 3.540, median = 1.177\n'
                                '    Iter. 46: kernel = 3.640, median = 1.190\n'
                                '    Iter. 47: kernel = 3.740, median = 1.202\n'
                                '    Iter. 48: kernel = 3.840, median = 1.213\n'
                                '    Iter. 49: kernel = 3.940, median = 1.224\n'
                                '    Iter. 50: kernel = 4.040, median = 1.232\n'
                                'WARNING: Auto-kernel failed to converge, defaulting to kernel '
                                'scale of 0.300.\n'
                                '  \n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_rel.eps\n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_skellam.eps\n'
                                '\n'
                                'ERROR: No reliable sources found. Terminating pipeline.\n'
                                '       Terminating with error code 8.\n'
                                '\n',
                 'error': "Command '['sofia', "
                          "'/home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID5618.par']' "
                          'returned non-zero exit status 8.',
                 'sw_status': 'error',
                 'sofia_par_changes': {'pipeline.threads': '3',
                                       'input.invert': 'false',
                                       'flag.cube': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mask.fits',
                                       'output.directory': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission',
                                       'input.data': 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor.fits'},
                 'sofia_parfile': '# SoFiA 2 parameter file for the official SoFiA test datacube\n'
                                  '\n'
                                  '\n'
                                  '# Global settings\n'
                                  '\n'
                                  'pipeline.verbose           =  false\n'
                                  'pipeline.pedantic          =  true\n'
                                  'pipeline.threads           =  0\n'
                                  '\n'
                                  '\n'
                                  '# Input\n'
                                  '\n'
                                  '#input.data                 =  sofia_test_datacube.test\n'
                                  '#input.primaryBeam          =  \n'
                                  'input.region               =  \n'
                                  'input.gain                 =  \n'
                                  'input.noise                =  \n'
                                  'input.weights              =  \n'
                                  'input.mask                 =  \n'
                                  'input.invert               =   \n'
                                  '\n'
                                  '\n'
                                  '# Flagging\n'
                                  '\n'
                                  'flag.region                =  \n'
                                  'flag.catalog               =  \n'
                                  'flag.radius                =  5\n'
                                  'flag.auto                  =  false\n'
                                  'flag.threshold             =  5.0\n'
                                  'flag.log                   =  false\n'
                                  'flag.cube                  =  \n'
                                  '\n'
                                  '\n'
                                  '# Continuum subtraction\n'
                                  '\n'
                                  'contsub.enable             =  false\n'
                                  'contsub.order              =  0\n'
                                  'contsub.threshold          =  2.0\n'
                                  'contsub.shift              =  4\n'
                                  'contsub.padding            =  3\n'
                                  '\n'
                                  '\n'
                                  '# Noise scaling\n'
                                  '\n'
                                  'scaleNoise.enable          =  false\n'
                                  'scaleNoise.mode            =  local\n'
                                  'scaleNoise.statistic       =  mad\n'
                                  'scaleNoise.fluxRange       =  negative\n'
                                  'scaleNoise.windowXY        =  31\n'
                                  'scaleNoise.windowZ         =  31\n'
                                  'scaleNoise.gridXY          =  0\n'
                                  'scaleNoise.gridZ           =  0\n'
                                  'scaleNoise.interpolate     =  false\n'
                                  'scaleNoise.scfind          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Ripple filter\n'
                                  '\n'
                                  'rippleFilter.enable        =  false\n'
                                  'rippleFilter.statistic     =  median\n'
                                  'rippleFilter.windowXY      =  31\n'
                                  'rippleFilter.windowZ       =  15\n'
                                  'rippleFilter.gridXY        =  0\n'
                                  'rippleFilter.gridZ         =  0\n'
                                  'rippleFilter.interpolate   =  false\n'
                                  '\n'
                                  '\n'
                                  '# S+C finder\n'
                                  '\n'
                                  'scfind.enable              =  true\n'
                                  'scfind.kernelsXY           =  0, 3, 6, 9\n'
                                  'scfind.kernelsZ            =  0, 3, 7, 15\n'
                                  'scfind.threshold           =  3.8\n'
                                  'scfind.replacement         =  2.0\n'
                                  'scfind.statistic           =  mad\n'
                                  'scfind.fluxRange           =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Threshold finder\n'
                                  '\n'
                                  'threshold.enable           =  false\n'
                                  'threshold.threshold        =  5.0\n'
                                  'threshold.mode             =  relative\n'
                                  'threshold.statistic        =  mad\n'
                                  'threshold.fluxRange        =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Linker\n'
                                  '\n'
                                  'linker.enable              =  true\n'
                                  'linker.radiusXY            =  2\n'
                                  'linker.radiusZ             =  3\n'
                                  'linker.minSizeXY           =  5\n'
                                  'linker.minSizeZ            =  5\n'
                                  'linker.maxSizeXY           =  0\n'
                                  'linker.maxSizeZ            =  0\n'
                                  'linker.minPixels           =  0\n'
                                  'linker.maxPixels           =  0\n'
                                  'linker.minFill             =  0.05\n'
                                  'linker.maxFill             =  0.0\n'
                                  'linker.positivity          =  false\n'
                                  'linker.keepNegative        =  false\n'
                                  '\n'
                                  '\n'
                                  '# Reliability\n'
                                  '\n'
                                  'reliability.enable         =  true\n'
                                  'reliability.parameters     =  peak, sum, mean\n'
                                  'reliability.threshold      =  0.9\n'
                                  'reliability.scaleKernel    =  0.3\n'
                                  'reliability.minSNR         =  6.0\n'
                                  'reliability.minPixels      =  150\n'
                                  'reliability.autoKernel     =  true\n'
                                  'reliability.iterations     =  50\n'
                                  'reliability.tolerance      =  0.05\n'
                                  'reliability.catalog        =  \n'
                                  'reliability.plot           =  true\n'
                                  'reliability.plotExtra      =  false\n'
                                  'reliability.debug          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Mask dilation\n'
                                  '\n'
                                  'dilation.enable            =  false\n'
                                  'dilation.iterationsXY      =  10\n'
                                  'dilation.iterationsZ       =  5\n'
                                  'dilation.threshold         =  0.001\n'
                                  '\n'
                                  '\n'
                                  '# Parameterisation\n'
                                  '\n'
                                  'parameter.enable           =  true\n'
                                  'parameter.wcs              =  true\n'
                                  'parameter.physical         =  true\n'
                                  'parameter.prefix           =  SoFiA\n'
                                  'parameter.offset           =  false\n'
                                  '\n'
                                  '\n'
                                  '# Output\n'
                                  '\n'
                                  'output.directory           =  \n'
                                  'output.filename            =  \n'
                                  'output.writeCatASCII       =  true\n'
                                  'output.writeCatXML         =  true\n'
                                  'output.writeCatSQL         =  false\n'
                                  'output.writeKarma          =  false\n'
                                  'output.writeNoise          =  false\n'
                                  'output.writeFiltered       =  false\n'
                                  'output.writeMask           =  true\n'
                                  'output.writeMask2d         =  true\n'
                                  'output.writeRawMask        =  false\n'
                                  'output.writeMoments        =  true\n'
                                  'output.writeCubelets       =  true\n'
                                  'output.writePV             =  true\n'
                                  'output.marginAperSpec      =  10\n'
                                  'output.marginCubelets      =  10\n'
                                  'output.thresholdMom12      =  0.0\n'
                                  'output.overwrite           =  true\n',
                 'command': ''},
                {'software_id': 'SIP',
                 'mode': 'absorption',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_sip.log',
                 'log_content': '2025-09-04 10:17:13,298 | INFO | image_pipeline: - '
                                '*****************************************************************\n'
                                '2025-09-04 10:17:13,298 | INFO | image_pipeline: - \tBeginning '
                                'SoFiA-image-pipeline (SIP) 1.3.16.\n'
                                '2025-09-04 10:17:13,298 | INFO | image_pipeline: - \tOffline mode '
                                'requested: will not make ancillary data overlays.\n'
                                '2025-09-04 10:17:13,298 | INFO | image_pipeline: - \tReading '
                                'catalog in ascii format.\n'
                                '2025-09-04 10:17:13,303 | INFO | image_pipeline: - \tCatalog '
                                'generated by SoFiA-2?\n'
                                '2025-09-04 10:17:13,303 | INFO | image_pipeline: - \tAssuming all '
                                'requested sources are associated with CO(1-0) line transition\n'
                                '2025-09-04 10:17:15,004 | INFO | image_pipeline: -  \n'
                                '2025-09-04 10:17:15,005 | INFO | image_pipeline: - \t-Source 1: '
                                'SoFiA J100113.98+021709.7.\n'
                                '2025-09-04 10:17:15,005 | INFO | make_images: - \tStart making '
                                'spatial images.\n'
                                '2025-09-04 10:17:15,006 | INFO | functions: - \t\tFound 2.1 '
                                'arcsec by 1.6 arcsec beam with PA=87.7 deg in primary header.\n'
                                '2025-09-04 10:17:15,007 | WARNING | functions: - \tNo equinox '
                                'information in header; assuming ICRS frame.\n'
                                '2025-09-04 10:17:15,007 | INFO | functions: - \t\tFound LSRK '
                                'reference frame specified in SPECSYS in header.\n'
                                '2025-09-04 10:17:15,007 | INFO | functions: - \t\tFound CTYPE3 '
                                'spectral axis type FREQ in header.\n'
                                '2025-09-04 10:17:15,010 | INFO | make_images: - \tThe first '
                                'contour defined at SNR = [2.0, 3.0] has level = 2.872e+04 (mom0 '
                                'data units).\n'
                                '2025-09-04 10:17:15,012 | INFO | make_images: - \tImage size '
                                'bigger than default. Now 0.24 arcmin\n'
                                '2025-09-04 10:17:15,012 | INFO | make_images: - \tNo user image '
                                'given and offline mode requested. Making radio spectral line '
                                'images.\n'
                                '2025-09-04 10:17:15,013 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom0.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:17:15,013 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_snr.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:17:15,013 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom1.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:17:15,013 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom2.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:17:15,013 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:17:15,013 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv_min.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:17:15,013 | INFO | make_images: - \tDone making '
                                'spatial images.\n'
                                '2025-09-04 10:17:15,014 | INFO | make_spectra: - \tStart making '
                                'spectral profiles\n'
                                '2025-09-04 10:17:15,015 | INFO | functions: - \t\tFound 2.1 '
                                'arcsec by 1.6 arcsec beam with PA=87.7 deg in primary header.\n'
                                '2025-09-04 10:17:15,015 | WARNING | functions: - \tNo equinox '
                                'information in header; assuming ICRS frame.\n'
                                '2025-09-04 10:17:15,015 | INFO | functions: - \t\tFound LSRK '
                                'reference frame specified in SPECSYS in header.\n'
                                '2025-09-04 10:17:15,015 | INFO | functions: - \t\tFound CTYPE3 '
                                'spectral axis type FREQ in header.\n'
                                '2025-09-04 10:17:15,015 | WARNING | make_spectra: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_spec.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:17:15,015 | INFO | make_spectra: - \tUsing '
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_cubelets/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_spec_aperture.txt '
                                'to make aperture spectrum plot.\n'
                                '2025-09-04 10:17:15,015 | WARNING | make_spectra: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_specfull.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:17:15,016 | INFO | make_spectra: - \tDone making '
                                'spectral profiles.\n'
                                '2025-09-04 10:17:15,016 | INFO | image_pipeline: -  \n'
                                '2025-09-04 10:17:15,016 | INFO | image_pipeline: - \tDONE! Made '
                                'images for 1 sources.\n'
                                '2025-09-04 10:17:15,016 | INFO | image_pipeline: - \tCreated log '
                                'file: '
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_sip.log\n'
                                '2025-09-04 10:17:15,016 | INFO | image_pipeline: - '
                                '*****************************************************************\n'
                                '\n',
                 'error': '',
                 'sw_status': 'ok',
                 'sofia_par_changes': {},
                 'sofia_parfile': 'No log file available: ',
                 'command': 'sofia_image_pipeline-c/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_cat.txt-xpng-i0.05-snone-lineCO(1-0)-log/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_sip.log'},
                {'software_id': 'SIP',
                 'mode': 'emission',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_sip.log',
                 'log_content': 'No log file available: '
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_sip.log',
                 'error': 'No valid .txt or .xml catalog for SIP found within the  '
                          '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission  directory.',
                 'sw_status': 'error',
                 'sofia_par_changes': {},
                 'sofia_parfile': 'No log file available: ',
                 'command': ''}],
  'images': [{'type': 'rel',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_rel.eps',
              'description': 'Realibiliy Plot',
              'software-id': 'sofia',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'skellman',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_skellam.eps',
              'description': 'Skellman Plot',
              'software-id': 'sofia',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'mom0',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom0.png',
              'source_id': 1,
              'description': 'Momment 0 image',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'mom1',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom1.png',
              'source_id': 1,
              'description': 'Momment 1 image',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'mom2',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom2.png',
              'source_id': 1,
              'description': 'Momment 2 image',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'spec',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_spec.png',
              'source_id': 1,
              'description': 'Spectrum plot',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'pv',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv.png',
              'source_id': 1,
              'description': 'Position-Velociy (major axis) plot',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'pv_min',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv_min.png',
              'source_id': 1,
              'description': 'Position-Velociy (minoe axis) plot',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'mom8',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/quality_assesment_products/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_QA.png',
              'description': 'Moment 8 image',
              'software-id': 'qa',
              'is_qa': True}],
  'images_grouped': {'sofia': {'absorption': [{'type': 'rel',
                                               'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_rel.eps',
                                               'description': 'Realibiliy Plot',
                                               'software-id': 'sofia',
                                               'mode': 'absorption',
                                               'is_qa': False},
                                              {'type': 'skellman',
                                               'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_skellam.eps',
                                               'description': 'Skellman Plot',
                                               'software-id': 'sofia',
                                               'mode': 'absorption',
                                               'is_qa': False}],
                               'emission': []},
                     'sip': {'absorption': {1: [{'type': 'mom0',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom0.png',
                                                 'source_id': 1,
                                                 'description': 'Momment 0 image',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'mom1',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom1.png',
                                                 'source_id': 1,
                                                 'description': 'Momment 1 image',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'mom2',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom2.png',
                                                 'source_id': 1,
                                                 'description': 'Momment 2 image',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'spec',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_spec.png',
                                                 'source_id': 1,
                                                 'description': 'Spectrum plot',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'pv',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv.png',
                                                 'source_id': 1,
                                                 'description': 'Position-Velociy (major axis) '
                                                                'plot',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'pv_min',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv_min.png',
                                                 'source_id': 1,
                                                 'description': 'Position-Velociy (minoe axis) '
                                                                'plot',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False}]},
                             'emission': {}},
                     'qa': [{'type': 'mom8',
                             'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/quality_assesment_products/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_QA.png',
                             'description': 'Moment 8 image',
                             'software-id': 'qa',
                             'is_qa': True}]}},
 {'input_data': 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor.fits',
  'status': 'ok',
  'softwares': [{'software_id': 'SoFiA-2',
                 'mode': 'absorption',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_logfile.log',
                 'log_content': '____________________________________________________________________________\n'
                                '\n'
                                ' Pipeline started\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Software:  Source Finding Application (SoFiA)\n'
                                '  Version:   2.6.14 (2025-05-14)\n'
                                '  CPU:       12 threads available\n'
                                '  Memory:    12.7 GB total / 6.6 GB free\n'
                                '  Date:      2025-09-04\n'
                                '  Time:      08:16:58 h\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading parameter settings\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Activating SoFiA default parameter settings.\n'
                                '  Loading user-specified parameters.\n'
                                '  - Loading user parameter file: '
                                '/home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID5621.par\n'
                                '  Using 3 out of 12 available CPU threads.\n'
                                '\n'
                                'WARNING: '
                                '┌──────────────────────────────────────────────────────────┐\n'
                                '         │ You have set parameter.physical = true. SoFiA will '
                                'try   │\n'
                                '         │ to convert some parameters to physical units under '
                                'the   │\n'
                                '         │ following fundamental '
                                'assumptions:                       │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The beam information in the FITS header (BMAJ, '
                                'BMIN)  │\n'
                                '         │    is correct and accurate across the entire data '
                                'cube.  │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The spectral channels of the data cube are '
                                'uncorrela- │\n'
                                '         │    ted, i.e. spectral resolution equals channel '
                                'width.   │\n'
                                '         '
                                '│                                                          │\n'
                                '         │ Should any of these assumptions be incorrect then '
                                'the    │\n'
                                '         │ measurement of \n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading data cube\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Opening FITS file '
                                "'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor.fits'.\n"
                                '  Reading FITS data with the following specifications:\n'
                                '    Data type:    -32\n'
                                '    No. of axes:  4\n'
                                '    Axis sizes:   350, 350, 1918\n'
                                '    Region:       0-349, 0-349, 0-1917\n'
                                '    Memory used:  896.3 MB\n'
                                '  Searching for values of infinity.\n'
                                '    No infinite data values found.\n'
                                '  Inverting data cube\n'
                                '\n'
                                '  Elapsed time: 00:00:07 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring global noise level\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Global RMS:  2.255e-03  (using stride of 234)\n'
                                '\n'
                                '  Elapsed time: 00:00:07 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running S+C finder\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using the following parameters:\n'
                                '  - Kernels\n'
                                '    - spatial:        0, 3, 6, 9\n'
                                '    - spectral:       0, 3, 7, 15\n'
                                '  - Flux threshold:   3.8 * rms\n'
                                '  - Noise statistic:  median absolute deviation\n'
                                '  - Flux range:       negative\n'
                                '\n'
                                '  Using a stride of 234 in noise measurement.\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [0]\n'
                                '  Noise level:       2.255e-03\n'
                                '\n'
                                '  Elapsed time: 00:00:08 h\n'
                                '  CPU time:     00:00:07 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [3]\n'
                                '  Noise level:       1.545e-03\n'
                                '\n'
                                '  Elapsed time: 00:00:13 h\n'
                                '  CPU time:     00:00:14 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [7]\n'
                                '  Noise level:       1.038e-03\n'
                                '\n'
                                '  Elapsed time: 00:00:15 h\n'
                                '  CPU time:     00:00:18 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [15]\n'
                                '  Noise level:       7.183e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:16 h\n'
                                '  CPU time:     00:00:21 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [0]\n'
                                '  Noise level:       1.520e-03\n'
                                '\n'
                                '  Elapsed time: 00:00:18 h\n'
                                '  CPU time:     00:00:25 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [3]\n'
                                '  Noise level:       1.046e-03\n'
                                '\n'
                                '  Elapsed time: 00:00:20 h\n'
                                '  CPU time:     00:00:29 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [7]\n'
                                '  Noise level:       7.063e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:21 h\n'
                                '  CPU time:     00:00:33 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [15]\n'
                                '  Noise level:       4.898e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:23 h\n'
                                '  CPU time:     00:00:37 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [0]\n'
                                '  Noise level:       9.906e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:24 h\n'
                                '  CPU time:     00:00:39 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [3]\n'
                                '  Noise level:       6.883e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:26 h\n'
                                '  CPU time:     00:00:43 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [7]\n'
                                '  Noise level:       4.645e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:27 h\n'
                                '  CPU time:     00:00:46 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [15]\n'
                                '  Noise level:       3.223e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:29 h\n'
                                '  CPU time:     00:00:49 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [0]\n'
                                '  Noise level:       5.970e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:30 h\n'
                                '  CPU time:     00:00:52 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [3]\n'
                                '  Noise level:       4.203e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:31 h\n'
                                '  CPU time:     00:00:56 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [7]\n'
                                '  Noise level:       2.863e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:33 h\n'
                                '  CPU time:     00:00:59 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [15]\n'
                                '  Noise level:       1.985e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:35 h\n'
                                '  CPU time:     00:01:03 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating source mask\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  5045877 pixels detected by source finder (2.148%).\n'
                                '\n'
                                '  Elapsed time: 00:00:35 h\n'
                                '  CPU time:     00:01:04 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running Linker\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Linker settings:\n'
                                '   - Merging radii:   2, 2, 3\n'
                                '   - Minimum size:    5 x 5 x 5\n'
                                '   - Min/max fill:    5.0%, 0.0%\n'
                                '   - Keep negative:   yes\n'
                                '\n'
                                '  Linker status:\n'
                                '   - No. of objects:  2865\n'
                                '   - Memory usage:    383.31 kB\n'
                                '\n'
                                '\n'
                                '  Elapsed time: 00:00:37 h\n'
                                '  CPU time:     00:01:06 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring reliability\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using 3D parameter space:\n'
                                '   - peak\n'
                                '   - sum\n'
                                '   - mean\n'
                                '  Found 1400 positive and 1465 negative sources.\n'
                                '  Retaining all negative detections.\n'
                                '  Using auto-kernel feature.\n'
                                '    Iter.  1: kernel = 0.100, median = 0.749\n'
                                '    Iter.  2: kernel = 0.200, median = 0.394\n'
                                '    Iter.  3: kernel = 0.240, median = 0.337\n'
                                '    Iter.  4: kernel = 0.280, median = 0.310\n'
                                '    Iter.  5: kernel = 0.320, median = 0.275\n'
                                '    Iter.  6: kernel = 0.360, median = 0.258\n'
                                '    Iter.  7: kernel = 0.400, median = 0.249\n'
                                '    Iter.  8: kernel = 0.440, median = 0.241\n'
                                '    Iter.  9: kernel = 0.480, median = 0.223\n'
                                '    Iter. 10: kernel = 0.520, median = 0.204\n'
                                '    Iter. 11: kernel = 0.560, median = 0.216\n'
                                '    Iter. 12: kernel = 0.600, median = 0.210\n'
                                '    Iter. 13: kernel = 0.640, median = 0.212\n'
                                '    Iter. 14: kernel = 0.680, median = 0.219\n'
                                '    Iter. 15: kernel = 0.720, median = 0.218\n'
                                '    Iter. 16: kernel = 0.760, median = 0.226\n'
                                '    Iter. 17: kernel = 0.800, median = 0.239\n'
                                '    Iter. 18: kernel = 0.840, median = 0.241\n'
                                '    Iter. 19: kernel = 0.880, median = 0.257\n'
                                '    Iter. 20: kernel = 0.920, median = 0.272\n'
                                '    Iter. 21: kernel = 0.960, median = 0.284\n'
                                '    Iter. 22: kernel = 1.000, median = 0.304\n'
                                '    Iter. 23: kernel = 1.040, median = 0.321\n'
                                '    Iter. 24: kernel = 1.080, median = 0.341\n'
                                '    Iter. 25: kernel = 1.120, median = 0.354\n'
                                '    Iter. 26: kernel = 1.160, median = 0.377\n'
                                '    Iter. 27: kernel = 1.200, median = 0.396\n'
                                '    Iter. 28: kernel = 1.240, median = 0.415\n'
                                '    Iter. 29: kernel = 1.280, median = 0.437\n'
                                '    Iter. 30: kernel = 1.320, median = 0.448\n'
                                '    Iter. 31: kernel = 1.360, median = 0.470\n'
                                '    Iter. 32: kernel = 1.400, median = 0.492\n'
                                '    Iter. 33: kernel = 1.440, median = 0.512\n'
                                '    Iter. 34: kernel = 1.540, median = 0.559\n'
                                '    Iter. 35: kernel = 1.640, median = 0.602\n'
                                '    Iter. 36: kernel = 1.740, median = 0.642\n'
                                '    Iter. 37: kernel = 1.840, median = 0.684\n'
                                '    Iter. 38: kernel = 1.940, median = 0.722\n'
                                '    Iter. 39: kernel = 2.040, median = 0.758\n'
                                '    Iter. 40: kernel = 2.140, median = 0.791\n'
                                '    Iter. 41: kernel = 2.240, median = 0.821\n'
                                '    Iter. 42: kernel = 2.340, median = 0.849\n'
                                '    Iter. 43: kernel = 2.440, median = 0.874\n'
                                '    Iter. 44: kernel = 2.540, median = 0.897\n'
                                '    Iter. 45: kernel = 2.640, median = 0.918\n'
                                '    Iter. 46: kernel = 2.740, median = 0.937\n'
                                '    Iter. 47: kernel = 2.840, median = 0.955\n'
                                '    Iter. 48: kernel = 2.940, median = 0.970\n'
                                '    Iter. 49: kernel = 3.040, median = 0.985\n'
                                '    Iter. 50: kernel = 3.140, median = 0.998\n'
                                'WARNING: Auto-kernel failed to converge, defaulting to kernel '
                                'scale of 0.300.\n'
                                '  \n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_rel.eps\n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_skellam.eps\n'
                                '  2 reliable sources found.\n'
                                '\n'
                                '  Elapsed time: 00:00:41 h\n'
                                '  CPU time:     00:01:16 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating initial catalogue\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Initial source catalogue created.\n'
                                '\n'
                                '  Elapsed time: 00:00:41 h\n'
                                '  CPU time:     00:01:16 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring source parameters\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Found 2 sources in need of parameterisation.\n'
                                '  Assuming beam size of 6.4 x 5.1 pixels.\n'
                                '\n'
                                '  Attempting to measure parameters in physical units.\n'
                                '\n'
                                '  Elapsed time: 00:00:41 h\n'
                                '  CPU time:     00:01:16 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating cubelets\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Flux threshold (moment 1 and 2): 0.00e+00\n'
                                '  Assuming beam size of 6.4 x 5.1 pixels.\n'
                                '\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_cube.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mask.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom0.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom1.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom2.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_chan.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_snr.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_mask.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min_mask.fits\n'
                                '  Creating text file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec.txt\n'
                                '  Creating text file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec_aperture.txt\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_cube.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mask.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom0.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom1.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom2.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_chan.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_snr.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv_min.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv_mask.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv_min_mask.fits\n'
                                '  Creating text file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_spec.txt\n'
                                '  Creating text file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_spec_aperture.txt\n'
                                '\n'
                                '  Elapsed time: 00:00:41 h\n'
                                '  CPU time:     00:01:16 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating moment maps\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mom0.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mom1.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mom2.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_chan.fits\n'
                                '\n'
                                '  Elapsed time: 00:00:41 h\n'
                                '  CPU time:     00:01:17 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Writing mask cube\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mask-2d.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mask.fits\n'
                                '\n'
                                '  Elapsed time: 00:00:46 h\n'
                                '  CPU time:     00:01:26 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Writing source catalogue\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Writing ASCII file:   '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cat.txt\n'
                                '  Writing VOTable file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cat.xml\n'
                                '\n'
                                '  Elapsed time: 00:00:46 h\n'
                                '  CPU time:     00:01:26 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Pipeline finished\n'
                                '____________________________________________________________________________\n'
                                '\n',
                 'error': '',
                 'sw_status': 'ok',
                 'sofia_par_changes': {'pipeline.threads': '3',
                                       'input.data': 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor.fits',
                                       'input.invert': 'true',
                                       'output.directory': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption'},
                 'sofia_parfile': '# SoFiA 2 parameter file for the official SoFiA test datacube\n'
                                  '\n'
                                  '\n'
                                  '# Global settings\n'
                                  '\n'
                                  'pipeline.verbose           =  false\n'
                                  'pipeline.pedantic          =  true\n'
                                  'pipeline.threads           =  0\n'
                                  '\n'
                                  '\n'
                                  '# Input\n'
                                  '\n'
                                  'input.data                 =  sofia_test_datacube.test\n'
                                  'input.primaryBeam          =  \n'
                                  'input.region               =  \n'
                                  'input.gain                 =  \n'
                                  'input.noise                =  \n'
                                  'input.weights              =  \n'
                                  'input.mask                 =  \n'
                                  'input.invert               =  falseee\n'
                                  '\n'
                                  '\n'
                                  '# Flagging\n'
                                  '\n'
                                  'flag.region                =  \n'
                                  'flag.catalog               =  \n'
                                  'flag.radius                =  5\n'
                                  'flag.auto                  =  false\n'
                                  'flag.threshold             =  5.0\n'
                                  'flag.log                   =  false\n'
                                  'flag.cube                  =  \n'
                                  '\n'
                                  '\n'
                                  '# Continuum subtraction\n'
                                  '\n'
                                  'contsub.enable             =  false\n'
                                  'contsub.order              =  0\n'
                                  'contsub.threshold          =  2.0\n'
                                  'contsub.shift              =  4\n'
                                  'contsub.padding            =  3\n'
                                  '\n'
                                  '\n'
                                  '# Noise scaling\n'
                                  '\n'
                                  'scaleNoise.enable          =  false\n'
                                  'scaleNoise.mode            =  local\n'
                                  'scaleNoise.statistic       =  mad\n'
                                  'scaleNoise.fluxRange       =  negative\n'
                                  'scaleNoise.windowXY        =  31\n'
                                  'scaleNoise.windowZ         =  31\n'
                                  'scaleNoise.gridXY          =  0\n'
                                  'scaleNoise.gridZ           =  0\n'
                                  'scaleNoise.interpolate     =  false\n'
                                  'scaleNoise.scfind          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Ripple filter\n'
                                  '\n'
                                  'rippleFilter.enable        =  false\n'
                                  'rippleFilter.statistic     =  median\n'
                                  'rippleFilter.windowXY      =  31\n'
                                  'rippleFilter.windowZ       =  15\n'
                                  'rippleFilter.gridXY        =  0\n'
                                  'rippleFilter.gridZ         =  0\n'
                                  'rippleFilter.interpolate   =  false\n'
                                  '\n'
                                  '\n'
                                  '# S+C finder\n'
                                  '\n'
                                  'scfind.enable              =  true\n'
                                  'scfind.kernelsXY           =  0, 3, 6, 9\n'
                                  'scfind.kernelsZ            =  0, 3, 7, 15\n'
                                  'scfind.threshold           =  3.8\n'
                                  'scfind.replacement         =  2.0\n'
                                  'scfind.statistic           =  mad\n'
                                  'scfind.fluxRange           =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Threshold finder\n'
                                  '\n'
                                  'threshold.enable           =  false\n'
                                  'threshold.threshold        =  5.0\n'
                                  'threshold.mode             =  relative\n'
                                  'threshold.statistic        =  mad\n'
                                  'threshold.fluxRange        =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Linker\n'
                                  '\n'
                                  'linker.enable              =  true\n'
                                  'linker.radiusXY            =  2\n'
                                  'linker.radiusZ             =  3\n'
                                  'linker.minSizeXY           =  5\n'
                                  'linker.minSizeZ            =  5\n'
                                  'linker.maxSizeXY           =  0\n'
                                  'linker.maxSizeZ            =  0\n'
                                  'linker.minPixels           =  0\n'
                                  'linker.maxPixels           =  0\n'
                                  'linker.minFill             =  0.05\n'
                                  'linker.maxFill             =  0.0\n'
                                  'linker.positivity          =  false\n'
                                  'linker.keepNegative        =  false\n'
                                  '\n'
                                  '\n'
                                  '# Reliability\n'
                                  '\n'
                                  'reliability.enable         =  true\n'
                                  'reliability.parameters     =  peak, sum, mean\n'
                                  'reliability.threshold      =  0.9\n'
                                  'reliability.scaleKernel    =  0.3\n'
                                  'reliability.minSNR         =  6.0\n'
                                  'reliability.minPixels      =  150\n'
                                  'reliability.autoKernel     =  true\n'
                                  'reliability.iterations     =  50\n'
                                  'reliability.tolerance      =  0.05\n'
                                  'reliability.catalog        =  \n'
                                  'reliability.plot           =  true\n'
                                  'reliability.plotExtra      =  false\n'
                                  'reliability.debug          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Mask dilation\n'
                                  '\n'
                                  'dilation.enable            =  false\n'
                                  'dilation.iterationsXY      =  10\n'
                                  'dilation.iterationsZ       =  5\n'
                                  'dilation.threshold         =  0.001\n'
                                  '\n'
                                  '\n'
                                  '# Parameterisation\n'
                                  '\n'
                                  'parameter.enable           =  true\n'
                                  'parameter.wcs              =  true\n'
                                  'parameter.physical         =  true\n'
                                  'parameter.prefix           =  SoFiA\n'
                                  'parameter.offset           =  false\n'
                                  '\n'
                                  '\n'
                                  '# Output\n'
                                  '\n'
                                  'output.directory           =  \n'
                                  'output.filename            =  \n'
                                  'output.writeCatASCII       =  true\n'
                                  'output.writeCatXML         =  true\n'
                                  'output.writeCatSQL         =  false\n'
                                  'output.writeKarma          =  false\n'
                                  'output.writeNoise          =  false\n'
                                  'output.writeFiltered       =  false\n'
                                  'output.writeMask           =  true\n'
                                  'output.writeMask2d         =  true\n'
                                  'output.writeRawMask        =  false\n'
                                  'output.writeMoments        =  true\n'
                                  'output.writeCubelets       =  true\n'
                                  'output.writePV             =  true\n'
                                  'output.marginAperSpec      =  10\n'
                                  'output.marginCubelets      =  10\n'
                                  'output.thresholdMom12      =  0.0\n'
                                  'output.overwrite           =  true\n',
                 'command': ''},
                {'software_id': 'SoFiA-2',
                 'mode': 'emission',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_logfile.log',
                 'log_content': '____________________________________________________________________________\n'
                                '\n'
                                ' Pipeline started\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Software:  Source Finding Application (SoFiA)\n'
                                '  Version:   2.6.14 (2025-05-14)\n'
                                '  CPU:       12 threads available\n'
                                '  Memory:    12.7 GB total / 4.1 GB free\n'
                                '  Date:      2025-09-04\n'
                                '  Time:      08:17:50 h\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading parameter settings\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Activating SoFiA default parameter settings.\n'
                                '  Loading user-specified parameters.\n'
                                '  - Loading user parameter file: '
                                '/home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID5621.par\n'
                                '  Using 3 out of 12 available CPU threads.\n'
                                '\n'
                                'WARNING: '
                                '┌──────────────────────────────────────────────────────────┐\n'
                                '         │ You have set parameter.physical = true. SoFiA will '
                                'try   │\n'
                                '         │ to convert some parameters to physical units under '
                                'the   │\n'
                                '         │ following fundamental '
                                'assumptions:                       │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The beam information in the FITS header (BMAJ, '
                                'BMIN)  │\n'
                                '         │    is correct and accurate across the entire data '
                                'cube.  │\n'
                                '         '
                                '│                                                          │\n'
                                '         │  * The spectral channels of the data cube are '
                                'uncorrela- │\n'
                                '         │    ted, i.e. spectral resolution equals channel '
                                'width.   │\n'
                                '         '
                                '│                                                          │\n'
                                '         │ Should any of these assumptions be incorrect then '
                                'the    │\n'
                                '         │ measurement of \n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading data cube\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Opening FITS file '
                                "'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor.fits'.\n"
                                '  Reading FITS data with the following specifications:\n'
                                '    Data type:    -32\n'
                                '    No. of axes:  4\n'
                                '    Axis sizes:   350, 350, 1918\n'
                                '    Region:       0-349, 0-349, 0-1917\n'
                                '    Memory used:  896.3 MB\n'
                                '  Searching for values of infinity.\n'
                                '    No infinite data values found.\n'
                                '\n'
                                '  Elapsed time: 00:00:00 h\n'
                                '  CPU time:     00:00:00 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Loading and applying flag cube\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Opening FITS file '
                                "'/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mask.fits'.\n"
                                '  Reading FITS data with the following specifications:\n'
                                '    Data type:    32\n'
                                '    No. of axes:  3\n'
                                '    Axis sizes:   350, 350, 1918\n'
                                '    Region:       0-349, 0-349, 0-1917\n'
                                '    Memory used:  896.3 MB\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring global noise level\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Global RMS:  2.249e-03  (using stride of 234)\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running S+C finder\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using the following parameters:\n'
                                '  - Kernels\n'
                                '    - spatial:        0, 3, 6, 9\n'
                                '    - spectral:       0, 3, 7, 15\n'
                                '  - Flux threshold:   3.8 * rms\n'
                                '  - Noise statistic:  median absolute deviation\n'
                                '  - Flux range:       negative\n'
                                '\n'
                                '  Using a stride of 234 in noise measurement.\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [0]\n'
                                '  Noise level:       2.249e-03\n'
                                '\n'
                                '  Elapsed time: 00:00:01 h\n'
                                '  CPU time:     00:00:01 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [3]\n'
                                '  Noise level:       1.554e-03\n'
                                '\n'
                                '  Elapsed time: 00:00:02 h\n'
                                '  CPU time:     00:00:04 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [7]\n'
                                '  Noise level:       1.052e-03\n'
                                '\n'
                                '  Elapsed time: 00:00:04 h\n'
                                '  CPU time:     00:00:06 h\n'
                                '\n'
                                '  Smoothing kernel:  [0.0] x [15]\n'
                                '  Noise level:       7.272e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:05 h\n'
                                '  CPU time:     00:00:08 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [0]\n'
                                '  Noise level:       1.528e-03\n'
                                '\n'
                                '  Elapsed time: 00:00:06 h\n'
                                '  CPU time:     00:00:11 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [3]\n'
                                '  Noise level:       1.058e-03\n'
                                '\n'
                                '  Elapsed time: 00:00:07 h\n'
                                '  CPU time:     00:00:14 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [7]\n'
                                '  Noise level:       7.177e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:09 h\n'
                                '  CPU time:     00:00:17 h\n'
                                '\n'
                                '  Smoothing kernel:  [3.0] x [15]\n'
                                '  Noise level:       4.953e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:10 h\n'
                                '  CPU time:     00:00:21 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [0]\n'
                                '  Noise level:       9.928e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:11 h\n'
                                '  CPU time:     00:00:23 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [3]\n'
                                '  Noise level:       6.963e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:12 h\n'
                                '  CPU time:     00:00:26 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [7]\n'
                                '  Noise level:       4.738e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:14 h\n'
                                '  CPU time:     00:00:29 h\n'
                                '\n'
                                '  Smoothing kernel:  [6.0] x [15]\n'
                                '  Noise level:       3.272e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:15 h\n'
                                '  CPU time:     00:00:33 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [0]\n'
                                '  Noise level:       6.005e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:16 h\n'
                                '  CPU time:     00:00:35 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [3]\n'
                                '  Noise level:       4.236e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:18 h\n'
                                '  CPU time:     00:00:38 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [7]\n'
                                '  Noise level:       2.909e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:19 h\n'
                                '  CPU time:     00:00:42 h\n'
                                '\n'
                                '  Smoothing kernel:  [9.0] x [15]\n'
                                '  Noise level:       2.022e-04\n'
                                '\n'
                                '  Elapsed time: 00:00:21 h\n'
                                '  CPU time:     00:00:46 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating source mask\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  4766842 pixels detected by source finder (2.029%).\n'
                                '\n'
                                '  Elapsed time: 00:00:21 h\n'
                                '  CPU time:     00:00:46 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Running Linker\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Linker settings:\n'
                                '   - Merging radii:   2, 2, 3\n'
                                '   - Minimum size:    5 x 5 x 5\n'
                                '   - Min/max fill:    5.0%, 0.0%\n'
                                '   - Keep negative:   yes\n'
                                '\n'
                                '  Linker status:\n'
                                '   - No. of objects:  2898\n'
                                '   - Memory usage:    387.72 kB\n'
                                '\n'
                                '\n'
                                '  Elapsed time: 00:00:24 h\n'
                                '  CPU time:     00:00:49 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring reliability\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Using 3D parameter space:\n'
                                '   - peak\n'
                                '   - sum\n'
                                '   - mean\n'
                                '  Found 1468 positive and 1430 negative sources.\n'
                                '  Retaining all negative detections.\n'
                                '  Using auto-kernel feature.\n'
                                '    Iter.  1: kernel = 0.100, median = 0.719\n'
                                '    Iter.  2: kernel = 0.200, median = 0.331\n'
                                '    Iter.  3: kernel = 0.240, median = 0.221\n'
                                '    Iter.  4: kernel = 0.280, median = 0.136\n'
                                '    Iter.  5: kernel = 0.320, median = 0.074\n'
                                '    Iter.  6: kernel = 0.360, median = 0.037\n'
                                '  Converged to scale_kernel = 0.360 after 6 iterations.\n'
                                '  \n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_rel.eps\n'
                                '  Creating postscript file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_skellam.eps\n'
                                '  1 reliable source found.\n'
                                '\n'
                                '  Elapsed time: 00:00:24 h\n'
                                '  CPU time:     00:00:50 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating initial catalogue\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Initial source catalogue created.\n'
                                '\n'
                                '  Elapsed time: 00:00:24 h\n'
                                '  CPU time:     00:00:50 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Reloading data cube for parameterisation\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Opening FITS file '
                                "'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor.fits'.\n"
                                '  Reading FITS data with the following specifications:\n'
                                '    Data type:    -32\n'
                                '    No. of axes:  4\n'
                                '    Axis sizes:   350, 350, 1918\n'
                                '    Region:       0-349, 0-349, 0-1917\n'
                                '    Memory used:  896.3 MB\n'
                                '\n'
                                '  Elapsed time: 00:00:24 h\n'
                                '  CPU time:     00:00:50 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Measuring source parameters\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Found 1 source in need of parameterisation.\n'
                                '  Assuming beam size of 6.4 x 5.1 pixels.\n'
                                '\n'
                                '  Attempting to measure parameters in physical units.\n'
                                '\n'
                                '  Elapsed time: 00:00:24 h\n'
                                '  CPU time:     00:00:50 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating cubelets\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Flux threshold (moment 1 and 2): 0.00e+00\n'
                                '  Assuming beam size of 6.4 x 5.1 pixels.\n'
                                '\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_cube.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mask.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom0.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom1.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom2.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_chan.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_snr.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_mask.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min_mask.fits\n'
                                '  Creating text file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec.txt\n'
                                '  Creating text file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec_aperture.txt\n'
                                '\n'
                                '  Elapsed time: 00:00:24 h\n'
                                '  CPU time:     00:00:50 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Creating moment maps\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mom0.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mom1.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mom2.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_chan.fits\n'
                                '\n'
                                '  Elapsed time: 00:00:25 h\n'
                                '  CPU time:     00:00:51 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Writing mask cube\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mask-2d.fits\n'
                                '  Creating FITS file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mask.fits\n'
                                '\n'
                                '  Elapsed time: 00:00:28 h\n'
                                '  CPU time:     00:00:59 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Writing source catalogue\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                '  Writing ASCII file:   '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cat.txt\n'
                                '  Writing VOTable file: '
                                'member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cat.xml\n'
                                '\n'
                                '  Elapsed time: 00:00:28 h\n'
                                '  CPU time:     00:00:59 h\n'
                                '\n'
                                '____________________________________________________________________________\n'
                                '\n'
                                ' Pipeline finished\n'
                                '____________________________________________________________________________\n'
                                '\n',
                 'error': '',
                 'sw_status': 'ok',
                 'sofia_par_changes': {'pipeline.threads': '3',
                                       'input.invert': 'false',
                                       'flag.cube': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mask.fits',
                                       'output.directory': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission',
                                       'input.data': 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor.fits'},
                 'sofia_parfile': '# SoFiA 2 parameter file for the official SoFiA test datacube\n'
                                  '\n'
                                  '\n'
                                  '# Global settings\n'
                                  '\n'
                                  'pipeline.verbose           =  false\n'
                                  'pipeline.pedantic          =  true\n'
                                  'pipeline.threads           =  0\n'
                                  '\n'
                                  '\n'
                                  '# Input\n'
                                  '\n'
                                  '#input.data                 =  sofia_test_datacube.test\n'
                                  '#input.primaryBeam          =  \n'
                                  'input.region               =  \n'
                                  'input.gain                 =  \n'
                                  'input.noise                =  \n'
                                  'input.weights              =  \n'
                                  'input.mask                 =  \n'
                                  'input.invert               =   \n'
                                  '\n'
                                  '\n'
                                  '# Flagging\n'
                                  '\n'
                                  'flag.region                =  \n'
                                  'flag.catalog               =  \n'
                                  'flag.radius                =  5\n'
                                  'flag.auto                  =  false\n'
                                  'flag.threshold             =  5.0\n'
                                  'flag.log                   =  false\n'
                                  'flag.cube                  =  \n'
                                  '\n'
                                  '\n'
                                  '# Continuum subtraction\n'
                                  '\n'
                                  'contsub.enable             =  false\n'
                                  'contsub.order              =  0\n'
                                  'contsub.threshold          =  2.0\n'
                                  'contsub.shift              =  4\n'
                                  'contsub.padding            =  3\n'
                                  '\n'
                                  '\n'
                                  '# Noise scaling\n'
                                  '\n'
                                  'scaleNoise.enable          =  false\n'
                                  'scaleNoise.mode            =  local\n'
                                  'scaleNoise.statistic       =  mad\n'
                                  'scaleNoise.fluxRange       =  negative\n'
                                  'scaleNoise.windowXY        =  31\n'
                                  'scaleNoise.windowZ         =  31\n'
                                  'scaleNoise.gridXY          =  0\n'
                                  'scaleNoise.gridZ           =  0\n'
                                  'scaleNoise.interpolate     =  false\n'
                                  'scaleNoise.scfind          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Ripple filter\n'
                                  '\n'
                                  'rippleFilter.enable        =  false\n'
                                  'rippleFilter.statistic     =  median\n'
                                  'rippleFilter.windowXY      =  31\n'
                                  'rippleFilter.windowZ       =  15\n'
                                  'rippleFilter.gridXY        =  0\n'
                                  'rippleFilter.gridZ         =  0\n'
                                  'rippleFilter.interpolate   =  false\n'
                                  '\n'
                                  '\n'
                                  '# S+C finder\n'
                                  '\n'
                                  'scfind.enable              =  true\n'
                                  'scfind.kernelsXY           =  0, 3, 6, 9\n'
                                  'scfind.kernelsZ            =  0, 3, 7, 15\n'
                                  'scfind.threshold           =  3.8\n'
                                  'scfind.replacement         =  2.0\n'
                                  'scfind.statistic           =  mad\n'
                                  'scfind.fluxRange           =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Threshold finder\n'
                                  '\n'
                                  'threshold.enable           =  false\n'
                                  'threshold.threshold        =  5.0\n'
                                  'threshold.mode             =  relative\n'
                                  'threshold.statistic        =  mad\n'
                                  'threshold.fluxRange        =  negative\n'
                                  '\n'
                                  '\n'
                                  '# Linker\n'
                                  '\n'
                                  'linker.enable              =  true\n'
                                  'linker.radiusXY            =  2\n'
                                  'linker.radiusZ             =  3\n'
                                  'linker.minSizeXY           =  5\n'
                                  'linker.minSizeZ            =  5\n'
                                  'linker.maxSizeXY           =  0\n'
                                  'linker.maxSizeZ            =  0\n'
                                  'linker.minPixels           =  0\n'
                                  'linker.maxPixels           =  0\n'
                                  'linker.minFill             =  0.05\n'
                                  'linker.maxFill             =  0.0\n'
                                  'linker.positivity          =  false\n'
                                  'linker.keepNegative        =  false\n'
                                  '\n'
                                  '\n'
                                  '# Reliability\n'
                                  '\n'
                                  'reliability.enable         =  true\n'
                                  'reliability.parameters     =  peak, sum, mean\n'
                                  'reliability.threshold      =  0.9\n'
                                  'reliability.scaleKernel    =  0.3\n'
                                  'reliability.minSNR         =  6.0\n'
                                  'reliability.minPixels      =  150\n'
                                  'reliability.autoKernel     =  true\n'
                                  'reliability.iterations     =  50\n'
                                  'reliability.tolerance      =  0.05\n'
                                  'reliability.catalog        =  \n'
                                  'reliability.plot           =  true\n'
                                  'reliability.plotExtra      =  false\n'
                                  'reliability.debug          =  false\n'
                                  '\n'
                                  '\n'
                                  '# Mask dilation\n'
                                  '\n'
                                  'dilation.enable            =  false\n'
                                  'dilation.iterationsXY      =  10\n'
                                  'dilation.iterationsZ       =  5\n'
                                  'dilation.threshold         =  0.001\n'
                                  '\n'
                                  '\n'
                                  '# Parameterisation\n'
                                  '\n'
                                  'parameter.enable           =  true\n'
                                  'parameter.wcs              =  true\n'
                                  'parameter.physical         =  true\n'
                                  'parameter.prefix           =  SoFiA\n'
                                  'parameter.offset           =  false\n'
                                  '\n'
                                  '\n'
                                  '# Output\n'
                                  '\n'
                                  'output.directory           =  \n'
                                  'output.filename            =  \n'
                                  'output.writeCatASCII       =  true\n'
                                  'output.writeCatXML         =  true\n'
                                  'output.writeCatSQL         =  false\n'
                                  'output.writeKarma          =  false\n'
                                  'output.writeNoise          =  false\n'
                                  'output.writeFiltered       =  false\n'
                                  'output.writeMask           =  true\n'
                                  'output.writeMask2d         =  true\n'
                                  'output.writeRawMask        =  false\n'
                                  'output.writeMoments        =  true\n'
                                  'output.writeCubelets       =  true\n'
                                  'output.writePV             =  true\n'
                                  'output.marginAperSpec      =  10\n'
                                  'output.marginCubelets      =  10\n'
                                  'output.thresholdMom12      =  0.0\n'
                                  'output.overwrite           =  true\n',
                 'command': ''},
                {'software_id': 'SIP',
                 'mode': 'absorption',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_sip.log',
                 'log_content': '2025-09-04 10:18:22,261 | INFO | image_pipeline: - '
                                '*****************************************************************\n'
                                '2025-09-04 10:18:22,261 | INFO | image_pipeline: - \tBeginning '
                                'SoFiA-image-pipeline (SIP) 1.3.16.\n'
                                '2025-09-04 10:18:22,261 | INFO | image_pipeline: - \tOffline mode '
                                'requested: will not make ancillary data overlays.\n'
                                '2025-09-04 10:18:22,261 | INFO | image_pipeline: - \tReading '
                                'catalog in ascii format.\n'
                                '2025-09-04 10:18:22,265 | INFO | image_pipeline: - \tCatalog '
                                'generated by SoFiA-2?\n'
                                '2025-09-04 10:18:22,266 | INFO | image_pipeline: - \tAssuming all '
                                'requested sources are associated with CO(1-0) line transition\n'
                                '2025-09-04 10:18:23,027 | INFO | image_pipeline: -  \n'
                                '2025-09-04 10:18:23,027 | INFO | image_pipeline: - \t-Source 1: '
                                'SoFiA J100115.97+021748.2.\n'
                                '2025-09-04 10:18:23,027 | INFO | make_images: - \tStart making '
                                'spatial images.\n'
                                '2025-09-04 10:18:23,030 | INFO | functions: - \t\tFound 2.0 '
                                'arcsec by 1.6 arcsec beam with PA=87.3 deg in primary header.\n'
                                '2025-09-04 10:18:23,030 | WARNING | functions: - \tNo equinox '
                                'information in header; assuming ICRS frame.\n'
                                '2025-09-04 10:18:23,030 | INFO | functions: - \t\tFound LSRK '
                                'reference frame specified in SPECSYS in header.\n'
                                '2025-09-04 10:18:23,031 | INFO | functions: - \t\tFound CTYPE3 '
                                'spectral axis type FREQ in header.\n'
                                '2025-09-04 10:18:23,034 | INFO | make_images: - \tThe first '
                                'contour defined at SNR = [2.0, 3.0] has level = 1.065e+04 (mom0 '
                                'data units).\n'
                                '2025-09-04 10:18:23,036 | INFO | make_images: - \tImage size '
                                'bigger than default. Now 0.12 arcmin\n'
                                '2025-09-04 10:18:23,037 | INFO | make_images: - \tNo user image '
                                'given and offline mode requested. Making radio spectral line '
                                'images.\n'
                                '2025-09-04 10:18:23,039 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom0.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,040 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_snr.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,040 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom1.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,040 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom2.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,041 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,041 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,041 | INFO | make_images: - \tDone making '
                                'spatial images.\n'
                                '2025-09-04 10:18:23,041 | INFO | make_spectra: - \tStart making '
                                'spectral profiles\n'
                                '2025-09-04 10:18:23,044 | INFO | functions: - \t\tFound 2.0 '
                                'arcsec by 1.6 arcsec beam with PA=87.3 deg in primary header.\n'
                                '2025-09-04 10:18:23,045 | WARNING | functions: - \tNo equinox '
                                'information in header; assuming ICRS frame.\n'
                                '2025-09-04 10:18:23,045 | INFO | functions: - \t\tFound LSRK '
                                'reference frame specified in SPECSYS in header.\n'
                                '2025-09-04 10:18:23,045 | INFO | functions: - \t\tFound CTYPE3 '
                                'spectral axis type FREQ in header.\n'
                                '2025-09-04 10:18:23,046 | WARNING | make_spectra: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,046 | INFO | make_spectra: - \tUsing '
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cubelets/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec_aperture.txt '
                                'to make aperture spectrum plot.\n'
                                '2025-09-04 10:18:23,046 | WARNING | make_spectra: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_specfull.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,046 | INFO | make_spectra: - \tDone making '
                                'spectral profiles.\n'
                                '2025-09-04 10:18:23,046 | INFO | image_pipeline: -  \n'
                                '2025-09-04 10:18:23,046 | INFO | image_pipeline: - \t-Source 2: '
                                'SoFiA J100114.43+021713.7.\n'
                                '2025-09-04 10:18:23,046 | INFO | make_images: - \tStart making '
                                'spatial images.\n'
                                '2025-09-04 10:18:23,049 | INFO | functions: - \t\tFound 2.0 '
                                'arcsec by 1.6 arcsec beam with PA=87.3 deg in primary header.\n'
                                '2025-09-04 10:18:23,050 | WARNING | functions: - \tNo equinox '
                                'information in header; assuming ICRS frame.\n'
                                '2025-09-04 10:18:23,050 | INFO | functions: - \t\tFound LSRK '
                                'reference frame specified in SPECSYS in header.\n'
                                '2025-09-04 10:18:23,050 | INFO | functions: - \t\tFound CTYPE3 '
                                'spectral axis type FREQ in header.\n'
                                '2025-09-04 10:18:23,054 | INFO | make_images: - \tThe first '
                                'contour defined at SNR = [2.0, 3.0] has level = 1.707e+04 (mom0 '
                                'data units).\n'
                                '2025-09-04 10:18:23,057 | INFO | make_images: - \tImage size '
                                'bigger than default. Now 0.20 arcmin\n'
                                '2025-09-04 10:18:23,058 | INFO | make_images: - \tNo user image '
                                'given and offline mode requested. Making radio spectral line '
                                'images.\n'
                                '2025-09-04 10:18:23,059 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom0.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,060 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_snr.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,060 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom1.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,060 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom2.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,060 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,060 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv_min.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,060 | INFO | make_images: - \tDone making '
                                'spatial images.\n'
                                '2025-09-04 10:18:23,060 | INFO | make_spectra: - \tStart making '
                                'spectral profiles\n'
                                '2025-09-04 10:18:23,061 | INFO | functions: - \t\tFound 2.0 '
                                'arcsec by 1.6 arcsec beam with PA=87.3 deg in primary header.\n'
                                '2025-09-04 10:18:23,062 | WARNING | functions: - \tNo equinox '
                                'information in header; assuming ICRS frame.\n'
                                '2025-09-04 10:18:23,062 | INFO | functions: - \t\tFound LSRK '
                                'reference frame specified in SPECSYS in header.\n'
                                '2025-09-04 10:18:23,062 | INFO | functions: - \t\tFound CTYPE3 '
                                'spectral axis type FREQ in header.\n'
                                '2025-09-04 10:18:23,062 | WARNING | make_spectra: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_spec.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,062 | INFO | make_spectra: - \tUsing '
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cubelets/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_spec_aperture.txt '
                                'to make aperture spectrum plot.\n'
                                '2025-09-04 10:18:23,062 | WARNING | make_spectra: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_specfull.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:23,062 | INFO | make_spectra: - \tDone making '
                                'spectral profiles.\n'
                                '2025-09-04 10:18:23,062 | INFO | image_pipeline: -  \n'
                                '2025-09-04 10:18:23,062 | INFO | image_pipeline: - \tDONE! Made '
                                'images for 2 sources.\n'
                                '2025-09-04 10:18:23,062 | INFO | image_pipeline: - \tCreated log '
                                'file: '
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_sip.log\n'
                                '2025-09-04 10:18:23,062 | INFO | image_pipeline: - '
                                '*****************************************************************\n'
                                '\n',
                 'error': '',
                 'sw_status': 'ok',
                 'sofia_par_changes': {},
                 'sofia_parfile': 'No log file available: ',
                 'command': 'sofia_image_pipeline-c/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cat.txt-xpng-i0.05-snone-lineCO(1-0)-log/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_sip.log'},
                {'software_id': 'SIP',
                 'mode': 'emission',
                 'warning_number': 2,
                 'log_path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_sip.log',
                 'log_content': '2025-09-04 10:18:23,665 | INFO | image_pipeline: - '
                                '*****************************************************************\n'
                                '2025-09-04 10:18:23,666 | INFO | image_pipeline: - \tBeginning '
                                'SoFiA-image-pipeline (SIP) 1.3.16.\n'
                                '2025-09-04 10:18:23,666 | INFO | image_pipeline: - \tOffline mode '
                                'requested: will not make ancillary data overlays.\n'
                                '2025-09-04 10:18:23,666 | INFO | image_pipeline: - \tReading '
                                'catalog in ascii format.\n'
                                '2025-09-04 10:18:23,670 | INFO | image_pipeline: - \tCatalog '
                                'generated by SoFiA-2?\n'
                                '2025-09-04 10:18:23,671 | INFO | image_pipeline: - \tAssuming all '
                                'requested sources are associated with CO(1-0) line transition\n'
                                '2025-09-04 10:18:24,360 | INFO | image_pipeline: -  \n'
                                '2025-09-04 10:18:24,360 | INFO | image_pipeline: - \t-Source 1: '
                                'SoFiA J100117.61+021639.9.\n'
                                '2025-09-04 10:18:24,360 | INFO | make_images: - \tStart making '
                                'spatial images.\n'
                                '2025-09-04 10:18:24,362 | INFO | functions: - \t\tFound 2.0 '
                                'arcsec by 1.6 arcsec beam with PA=87.3 deg in primary header.\n'
                                '2025-09-04 10:18:24,362 | WARNING | functions: - \tNo equinox '
                                'information in header; assuming ICRS frame.\n'
                                '2025-09-04 10:18:24,363 | INFO | functions: - \t\tFound LSRK '
                                'reference frame specified in SPECSYS in header.\n'
                                '2025-09-04 10:18:24,363 | INFO | functions: - \t\tFound CTYPE3 '
                                'spectral axis type FREQ in header.\n'
                                '2025-09-04 10:18:24,365 | INFO | make_images: - \tThe first '
                                'contour defined at SNR = [2.0, 3.0] has level = 1.393e+04 (mom0 '
                                'data units).\n'
                                '2025-09-04 10:18:24,366 | INFO | make_images: - \tImage size '
                                'bigger than default. Now 0.20 arcmin\n'
                                '2025-09-04 10:18:24,367 | INFO | make_images: - \tNo user image '
                                'given and offline mode requested. Making radio spectral line '
                                'images.\n'
                                '2025-09-04 10:18:24,367 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom0.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:24,367 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_snr.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:24,367 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom1.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:24,368 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom2.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:24,368 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:24,368 | WARNING | make_images: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:24,368 | INFO | make_images: - \tDone making '
                                'spatial images.\n'
                                '2025-09-04 10:18:24,368 | INFO | make_spectra: - \tStart making '
                                'spectral profiles\n'
                                '2025-09-04 10:18:24,369 | INFO | functions: - \t\tFound 2.0 '
                                'arcsec by 1.6 arcsec beam with PA=87.3 deg in primary header.\n'
                                '2025-09-04 10:18:24,369 | WARNING | functions: - \tNo equinox '
                                'information in header; assuming ICRS frame.\n'
                                '2025-09-04 10:18:24,369 | INFO | functions: - \t\tFound LSRK '
                                'reference frame specified in SPECSYS in header.\n'
                                '2025-09-04 10:18:24,369 | INFO | functions: - \t\tFound CTYPE3 '
                                'spectral axis type FREQ in header.\n'
                                '2025-09-04 10:18:24,369 | WARNING | make_spectra: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:24,369 | INFO | make_spectra: - \tUsing '
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cubelets/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec_aperture.txt '
                                'to make aperture spectrum plot.\n'
                                '2025-09-04 10:18:24,369 | WARNING | make_spectra: - \t'
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_specfull.png '
                                'already exists. Will not overwrite.\n'
                                '2025-09-04 10:18:24,370 | INFO | make_spectra: - \tDone making '
                                'spectral profiles.\n'
                                '2025-09-04 10:18:24,370 | INFO | image_pipeline: -  \n'
                                '2025-09-04 10:18:24,370 | INFO | image_pipeline: - \tDONE! Made '
                                'images for 1 sources.\n'
                                '2025-09-04 10:18:24,370 | INFO | image_pipeline: - \tCreated log '
                                'file: '
                                '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_sip.log\n'
                                '2025-09-04 10:18:24,370 | INFO | image_pipeline: - '
                                '*****************************************************************\n'
                                '\n',
                 'error': '',
                 'sw_status': 'ok',
                 'sofia_par_changes': {},
                 'sofia_parfile': 'No log file available: ',
                 'command': 'sofia_image_pipeline-c/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cat.txt-xpng-i0.05-snone-lineCO(1-0)-log/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_sip.log'}],
  'images': [{'type': 'rel',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_rel.eps',
              'description': 'Realibiliy Plot',
              'software-id': 'sofia',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'skellman',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_skellam.eps',
              'description': 'Skellman Plot',
              'software-id': 'sofia',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'rel',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_rel.eps',
              'description': 'Realibiliy Plot',
              'software-id': 'sofia',
              'mode': 'emission',
              'is_qa': False},
             {'type': 'skellman',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_skellam.eps',
              'description': 'Skellman Plot',
              'software-id': 'sofia',
              'mode': 'emission',
              'is_qa': False},
             {'type': 'mom0',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom0.png',
              'source_id': 1,
              'description': 'Momment 0 image',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'mom1',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom1.png',
              'source_id': 1,
              'description': 'Momment 1 image',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'mom2',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom2.png',
              'source_id': 1,
              'description': 'Momment 2 image',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'spec',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec.png',
              'source_id': 1,
              'description': 'Spectrum plot',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'pv',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv.png',
              'source_id': 1,
              'description': 'Position-Velociy (major axis) plot',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'pv_min',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min.png',
              'source_id': 1,
              'description': 'Position-Velociy (minoe axis) plot',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'mom0',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom0.png',
              'source_id': 2,
              'description': 'Momment 0 image',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'mom1',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom1.png',
              'source_id': 2,
              'description': 'Momment 1 image',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'mom2',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom2.png',
              'source_id': 2,
              'description': 'Momment 2 image',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'spec',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_spec.png',
              'source_id': 2,
              'description': 'Spectrum plot',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'pv',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv.png',
              'source_id': 2,
              'description': 'Position-Velociy (major axis) plot',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'pv_min',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv_min.png',
              'source_id': 2,
              'description': 'Position-Velociy (minoe axis) plot',
              'software-id': 'sip',
              'mode': 'absorption',
              'is_qa': False},
             {'type': 'mom0',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom0.png',
              'source_id': 1,
              'description': 'Momment 0 image',
              'software-id': 'sip',
              'mode': 'emission',
              'is_qa': False},
             {'type': 'mom1',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom1.png',
              'source_id': 1,
              'description': 'Momment 1 image',
              'software-id': 'sip',
              'mode': 'emission',
              'is_qa': False},
             {'type': 'mom2',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom2.png',
              'source_id': 1,
              'description': 'Momment 2 image',
              'software-id': 'sip',
              'mode': 'emission',
              'is_qa': False},
             {'type': 'spec',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec.png',
              'source_id': 1,
              'description': 'Spectrum plot',
              'software-id': 'sip',
              'mode': 'emission',
              'is_qa': False},
             {'type': 'pv',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv.png',
              'source_id': 1,
              'description': 'Position-Velociy (major axis) plot',
              'software-id': 'sip',
              'mode': 'emission',
              'is_qa': False},
             {'type': 'pv_min',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min.png',
              'source_id': 1,
              'description': 'Position-Velociy (minoe axis) plot',
              'software-id': 'sip',
              'mode': 'emission',
              'is_qa': False},
             {'type': 'mom8',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/quality_assesment_products/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_QA.png',
              'description': 'Moment 8 image',
              'software-id': 'qa',
              'is_qa': True},
             {'type': 'mom8',
              'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/quality_assesment_products/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_QA.png',
              'description': 'Moment 8 image',
              'software-id': 'qa',
              'is_qa': True}],
  'images_grouped': {'sofia': {'absorption': [{'type': 'rel',
                                               'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_rel.eps',
                                               'description': 'Realibiliy Plot',
                                               'software-id': 'sofia',
                                               'mode': 'absorption',
                                               'is_qa': False},
                                              {'type': 'skellman',
                                               'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_skellam.eps',
                                               'description': 'Skellman Plot',
                                               'software-id': 'sofia',
                                               'mode': 'absorption',
                                               'is_qa': False}],
                               'emission': [{'type': 'rel',
                                             'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_rel.eps',
                                             'description': 'Realibiliy Plot',
                                             'software-id': 'sofia',
                                             'mode': 'emission',
                                             'is_qa': False},
                                            {'type': 'skellman',
                                             'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_skellam.eps',
                                             'description': 'Skellman Plot',
                                             'software-id': 'sofia',
                                             'mode': 'emission',
                                             'is_qa': False}]},
                     'sip': {'absorption': {1: [{'type': 'mom0',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom0.png',
                                                 'source_id': 1,
                                                 'description': 'Momment 0 image',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'mom1',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom1.png',
                                                 'source_id': 1,
                                                 'description': 'Momment 1 image',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'mom2',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom2.png',
                                                 'source_id': 1,
                                                 'description': 'Momment 2 image',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'spec',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec.png',
                                                 'source_id': 1,
                                                 'description': 'Spectrum plot',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'pv',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv.png',
                                                 'source_id': 1,
                                                 'description': 'Position-Velociy (major axis) '
                                                                'plot',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'pv_min',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min.png',
                                                 'source_id': 1,
                                                 'description': 'Position-Velociy (minoe axis) '
                                                                'plot',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False}],
                                            2: [{'type': 'mom0',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom0.png',
                                                 'source_id': 2,
                                                 'description': 'Momment 0 image',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'mom1',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom1.png',
                                                 'source_id': 2,
                                                 'description': 'Momment 1 image',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'mom2',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom2.png',
                                                 'source_id': 2,
                                                 'description': 'Momment 2 image',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'spec',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_spec.png',
                                                 'source_id': 2,
                                                 'description': 'Spectrum plot',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'pv',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv.png',
                                                 'source_id': 2,
                                                 'description': 'Position-Velociy (major axis) '
                                                                'plot',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False},
                                                {'type': 'pv_min',
                                                 'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv_min.png',
                                                 'source_id': 2,
                                                 'description': 'Position-Velociy (minoe axis) '
                                                                'plot',
                                                 'software-id': 'sip',
                                                 'mode': 'absorption',
                                                 'is_qa': False}]},
                             'emission': {1: [{'type': 'mom0',
                                               'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom0.png',
                                               'source_id': 1,
                                               'description': 'Momment 0 image',
                                               'software-id': 'sip',
                                               'mode': 'emission',
                                               'is_qa': False},
                                              {'type': 'mom1',
                                               'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom1.png',
                                               'source_id': 1,
                                               'description': 'Momment 1 image',
                                               'software-id': 'sip',
                                               'mode': 'emission',
                                               'is_qa': False},
                                              {'type': 'mom2',
                                               'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom2.png',
                                               'source_id': 1,
                                               'description': 'Momment 2 image',
                                               'software-id': 'sip',
                                               'mode': 'emission',
                                               'is_qa': False},
                                              {'type': 'spec',
                                               'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec.png',
                                               'source_id': 1,
                                               'description': 'Spectrum plot',
                                               'software-id': 'sip',
                                               'mode': 'emission',
                                               'is_qa': False},
                                              {'type': 'pv',
                                               'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv.png',
                                               'source_id': 1,
                                               'description': 'Position-Velociy (major axis) plot',
                                               'software-id': 'sip',
                                               'mode': 'emission',
                                               'is_qa': False},
                                              {'type': 'pv_min',
                                               'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min.png',
                                               'source_id': 1,
                                               'description': 'Position-Velociy (minoe axis) plot',
                                               'software-id': 'sip',
                                               'mode': 'emission',
                                               'is_qa': False}]}},
                     'qa': [{'type': 'mom8',
                             'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/quality_assesment_products/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_QA.png',
                             'description': 'Moment 8 image',
                             'software-id': 'qa',
                             'is_qa': True},
                            {'type': 'mom8',
                             'path': '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/quality_assesment_products/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_QA.png',
                             'description': 'Moment 8 image',
                             'software-id': 'qa',
                             'is_qa': True}]}}]

adp_log = """2025-09-03 15:19:36,020 | INFO | [PID:13228] adpalmap: - ADPALMAP start point
2025-09-03 15:19:36,578 | INFO | [PID:13228] datap: - The file in '/home/usuario/ADP-ALMA-Pipeline/adplib/tap/download_par.yaml' have been loaded successfully
2025-09-03 15:19:36,581 | INFO | [PID:13228] datap: - Validation successful: all parameters for 'query_type = proposal' are correct.
2025-09-03 15:19:36,581 | INFO | [PID:13228] datap: - Your query is: SELECT *  FROM ivoa.obscore WHERE obs_publisher_did like '%2018.1.01852.S%' AND data_rights LIKE '%Public%'
2025-09-03 15:19:41,841 | INFO | [PID:13228] datap: - Starting download. Please wait...
2025-09-03 15:19:43,897 | INFO | [PID:13228] datap: - Download location = archive_data
2025-09-03 15:19:43,897 | INFO | [PID:13228] datap: - Total number of Member OUSs to download = 1
2025-09-03 15:19:43,897 | INFO | [PID:13228] datap: - Selected Member OUSs: ['2018.1.01852.S_uid___A001_X133d_X4226_001_of_001.tar']
2025-09-03 15:19:43,897 | INFO | [PID:13228] datap: - Number of files to download = 4
2025-09-03 15:19:43,897 | INFO | [PID:13228] datap: - Needed disk space = 1.1 GB
2025-09-03 15:19:43,897 | INFO | [PID:13228] datap: - File URLs to download: 
[13228] https://almascience.eso.org/dataPortal/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor.fits
[13228] https://almascience.eso.org/dataPortal/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor.fits
[13228] https://almascience.eso.org/dataPortal/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor.fits
[13228] https://almascience.eso.org/dataPortal/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor.fits
2025-09-03 15:19:43,898 | INFO | [PID:13228] datap: - Data download ended.
2025-09-03 15:19:47,009 | INFO | [PID:13228] datap: - Starting download masks for QA. Please wait...
2025-09-03 15:19:49,135 | INFO | [PID:13228] datap: - The decompressed file already exists: archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.mask.fits
2025-09-03 15:19:49,139 | INFO | [PID:13228] datap: - Found cached mask integer file 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.mask_int.fits'
2025-09-03 15:19:49,139 | INFO | [PID:13228] datap: - The decompressed file already exists: archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.mask.fits
2025-09-03 15:19:49,139 | INFO | [PID:13228] datap: - Found cached mask integer file 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.mask_int.fits'
2025-09-03 15:19:49,139 | INFO | [PID:13228] datap: - The decompressed file already exists: archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.mask.fits
2025-09-03 15:19:49,140 | INFO | [PID:13228] datap: - Found cached mask integer file 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.mask_int.fits'
2025-09-03 15:19:49,140 | INFO | [PID:13228] datap: - The decompressed file already exists: archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.mask.fits
2025-09-03 15:19:49,140 | INFO | [PID:13228] datap: - Found cached mask integer file 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.mask_int.fits'
2025-09-03 15:19:49,140 | INFO | [PID:13228] datap: - Mask download for QA ended.
2025-09-03 15:19:49,140 | INFO | [PID:13228] adpalmap: - The worker number has been set to 4

=== Subprocess PID: 13387 start ===
2025-09-03 15:19:49,536 | INFO | [PID:13387] sopar: - The file in '/home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_abs_default.par' have been loaded successfully
2025-09-03 15:19:49,540 | INFO | [PID:13387] sopar: - The file in '/home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_emi_default.par' have been loaded successfully
2025-09-03 15:19:49,541 | INFO | [PID:13387] sopar: - Reading parameters. Mode: absorption.
2025-09-03 15:19:49,541 | WARNING | [PID:13387] sopar: - Ignoring parameter 'input.data' provided in the parameter file /home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_abs_default.par. If you want to change this, specify it in the input_data_set or input_data_file parameter in the configuration file.
2025-09-03 15:19:49,543 | INFO | [PID:13387] sopar: - Parameters ready. Mode: absorption.
2025-09-03 15:19:49,543 | INFO | [PID:13387] sopar: - Reading parameters. Mode: emission.
2025-09-03 15:19:49,543 | INFO | [PID:13387] sopar: - Parameters ready. Mode: emission.
2025-09-03 15:19:49,545 | INFO | [PID:13387] sopar: - Creating temporary SoFiA parameter file based on the parameter file /home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_abs_default.par.
2025-09-03 15:19:49,546 | INFO | [PID:13387] sopar: - Parameters set for the run: 
[13387]pipeline.verbose=false
[13387]pipeline.pedantic=true
[13387]pipeline.threads=3
[13387]input.data=archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor.fits
[13387]input.primaryBeam=
[13387]input.region=
[13387]input.gain=
[13387]input.noise=
[13387]input.weights=
[13387]input.mask=
[13387]input.invert=true
[13387]flag.region=
[13387]flag.catalog=
[13387]flag.radius=5
[13387]flag.auto=false
[13387]flag.threshold=5.0
[13387]flag.log=false
[13387]flag.cube=
[13387]contsub.enable=false
[13387]contsub.order=0
[13387]contsub.threshold=2.0
[13387]contsub.shift=4
[13387]contsub.padding=3
[13387]scaleNoise.enable=false
[13387]scaleNoise.mode=local
[13387]scaleNoise.statistic=mad
[13387]scaleNoise.fluxRange=negative
[13387]scaleNoise.windowXY=31
[13387]scaleNoise.windowZ=31
[13387]scaleNoise.gridXY=0
[13387]scaleNoise.gridZ=0
[13387]scaleNoise.interpolate=false
[13387]scaleNoise.scfind=false
[13387]rippleFilter.enable=false
[13387]rippleFilter.statistic=median
[13387]rippleFilter.windowXY=31
[13387]rippleFilter.windowZ=15
[13387]rippleFilter.gridXY=0
[13387]rippleFilter.gridZ=0
[13387]rippleFilter.interpolate=false
[13387]scfind.enable=true
[13387]scfind.kernelsXY=0, 3, 6, 9
[13387]scfind.kernelsZ=0, 3, 7, 15
[13387]scfind.threshold=3.8
[13387]scfind.replacement=2.0
[13387]scfind.statistic=mad
[13387]scfind.fluxRange=negative
[13387]threshold.enable=false
[13387]threshold.threshold=5.0
[13387]threshold.mode=relative
[13387]threshold.statistic=mad
[13387]threshold.fluxRange=negative
[13387]linker.enable=true
[13387]linker.radiusXY=2
[13387]linker.radiusZ=3
[13387]linker.minSizeXY=5
[13387]linker.minSizeZ=5
[13387]linker.maxSizeXY=0
[13387]linker.maxSizeZ=0
[13387]linker.minPixels=0
[13387]linker.maxPixels=0
[13387]linker.minFill=0.05
[13387]linker.maxFill=0.0
[13387]linker.positivity=false
[13387]linker.keepNegative=false
[13387]reliability.enable=true
[13387]reliability.parameters=peak, sum, mean
[13387]reliability.threshold=0.9
[13387]reliability.scaleKernel=0.3
[13387]reliability.minSNR=6.0
[13387]reliability.minPixels=150
[13387]reliability.autoKernel=true
[13387]reliability.iterations=50
[13387]reliability.tolerance=0.05
[13387]reliability.catalog=
[13387]reliability.plot=true
[13387]reliability.plotExtra=false
[13387]reliability.debug=false
[13387]dilation.enable=false
[13387]dilation.iterationsXY=10
[13387]dilation.iterationsZ=5
[13387]dilation.threshold=0.001
[13387]parameter.enable=true
[13387]parameter.wcs=true
[13387]parameter.physical=true
[13387]parameter.prefix=SoFiA
[13387]parameter.offset=false
[13387]output.directory=/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption
[13387]output.file= 
2025-09-03 15:19:49,559 | INFO | [PID:13387] sopar: - SoFia start. Mode: absorption. Input data: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor
    ____________________________________________________________________________
    
     Pipeline started
    ____________________________________________________________________________
    
      Software:  Source Finding Application (SoFiA)
      Version:   2.6.14 (2025-05-14)
      CPU:       12 threads available
      Memory:    12.7 GB total / 2.1 GB free
      Date:      2025-09-03
      Time:      13:19:49 h
    ____________________________________________________________________________
    
     Loading parameter settings
    ____________________________________________________________________________
    
      Activating SoFiA default parameter settings.
      Loading user-specified parameters.
      - Loading user parameter file: /home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID13387.par
      Using 3 out of 12 available CPU threads.
    
    WARNING: ┌──────────────────────────────────────────────────────────┐
             │ You have set parameter.physical = true. SoFiA will try   │
             │ to convert some parameters to physical units under the   │
             │ following fundamental assumptions:                       │
             │                                                          │
             │  * The beam information in the FITS header (BMAJ, BMIN)  │
             │    is correct and accurate across the entire data cube.  │
             │                                                          │
             │  * The spectral channels of the data cube are uncorrela- │
             │    ted, i.e. spectral resolution equals channel width.   │
             │                                                          │
             │ Should any of these assumptions be incorrect then the    │
             │ measurement of 
    ____________________________________________________________________________
    
     Loading data cube
    ____________________________________________________________________________
    
      Opening FITS file 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor.fits'.
      Reading FITS data with the following specifications:
        Data type:    -32
        No. of axes:  4
        Axis sizes:   350, 350, 118
        Region:       0-349, 0-349, 0-117
        Memory used:  55.1 MB
      Searching for values of infinity.
        No infinite data values found.
      Inverting data cube
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Measuring global noise level
    ____________________________________________________________________________
    
      Global RMS:  4.042e-04  (using stride of 14)
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Running S+C finder
    ____________________________________________________________________________
    
      Using the following parameters:
      - Kernels
        - spatial:        0, 3, 6, 9
        - spectral:       0, 3, 7, 15
      - Flux threshold:   3.8 * rms
      - Noise statistic:  median absolute deviation
      - Flux range:       negative
    
      Using a stride of 14 in noise measurement.
    
      Smoothing kernel:  [0.0] x [0]
      Noise level:       4.042e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [3]
      Noise level:       3.201e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [7]
      Noise level:       2.194e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [15]
      Noise level:       1.412e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [3.0] x [0]
      Noise level:       2.781e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [3.0] x [3]
      Noise level:       2.208e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [3.0] x [7]
      Noise level:       1.507e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [3.0] x [15]
      Noise level:       9.642e-05
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [6.0] x [0]
      Noise level:       1.824e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [6.0] x [3]
      Noise level:       1.455e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [6.0] x [7]
      Noise level:       9.892e-05
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [6.0] x [15]
      Noise level:       6.316e-05
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [9.0] x [0]
      Noise level:       1.118e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [9.0] x [3]
      Noise level:       8.925e-05
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:04 h
    
      Smoothing kernel:  [9.0] x [7]
      Noise level:       6.031e-05
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:04 h
    
      Smoothing kernel:  [9.0] x [15]
      Noise level:       3.899e-05
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
    ____________________________________________________________________________
    
     Creating source mask
    ____________________________________________________________________________
    
      284523 pixels detected by source finder (1.968%).
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
    ____________________________________________________________________________
    
     Running Linker
    ____________________________________________________________________________
    
      Linker settings:
       - Merging radii:   2, 2, 3
       - Minimum size:    5 x 5 x 5
       - Min/max fill:    5.0%, 0.0%
       - Keep negative:   yes
    
      Linker status:
       - No. of objects:  246
       - Memory usage:    32.91 kB
    
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
    ____________________________________________________________________________
    
     Measuring reliability
    ____________________________________________________________________________
    
      Using 3D parameter space:
       - peak
       - sum
       - mean
      Found 134 positive and 112 negative sources.
      Retaining all negative detections.
      Using auto-kernel feature.
        Iter.  1: kernel = 0.100, median = 1.000
        Iter.  2: kernel = 0.200, median = 0.896
        Iter.  3: kernel = 0.300, median = 0.645
        Iter.  4: kernel = 0.400, median = 0.393
        Iter.  5: kernel = 0.440, median = 0.296
        Iter.  6: kernel = 0.480, median = 0.273
        Iter.  7: kernel = 0.520, median = 0.239
        Iter.  8: kernel = 0.560, median = 0.175
        Iter.  9: kernel = 0.600, median = 0.115
        Iter. 10: kernel = 0.640, median = 0.069
        Iter. 11: kernel = 0.680, median = 0.032
      Converged to scale_kernel = 0.680 after 11 iterations.
      
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_rel.eps
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_skellam.eps
      1 reliable source found.
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
    ____________________________________________________________________________
    
     Creating initial catalogue
    ____________________________________________________________________________
    
      Initial source catalogue created.
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
    ____________________________________________________________________________
    
     Measuring source parameters
    ____________________________________________________________________________
    
      Found 1 source in need of parameterisation.
      Assuming beam size of 6.6 x 5.1 pixels.
    
      Attempting to measure parameters in physical units.
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
    ____________________________________________________________________________
    
     Creating cubelets
    ____________________________________________________________________________
    
      Flux threshold (moment 1 and 2): 0.00e+00
      Assuming beam size of 6.6 x 5.1 pixels.
    
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_cube.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mask.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom0.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom1.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom2.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_chan.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_snr.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv_min.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv_mask.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv_min_mask.fits
      Creating text file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_spec.txt
      Creating text file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_spec_aperture.txt
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
    ____________________________________________________________________________
    
     Creating moment maps
    ____________________________________________________________________________
    
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mom0.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mom1.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mom2.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_chan.fits
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
    ____________________________________________________________________________
    
     Writing mask cube
    ____________________________________________________________________________
    
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mask-2d.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mask.fits
    
      Elapsed time: 00:00:05 h
      CPU time:     00:00:10 h
    
    ____________________________________________________________________________
    
     Writing source catalogue
    ____________________________________________________________________________
    
      Writing ASCII file:   member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_cat.txt
      Writing VOTable file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_cat.xml
    
      Elapsed time: 00:00:05 h
      CPU time:     00:00:10 h
    
    ____________________________________________________________________________
    
     Pipeline finished
    ____________________________________________________________________________
    
2025-09-03 15:19:54,634 | INFO | [PID:13387] sopar: - SoFia finished. Mode: absorption
2025-09-03 15:19:54,656 | INFO | [PID:13387] sopar: - Quality assesment start. Mode: absorption.
2025-09-03 15:19:54,672 | WARNING | [PID:13387] sopar: - No data cube has been specified with Primary Beam information.
2025-09-03 15:19:59,029 | INFO | [PID:13387] sopar: - QA file saved in /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/quality_assesment_products. Quality assesment completed successfully. Mode: absorption
2025-09-03 15:19:59,030 | INFO | [PID:13387] sopar: - Creating temporary SoFiA parameter file based on the parameter file /home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_emi_default.par.
2025-09-03 15:19:59,031 | INFO | [PID:13387] sopar: - Parameters set for the run: 
[13387]pipeline.verbose=false
[13387]pipeline.pedantic=true
[13387]pipeline.threads=3
[13387]input.data=archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor.fits
[13387]input.primaryBeam= 
[13387]input.region=
[13387]input.gain=
[13387]input.noise=
[13387]input.weights=
[13387]input.mask=
[13387]input.invert=false
[13387]flag.region=
[13387]flag.catalog=
[13387]flag.radius=5
[13387]flag.auto=false
[13387]flag.threshold=5.0
[13387]flag.log=false
[13387]flag.cube=/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mask.fits
[13387]contsub.enable=false
[13387]contsub.order=0
[13387]contsub.threshold=2.0
[13387]contsub.shift=4
[13387]contsub.padding=3
[13387]scaleNoise.enable=false
[13387]scaleNoise.mode=local
[13387]scaleNoise.statistic=mad
[13387]scaleNoise.fluxRange=negative
[13387]scaleNoise.windowXY=31
[13387]scaleNoise.windowZ=31
[13387]scaleNoise.gridXY=0
[13387]scaleNoise.gridZ=0
[13387]scaleNoise.interpolate=false
[13387]scaleNoise.scfind=false
[13387]rippleFilter.enable=false
[13387]rippleFilter.statistic=median
[13387]rippleFilter.windowXY=31
[13387]rippleFilter.windowZ=15
[13387]rippleFilter.gridXY=0
[13387]rippleFilter.gridZ=0
[13387]rippleFilter.interpolate=false
[13387]scfind.enable=true
[13387]scfind.kernelsXY=0, 3, 6, 9
[13387]scfind.kernelsZ=0, 3, 7, 15
[13387]scfind.threshold=3.8
[13387]scfind.replacement=2.0
[13387]scfind.statistic=mad
[13387]scfind.fluxRange=negative
[13387]threshold.enable=false
[13387]threshold.threshold=5.0
[13387]threshold.mode=relative
[13387]threshold.statistic=mad
[13387]threshold.fluxRange=negative
[13387]linker.enable=true
[13387]linker.radiusXY=2
[13387]linker.radiusZ=3
[13387]linker.minSizeXY=5
[13387]linker.minSizeZ=5
[13387]linker.maxSizeXY=0
[13387]linker.maxSizeZ=0
[13387]linker.minPixels=0
[13387]linker.maxPixels=0
[13387]linker.minFill=0.05
[13387]linker.maxFill=0.0
[13387]linker.positivity=false
[13387]linker.keepNegative=false
[13387]reliability.enable=true
[13387]reliability.parameters=peak, sum, mean
[13387]reliability.threshold=0.9
[13387]reliability.scaleKernel=0.3
[13387]reliability.minSNR=6.0
[13387]reliability.minPixels=150
[13387]reliability.autoKernel=true
[13387]reliability.iterations=50
[13387]reliability.tolerance=0.05
[13387]reliability.catalog=
[13387]reliability.plot=true
[13387]reliability.plotExtra=false
[13387]reliability.debug=false
[13387]dilation.enable=false
[13387]dilation.iterationsXY=10
[13387]dilation.iterationsZ=5
[13387]dilation.threshold=0.001
[13387]parameter.enable=true
[13387]parameter.wcs=true
[13387]parameter.physical=true
[13387]parameter.prefix=SoFiA
[13387]parameter.offset=false
[13387]output.directory=/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission
[13387]output.file= 
2025-09-03 15:19:59,032 | INFO | [PID:13387] sopar: - SoFia start. Mode: emission. Input data: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor
    ____________________________________________________________________________
    
     Pipeline started
    ____________________________________________________________________________
    
      Software:  Source Finding Application (SoFiA)
      Version:   2.6.14 (2025-05-14)
      CPU:       12 threads available
      Memory:    12.7 GB total / 0.6 GB free
      Date:      2025-09-03
      Time:      13:19:59 h
    ____________________________________________________________________________
    
     Loading parameter settings
    ____________________________________________________________________________
    
      Activating SoFiA default parameter settings.
      Loading user-specified parameters.
      - Loading user parameter file: /home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID13387.par
      Using 3 out of 12 available CPU threads.
    
    WARNING: ┌──────────────────────────────────────────────────────────┐
             │ You have set parameter.physical = true. SoFiA will try   │
             │ to convert some parameters to physical units under the   │
             │ following fundamental assumptions:                       │
             │                                                          │
             │  * The beam information in the FITS header (BMAJ, BMIN)  │
             │    is correct and accurate across the entire data cube.  │
             │                                                          │
             │  * The spectral channels of the data cube are uncorrela- │
             │    ted, i.e. spectral resolution equals channel width.   │
             │                                                          │
             │ Should any of these assumptions be incorrect then the    │
             │ measurement of 
    ____________________________________________________________________________
    
     Loading data cube
    ____________________________________________________________________________
    
      Opening FITS file 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor.fits'.
      Reading FITS data with the following specifications:
        Data type:    -32
        No. of axes:  4
        Axis sizes:   350, 350, 118
        Region:       0-349, 0-349, 0-117
        Memory used:  55.1 MB
      Searching for values of infinity.
        No infinite data values found.
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Loading and applying flag cube
    ____________________________________________________________________________
    
      Opening FITS file '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_mask.fits'.
      Reading FITS data with the following specifications:
        Data type:    32
        No. of axes:  3
        Axis sizes:   350, 350, 118
        Region:       0-349, 0-349, 0-117
        Memory used:  55.1 MB
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Measuring global noise level
    ____________________________________________________________________________
    
      Global RMS:  4.033e-04  (using stride of 14)
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Running S+C finder
    ____________________________________________________________________________
    
      Using the following parameters:
      - Kernels
        - spatial:        0, 3, 6, 9
        - spectral:       0, 3, 7, 15
      - Flux threshold:   3.8 * rms
      - Noise statistic:  median absolute deviation
      - Flux range:       negative
    
      Using a stride of 14 in noise measurement.
    
      Smoothing kernel:  [0.0] x [0]
      Noise level:       4.033e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [3]
      Noise level:       3.229e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [7]
      Noise level:       2.181e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [15]
      Noise level:       1.401e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [3.0] x [0]
      Noise level:       2.779e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [3.0] x [3]
      Noise level:       2.210e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [3.0] x [7]
      Noise level:       1.500e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [3.0] x [15]
      Noise level:       9.592e-05
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [6.0] x [0]
      Noise level:       1.823e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [6.0] x [3]
      Noise level:       1.451e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [6.0] x [7]
      Noise level:       9.905e-05
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [6.0] x [15]
      Noise level:       6.325e-05
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [9.0] x [0]
      Noise level:       1.107e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [9.0] x [3]
      Noise level:       8.805e-05
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [9.0] x [7]
      Noise level:       6.040e-05
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [9.0] x [15]
      Noise level:       3.853e-05
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:03 h
    
    ____________________________________________________________________________
    
     Creating source mask
    ____________________________________________________________________________
    
      289654 pixels detected by source finder (2.004%).
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:03 h
    
    ____________________________________________________________________________
    
     Running Linker
    ____________________________________________________________________________
    
      Linker settings:
       - Merging radii:   2, 2, 3
       - Minimum size:    5 x 5 x 5
       - Min/max fill:    5.0%, 0.0%
       - Keep negative:   yes
    
      Linker status:
       - No. of objects:  236
       - Memory usage:    31.57 kB
    
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:03 h
    
    ____________________________________________________________________________
    
     Measuring reliability
    ____________________________________________________________________________
    
      Using 3D parameter space:
       - peak
       - sum
       - mean
      Found 107 positive and 129 negative sources.
      Retaining all negative detections.
      Using auto-kernel feature.
        Iter.  1: kernel = 0.100, median = 1.000
        Iter.  2: kernel = 0.200, median = 0.900
        Iter.  3: kernel = 0.300, median = 0.679
        Iter.  4: kernel = 0.400, median = 0.570
        Iter.  5: kernel = 0.500, median = 0.491
        Iter.  6: kernel = 0.540, median = 0.470
        Iter.  7: kernel = 0.580, median = 0.459
        Iter.  8: kernel = 0.620, median = 0.450
        Iter.  9: kernel = 0.660, median = 0.430
        Iter. 10: kernel = 0.700, median = 0.415
        Iter. 11: kernel = 0.740, median = 0.415
        Iter. 12: kernel = 0.780, median = 0.402
        Iter. 13: kernel = 0.820, median = 0.405
        Iter. 14: kernel = 0.860, median = 0.417
        Iter. 15: kernel = 0.900, median = 0.433
        Iter. 16: kernel = 0.940, median = 0.450
        Iter. 17: kernel = 0.980, median = 0.469
        Iter. 18: kernel = 1.020, median = 0.478
        Iter. 19: kernel = 1.060, median = 0.483
        Iter. 20: kernel = 1.100, median = 0.496
        Iter. 21: kernel = 1.140, median = 0.515
        Iter. 22: kernel = 1.240, median = 0.542
        Iter. 23: kernel = 1.340, median = 0.583
        Iter. 24: kernel = 1.440, median = 0.633
        Iter. 25: kernel = 1.540, median = 0.671
        Iter. 26: kernel = 1.640, median = 0.719
        Iter. 27: kernel = 1.740, median = 0.760
        Iter. 28: kernel = 1.840, median = 0.798
        Iter. 29: kernel = 1.940, median = 0.831
        Iter. 30: kernel = 2.040, median = 0.864
        Iter. 31: kernel = 2.140, median = 0.896
        Iter. 32: kernel = 2.240, median = 0.924
        Iter. 33: kernel = 2.340, median = 0.945
        Iter. 34: kernel = 2.440, median = 0.972
        Iter. 35: kernel = 2.540, median = 0.996
        Iter. 36: kernel = 2.640, median = 1.017
        Iter. 37: kernel = 2.740, median = 1.039
        Iter. 38: kernel = 2.840, median = 1.061
        Iter. 39: kernel = 2.940, median = 1.082
        Iter. 40: kernel = 3.040, median = 1.101
        Iter. 41: kernel = 3.140, median = 1.119
        Iter. 42: kernel = 3.240, median = 1.135
        Iter. 43: kernel = 3.340, median = 1.147
        Iter. 44: kernel = 3.440, median = 1.162
        Iter. 45: kernel = 3.540, median = 1.177
        Iter. 46: kernel = 3.640, median = 1.190
        Iter. 47: kernel = 3.740, median = 1.202
        Iter. 48: kernel = 3.840, median = 1.213
        Iter. 49: kernel = 3.940, median = 1.224
        Iter. 50: kernel = 4.040, median = 1.232
    WARNING: Auto-kernel failed to converge, defaulting to kernel scale of 0.300.
      
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_rel.eps
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_skellam.eps
    
    ERROR: No reliable sources found. Terminating pipeline.
           Terminating with error code 8.
    
2025-09-03 15:20:00,683 | ERROR | [PID:13387] sopar: - Error running SoFia. Mode: emission. Error: Command '['sofia', '/home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID13387.par']' returned non-zero exit status 8.
2025-09-03 15:20:00,683 | INFO | [PID:13387] sopar: - SoFia execution aborted. Mode: emission.
2025-09-03 15:20:00,683 | INFO | [PID:13387] sopar: - Quality assesment start. Mode: emission.
2025-09-03 15:20:00,685 | WARNING | [PID:13387] sopar: - No data cube has been specified with Primary Beam information.
2025-09-03 15:20:00,695 | WARNING | [PID:13387] sopar: - 2D-Mask file from SoFia not found in /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission.
2025-09-03 15:20:00,696 | INFO | [PID:13387] sopar: - Quality assesment aborted.
2025-09-03 15:20:00,699 | INFO | [PID:13387] sipargs: - The file in /home/usuario/ADP-ALMA-Pipeline/adplib/sip/sip_args.yaml have been loaded successfully
2025-09-03 15:20:00,701 | INFO | [PID:13387] sipargs: - SIP start. Mode: absorption. Input data: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor
    2025-09-03 15:20:01,015 | INFO | image_pipeline: - *****************************************************************
    2025-09-03 15:20:01,015 | INFO | image_pipeline: - 	Beginning SoFiA-image-pipeline (SIP) 1.3.16.
    2025-09-03 15:20:01,015 | INFO | image_pipeline: - 	Offline mode requested: will not make ancillary data overlays.
    2025-09-03 15:20:01,015 | INFO | image_pipeline: - 	Reading catalog in ascii format.
    2025-09-03 15:20:01,020 | INFO | image_pipeline: - 	Catalog generated by SoFiA-2?
    2025-09-03 15:20:01,020 | INFO | image_pipeline: - 	Assuming all requested sources are associated with CO(1-0) line transition
    2025-09-03 15:20:01,832 | INFO | image_pipeline: -  
    2025-09-03 15:20:01,832 | INFO | image_pipeline: - 	-Source 1: SoFiA J100113.98+021709.7.
    2025-09-03 15:20:01,832 | INFO | make_images: - 	Start making spatial images.
    2025-09-03 15:20:01,834 | INFO | functions: - 		Found 2.1 arcsec by 1.6 arcsec beam with PA=87.7 deg in primary header.
    2025-09-03 15:20:01,834 | WARNING | functions: - 	No equinox information in header; assuming ICRS frame.
    2025-09-03 15:20:01,834 | INFO | functions: - 		Found LSRK reference frame specified in SPECSYS in header.
    2025-09-03 15:20:01,834 | INFO | functions: - 		Found CTYPE3 spectral axis type FREQ in header.
    2025-09-03 15:20:01,836 | INFO | make_images: - 	The first contour defined at SNR = [2.0, 3.0] has level = 2.872e+04 (mom0 data units).
    2025-09-03 15:20:01,838 | INFO | make_images: - 	Image size bigger than default. Now 0.24 arcmin
    2025-09-03 15:20:01,838 | INFO | make_images: - 	No user image given and offline mode requested. Making radio spectral line images.
    2025-09-03 15:20:01,839 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom0.png already exists. Will not overwrite.
    2025-09-03 15:20:01,839 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_snr.png already exists. Will not overwrite.
    2025-09-03 15:20:01,839 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom1.png already exists. Will not overwrite.
    2025-09-03 15:20:01,839 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_mom2.png already exists. Will not overwrite.
    2025-09-03 15:20:01,839 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv.png already exists. Will not overwrite.
    2025-09-03 15:20:01,839 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_pv_min.png already exists. Will not overwrite.
    2025-09-03 15:20:01,839 | INFO | make_images: - 	Done making spatial images.
    2025-09-03 15:20:01,839 | INFO | make_spectra: - 	Start making spectral profiles
    2025-09-03 15:20:01,841 | INFO | functions: - 		Found 2.1 arcsec by 1.6 arcsec beam with PA=87.7 deg in primary header.
    2025-09-03 15:20:01,841 | WARNING | functions: - 	No equinox information in header; assuming ICRS frame.
    2025-09-03 15:20:01,841 | INFO | functions: - 		Found LSRK reference frame specified in SPECSYS in header.
    2025-09-03 15:20:01,841 | INFO | functions: - 		Found CTYPE3 spectral axis type FREQ in header.
    2025-09-03 15:20:01,841 | WARNING | make_spectra: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_spec.png already exists. Will not overwrite.
    2025-09-03 15:20:01,842 | INFO | make_spectra: - 	Using /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_cubelets/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_spec_aperture.txt to make aperture spectrum plot.
    2025-09-03 15:20:01,842 | WARNING | make_spectra: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_1_specfull.png already exists. Will not overwrite.
    2025-09-03 15:20:01,842 | INFO | make_spectra: - 	Done making spectral profiles.
    2025-09-03 15:20:01,842 | INFO | image_pipeline: -  
    2025-09-03 15:20:01,842 | INFO | image_pipeline: - 	DONE! Made images for 1 sources.
    2025-09-03 15:20:01,842 | INFO | image_pipeline: - 	Created log file: /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_sip.log
    2025-09-03 15:20:01,842 | INFO | image_pipeline: - *****************************************************************
    
2025-09-03 15:20:00,701 | INFO | [PID:13387] sipargs: - Command used to run SIP: sofia_image_pipeline -c /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_cat.txt -x png -i 0.05 -s none -line CO(1-0) -log /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw19.cube.I.pbcor_sip.log
2025-09-03 15:20:02,019 | INFO | [PID:13387] sipargs: - SIP finished. Mode: absorption
2025-09-03 15:20:02,020 | ERROR | [PID:13387] sipargs: - No valid .txt or .xml catalog for SIP found within the  /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission  directory.
2025-09-03 15:20:02,021 | INFO | [PID:13387] sipargs: - SIP execution aborted. Run: emission.
===  Subprocess PID: 13387 end  ===


=== Subprocess PID: 13388 start ===
2025-09-03 15:19:49,546 | INFO | [PID:13388] sopar: - The file in '/home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_abs_default.par' have been loaded successfully
2025-09-03 15:19:49,547 | INFO | [PID:13388] sopar: - The file in '/home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_emi_default.par' have been loaded successfully
2025-09-03 15:19:49,559 | INFO | [PID:13388] sopar: - Reading parameters. Mode: absorption.
2025-09-03 15:19:49,572 | WARNING | [PID:13388] sopar: - Ignoring parameter 'input.data' provided in the parameter file /home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_abs_default.par. If you want to change this, specify it in the input_data_set or input_data_file parameter in the configuration file.
2025-09-03 15:19:49,676 | INFO | [PID:13388] sopar: - Parameters ready. Mode: absorption.
2025-09-03 15:19:49,682 | INFO | [PID:13388] sopar: - Reading parameters. Mode: emission.
2025-09-03 15:19:49,683 | INFO | [PID:13388] sopar: - Parameters ready. Mode: emission.
2025-09-03 15:19:49,686 | INFO | [PID:13388] sopar: - Creating temporary SoFiA parameter file based on the parameter file /home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_abs_default.par.
2025-09-03 15:19:49,687 | INFO | [PID:13388] sopar: - Parameters set for the run: 
[13388]pipeline.verbose=false
[13388]pipeline.pedantic=true
[13388]pipeline.threads=3
[13388]input.data=archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor.fits
[13388]input.primaryBeam=
[13388]input.region=
[13388]input.gain=
[13388]input.noise=
[13388]input.weights=
[13388]input.mask=
[13388]input.invert=true
[13388]flag.region=
[13388]flag.catalog=
[13388]flag.radius=5
[13388]flag.auto=false
[13388]flag.threshold=5.0
[13388]flag.log=false
[13388]flag.cube=
[13388]contsub.enable=false
[13388]contsub.order=0
[13388]contsub.threshold=2.0
[13388]contsub.shift=4
[13388]contsub.padding=3
[13388]scaleNoise.enable=false
[13388]scaleNoise.mode=local
[13388]scaleNoise.statistic=mad
[13388]scaleNoise.fluxRange=negative
[13388]scaleNoise.windowXY=31
[13388]scaleNoise.windowZ=31
[13388]scaleNoise.gridXY=0
[13388]scaleNoise.gridZ=0
[13388]scaleNoise.interpolate=false
[13388]scaleNoise.scfind=false
[13388]rippleFilter.enable=false
[13388]rippleFilter.statistic=median
[13388]rippleFilter.windowXY=31
[13388]rippleFilter.windowZ=15
[13388]rippleFilter.gridXY=0
[13388]rippleFilter.gridZ=0
[13388]rippleFilter.interpolate=false
[13388]scfind.enable=true
[13388]scfind.kernelsXY=0, 3, 6, 9
[13388]scfind.kernelsZ=0, 3, 7, 15
[13388]scfind.threshold=3.8
[13388]scfind.replacement=2.0
[13388]scfind.statistic=mad
[13388]scfind.fluxRange=negative
[13388]threshold.enable=false
[13388]threshold.threshold=5.0
[13388]threshold.mode=relative
[13388]threshold.statistic=mad
[13388]threshold.fluxRange=negative
[13388]linker.enable=true
[13388]linker.radiusXY=2
[13388]linker.radiusZ=3
[13388]linker.minSizeXY=5
[13388]linker.minSizeZ=5
[13388]linker.maxSizeXY=0
[13388]linker.maxSizeZ=0
[13388]linker.minPixels=0
[13388]linker.maxPixels=0
[13388]linker.minFill=0.05
[13388]linker.maxFill=0.0
[13388]linker.positivity=false
[13388]linker.keepNegative=false
[13388]reliability.enable=true
[13388]reliability.parameters=peak, sum, mean
[13388]reliability.threshold=0.9
[13388]reliability.scaleKernel=0.3
[13388]reliability.minSNR=6.0
[13388]reliability.minPixels=150
[13388]reliability.autoKernel=true
[13388]reliability.iterations=50
[13388]reliability.tolerance=0.05
[13388]reliability.catalog=
[13388]reliability.plot=true
[13388]reliability.plotExtra=false
[13388]reliability.debug=false
[13388]dilation.enable=false
[13388]dilation.iterationsXY=10
[13388]dilation.iterationsZ=5
[13388]dilation.threshold=0.001
[13388]parameter.enable=true
[13388]parameter.wcs=true
[13388]parameter.physical=true
[13388]parameter.prefix=SoFiA
[13388]parameter.offset=false
[13388]output.directory=/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption
[13388]output.file= 
2025-09-03 15:19:49,690 | INFO | [PID:13388] sopar: - SoFia start. Mode: absorption. Input data: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor
    ____________________________________________________________________________
    
     Pipeline started
    ____________________________________________________________________________
    
      Software:  Source Finding Application (SoFiA)
      Version:   2.6.14 (2025-05-14)
      CPU:       12 threads available
      Memory:    12.7 GB total / 2.0 GB free
      Date:      2025-09-03
      Time:      13:19:49 h
    ____________________________________________________________________________
    
     Loading parameter settings
    ____________________________________________________________________________
    
      Activating SoFiA default parameter settings.
      Loading user-specified parameters.
      - Loading user parameter file: /home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID13388.par
      Using 3 out of 12 available CPU threads.
    
    WARNING: ┌──────────────────────────────────────────────────────────┐
             │ You have set parameter.physical = true. SoFiA will try   │
             │ to convert some parameters to physical units under the   │
             │ following fundamental assumptions:                       │
             │                                                          │
             │  * The beam information in the FITS header (BMAJ, BMIN)  │
             │    is correct and accurate across the entire data cube.  │
             │                                                          │
             │  * The spectral channels of the data cube are uncorrela- │
             │    ted, i.e. spectral resolution equals channel width.   │
             │                                                          │
             │ Should any of these assumptions be incorrect then the    │
             │ measurement of 
    ____________________________________________________________________________
    
     Loading data cube
    ____________________________________________________________________________
    
      Opening FITS file 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor.fits'.
      Reading FITS data with the following specifications:
        Data type:    -32
        No. of axes:  4
        Axis sizes:   350, 350, 118
        Region:       0-349, 0-349, 0-117
        Memory used:  55.1 MB
      Searching for values of infinity.
        No infinite data values found.
      Inverting data cube
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Measuring global noise level
    ____________________________________________________________________________
    
      Global RMS:  3.947e-04  (using stride of 14)
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Running S+C finder
    ____________________________________________________________________________
    
      Using the following parameters:
      - Kernels
        - spatial:        0, 3, 6, 9
        - spectral:       0, 3, 7, 15
      - Flux threshold:   3.8 * rms
      - Noise statistic:  median absolute deviation
      - Flux range:       negative
    
      Using a stride of 14 in noise measurement.
    
      Smoothing kernel:  [0.0] x [0]
      Noise level:       3.947e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [3]
      Noise level:       3.165e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [7]
      Noise level:       2.140e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [15]
      Noise level:       1.374e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [3.0] x [0]
      Noise level:       2.875e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [3.0] x [3]
      Noise level:       2.296e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [3.0] x [7]
      Noise level:       1.549e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [3.0] x [15]
      Noise level:       9.927e-05
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [6.0] x [0]
      Noise level:       1.949e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [6.0] x [3]
      Noise level:       1.560e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [6.0] x [7]
      Noise level:       1.064e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [6.0] x [15]
      Noise level:       6.777e-05
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [9.0] x [0]
      Noise level:       1.200e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:04 h
    
      Smoothing kernel:  [9.0] x [3]
      Noise level:       9.727e-05
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:04 h
    
      Smoothing kernel:  [9.0] x [7]
      Noise level:       6.659e-05
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:04 h
    
      Smoothing kernel:  [9.0] x [15]
      Noise level:       4.286e-05
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
    ____________________________________________________________________________
    
     Creating source mask
    ____________________________________________________________________________
    
      340062 pixels detected by source finder (2.353%).
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
    ____________________________________________________________________________
    
     Running Linker
    ____________________________________________________________________________
    
      Linker settings:
       - Merging radii:   2, 2, 3
       - Minimum size:    5 x 5 x 5
       - Min/max fill:    5.0%, 0.0%
       - Keep negative:   yes
    
      Linker status:
       - No. of objects:  335
       - Memory usage:    44.82 kB
    
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
    ____________________________________________________________________________
    
     Measuring reliability
    ____________________________________________________________________________
    
      Using 3D parameter space:
       - peak
       - sum
       - mean
      Found 164 positive and 171 negative sources.
      Retaining all negative detections.
      Using auto-kernel feature.
        Iter.  1: kernel = 0.100, median = 1.000
        Iter.  2: kernel = 0.200, median = 0.860
        Iter.  3: kernel = 0.300, median = 0.655
        Iter.  4: kernel = 0.400, median = 0.585
        Iter.  5: kernel = 0.500, median = 0.438
        Iter.  6: kernel = 0.540, median = 0.382
        Iter.  7: kernel = 0.580, median = 0.340
        Iter.  8: kernel = 0.620, median = 0.288
        Iter.  9: kernel = 0.660, median = 0.250
        Iter. 10: kernel = 0.700, median = 0.224
        Iter. 11: kernel = 0.740, median = 0.171
        Iter. 12: kernel = 0.780, median = 0.144
        Iter. 13: kernel = 0.820, median = 0.121
        Iter. 14: kernel = 0.860, median = 0.093
        Iter. 15: kernel = 0.900, median = 0.078
        Iter. 16: kernel = 0.940, median = 0.069
        Iter. 17: kernel = 0.980, median = 0.062
        Iter. 18: kernel = 1.020, median = 0.057
        Iter. 19: kernel = 1.060, median = 0.042
      Converged to scale_kernel = 1.060 after 19 iterations.
      
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_rel.eps
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_skellam.eps
    
    ERROR: No reliable sources found. Terminating pipeline.
           Terminating with error code 8.
    
2025-09-03 15:19:52,742 | ERROR | [PID:13388] sopar: - Error running SoFia. Mode: absorption. Error: Command '['sofia', '/home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID13388.par']' returned non-zero exit status 8.
2025-09-03 15:19:52,762 | INFO | [PID:13388] sopar: - SoFiA will try to run again in mode: emission.
2025-09-03 15:19:52,764 | INFO | [PID:13388] sopar: - Quality assesment start. Mode: absorption.
2025-09-03 15:19:52,799 | WARNING | [PID:13388] sopar: - No data cube has been specified with Primary Beam information.
2025-09-03 15:19:52,849 | WARNING | [PID:13388] sopar: - 2D-Mask file from SoFia not found in /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption.
2025-09-03 15:19:52,857 | INFO | [PID:13388] sopar: - Quality assesment aborted.
2025-09-03 15:19:52,878 | WARNING | [PID:13388] sopar: - There is no mask available from the absorption run. The parameter 'flag_cube' will not be used
2025-09-03 15:19:52,878 | INFO | [PID:13388] sopar: - Creating temporary SoFiA parameter file based on the parameter file /home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_emi_default.par.
2025-09-03 15:19:52,878 | INFO | [PID:13388] sopar: - Parameters set for the run: 
[13388]pipeline.verbose=false
[13388]pipeline.pedantic=true
[13388]pipeline.threads=3
[13388]input.data=archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor.fits
[13388]input.primaryBeam= 
[13388]input.region=
[13388]input.gain=
[13388]input.noise=
[13388]input.weights=
[13388]input.mask=
[13388]input.invert=false
[13388]flag.region=
[13388]flag.catalog=
[13388]flag.radius=5
[13388]flag.auto=false
[13388]flag.threshold=5.0
[13388]flag.log=false
[13388]flag.cube=
[13388]contsub.enable=false
[13388]contsub.order=0
[13388]contsub.threshold=2.0
[13388]contsub.shift=4
[13388]contsub.padding=3
[13388]scaleNoise.enable=false
[13388]scaleNoise.mode=local
[13388]scaleNoise.statistic=mad
[13388]scaleNoise.fluxRange=negative
[13388]scaleNoise.windowXY=31
[13388]scaleNoise.windowZ=31
[13388]scaleNoise.gridXY=0
[13388]scaleNoise.gridZ=0
[13388]scaleNoise.interpolate=false
[13388]scaleNoise.scfind=false
[13388]rippleFilter.enable=false
[13388]rippleFilter.statistic=median
[13388]rippleFilter.windowXY=31
[13388]rippleFilter.windowZ=15
[13388]rippleFilter.gridXY=0
[13388]rippleFilter.gridZ=0
[13388]rippleFilter.interpolate=false
[13388]scfind.enable=true
[13388]scfind.kernelsXY=0, 3, 6, 9
[13388]scfind.kernelsZ=0, 3, 7, 15
[13388]scfind.threshold=3.8
[13388]scfind.replacement=2.0
[13388]scfind.statistic=mad
[13388]scfind.fluxRange=negative
[13388]threshold.enable=false
[13388]threshold.threshold=5.0
[13388]threshold.mode=relative
[13388]threshold.statistic=mad
[13388]threshold.fluxRange=negative
[13388]linker.enable=true
[13388]linker.radiusXY=2
[13388]linker.radiusZ=3
[13388]linker.minSizeXY=5
[13388]linker.minSizeZ=5
[13388]linker.maxSizeXY=0
[13388]linker.maxSizeZ=0
[13388]linker.minPixels=0
[13388]linker.maxPixels=0
[13388]linker.minFill=0.05
[13388]linker.maxFill=0.0
[13388]linker.positivity=false
[13388]linker.keepNegative=false
[13388]reliability.enable=true
[13388]reliability.parameters=peak, sum, mean
[13388]reliability.threshold=0.9
[13388]reliability.scaleKernel=0.3
[13388]reliability.minSNR=6.0
[13388]reliability.minPixels=150
[13388]reliability.autoKernel=true
[13388]reliability.iterations=50
[13388]reliability.tolerance=0.05
[13388]reliability.catalog=
[13388]reliability.plot=true
[13388]reliability.plotExtra=false
[13388]reliability.debug=false
[13388]dilation.enable=false
[13388]dilation.iterationsXY=10
[13388]dilation.iterationsZ=5
[13388]dilation.threshold=0.001
[13388]parameter.enable=true
[13388]parameter.wcs=true
[13388]parameter.physical=true
[13388]parameter.prefix=SoFiA
[13388]parameter.offset=false
[13388]output.directory=/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission
[13388]output.file= 
2025-09-03 15:19:52,907 | INFO | [PID:13388] sopar: - SoFia start. Mode: emission. Input data: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor
    ____________________________________________________________________________
    
     Pipeline started
    ____________________________________________________________________________
    
      Software:  Source Finding Application (SoFiA)
      Version:   2.6.14 (2025-05-14)
      CPU:       12 threads available
      Memory:    12.7 GB total / 0.4 GB free
      Date:      2025-09-03
      Time:      13:19:52 h
    ____________________________________________________________________________
    
     Loading parameter settings
    ____________________________________________________________________________
    
      Activating SoFiA default parameter settings.
      Loading user-specified parameters.
      - Loading user parameter file: /home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID13388.par
      Using 3 out of 12 available CPU threads.
    
    WARNING: ┌──────────────────────────────────────────────────────────┐
             │ You have set parameter.physical = true. SoFiA will try   │
             │ to convert some parameters to physical units under the   │
             │ following fundamental assumptions:                       │
             │                                                          │
             │  * The beam information in the FITS header (BMAJ, BMIN)  │
             │    is correct and accurate across the entire data cube.  │
             │                                                          │
             │  * The spectral channels of the data cube are uncorrela- │
             │    ted, i.e. spectral resolution equals channel width.   │
             │                                                          │
             │ Should any of these assumptions be incorrect then the    │
             │ measurement of 
    ____________________________________________________________________________
    
     Loading data cube
    ____________________________________________________________________________
    
      Opening FITS file 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor.fits'.
      Reading FITS data with the following specifications:
        Data type:    -32
        No. of axes:  4
        Axis sizes:   350, 350, 118
        Region:       0-349, 0-349, 0-117
        Memory used:  55.1 MB
      Searching for values of infinity.
        No infinite data values found.
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Measuring global noise level
    ____________________________________________________________________________
    
      Global RMS:  3.933e-04  (using stride of 14)
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Running S+C finder
    ____________________________________________________________________________
    
      Using the following parameters:
      - Kernels
        - spatial:        0, 3, 6, 9
        - spectral:       0, 3, 7, 15
      - Flux threshold:   3.8 * rms
      - Noise statistic:  median absolute deviation
      - Flux range:       negative
    
      Using a stride of 14 in noise measurement.
    
      Smoothing kernel:  [0.0] x [0]
      Noise level:       3.933e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [3]
      Noise level:       3.149e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [0.0] x [7]
      Noise level:       2.152e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [0.0] x [15]
      Noise level:       1.380e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [3.0] x [0]
      Noise level:       2.868e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [3.0] x [3]
      Noise level:       2.289e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [3.0] x [7]
      Noise level:       1.556e-04
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [3.0] x [15]
      Noise level:       1.001e-04
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [6.0] x [0]
      Noise level:       1.947e-04
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:04 h
    
      Smoothing kernel:  [6.0] x [3]
      Noise level:       1.561e-04
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:04 h
    
      Smoothing kernel:  [6.0] x [7]
      Noise level:       1.053e-04
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
      Smoothing kernel:  [6.0] x [15]
      Noise level:       6.792e-05
    
      Elapsed time: 00:00:04 h
      CPU time:     00:00:05 h
    
      Smoothing kernel:  [9.0] x [0]
      Noise level:       1.206e-04
    
      Elapsed time: 00:00:04 h
      CPU time:     00:00:05 h
    
      Smoothing kernel:  [9.0] x [3]
      Noise level:       9.713e-05
    
      Elapsed time: 00:00:04 h
      CPU time:     00:00:06 h
    
      Smoothing kernel:  [9.0] x [7]
      Noise level:       6.576e-05
    
      Elapsed time: 00:00:04 h
      CPU time:     00:00:06 h
    
      Smoothing kernel:  [9.0] x [15]
      Noise level:       4.225e-05
    
      Elapsed time: 00:00:04 h
      CPU time:     00:00:06 h
    
    ____________________________________________________________________________
    
     Creating source mask
    ____________________________________________________________________________
    
      340830 pixels detected by source finder (2.358%).
    
      Elapsed time: 00:00:04 h
      CPU time:     00:00:06 h
    
    ____________________________________________________________________________
    
     Running Linker
    ____________________________________________________________________________
    
      Linker settings:
       - Merging radii:   2, 2, 3
       - Minimum size:    5 x 5 x 5
       - Min/max fill:    5.0%, 0.0%
       - Keep negative:   yes
    
      Linker status:
       - No. of objects:  338
       - Memory usage:    45.22 kB
    
    
      Elapsed time: 00:00:04 h
      CPU time:     00:00:07 h
    
    ____________________________________________________________________________
    
     Measuring reliability
    ____________________________________________________________________________
    
      Using 3D parameter space:
       - peak
       - sum
       - mean
      Found 173 positive and 165 negative sources.
      Retaining all negative detections.
      Using auto-kernel feature.
        Iter.  1: kernel = 0.100, median = 0.990
        Iter.  2: kernel = 0.200, median = 0.749
        Iter.  3: kernel = 0.300, median = 0.563
        Iter.  4: kernel = 0.400, median = 0.459
        Iter.  5: kernel = 0.440, median = 0.396
        Iter.  6: kernel = 0.480, median = 0.323
        Iter.  7: kernel = 0.520, median = 0.284
        Iter.  8: kernel = 0.560, median = 0.232
        Iter.  9: kernel = 0.600, median = 0.204
        Iter. 10: kernel = 0.640, median = 0.169
        Iter. 11: kernel = 0.680, median = 0.163
        Iter. 12: kernel = 0.720, median = 0.146
        Iter. 13: kernel = 0.760, median = 0.130
        Iter. 14: kernel = 0.800, median = 0.128
        Iter. 15: kernel = 0.840, median = 0.111
        Iter. 16: kernel = 0.880, median = 0.091
        Iter. 17: kernel = 0.920, median = 0.083
        Iter. 18: kernel = 0.960, median = 0.072
        Iter. 19: kernel = 1.000, median = 0.062
        Iter. 20: kernel = 1.040, median = 0.049
      Converged to scale_kernel = 1.040 after 20 iterations.
      
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_rel.eps
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw21.cube.I.pbcor_skellam.eps
    
    ERROR: No reliable sources found. Terminating pipeline.
           Terminating with error code 8.
    
2025-09-03 15:19:57,049 | ERROR | [PID:13388] sopar: - Error running SoFia. Mode: emission. Error: Command '['sofia', '/home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID13388.par']' returned non-zero exit status 8.
2025-09-03 15:19:57,051 | INFO | [PID:13388] sopar: - SoFia execution aborted. Mode: emission.
2025-09-03 15:19:57,056 | INFO | [PID:13388] sopar: - Quality assesment start. Mode: emission.
2025-09-03 15:19:57,059 | WARNING | [PID:13388] sopar: - No data cube has been specified with Primary Beam information.
2025-09-03 15:19:57,071 | WARNING | [PID:13388] sopar: - 2D-Mask file from SoFia not found in /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission.
2025-09-03 15:19:57,072 | INFO | [PID:13388] sopar: - Quality assesment aborted.
2025-09-03 15:19:57,074 | INFO | [PID:13388] sipargs: - The file in /home/usuario/ADP-ALMA-Pipeline/adplib/sip/sip_args.yaml have been loaded successfully
2025-09-03 15:19:57,078 | ERROR | [PID:13388] sipargs: - No valid .txt or .xml catalog for SIP found within the  /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption  directory.
2025-09-03 15:19:57,078 | INFO | [PID:13388] sipargs: - SIP execution skipped. Run: absorption
2025-09-03 15:19:57,078 | ERROR | [PID:13388] sipargs: - No valid .txt or .xml catalog for SIP found within the  /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission  directory.
2025-09-03 15:19:57,078 | INFO | [PID:13388] sipargs: - SIP execution aborted. Run: emission.
===  Subprocess PID: 13388 end  ===


=== Subprocess PID: 13389 start ===
2025-09-03 15:19:49,555 | INFO | [PID:13389] sopar: - The file in '/home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_abs_default.par' have been loaded successfully
2025-09-03 15:19:49,582 | INFO | [PID:13389] sopar: - The file in '/home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_emi_default.par' have been loaded successfully
2025-09-03 15:19:49,674 | INFO | [PID:13389] sopar: - Reading parameters. Mode: absorption.
2025-09-03 15:19:49,674 | WARNING | [PID:13389] sopar: - Ignoring parameter 'input.data' provided in the parameter file /home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_abs_default.par. If you want to change this, specify it in the input_data_set or input_data_file parameter in the configuration file.
2025-09-03 15:19:49,674 | INFO | [PID:13389] sopar: - Parameters ready. Mode: absorption.
2025-09-03 15:19:49,674 | INFO | [PID:13389] sopar: - Reading parameters. Mode: emission.
2025-09-03 15:19:49,682 | INFO | [PID:13389] sopar: - Parameters ready. Mode: emission.
2025-09-03 15:19:49,691 | INFO | [PID:13389] sopar: - Creating temporary SoFiA parameter file based on the parameter file /home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_abs_default.par.
2025-09-03 15:19:49,693 | INFO | [PID:13389] sopar: - Parameters set for the run: 
[13389]pipeline.verbose=false
[13389]pipeline.pedantic=true
[13389]pipeline.threads=3
[13389]input.data=archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor.fits
[13389]input.primaryBeam=
[13389]input.region=
[13389]input.gain=
[13389]input.noise=
[13389]input.weights=
[13389]input.mask=
[13389]input.invert=true
[13389]flag.region=
[13389]flag.catalog=
[13389]flag.radius=5
[13389]flag.auto=false
[13389]flag.threshold=5.0
[13389]flag.log=false
[13389]flag.cube=
[13389]contsub.enable=false
[13389]contsub.order=0
[13389]contsub.threshold=2.0
[13389]contsub.shift=4
[13389]contsub.padding=3
[13389]scaleNoise.enable=false
[13389]scaleNoise.mode=local
[13389]scaleNoise.statistic=mad
[13389]scaleNoise.fluxRange=negative
[13389]scaleNoise.windowXY=31
[13389]scaleNoise.windowZ=31
[13389]scaleNoise.gridXY=0
[13389]scaleNoise.gridZ=0
[13389]scaleNoise.interpolate=false
[13389]scaleNoise.scfind=false
[13389]rippleFilter.enable=false
[13389]rippleFilter.statistic=median
[13389]rippleFilter.windowXY=31
[13389]rippleFilter.windowZ=15
[13389]rippleFilter.gridXY=0
[13389]rippleFilter.gridZ=0
[13389]rippleFilter.interpolate=false
[13389]scfind.enable=true
[13389]scfind.kernelsXY=0, 3, 6, 9
[13389]scfind.kernelsZ=0, 3, 7, 15
[13389]scfind.threshold=3.8
[13389]scfind.replacement=2.0
[13389]scfind.statistic=mad
[13389]scfind.fluxRange=negative
[13389]threshold.enable=false
[13389]threshold.threshold=5.0
[13389]threshold.mode=relative
[13389]threshold.statistic=mad
[13389]threshold.fluxRange=negative
[13389]linker.enable=true
[13389]linker.radiusXY=2
[13389]linker.radiusZ=3
[13389]linker.minSizeXY=5
[13389]linker.minSizeZ=5
[13389]linker.maxSizeXY=0
[13389]linker.maxSizeZ=0
[13389]linker.minPixels=0
[13389]linker.maxPixels=0
[13389]linker.minFill=0.05
[13389]linker.maxFill=0.0
[13389]linker.positivity=false
[13389]linker.keepNegative=false
[13389]reliability.enable=true
[13389]reliability.parameters=peak, sum, mean
[13389]reliability.threshold=0.9
[13389]reliability.scaleKernel=0.3
[13389]reliability.minSNR=6.0
[13389]reliability.minPixels=150
[13389]reliability.autoKernel=true
[13389]reliability.iterations=50
[13389]reliability.tolerance=0.05
[13389]reliability.catalog=
[13389]reliability.plot=true
[13389]reliability.plotExtra=false
[13389]reliability.debug=false
[13389]dilation.enable=false
[13389]dilation.iterationsXY=10
[13389]dilation.iterationsZ=5
[13389]dilation.threshold=0.001
[13389]parameter.enable=true
[13389]parameter.wcs=true
[13389]parameter.physical=true
[13389]parameter.prefix=SoFiA
[13389]parameter.offset=false
[13389]output.directory=/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption
[13389]output.file= 
2025-09-03 15:19:49,693 | INFO | [PID:13389] sopar: - SoFia start. Mode: absorption. Input data: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor
    ____________________________________________________________________________
    
     Pipeline started
    ____________________________________________________________________________
    
      Software:  Source Finding Application (SoFiA)
      Version:   2.6.14 (2025-05-14)
      CPU:       12 threads available
      Memory:    12.7 GB total / 2.0 GB free
      Date:      2025-09-03
      Time:      13:19:49 h
    ____________________________________________________________________________
    
     Loading parameter settings
    ____________________________________________________________________________
    
      Activating SoFiA default parameter settings.
      Loading user-specified parameters.
      - Loading user parameter file: /home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID13389.par
      Using 3 out of 12 available CPU threads.
    
    WARNING: ┌──────────────────────────────────────────────────────────┐
             │ You have set parameter.physical = true. SoFiA will try   │
             │ to convert some parameters to physical units under the   │
             │ following fundamental assumptions:                       │
             │                                                          │
             │  * The beam information in the FITS header (BMAJ, BMIN)  │
             │    is correct and accurate across the entire data cube.  │
             │                                                          │
             │  * The spectral channels of the data cube are uncorrela- │
             │    ted, i.e. spectral resolution equals channel width.   │
             │                                                          │
             │ Should any of these assumptions be incorrect then the    │
             │ measurement of 
    ____________________________________________________________________________
    
     Loading data cube
    ____________________________________________________________________________
    
      Opening FITS file 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor.fits'.
      Reading FITS data with the following specifications:
        Data type:    -32
        No. of axes:  4
        Axis sizes:   350, 350, 118
        Region:       0-349, 0-349, 0-117
        Memory used:  55.1 MB
      Searching for values of infinity.
        No infinite data values found.
      Inverting data cube
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Measuring global noise level
    ____________________________________________________________________________
    
      Global RMS:  4.146e-04  (using stride of 14)
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Running S+C finder
    ____________________________________________________________________________
    
      Using the following parameters:
      - Kernels
        - spatial:        0, 3, 6, 9
        - spectral:       0, 3, 7, 15
      - Flux threshold:   3.8 * rms
      - Noise statistic:  median absolute deviation
      - Flux range:       negative
    
      Using a stride of 14 in noise measurement.
    
      Smoothing kernel:  [0.0] x [0]
      Noise level:       4.146e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [3]
      Noise level:       3.304e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [7]
      Noise level:       2.238e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [15]
      Noise level:       1.431e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [3.0] x [0]
      Noise level:       3.036e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [3.0] x [3]
      Noise level:       2.415e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [3.0] x [7]
      Noise level:       1.627e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [3.0] x [15]
      Noise level:       1.044e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [6.0] x [0]
      Noise level:       2.065e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [6.0] x [3]
      Noise level:       1.644e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [6.0] x [7]
      Noise level:       1.105e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [6.0] x [15]
      Noise level:       7.082e-05
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [9.0] x [0]
      Noise level:       1.287e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [9.0] x [3]
      Noise level:       1.032e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:04 h
    
      Smoothing kernel:  [9.0] x [7]
      Noise level:       6.898e-05
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:04 h
    
      Smoothing kernel:  [9.0] x [15]
      Noise level:       4.467e-05
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:04 h
    
    ____________________________________________________________________________
    
     Creating source mask
    ____________________________________________________________________________
    
      362741 pixels detected by source finder (2.509%).
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:04 h
    
    ____________________________________________________________________________
    
     Running Linker
    ____________________________________________________________________________
    
      Linker settings:
       - Merging radii:   2, 2, 3
       - Minimum size:    5 x 5 x 5
       - Min/max fill:    5.0%, 0.0%
       - Keep negative:   yes
    
      Linker status:
       - No. of objects:  368
       - Memory usage:    49.23 kB
    
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
    ____________________________________________________________________________
    
     Measuring reliability
    ____________________________________________________________________________
    
      Using 3D parameter space:
       - peak
       - sum
       - mean
      Found 184 positive and 184 negative sources.
      Retaining all negative detections.
      Using auto-kernel feature.
        Iter.  1: kernel = 0.100, median = 0.999
        Iter.  2: kernel = 0.200, median = 0.738
        Iter.  3: kernel = 0.300, median = 0.460
        Iter.  4: kernel = 0.340, median = 0.425
        Iter.  5: kernel = 0.380, median = 0.374
        Iter.  6: kernel = 0.420, median = 0.343
        Iter.  7: kernel = 0.460, median = 0.331
        Iter.  8: kernel = 0.500, median = 0.287
        Iter.  9: kernel = 0.540, median = 0.311
        Iter. 10: kernel = 0.580, median = 0.286
        Iter. 11: kernel = 0.620, median = 0.275
        Iter. 12: kernel = 0.660, median = 0.254
        Iter. 13: kernel = 0.700, median = 0.232
        Iter. 14: kernel = 0.740, median = 0.217
        Iter. 15: kernel = 0.780, median = 0.179
        Iter. 16: kernel = 0.820, median = 0.173
        Iter. 17: kernel = 0.860, median = 0.183
        Iter. 18: kernel = 0.900, median = 0.174
        Iter. 19: kernel = 0.940, median = 0.159
        Iter. 20: kernel = 0.980, median = 0.153
        Iter. 21: kernel = 1.020, median = 0.130
        Iter. 22: kernel = 1.060, median = 0.109
        Iter. 23: kernel = 1.100, median = 0.101
        Iter. 24: kernel = 1.140, median = 0.091
        Iter. 25: kernel = 1.180, median = 0.088
        Iter. 26: kernel = 1.220, median = 0.085
        Iter. 27: kernel = 1.260, median = 0.082
        Iter. 28: kernel = 1.300, median = 0.075
        Iter. 29: kernel = 1.340, median = 0.069
        Iter. 30: kernel = 1.380, median = 0.067
        Iter. 31: kernel = 1.420, median = 0.064
        Iter. 32: kernel = 1.460, median = 0.058
        Iter. 33: kernel = 1.500, median = 0.053
        Iter. 34: kernel = 1.540, median = 0.049
      Converged to scale_kernel = 1.540 after 34 iterations.
      
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_rel.eps
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_skellam.eps
    
    ERROR: No reliable sources found. Terminating pipeline.
           Terminating with error code 8.
    
2025-09-03 15:19:52,474 | ERROR | [PID:13389] sopar: - Error running SoFia. Mode: absorption. Error: Command '['sofia', '/home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID13389.par']' returned non-zero exit status 8.
2025-09-03 15:19:52,474 | INFO | [PID:13389] sopar: - SoFiA will try to run again in mode: emission.
2025-09-03 15:19:52,475 | INFO | [PID:13389] sopar: - Quality assesment start. Mode: absorption.
2025-09-03 15:19:52,481 | WARNING | [PID:13389] sopar: - No data cube has been specified with Primary Beam information.
2025-09-03 15:19:52,501 | WARNING | [PID:13389] sopar: - 2D-Mask file from SoFia not found in /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption.
2025-09-03 15:19:52,501 | INFO | [PID:13389] sopar: - Quality assesment aborted.
2025-09-03 15:19:52,502 | WARNING | [PID:13389] sopar: - There is no mask available from the absorption run. The parameter 'flag_cube' will not be used
2025-09-03 15:19:52,503 | INFO | [PID:13389] sopar: - Creating temporary SoFiA parameter file based on the parameter file /home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_emi_default.par.
2025-09-03 15:19:52,504 | INFO | [PID:13389] sopar: - Parameters set for the run: 
[13389]pipeline.verbose=false
[13389]pipeline.pedantic=true
[13389]pipeline.threads=3
[13389]input.data=archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor.fits
[13389]input.primaryBeam= 
[13389]input.region=
[13389]input.gain=
[13389]input.noise=
[13389]input.weights=
[13389]input.mask=
[13389]input.invert=false
[13389]flag.region=
[13389]flag.catalog=
[13389]flag.radius=5
[13389]flag.auto=false
[13389]flag.threshold=5.0
[13389]flag.log=false
[13389]flag.cube=
[13389]contsub.enable=false
[13389]contsub.order=0
[13389]contsub.threshold=2.0
[13389]contsub.shift=4
[13389]contsub.padding=3
[13389]scaleNoise.enable=false
[13389]scaleNoise.mode=local
[13389]scaleNoise.statistic=mad
[13389]scaleNoise.fluxRange=negative
[13389]scaleNoise.windowXY=31
[13389]scaleNoise.windowZ=31
[13389]scaleNoise.gridXY=0
[13389]scaleNoise.gridZ=0
[13389]scaleNoise.interpolate=false
[13389]scaleNoise.scfind=false
[13389]rippleFilter.enable=false
[13389]rippleFilter.statistic=median
[13389]rippleFilter.windowXY=31
[13389]rippleFilter.windowZ=15
[13389]rippleFilter.gridXY=0
[13389]rippleFilter.gridZ=0
[13389]rippleFilter.interpolate=false
[13389]scfind.enable=true
[13389]scfind.kernelsXY=0, 3, 6, 9
[13389]scfind.kernelsZ=0, 3, 7, 15
[13389]scfind.threshold=3.8
[13389]scfind.replacement=2.0
[13389]scfind.statistic=mad
[13389]scfind.fluxRange=negative
[13389]threshold.enable=false
[13389]threshold.threshold=5.0
[13389]threshold.mode=relative
[13389]threshold.statistic=mad
[13389]threshold.fluxRange=negative
[13389]linker.enable=true
[13389]linker.radiusXY=2
[13389]linker.radiusZ=3
[13389]linker.minSizeXY=5
[13389]linker.minSizeZ=5
[13389]linker.maxSizeXY=0
[13389]linker.maxSizeZ=0
[13389]linker.minPixels=0
[13389]linker.maxPixels=0
[13389]linker.minFill=0.05
[13389]linker.maxFill=0.0
[13389]linker.positivity=false
[13389]linker.keepNegative=false
[13389]reliability.enable=true
[13389]reliability.parameters=peak, sum, mean
[13389]reliability.threshold=0.9
[13389]reliability.scaleKernel=0.3
[13389]reliability.minSNR=6.0
[13389]reliability.minPixels=150
[13389]reliability.autoKernel=true
[13389]reliability.iterations=50
[13389]reliability.tolerance=0.05
[13389]reliability.catalog=
[13389]reliability.plot=true
[13389]reliability.plotExtra=false
[13389]reliability.debug=false
[13389]dilation.enable=false
[13389]dilation.iterationsXY=10
[13389]dilation.iterationsZ=5
[13389]dilation.threshold=0.001
[13389]parameter.enable=true
[13389]parameter.wcs=true
[13389]parameter.physical=true
[13389]parameter.prefix=SoFiA
[13389]parameter.offset=false
[13389]output.directory=/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission
[13389]output.file= 
2025-09-03 15:19:52,505 | INFO | [PID:13389] sopar: - SoFia start. Mode: emission. Input data: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor
    ____________________________________________________________________________
    
     Pipeline started
    ____________________________________________________________________________
    
      Software:  Source Finding Application (SoFiA)
      Version:   2.6.14 (2025-05-14)
      CPU:       12 threads available
      Memory:    12.7 GB total / 0.6 GB free
      Date:      2025-09-03
      Time:      13:19:52 h
    ____________________________________________________________________________
    
     Loading parameter settings
    ____________________________________________________________________________
    
      Activating SoFiA default parameter settings.
      Loading user-specified parameters.
      - Loading user parameter file: /home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID13389.par
      Using 3 out of 12 available CPU threads.
    
    WARNING: ┌──────────────────────────────────────────────────────────┐
             │ You have set parameter.physical = true. SoFiA will try   │
             │ to convert some parameters to physical units under the   │
             │ following fundamental assumptions:                       │
             │                                                          │
             │  * The beam information in the FITS header (BMAJ, BMIN)  │
             │    is correct and accurate across the entire data cube.  │
             │                                                          │
             │  * The spectral channels of the data cube are uncorrela- │
             │    ted, i.e. spectral resolution equals channel width.   │
             │                                                          │
             │ Should any of these assumptions be incorrect then the    │
             │ measurement of 
    ____________________________________________________________________________
    
     Loading data cube
    ____________________________________________________________________________
    
      Opening FITS file 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor.fits'.
      Reading FITS data with the following specifications:
        Data type:    -32
        No. of axes:  4
        Axis sizes:   350, 350, 118
        Region:       0-349, 0-349, 0-117
        Memory used:  55.1 MB
      Searching for values of infinity.
        No infinite data values found.
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Measuring global noise level
    ____________________________________________________________________________
    
      Global RMS:  4.166e-04  (using stride of 14)
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Running S+C finder
    ____________________________________________________________________________
    
      Using the following parameters:
      - Kernels
        - spatial:        0, 3, 6, 9
        - spectral:       0, 3, 7, 15
      - Flux threshold:   3.8 * rms
      - Noise statistic:  median absolute deviation
      - Flux range:       negative
    
      Using a stride of 14 in noise measurement.
    
      Smoothing kernel:  [0.0] x [0]
      Noise level:       4.166e-04
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [3]
      Noise level:       3.324e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:00 h
    
      Smoothing kernel:  [0.0] x [7]
      Noise level:       2.250e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [0.0] x [15]
      Noise level:       1.445e-04
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [3.0] x [0]
      Noise level:       3.062e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [3.0] x [3]
      Noise level:       2.428e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:02 h
    
      Smoothing kernel:  [3.0] x [7]
      Noise level:       1.644e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [3.0] x [15]
      Noise level:       1.058e-04
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [6.0] x [0]
      Noise level:       2.090e-04
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:04 h
    
      Smoothing kernel:  [6.0] x [3]
      Noise level:       1.657e-04
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:04 h
    
      Smoothing kernel:  [6.0] x [7]
      Noise level:       1.121e-04
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:04 h
    
      Smoothing kernel:  [6.0] x [15]
      Noise level:       7.195e-05
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
      Smoothing kernel:  [9.0] x [0]
      Noise level:       1.280e-04
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:05 h
    
      Smoothing kernel:  [9.0] x [3]
      Noise level:       1.017e-04
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:06 h
    
      Smoothing kernel:  [9.0] x [7]
      Noise level:       6.962e-05
    
      Elapsed time: 00:00:04 h
      CPU time:     00:00:06 h
    
      Smoothing kernel:  [9.0] x [15]
      Noise level:       4.450e-05
    
      Elapsed time: 00:00:04 h
      CPU time:     00:00:06 h
    
    ____________________________________________________________________________
    
     Creating source mask
    ____________________________________________________________________________
    
      356422 pixels detected by source finder (2.466%).
    
      Elapsed time: 00:00:04 h
      CPU time:     00:00:06 h
    
    ____________________________________________________________________________
    
     Running Linker
    ____________________________________________________________________________
    
      Linker settings:
       - Merging radii:   2, 2, 3
       - Minimum size:    5 x 5 x 5
       - Min/max fill:    5.0%, 0.0%
       - Keep negative:   yes
    
      Linker status:
       - No. of objects:  359
       - Memory usage:    48.03 kB
    
    
      Elapsed time: 00:00:04 h
      CPU time:     00:00:07 h
    
    ____________________________________________________________________________
    
     Measuring reliability
    ____________________________________________________________________________
    
      Using 3D parameter space:
       - peak
       - sum
       - mean
      Found 184 positive and 175 negative sources.
      Retaining all negative detections.
      Using auto-kernel feature.
        Iter.  1: kernel = 0.100, median = 1.000
        Iter.  2: kernel = 0.200, median = 0.842
        Iter.  3: kernel = 0.300, median = 0.673
        Iter.  4: kernel = 0.400, median = 0.527
        Iter.  5: kernel = 0.500, median = 0.448
        Iter.  6: kernel = 0.540, median = 0.415
        Iter.  7: kernel = 0.580, median = 0.393
        Iter.  8: kernel = 0.620, median = 0.394
        Iter.  9: kernel = 0.660, median = 0.381
        Iter. 10: kernel = 0.700, median = 0.332
        Iter. 11: kernel = 0.740, median = 0.304
        Iter. 12: kernel = 0.780, median = 0.216
        Iter. 13: kernel = 0.820, median = 0.199
        Iter. 14: kernel = 0.860, median = 0.160
        Iter. 15: kernel = 0.900, median = 0.134
        Iter. 16: kernel = 0.940, median = 0.126
        Iter. 17: kernel = 0.980, median = 0.111
        Iter. 18: kernel = 1.020, median = 0.111
        Iter. 19: kernel = 1.060, median = 0.103
        Iter. 20: kernel = 1.100, median = 0.089
        Iter. 21: kernel = 1.140, median = 0.073
        Iter. 22: kernel = 1.180, median = 0.066
        Iter. 23: kernel = 1.220, median = 0.057
        Iter. 24: kernel = 1.260, median = 0.047
      Converged to scale_kernel = 1.260 after 24 iterations.
      
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_rel.eps
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw23.cube.I.pbcor_skellam.eps
    
    ERROR: No reliable sources found. Terminating pipeline.
           Terminating with error code 8.
    
2025-09-03 15:19:56,518 | ERROR | [PID:13389] sopar: - Error running SoFia. Mode: emission. Error: Command '['sofia', '/home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID13389.par']' returned non-zero exit status 8.
2025-09-03 15:19:56,518 | INFO | [PID:13389] sopar: - SoFia execution aborted. Mode: emission.
2025-09-03 15:19:56,519 | INFO | [PID:13389] sopar: - Quality assesment start. Mode: emission.
2025-09-03 15:19:56,521 | WARNING | [PID:13389] sopar: - No data cube has been specified with Primary Beam information.
2025-09-03 15:19:56,542 | WARNING | [PID:13389] sopar: - 2D-Mask file from SoFia not found in /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission.
2025-09-03 15:19:56,542 | INFO | [PID:13389] sopar: - Quality assesment aborted.
2025-09-03 15:19:56,543 | INFO | [PID:13389] sipargs: - The file in /home/usuario/ADP-ALMA-Pipeline/adplib/sip/sip_args.yaml have been loaded successfully
2025-09-03 15:19:56,546 | ERROR | [PID:13389] sipargs: - No valid .txt or .xml catalog for SIP found within the  /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption  directory.
2025-09-03 15:19:56,547 | INFO | [PID:13389] sipargs: - SIP execution skipped. Run: absorption
2025-09-03 15:19:56,548 | ERROR | [PID:13389] sipargs: - No valid .txt or .xml catalog for SIP found within the  /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission  directory.
2025-09-03 15:19:56,549 | INFO | [PID:13389] sipargs: - SIP execution aborted. Run: emission.
===  Subprocess PID: 13389 end  ===


=== Subprocess PID: 13390 start ===
2025-09-03 15:19:49,543 | INFO | [PID:13390] sopar: - The file in '/home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_abs_default.par' have been loaded successfully
2025-09-03 15:19:49,545 | INFO | [PID:13390] sopar: - The file in '/home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_emi_default.par' have been loaded successfully
2025-09-03 15:19:49,547 | INFO | [PID:13390] sopar: - Reading parameters. Mode: absorption.
2025-09-03 15:19:49,553 | WARNING | [PID:13390] sopar: - Ignoring parameter 'input.data' provided in the parameter file /home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_abs_default.par. If you want to change this, specify it in the input_data_set or input_data_file parameter in the configuration file.
2025-09-03 15:19:49,559 | INFO | [PID:13390] sopar: - Parameters ready. Mode: absorption.
2025-09-03 15:19:49,559 | INFO | [PID:13390] sopar: - Reading parameters. Mode: emission.
2025-09-03 15:19:49,582 | INFO | [PID:13390] sopar: - Parameters ready. Mode: emission.
2025-09-03 15:19:49,594 | INFO | [PID:13390] sopar: - Creating temporary SoFiA parameter file based on the parameter file /home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_abs_default.par.
2025-09-03 15:19:49,679 | INFO | [PID:13390] sopar: - Parameters set for the run: 
[13390]pipeline.verbose=false
[13390]pipeline.pedantic=true
[13390]pipeline.threads=3
[13390]input.data=archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor.fits
[13390]input.primaryBeam=
[13390]input.region=
[13390]input.gain=
[13390]input.noise=
[13390]input.weights=
[13390]input.mask=
[13390]input.invert=true
[13390]flag.region=
[13390]flag.catalog=
[13390]flag.radius=5
[13390]flag.auto=false
[13390]flag.threshold=5.0
[13390]flag.log=false
[13390]flag.cube=
[13390]contsub.enable=false
[13390]contsub.order=0
[13390]contsub.threshold=2.0
[13390]contsub.shift=4
[13390]contsub.padding=3
[13390]scaleNoise.enable=false
[13390]scaleNoise.mode=local
[13390]scaleNoise.statistic=mad
[13390]scaleNoise.fluxRange=negative
[13390]scaleNoise.windowXY=31
[13390]scaleNoise.windowZ=31
[13390]scaleNoise.gridXY=0
[13390]scaleNoise.gridZ=0
[13390]scaleNoise.interpolate=false
[13390]scaleNoise.scfind=false
[13390]rippleFilter.enable=false
[13390]rippleFilter.statistic=median
[13390]rippleFilter.windowXY=31
[13390]rippleFilter.windowZ=15
[13390]rippleFilter.gridXY=0
[13390]rippleFilter.gridZ=0
[13390]rippleFilter.interpolate=false
[13390]scfind.enable=true
[13390]scfind.kernelsXY=0, 3, 6, 9
[13390]scfind.kernelsZ=0, 3, 7, 15
[13390]scfind.threshold=3.8
[13390]scfind.replacement=2.0
[13390]scfind.statistic=mad
[13390]scfind.fluxRange=negative
[13390]threshold.enable=false
[13390]threshold.threshold=5.0
[13390]threshold.mode=relative
[13390]threshold.statistic=mad
[13390]threshold.fluxRange=negative
[13390]linker.enable=true
[13390]linker.radiusXY=2
[13390]linker.radiusZ=3
[13390]linker.minSizeXY=5
[13390]linker.minSizeZ=5
[13390]linker.maxSizeXY=0
[13390]linker.maxSizeZ=0
[13390]linker.minPixels=0
[13390]linker.maxPixels=0
[13390]linker.minFill=0.05
[13390]linker.maxFill=0.0
[13390]linker.positivity=false
[13390]linker.keepNegative=false
[13390]reliability.enable=true
[13390]reliability.parameters=peak, sum, mean
[13390]reliability.threshold=0.9
[13390]reliability.scaleKernel=0.3
[13390]reliability.minSNR=6.0
[13390]reliability.minPixels=150
[13390]reliability.autoKernel=true
[13390]reliability.iterations=50
[13390]reliability.tolerance=0.05
[13390]reliability.catalog=
[13390]reliability.plot=true
[13390]reliability.plotExtra=false
[13390]reliability.debug=false
[13390]dilation.enable=false
[13390]dilation.iterationsXY=10
[13390]dilation.iterationsZ=5
[13390]dilation.threshold=0.001
[13390]parameter.enable=true
[13390]parameter.wcs=true
[13390]parameter.physical=true
[13390]parameter.prefix=SoFiA
[13390]parameter.offset=false
[13390]output.directory=/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption
[13390]output.file= 
2025-09-03 15:19:49,683 | INFO | [PID:13390] sopar: - SoFia start. Mode: absorption. Input data: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor
    ____________________________________________________________________________
    
     Pipeline started
    ____________________________________________________________________________
    
      Software:  Source Finding Application (SoFiA)
      Version:   2.6.14 (2025-05-14)
      CPU:       12 threads available
      Memory:    12.7 GB total / 2.0 GB free
      Date:      2025-09-03
      Time:      13:19:49 h
    ____________________________________________________________________________
    
     Loading parameter settings
    ____________________________________________________________________________
    
      Activating SoFiA default parameter settings.
      Loading user-specified parameters.
      - Loading user parameter file: /home/usuario/ADP-ALMA-Pipeline/sofia_abs_default_tmp_PID13390.par
      Using 3 out of 12 available CPU threads.
    
    WARNING: ┌──────────────────────────────────────────────────────────┐
             │ You have set parameter.physical = true. SoFiA will try   │
             │ to convert some parameters to physical units under the   │
             │ following fundamental assumptions:                       │
             │                                                          │
             │  * The beam information in the FITS header (BMAJ, BMIN)  │
             │    is correct and accurate across the entire data cube.  │
             │                                                          │
             │  * The spectral channels of the data cube are uncorrela- │
             │    ted, i.e. spectral resolution equals channel width.   │
             │                                                          │
             │ Should any of these assumptions be incorrect then the    │
             │ measurement of 
    ____________________________________________________________________________
    
     Loading data cube
    ____________________________________________________________________________
    
      Opening FITS file 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor.fits'.
      Reading FITS data with the following specifications:
        Data type:    -32
        No. of axes:  4
        Axis sizes:   350, 350, 1918
        Region:       0-349, 0-349, 0-1917
        Memory used:  896.3 MB
      Searching for values of infinity.
        No infinite data values found.
      Inverting data cube
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:02 h
    
    ____________________________________________________________________________
    
     Measuring global noise level
    ____________________________________________________________________________
    
      Global RMS:  2.255e-03  (using stride of 234)
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:02 h
    
    ____________________________________________________________________________
    
     Running S+C finder
    ____________________________________________________________________________
    
      Using the following parameters:
      - Kernels
        - spatial:        0, 3, 6, 9
        - spectral:       0, 3, 7, 15
      - Flux threshold:   3.8 * rms
      - Noise statistic:  median absolute deviation
      - Flux range:       negative
    
      Using a stride of 234 in noise measurement.
    
      Smoothing kernel:  [0.0] x [0]
      Noise level:       2.255e-03
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:03 h
    
      Smoothing kernel:  [0.0] x [3]
      Noise level:       1.545e-03
    
      Elapsed time: 00:00:07 h
      CPU time:     00:00:08 h
    
      Smoothing kernel:  [0.0] x [7]
      Noise level:       1.038e-03
    
      Elapsed time: 00:00:09 h
      CPU time:     00:00:13 h
    
      Smoothing kernel:  [0.0] x [15]
      Noise level:       7.183e-04
    
      Elapsed time: 00:00:10 h
      CPU time:     00:00:16 h
    
      Smoothing kernel:  [3.0] x [0]
      Noise level:       1.520e-03
    
      Elapsed time: 00:00:11 h
      CPU time:     00:00:18 h
    
      Smoothing kernel:  [3.0] x [3]
      Noise level:       1.046e-03
    
      Elapsed time: 00:00:13 h
      CPU time:     00:00:22 h
    
      Smoothing kernel:  [3.0] x [7]
      Noise level:       7.063e-04
    
      Elapsed time: 00:00:14 h
      CPU time:     00:00:25 h
    
      Smoothing kernel:  [3.0] x [15]
      Noise level:       4.898e-04
    
      Elapsed time: 00:00:16 h
      CPU time:     00:00:28 h
    
      Smoothing kernel:  [6.0] x [0]
      Noise level:       9.906e-04
    
      Elapsed time: 00:00:17 h
      CPU time:     00:00:31 h
    
      Smoothing kernel:  [6.0] x [3]
      Noise level:       6.883e-04
    
      Elapsed time: 00:00:18 h
      CPU time:     00:00:34 h
    
      Smoothing kernel:  [6.0] x [7]
      Noise level:       4.645e-04
    
      Elapsed time: 00:00:20 h
      CPU time:     00:00:37 h
    
      Smoothing kernel:  [6.0] x [15]
      Noise level:       3.223e-04
    
      Elapsed time: 00:00:21 h
      CPU time:     00:00:41 h
    
      Smoothing kernel:  [9.0] x [0]
      Noise level:       5.970e-04
    
      Elapsed time: 00:00:22 h
      CPU time:     00:00:43 h
    
      Smoothing kernel:  [9.0] x [3]
      Noise level:       4.203e-04
    
      Elapsed time: 00:00:24 h
      CPU time:     00:00:47 h
    
      Smoothing kernel:  [9.0] x [7]
      Noise level:       2.863e-04
    
      Elapsed time: 00:00:26 h
      CPU time:     00:00:50 h
    
      Smoothing kernel:  [9.0] x [15]
      Noise level:       1.985e-04
    
      Elapsed time: 00:00:27 h
      CPU time:     00:00:54 h
    
    ____________________________________________________________________________
    
     Creating source mask
    ____________________________________________________________________________
    
      5045877 pixels detected by source finder (2.148%).
    
      Elapsed time: 00:00:27 h
      CPU time:     00:00:54 h
    
    ____________________________________________________________________________
    
     Running Linker
    ____________________________________________________________________________
    
      Linker settings:
       - Merging radii:   2, 2, 3
       - Minimum size:    5 x 5 x 5
       - Min/max fill:    5.0%, 0.0%
       - Keep negative:   yes
    
      Linker status:
       - No. of objects:  2865
       - Memory usage:    383.31 kB
    
    
      Elapsed time: 00:00:30 h
      CPU time:     00:00:57 h
    
    ____________________________________________________________________________
    
     Measuring reliability
    ____________________________________________________________________________
    
      Using 3D parameter space:
       - peak
       - sum
       - mean
      Found 1400 positive and 1465 negative sources.
      Retaining all negative detections.
      Using auto-kernel feature.
        Iter.  1: kernel = 0.100, median = 0.749
        Iter.  2: kernel = 0.200, median = 0.394
        Iter.  3: kernel = 0.240, median = 0.337
        Iter.  4: kernel = 0.280, median = 0.310
        Iter.  5: kernel = 0.320, median = 0.275
        Iter.  6: kernel = 0.360, median = 0.258
        Iter.  7: kernel = 0.400, median = 0.249
        Iter.  8: kernel = 0.440, median = 0.241
        Iter.  9: kernel = 0.480, median = 0.223
        Iter. 10: kernel = 0.520, median = 0.204
        Iter. 11: kernel = 0.560, median = 0.216
        Iter. 12: kernel = 0.600, median = 0.210
        Iter. 13: kernel = 0.640, median = 0.212
        Iter. 14: kernel = 0.680, median = 0.219
        Iter. 15: kernel = 0.720, median = 0.218
        Iter. 16: kernel = 0.760, median = 0.226
        Iter. 17: kernel = 0.800, median = 0.239
        Iter. 18: kernel = 0.840, median = 0.241
        Iter. 19: kernel = 0.880, median = 0.257
        Iter. 20: kernel = 0.920, median = 0.272
        Iter. 21: kernel = 0.960, median = 0.284
        Iter. 22: kernel = 1.000, median = 0.304
        Iter. 23: kernel = 1.040, median = 0.321
        Iter. 24: kernel = 1.080, median = 0.341
        Iter. 25: kernel = 1.120, median = 0.354
        Iter. 26: kernel = 1.160, median = 0.377
        Iter. 27: kernel = 1.200, median = 0.396
        Iter. 28: kernel = 1.240, median = 0.415
        Iter. 29: kernel = 1.280, median = 0.437
        Iter. 30: kernel = 1.320, median = 0.448
        Iter. 31: kernel = 1.360, median = 0.470
        Iter. 32: kernel = 1.400, median = 0.492
        Iter. 33: kernel = 1.440, median = 0.512
        Iter. 34: kernel = 1.540, median = 0.559
        Iter. 35: kernel = 1.640, median = 0.602
        Iter. 36: kernel = 1.740, median = 0.642
        Iter. 37: kernel = 1.840, median = 0.684
        Iter. 38: kernel = 1.940, median = 0.722
        Iter. 39: kernel = 2.040, median = 0.758
        Iter. 40: kernel = 2.140, median = 0.791
        Iter. 41: kernel = 2.240, median = 0.821
        Iter. 42: kernel = 2.340, median = 0.849
        Iter. 43: kernel = 2.440, median = 0.874
        Iter. 44: kernel = 2.540, median = 0.897
        Iter. 45: kernel = 2.640, median = 0.918
        Iter. 46: kernel = 2.740, median = 0.937
        Iter. 47: kernel = 2.840, median = 0.955
        Iter. 48: kernel = 2.940, median = 0.970
        Iter. 49: kernel = 3.040, median = 0.985
        Iter. 50: kernel = 3.140, median = 0.998
    WARNING: Auto-kernel failed to converge, defaulting to kernel scale of 0.300.
      
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_rel.eps
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_skellam.eps
      2 reliable sources found.
    
      Elapsed time: 00:00:33 h
      CPU time:     00:01:06 h
    
    ____________________________________________________________________________
    
     Creating initial catalogue
    ____________________________________________________________________________
    
      Initial source catalogue created.
    
      Elapsed time: 00:00:33 h
      CPU time:     00:01:06 h
    
    ____________________________________________________________________________
    
     Measuring source parameters
    ____________________________________________________________________________
    
      Found 2 sources in need of parameterisation.
      Assuming beam size of 6.4 x 5.1 pixels.
    
      Attempting to measure parameters in physical units.
    
      Elapsed time: 00:00:33 h
      CPU time:     00:01:06 h
    
    ____________________________________________________________________________
    
     Creating cubelets
    ____________________________________________________________________________
    
      Flux threshold (moment 1 and 2): 0.00e+00
      Assuming beam size of 6.4 x 5.1 pixels.
    
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_cube.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mask.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom0.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom1.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom2.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_chan.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_snr.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_mask.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min_mask.fits
      Creating text file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec.txt
      Creating text file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec_aperture.txt
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_cube.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mask.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom0.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom1.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom2.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_chan.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_snr.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv_min.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv_mask.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv_min_mask.fits
      Creating text file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_spec.txt
      Creating text file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_spec_aperture.txt
    
      Elapsed time: 00:00:33 h
      CPU time:     00:01:06 h
    
    ____________________________________________________________________________
    
     Creating moment maps
    ____________________________________________________________________________
    
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mom0.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mom1.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mom2.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_chan.fits
    
      Elapsed time: 00:00:34 h
      CPU time:     00:01:07 h
    
    ____________________________________________________________________________
    
     Writing mask cube
    ____________________________________________________________________________
    
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mask-2d.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mask.fits
    
      Elapsed time: 00:00:39 h
      CPU time:     00:01:21 h
    
    ____________________________________________________________________________
    
     Writing source catalogue
    ____________________________________________________________________________
    
      Writing ASCII file:   member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cat.txt
      Writing VOTable file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cat.xml
    
      Elapsed time: 00:00:39 h
      CPU time:     00:01:21 h
    
    ____________________________________________________________________________
    
     Pipeline finished
    ____________________________________________________________________________
    
2025-09-03 15:20:28,994 | INFO | [PID:13390] sopar: - SoFia finished. Mode: absorption
2025-09-03 15:20:28,995 | INFO | [PID:13390] sopar: - Quality assesment start. Mode: absorption.
2025-09-03 15:20:29,001 | WARNING | [PID:13390] sopar: - No data cube has been specified with Primary Beam information.
2025-09-03 15:20:32,170 | INFO | [PID:13390] sopar: - QA file saved in /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/quality_assesment_products. Quality assesment completed successfully. Mode: absorption
2025-09-03 15:20:32,178 | INFO | [PID:13390] sopar: - Creating temporary SoFiA parameter file based on the parameter file /home/usuario/ADP-ALMA-Pipeline/adplib/sofia/sofia_emi_default.par.
2025-09-03 15:20:32,179 | INFO | [PID:13390] sopar: - Parameters set for the run: 
[13390]pipeline.verbose=false
[13390]pipeline.pedantic=true
[13390]pipeline.threads=3
[13390]input.data=archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor.fits
[13390]input.primaryBeam= 
[13390]input.region=
[13390]input.gain=
[13390]input.noise=
[13390]input.weights=
[13390]input.mask=
[13390]input.invert=false
[13390]flag.region=
[13390]flag.catalog=
[13390]flag.radius=5
[13390]flag.auto=false
[13390]flag.threshold=5.0
[13390]flag.log=false
[13390]flag.cube=/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mask.fits
[13390]contsub.enable=false
[13390]contsub.order=0
[13390]contsub.threshold=2.0
[13390]contsub.shift=4
[13390]contsub.padding=3
[13390]scaleNoise.enable=false
[13390]scaleNoise.mode=local
[13390]scaleNoise.statistic=mad
[13390]scaleNoise.fluxRange=negative
[13390]scaleNoise.windowXY=31
[13390]scaleNoise.windowZ=31
[13390]scaleNoise.gridXY=0
[13390]scaleNoise.gridZ=0
[13390]scaleNoise.interpolate=false
[13390]scaleNoise.scfind=false
[13390]rippleFilter.enable=false
[13390]rippleFilter.statistic=median
[13390]rippleFilter.windowXY=31
[13390]rippleFilter.windowZ=15
[13390]rippleFilter.gridXY=0
[13390]rippleFilter.gridZ=0
[13390]rippleFilter.interpolate=false
[13390]scfind.enable=true
[13390]scfind.kernelsXY=0, 3, 6, 9
[13390]scfind.kernelsZ=0, 3, 7, 15
[13390]scfind.threshold=3.8
[13390]scfind.replacement=2.0
[13390]scfind.statistic=mad
[13390]scfind.fluxRange=negative
[13390]threshold.enable=false
[13390]threshold.threshold=5.0
[13390]threshold.mode=relative
[13390]threshold.statistic=mad
[13390]threshold.fluxRange=negative
[13390]linker.enable=true
[13390]linker.radiusXY=2
[13390]linker.radiusZ=3
[13390]linker.minSizeXY=5
[13390]linker.minSizeZ=5
[13390]linker.maxSizeXY=0
[13390]linker.maxSizeZ=0
[13390]linker.minPixels=0
[13390]linker.maxPixels=0
[13390]linker.minFill=0.05
[13390]linker.maxFill=0.0
[13390]linker.positivity=false
[13390]linker.keepNegative=false
[13390]reliability.enable=true
[13390]reliability.parameters=peak, sum, mean
[13390]reliability.threshold=0.9
[13390]reliability.scaleKernel=0.3
[13390]reliability.minSNR=6.0
[13390]reliability.minPixels=150
[13390]reliability.autoKernel=true
[13390]reliability.iterations=50
[13390]reliability.tolerance=0.05
[13390]reliability.catalog=
[13390]reliability.plot=true
[13390]reliability.plotExtra=false
[13390]reliability.debug=false
[13390]dilation.enable=false
[13390]dilation.iterationsXY=10
[13390]dilation.iterationsZ=5
[13390]dilation.threshold=0.001
[13390]parameter.enable=true
[13390]parameter.wcs=true
[13390]parameter.physical=true
[13390]parameter.prefix=SoFiA
[13390]parameter.offset=false
[13390]output.directory=/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission
[13390]output.file= 
2025-09-03 15:20:32,180 | INFO | [PID:13390] sopar: - SoFia start. Mode: emission. Input data: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor
    ____________________________________________________________________________
    
     Pipeline started
    ____________________________________________________________________________
    
      Software:  Source Finding Application (SoFiA)
      Version:   2.6.14 (2025-05-14)
      CPU:       12 threads available
      Memory:    12.7 GB total / 2.4 GB free
      Date:      2025-09-03
      Time:      13:20:32 h
    ____________________________________________________________________________
    
     Loading parameter settings
    ____________________________________________________________________________
    
      Activating SoFiA default parameter settings.
      Loading user-specified parameters.
      - Loading user parameter file: /home/usuario/ADP-ALMA-Pipeline/sofia_emi_default_tmp_PID13390.par
      Using 3 out of 12 available CPU threads.
    
    WARNING: ┌──────────────────────────────────────────────────────────┐
             │ You have set parameter.physical = true. SoFiA will try   │
             │ to convert some parameters to physical units under the   │
             │ following fundamental assumptions:                       │
             │                                                          │
             │  * The beam information in the FITS header (BMAJ, BMIN)  │
             │    is correct and accurate across the entire data cube.  │
             │                                                          │
             │  * The spectral channels of the data cube are uncorrela- │
             │    ted, i.e. spectral resolution equals channel width.   │
             │                                                          │
             │ Should any of these assumptions be incorrect then the    │
             │ measurement of 
    ____________________________________________________________________________
    
     Loading data cube
    ____________________________________________________________________________
    
      Opening FITS file 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor.fits'.
      Reading FITS data with the following specifications:
        Data type:    -32
        No. of axes:  4
        Axis sizes:   350, 350, 1918
        Region:       0-349, 0-349, 0-1917
        Memory used:  896.3 MB
      Searching for values of infinity.
        No infinite data values found.
    
      Elapsed time: 00:00:00 h
      CPU time:     00:00:00 h
    
    ____________________________________________________________________________
    
     Loading and applying flag cube
    ____________________________________________________________________________
    
      Opening FITS file '/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mask.fits'.
      Reading FITS data with the following specifications:
        Data type:    32
        No. of axes:  3
        Axis sizes:   350, 350, 1918
        Region:       0-349, 0-349, 0-1917
        Memory used:  896.3 MB
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
    ____________________________________________________________________________
    
     Measuring global noise level
    ____________________________________________________________________________
    
      Global RMS:  2.249e-03  (using stride of 234)
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
    ____________________________________________________________________________
    
     Running S+C finder
    ____________________________________________________________________________
    
      Using the following parameters:
      - Kernels
        - spatial:        0, 3, 6, 9
        - spectral:       0, 3, 7, 15
      - Flux threshold:   3.8 * rms
      - Noise statistic:  median absolute deviation
      - Flux range:       negative
    
      Using a stride of 234 in noise measurement.
    
      Smoothing kernel:  [0.0] x [0]
      Noise level:       2.249e-03
    
      Elapsed time: 00:00:01 h
      CPU time:     00:00:01 h
    
      Smoothing kernel:  [0.0] x [3]
      Noise level:       1.554e-03
    
      Elapsed time: 00:00:02 h
      CPU time:     00:00:04 h
    
      Smoothing kernel:  [0.0] x [7]
      Noise level:       1.052e-03
    
      Elapsed time: 00:00:03 h
      CPU time:     00:00:06 h
    
      Smoothing kernel:  [0.0] x [15]
      Noise level:       7.272e-04
    
      Elapsed time: 00:00:04 h
      CPU time:     00:00:08 h
    
      Smoothing kernel:  [3.0] x [0]
      Noise level:       1.528e-03
    
      Elapsed time: 00:00:05 h
      CPU time:     00:00:10 h
    
      Smoothing kernel:  [3.0] x [3]
      Noise level:       1.058e-03
    
      Elapsed time: 00:00:07 h
      CPU time:     00:00:14 h
    
      Smoothing kernel:  [3.0] x [7]
      Noise level:       7.177e-04
    
      Elapsed time: 00:00:08 h
      CPU time:     00:00:17 h
    
      Smoothing kernel:  [3.0] x [15]
      Noise level:       4.953e-04
    
      Elapsed time: 00:00:09 h
      CPU time:     00:00:20 h
    
      Smoothing kernel:  [6.0] x [0]
      Noise level:       9.928e-04
    
      Elapsed time: 00:00:11 h
      CPU time:     00:00:23 h
    
      Smoothing kernel:  [6.0] x [3]
      Noise level:       6.963e-04
    
      Elapsed time: 00:00:12 h
      CPU time:     00:00:27 h
    
      Smoothing kernel:  [6.0] x [7]
      Noise level:       4.738e-04
    
      Elapsed time: 00:00:14 h
      CPU time:     00:00:30 h
    
      Smoothing kernel:  [6.0] x [15]
      Noise level:       3.272e-04
    
      Elapsed time: 00:00:15 h
      CPU time:     00:00:34 h
    
      Smoothing kernel:  [9.0] x [0]
      Noise level:       6.005e-04
    
      Elapsed time: 00:00:17 h
      CPU time:     00:00:37 h
    
      Smoothing kernel:  [9.0] x [3]
      Noise level:       4.236e-04
    
      Elapsed time: 00:00:19 h
      CPU time:     00:00:42 h
    
      Smoothing kernel:  [9.0] x [7]
      Noise level:       2.909e-04
    
      Elapsed time: 00:00:21 h
      CPU time:     00:00:47 h
    
      Smoothing kernel:  [9.0] x [15]
      Noise level:       2.022e-04
    
      Elapsed time: 00:00:23 h
      CPU time:     00:00:50 h
    
    ____________________________________________________________________________
    
     Creating source mask
    ____________________________________________________________________________
    
      4766842 pixels detected by source finder (2.029%).
    
      Elapsed time: 00:00:23 h
      CPU time:     00:00:51 h
    
    ____________________________________________________________________________
    
     Running Linker
    ____________________________________________________________________________
    
      Linker settings:
       - Merging radii:   2, 2, 3
       - Minimum size:    5 x 5 x 5
       - Min/max fill:    5.0%, 0.0%
       - Keep negative:   yes
    
      Linker status:
       - No. of objects:  2898
       - Memory usage:    387.72 kB
    
    
      Elapsed time: 00:00:26 h
      CPU time:     00:00:54 h
    
    ____________________________________________________________________________
    
     Measuring reliability
    ____________________________________________________________________________
    
      Using 3D parameter space:
       - peak
       - sum
       - mean
      Found 1468 positive and 1430 negative sources.
      Retaining all negative detections.
      Using auto-kernel feature.
        Iter.  1: kernel = 0.100, median = 0.719
        Iter.  2: kernel = 0.200, median = 0.331
        Iter.  3: kernel = 0.240, median = 0.221
        Iter.  4: kernel = 0.280, median = 0.136
        Iter.  5: kernel = 0.320, median = 0.074
        Iter.  6: kernel = 0.360, median = 0.037
      Converged to scale_kernel = 0.360 after 6 iterations.
      
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_rel.eps
      Creating postscript file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_skellam.eps
      1 reliable source found.
    
      Elapsed time: 00:00:26 h
      CPU time:     00:00:55 h
    
    ____________________________________________________________________________
    
     Creating initial catalogue
    ____________________________________________________________________________
    
      Initial source catalogue created.
    
      Elapsed time: 00:00:26 h
      CPU time:     00:00:55 h
    
    ____________________________________________________________________________
    
     Reloading data cube for parameterisation
    ____________________________________________________________________________
    
      Opening FITS file 'archive_data/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor.fits'.
      Reading FITS data with the following specifications:
        Data type:    -32
        No. of axes:  4
        Axis sizes:   350, 350, 1918
        Region:       0-349, 0-349, 0-1917
        Memory used:  896.3 MB
    
      Elapsed time: 00:00:26 h
      CPU time:     00:00:55 h
    
    ____________________________________________________________________________
    
     Measuring source parameters
    ____________________________________________________________________________
    
      Found 1 source in need of parameterisation.
      Assuming beam size of 6.4 x 5.1 pixels.
    
      Attempting to measure parameters in physical units.
    
      Elapsed time: 00:00:26 h
      CPU time:     00:00:55 h
    
    ____________________________________________________________________________
    
     Creating cubelets
    ____________________________________________________________________________
    
      Flux threshold (moment 1 and 2): 0.00e+00
      Assuming beam size of 6.4 x 5.1 pixels.
    
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_cube.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mask.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom0.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom1.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom2.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_chan.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_snr.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_mask.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min_mask.fits
      Creating text file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec.txt
      Creating text file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec_aperture.txt
    
      Elapsed time: 00:00:26 h
      CPU time:     00:00:55 h
    
    ____________________________________________________________________________
    
     Creating moment maps
    ____________________________________________________________________________
    
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mom0.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mom1.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mom2.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_chan.fits
    
      Elapsed time: 00:00:27 h
      CPU time:     00:00:56 h
    
    ____________________________________________________________________________
    
     Writing mask cube
    ____________________________________________________________________________
    
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mask-2d.fits
      Creating FITS file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_mask.fits
    
      Elapsed time: 00:00:32 h
      CPU time:     00:01:07 h
    
    ____________________________________________________________________________
    
     Writing source catalogue
    ____________________________________________________________________________
    
      Writing ASCII file:   member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cat.txt
      Writing VOTable file: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cat.xml
    
      Elapsed time: 00:00:32 h
      CPU time:     00:01:07 h
    
    ____________________________________________________________________________
    
     Pipeline finished
    ____________________________________________________________________________
    
2025-09-03 15:21:04,818 | INFO | [PID:13390] sopar: - SoFia finished. Mode: emission
2025-09-03 15:21:04,819 | INFO | [PID:13390] sopar: - Quality assesment start. Mode: emission.
2025-09-03 15:21:04,822 | WARNING | [PID:13390] sopar: - No data cube has been specified with Primary Beam information.
2025-09-03 15:21:06,270 | INFO | [PID:13390] sopar: - QA file saved in /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/quality_assesment_products. Quality assesment completed successfully. Mode: emission
2025-09-03 15:21:06,279 | INFO | [PID:13390] sipargs: - The file in /home/usuario/ADP-ALMA-Pipeline/adplib/sip/sip_args.yaml have been loaded successfully
2025-09-03 15:21:06,284 | INFO | [PID:13390] sipargs: - SIP start. Mode: absorption. Input data: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor
    2025-09-03 15:21:06,607 | INFO | image_pipeline: - *****************************************************************
    2025-09-03 15:21:06,608 | INFO | image_pipeline: - 	Beginning SoFiA-image-pipeline (SIP) 1.3.16.
    2025-09-03 15:21:06,608 | INFO | image_pipeline: - 	Offline mode requested: will not make ancillary data overlays.
    2025-09-03 15:21:06,608 | INFO | image_pipeline: - 	Reading catalog in ascii format.
    2025-09-03 15:21:06,613 | INFO | image_pipeline: - 	Catalog generated by SoFiA-2?
    2025-09-03 15:21:06,614 | INFO | image_pipeline: - 	Assuming all requested sources are associated with CO(1-0) line transition
    2025-09-03 15:21:07,358 | INFO | image_pipeline: -  
    2025-09-03 15:21:07,358 | INFO | image_pipeline: - 	-Source 1: SoFiA J100115.97+021748.2.
    2025-09-03 15:21:07,358 | INFO | make_images: - 	Start making spatial images.
    2025-09-03 15:21:07,359 | INFO | functions: - 		Found 2.0 arcsec by 1.6 arcsec beam with PA=87.3 deg in primary header.
    2025-09-03 15:21:07,360 | WARNING | functions: - 	No equinox information in header; assuming ICRS frame.
    2025-09-03 15:21:07,360 | INFO | functions: - 		Found LSRK reference frame specified in SPECSYS in header.
    2025-09-03 15:21:07,360 | INFO | functions: - 		Found CTYPE3 spectral axis type FREQ in header.
    2025-09-03 15:21:07,362 | INFO | make_images: - 	The first contour defined at SNR = [2.0, 3.0] has level = 1.065e+04 (mom0 data units).
    2025-09-03 15:21:07,363 | INFO | make_images: - 	Image size bigger than default. Now 0.12 arcmin
    2025-09-03 15:21:07,363 | INFO | make_images: - 	No user image given and offline mode requested. Making radio spectral line images.
    2025-09-03 15:21:07,364 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom0.png already exists. Will not overwrite.
    2025-09-03 15:21:07,364 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_snr.png already exists. Will not overwrite.
    2025-09-03 15:21:07,364 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom1.png already exists. Will not overwrite.
    2025-09-03 15:21:07,364 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom2.png already exists. Will not overwrite.
    2025-09-03 15:21:07,364 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv.png already exists. Will not overwrite.
    2025-09-03 15:21:07,364 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min.png already exists. Will not overwrite.
    2025-09-03 15:21:07,365 | INFO | make_images: - 	Done making spatial images.
    2025-09-03 15:21:07,365 | INFO | make_spectra: - 	Start making spectral profiles
    2025-09-03 15:21:07,366 | INFO | functions: - 		Found 2.0 arcsec by 1.6 arcsec beam with PA=87.3 deg in primary header.
    2025-09-03 15:21:07,366 | WARNING | functions: - 	No equinox information in header; assuming ICRS frame.
    2025-09-03 15:21:07,366 | INFO | functions: - 		Found LSRK reference frame specified in SPECSYS in header.
    2025-09-03 15:21:07,366 | INFO | functions: - 		Found CTYPE3 spectral axis type FREQ in header.
    2025-09-03 15:21:07,366 | WARNING | make_spectra: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec.png already exists. Will not overwrite.
    2025-09-03 15:21:07,367 | INFO | make_spectra: - 	Using /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cubelets/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec_aperture.txt to make aperture spectrum plot.
    2025-09-03 15:21:07,367 | WARNING | make_spectra: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_specfull.png already exists. Will not overwrite.
    2025-09-03 15:21:07,367 | INFO | make_spectra: - 	Done making spectral profiles.
    2025-09-03 15:21:07,367 | INFO | image_pipeline: -  
    2025-09-03 15:21:07,367 | INFO | image_pipeline: - 	-Source 2: SoFiA J100114.43+021713.7.
    2025-09-03 15:21:07,367 | INFO | make_images: - 	Start making spatial images.
    2025-09-03 15:21:07,369 | INFO | functions: - 		Found 2.0 arcsec by 1.6 arcsec beam with PA=87.3 deg in primary header.
    2025-09-03 15:21:07,369 | WARNING | functions: - 	No equinox information in header; assuming ICRS frame.
    2025-09-03 15:21:07,369 | INFO | functions: - 		Found LSRK reference frame specified in SPECSYS in header.
    2025-09-03 15:21:07,370 | INFO | functions: - 		Found CTYPE3 spectral axis type FREQ in header.
    2025-09-03 15:21:07,372 | INFO | make_images: - 	The first contour defined at SNR = [2.0, 3.0] has level = 1.707e+04 (mom0 data units).
    2025-09-03 15:21:07,374 | INFO | make_images: - 	Image size bigger than default. Now 0.20 arcmin
    2025-09-03 15:21:07,374 | INFO | make_images: - 	No user image given and offline mode requested. Making radio spectral line images.
    2025-09-03 15:21:07,375 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom0.png already exists. Will not overwrite.
    2025-09-03 15:21:07,375 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_snr.png already exists. Will not overwrite.
    2025-09-03 15:21:07,375 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom1.png already exists. Will not overwrite.
    2025-09-03 15:21:07,375 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_mom2.png already exists. Will not overwrite.
    2025-09-03 15:21:07,375 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv.png already exists. Will not overwrite.
    2025-09-03 15:21:07,375 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_pv_min.png already exists. Will not overwrite.
    2025-09-03 15:21:07,375 | INFO | make_images: - 	Done making spatial images.
    2025-09-03 15:21:07,375 | INFO | make_spectra: - 	Start making spectral profiles
    2025-09-03 15:21:07,376 | INFO | functions: - 		Found 2.0 arcsec by 1.6 arcsec beam with PA=87.3 deg in primary header.
    2025-09-03 15:21:07,377 | WARNING | functions: - 	No equinox information in header; assuming ICRS frame.
    2025-09-03 15:21:07,377 | INFO | functions: - 		Found LSRK reference frame specified in SPECSYS in header.
    2025-09-03 15:21:07,377 | INFO | functions: - 		Found CTYPE3 spectral axis type FREQ in header.
    2025-09-03 15:21:07,377 | WARNING | make_spectra: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_spec.png already exists. Will not overwrite.
    2025-09-03 15:21:07,377 | INFO | make_spectra: - 	Using /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cubelets/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_spec_aperture.txt to make aperture spectrum plot.
    2025-09-03 15:21:07,377 | WARNING | make_spectra: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_2_specfull.png already exists. Will not overwrite.
    2025-09-03 15:21:07,377 | INFO | make_spectra: - 	Done making spectral profiles.
    2025-09-03 15:21:07,377 | INFO | image_pipeline: -  
    2025-09-03 15:21:07,377 | INFO | image_pipeline: - 	DONE! Made images for 2 sources.
    2025-09-03 15:21:07,377 | INFO | image_pipeline: - 	Created log file: /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_sip.log
    2025-09-03 15:21:07,377 | INFO | image_pipeline: - *****************************************************************
    
2025-09-03 15:21:06,284 | INFO | [PID:13390] sipargs: - Command used to run SIP: sofia_image_pipeline -c /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cat.txt -x png -i 0.05 -s none -line CO(1-0) -log /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_absorption/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_sip.log
2025-09-03 15:21:07,551 | INFO | [PID:13390] sipargs: - SIP finished. Mode: absorption
2025-09-03 15:21:07,551 | INFO | [PID:13390] sipargs: - SIP start. Mode: emission. Input data: member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor
    2025-09-03 15:21:07,899 | INFO | image_pipeline: - *****************************************************************
    2025-09-03 15:21:07,899 | INFO | image_pipeline: - 	Beginning SoFiA-image-pipeline (SIP) 1.3.16.
    2025-09-03 15:21:07,900 | INFO | image_pipeline: - 	Offline mode requested: will not make ancillary data overlays.
    2025-09-03 15:21:07,900 | INFO | image_pipeline: - 	Reading catalog in ascii format.
    2025-09-03 15:21:07,904 | INFO | image_pipeline: - 	Catalog generated by SoFiA-2?
    2025-09-03 15:21:07,904 | INFO | image_pipeline: - 	Assuming all requested sources are associated with CO(1-0) line transition
    2025-09-03 15:21:08,590 | INFO | image_pipeline: -  
    2025-09-03 15:21:08,591 | INFO | image_pipeline: - 	-Source 1: SoFiA J100117.61+021639.9.
    2025-09-03 15:21:08,591 | INFO | make_images: - 	Start making spatial images.
    2025-09-03 15:21:08,592 | INFO | functions: - 		Found 2.0 arcsec by 1.6 arcsec beam with PA=87.3 deg in primary header.
    2025-09-03 15:21:08,592 | WARNING | functions: - 	No equinox information in header; assuming ICRS frame.
    2025-09-03 15:21:08,593 | INFO | functions: - 		Found LSRK reference frame specified in SPECSYS in header.
    2025-09-03 15:21:08,593 | INFO | functions: - 		Found CTYPE3 spectral axis type FREQ in header.
    2025-09-03 15:21:08,594 | INFO | make_images: - 	The first contour defined at SNR = [2.0, 3.0] has level = 1.393e+04 (mom0 data units).
    2025-09-03 15:21:08,595 | INFO | make_images: - 	Image size bigger than default. Now 0.20 arcmin
    2025-09-03 15:21:08,596 | INFO | make_images: - 	No user image given and offline mode requested. Making radio spectral line images.
    2025-09-03 15:21:08,597 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom0.png already exists. Will not overwrite.
    2025-09-03 15:21:08,597 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_snr.png already exists. Will not overwrite.
    2025-09-03 15:21:08,597 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom1.png already exists. Will not overwrite.
    2025-09-03 15:21:08,597 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_mom2.png already exists. Will not overwrite.
    2025-09-03 15:21:08,597 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv.png already exists. Will not overwrite.
    2025-09-03 15:21:08,597 | WARNING | make_images: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_pv_min.png already exists. Will not overwrite.
    2025-09-03 15:21:08,597 | INFO | make_images: - 	Done making spatial images.
    2025-09-03 15:21:08,597 | INFO | make_spectra: - 	Start making spectral profiles
    2025-09-03 15:21:08,598 | INFO | functions: - 		Found 2.0 arcsec by 1.6 arcsec beam with PA=87.3 deg in primary header.
    2025-09-03 15:21:08,598 | WARNING | functions: - 	No equinox information in header; assuming ICRS frame.
    2025-09-03 15:21:08,599 | INFO | functions: - 		Found LSRK reference frame specified in SPECSYS in header.
    2025-09-03 15:21:08,599 | INFO | functions: - 		Found CTYPE3 spectral axis type FREQ in header.
    2025-09-03 15:21:08,599 | WARNING | make_spectra: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec.png already exists. Will not overwrite.
    2025-09-03 15:21:08,599 | INFO | make_spectra: - 	Using /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cubelets/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_spec_aperture.txt to make aperture spectrum plot.
    2025-09-03 15:21:08,599 | WARNING | make_spectra: - 	/home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_figures/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_1_specfull.png already exists. Will not overwrite.
    2025-09-03 15:21:08,599 | INFO | make_spectra: - 	Done making spectral profiles.
    2025-09-03 15:21:08,599 | INFO | image_pipeline: -  
    2025-09-03 15:21:08,599 | INFO | image_pipeline: - 	DONE! Made images for 1 sources.
    2025-09-03 15:21:08,599 | INFO | image_pipeline: - 	Created log file: /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_sip.log
    2025-09-03 15:21:08,599 | INFO | image_pipeline: - *****************************************************************
    
2025-09-03 15:21:07,552 | INFO | [PID:13390] sipargs: - Command used to run SIP: sofia_image_pipeline -c /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_cat.txt -x png -i 0.05 -s none -line CO(1-0) -log /home/usuario/ADP-ALMA-Pipeline/adpalmap_outputs_emission/member.uid___A001_X133d_X4226.COSMOS-0969208_sci.spw25.cube.I.pbcor_sip.log
2025-09-03 15:21:08,785 | INFO | [PID:13390] sipargs: - SIP finished. Mode: emission
===  Subprocess PID: 13390 end  ===

2025-09-03 15:21:08,798 | INFO | [PID:13228] adpalmap: - ADPALMAP successfully ended
2025-09-03 15:21:08,799 | INFO | [PID:13228] adpalmap: - Execution time: 92.78 second(s)

"""


html = template.render(datasets=datasets_test, adp_log_content=adp_log)

output_file = os.path.join(current_dir, 'report_test.html')
with open(output_file, 'w') as f:
    f.write(html)

#webbrowser.open('file://' + output_file)

