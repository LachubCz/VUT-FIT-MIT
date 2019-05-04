import numpy as np
import struct, sys, re, os
import warnings
import math

WAVEFORM = 0
LPC = 1
LPCREFC = 2
LPCEPSTRA = 3
LPCDELCEP = 4
IREFC = 5
MFCC = 6
FBANK = 7
MELSPEC = 8
USER = 9
DISCRETE = 10
PLP = 11
ANON = 12

_E = 0000100 # has energy
_N = 0000200 # absolute energy supressed
_D = 0000400 # has delta coefficients
_A = 0001000 # has acceleration coefficients
_C = 0002000 # is compressed
_Z = 0004000 # has zero mean static coef.
_K = 0010000 # has CRC checksum
_0 = 0020000 # has 0th cepstral coef.
_V = 0040000 # has VQ data
_T = 0100000 # has third differential coef.

parms16bit = [WAVEFORM, IREFC, DISCRETE]


def readhtk(file, return_parmKind_and_sampPeriod=False):
    """ Read htk feature file
     Input:
         file: file name or file-like object.
     Outputs:
          m  - data: column vector for waveforms, one row per frame for other types
          sampPeriod - frame rate [seconds]
          parmKind
    """
    try:
        fh = open(file,'rb')
    except TypeError:
        fh = file
    try:
        nSamples, sampPeriod, sampSize, parmKind = struct.unpack(">IIHH", fh.read(12))
        m = np.frombuffer(fh.read(nSamples*sampSize), 'i1')
        pk = parmKind & 0x3f
        if pk in parms16bit:
            m = m.view('>h').reshape(nSamples,sampSize/2)
        elif parmKind & _C:
            scale, bias = m[:sampSize*4].view('>f').reshape(2,sampSize/2)
            m = (m.view('>h').reshape(nSamples,sampSize/2)[4:] + bias) / scale
        else:
            m = m.view('>f').reshape(nSamples,sampSize/4)
        if pk == IREFC:
            m = m / 32767.0
        if pk == WAVEFORM:
            m = m.ravel()
        if parmKind & _K:
            fh.read(1)
    finally:
        if fh is not file: fh.close()
    return m if not return_parmKind_and_sampPeriod else (m, parmKind, sampPeriod/1e7)

def readhtk_segment_honza(segment, lc=0, rc=0, return_parmKind_and_sampPeriod=False):
    """ Read segment from htk feature file
     Input:
         segment - array with segment definition compatible with read_scp output [logical,physical,start,end,weight]
         If start is negative or when end points behind the end of the feature
         matrix, the first or/and the last frame are repeated as required
         to always return end-start frames.
         lc, rc = left and right context to extend features
     Outputs:
          m  - column vector for waveforms, one row per frame for other types
          sampPeriod - frame rate [seconds]
          parmKind
    """
    logical, physical, start, end, weight = segment
    try:
        fh = open(physical,'rb')
    except TypeError:
        fh = physical
    try:
        fh.seek(0)
        nSamples, sampPeriod, sampSize, parmKind = struct.unpack(">IIHH", fh.read(12))
        pk = parmKind & 0x3f
        if parmKind & _C:
            scale, bias = np.fromfile(fh, '>f', sampSize).reshape(2,sampSize/2)
            nSamples -= 4

        if not start:
          start = 0
        if not end:
          end = nSamples
        
        end = end+1 #include last frame - to be HTK/TNet/STK compatible
        
        start  = start - lc
        end = end + rc  
        
        s, e = max(0, start), min(nSamples, end)
        fh.seek(s*sampSize, 1)
        dtype, bytes = ('>h', 2) if parmKind & _C or pk in parms16bit else ('>f', 4)
        m = np.fromfile(fh, dtype, (e-s)*sampSize/bytes).reshape(e-s,sampSize/bytes)
        if parmKind & _C:
            m = (m + bias) / scale
        if pk == IREFC:
            m = m / 32767.0
        if pk == WAVEFORM:
            m = m.ravel()
    finally:
        if fh is not physical: fh.close()

    if start != s or end != e: # repeat first or/and last frame as required
      m = np.r_[np.repeat(m[[0]], s-start, axis=0), m, np.repeat(m[[-1]], end-e, axis=0)]
    return m if not return_parmKind_and_sampPeriod else (m, parmKind, sampPeriod/1e7)

def readhtk_segment(file, start, end, return_parmKind_and_sampPeriod=False):
    """ Read segment from htk feature file
     Input:
         file - file name or file-like object alowing to seek in the file
         start, end - only frames in the range start:end are extracted. 
         If start is negative or when end points behind the end of the feature
         matrix, the first or/and the last frame are repeated as required
         to always return end-start frames.
     Outputs:
          m  - column vector for waveforms, one row per frame for other types
          sampPeriod - frame rate [seconds]
          parmKind
    """
    try:
        fh = open(file,'rb')
    except TypeError:
        fh = file
    try:
        fh.seek(0)
        nSamples, sampPeriod, sampSize, parmKind = struct.unpack(">IIHH", fh.read(12))
        pk = parmKind & 0x3f
        if parmKind & _C:
            scale, bias = np.fromfile(fh, '>f', sampSize).reshape(2,sampSize/2)
            nSamples -= 4
        s, e = max(0, start), min(nSamples, end)
        fh.seek(s*sampSize, 1)
        dtype, bytes = ('>h', 2) if parmKind & _C or pk in parms16bit else ('>f', 4)
        m = np.fromfile(fh, dtype, (e-s)*sampSize/bytes).reshape(e-s,sampSize/bytes)
        if parmKind & _C:
            m = (m + bias) / scale
        if pk == IREFC:
            m = m / 32767.0
        if pk == WAVEFORM:
            m = m.ravel()
    finally:
        if fh is not file: fh.close()
    if start != s or end != e: # repeat first or/and last frame as required
      m = np.r_[np.repeat(m[[0]], s-start, axis=0), m, np.repeat(m[[-1]], end-e, axis=0)]
    return m if not return_parmKind_and_sampPeriod else (m, parmKind, sampPeriod/1e7)


def readhtk_header(file, return_parmKind_and_sampPeriod=False):
    with  open(file,'rb') as fh:
        nSamples, sampPeriod, sampSize, parmKind = struct.unpack(">IIHH", fh.read(12))
        if parmKind & _C: nSamples -= 4
    return nSamples, sampPeriod/1e7, sampSize, parmKind


def writehtk(file, m, parmKind=USER, sampPeriod=0.01):
    """ Write htk feature file
     Input:
          file: handle or filename
          m  - data: vector for waveforms, one row per frame for other types
          sampPeriod - frame rate [seconds]
          parmKind
    """
    
    pk = parmKind & 0x3f
    parmKind &= ~_K # clear unsupported CRC bit
    m = np.atleast_2d(m)
    if pk == WAVEFORM:
        m = m.reshape(-1,1)
    try:
        fh = open(file,'wb')
    except TypeError:
        fh = file
    #print fh
    try: 
        fh.write(struct.pack(">IIHH", len(m)+(4 if parmKind & _C else 0), sampPeriod*1e7,
            m.shape[1] * (2 if (pk in parms16bit or  parmKind & _C) else 4), parmKind))
        if pk == IREFC:
            m = m * 32767.0
        if pk in parms16bit:
            m = m.astype('>h')
        elif parmKind & _C:
            mmax, mmin = m.max(axis=0), m.min(axis=0)
            mmax[mmax==mmin] += 32767
            mmin[mmax==mmin] -= 32767 # to avoid division by zero for constant coefficients
            scale= 2*32767./(mmax-mmin)
            bias = 0.5*scale*(mmax+mmin)
            m = m * scale - bias
            fh.write(scale.astype('>f').tobytes())
            fh.write(bias.astype('>f').tobytes())
            m = m.astype('>h')
        else:
            m = m.astype('>f')
        fh.write(m.tobytes())
    finally:
        if fh is not file: fh.close()

def load_vad_lab_as_bool_vec(lab_file):
    lab_cont = np.loadtxt(lab_file, usecols=[0,1], dtype=object)
    vad = np.atleast_2d(lab_cont).astype(int).T / 100000

    if not vad.size: 
        return np.empty(0, dtype=bool)

    npc1 = np.c_[np.zeros_like(vad[0], dtype=bool), np.ones_like(vad[0], dtype=bool)]
    npc2 = np.c_[vad[0] - np.r_[0, vad[1,:-1]], vad[1]-vad[0]]
    return np.repeat(npc1, npc2.flat)

def read_lab_to_bool_vec(lab_file, true_label=None, length=0, frame_rate=100.):
    """
    Read HTK label file into boolean vector representing frame labels
    Inputs:
        lab_file: name of a HTK label file (possibly gzipped)
        true_label: label for which the output frames should have True value (defaul: all labels)
        length: Output vector is truncted or augmented with False values to have this length.
                For negative 'length', it will be only augmented if shorter than '-length'.
                By default (length=0), the vector entds with the last true value.
        frame_rate: frame rate of the output vector (in frames per second)
    Output:
        frames: boolean vector
    """
    min_len, max_len = (length, length) if length > 0 else (-length, None)
    labels = np.atleast_2d(np.loadtxt(lab_file, usecols=(0,1,2), dtype=object))
    if true_label: labels = labels[labels[:,2] == true_label]
    start, end = np.rint(frame_rate/1e7*labels.T[:2].astype(int)).astype(int)
    if not end.size: return np.zeros(min_len, dtype=bool)
    frms = np.repeat(np.r_[np.tile([False,True], len(end)), False],
                     np.r_[np.c_[start - np.r_[0, end[:-1]], end-start].flat, max(0, min_len-end[-1])])
    assert len(frms) >= min_len and np.sum(end-start) == np.sum(frms)
    return frms[:max_len]

def read_mlf(mlf_file, label_map=lambda x: x):
  from itertools import groupby
  with open(mlf_file) as fh:
    lines=(l.strip().split() for l in fh)
    ll = [list(x[1]) for x in groupby(lines, lambda x: x[0]=="." or x[0]=="#!MLF!#") if not x[0]]
    #return {r[0][0].strip('"').strip(".lab").strip('*/'): np.array([l if len(l) == 1 else (int(l[0]), int(l[1]), label_map(l[2])) for l in r[1:]], dtype=object) for r in ll}
    return {r[0][0].strip('"'): np.array([l if len(l) == 1 else (int(l[0]), int(l[1]), label_map(l[2])) for l in r[1:]], dtype=object) for r in ll}


def read_mlf_optimized(mlf_file, label_map=None):
  all_transcripts = []
  all_names = []
  with open(mlf_file) as fh:
      lines=(l.strip().split() for l in fh)
      if lines.next()[0] != "#!MLF!#":
        raise Exception("Wrong file format, missing MLF header!")
      #ii = 0
      #s1 = time.time()
      transcripts = []
      for line in lines:
        if len(line) == 1 and line[0] != "." :
          #print line[0]
          #ii +=1
          #if ii%100 == 0:
          #  e1 = time.time()
          #  print ii, e1-s1
          #  s1 = e1
          all_names.append(line[0].strip('"'))
        elif line[0] == ".":
          t = np.array(transcripts, dtype=object).reshape((-1,3))
          all_transcripts.append(np.hstack([t[:,:2].astype(np.int),t[:,2,None]]))
          #all_transcripts.append(transcripts)
          transcripts = []
        else:
          #print line
          if label_map:
            transcripts.extend(line[0],line[1],label_map(line[2]))
          else:
            transcripts.extend(line)
      return dict(zip(all_names, all_transcripts))
      
def write_mlf(mlf_dict, f):
    """
    Write MLF to file in HTK format
    """
    
    pass
    

def lab_to_frm(labels, length=0, frame_rate=100., empty_label=None):
    min_len, max_len = (length, length) if length > 0 else (-length, None)
    start, end = np.rint(frame_rate/1e7*labels.T[:2].astype(int)).astype(int)
    if not end.size:
      ret = np.empty(min_len, dtype=object)
      ret[:] = empty_label
      return ret
    [o for lab in labels[:,2] for o in (empty_label, lab)]+[empty_label]
    frms = np.repeat([o for lab in labels[:,2] for o in (empty_label, lab)]+[empty_label],
                     np.r_[np.c_[start - np.r_[0, end[:-1]], end-start].flat, max(0, min_len-end[-1])])
    assert len(frms) >= min_len
    return frms[:max_len]

def lab_to_frm_honza(segment,mlf_dict,frame_rate=100., empty_label=None):
    
    logical, physical, start, end, weight = segment
    if not logical:
      name = os.path.splitext(os.path.split(physical)[1])[0]
    else:
      name = os.path.splitext(logical)[0]
      
    labels = mlf_dict[name].astype(int)
    
    if not start:
      length=0
    else:
      length = end-start+1
    
    
    min_len, max_len = (length, length) if length > 0 else (-length, None)
    #print length
    start, end = np.rint(frame_rate/1e7*labels.T[:2].astype(int)).astype(int)
    if not end.size:
      ret = np.empty(min_len, dtype=object)
      ret[:] = empty_label
      return ret
      [o for lab in labels[:,2] for o in (empty_label, lab)]+[empty_label]
    frms = np.repeat([o for lab in labels[:,2] for o in (empty_label, lab)]+[empty_label],
                     np.r_[np.c_[start - np.r_[0, end[:-1]], end-start].flat, max(0, min_len-end[-1])])
    assert len(frms) >= min_len
    return frms[:max_len]

def readScp(scp_file):
  warnings.warn("This function is deprecated, use read_scp instead!", DeprecationWarning)
  import re
  return np.array([(l,f,int(s),int(e)+1) for l,f,s,e in [re.search(r'(.*)=(.*)\[(.*),(.*)]', line).groups()
                                           for line in np.loadtxt(scp_file, dtype=object, ndmin=1)]], dtype=object)


################################################################################
################################################################################
def parse_scp_line(line):
    """ Syntactic analysis of the SCP line
    """ 

    foo, logical, physical, foo, start, end, foo, weight = \
        re.search(
            r'^((.+?)=)?(.+?)(\[(\d+),(\d+)])?(\{(.+)\})?$', 
            line
        ).groups()

    if start  is not None: 
        start  = int(start)    
    if end    is not None: 
        end    = int(end)      
    if weight is not None: 
        weight = float(weight) 
    
    return logical, physical, start, end, weight


################################################################################
################################################################################
def read_scp(scp_file):
    """ Read the whole SCP file into memory as an np.array
    Output: 2D ndarray 
    rows are in format [logical_name, physical_name, start_time, end_time, weight]
    if item is not defined in scp_file, it returns None
    """
    return np.array(
        [parse_scp_line(line) for line in np.loadtxt(scp_file,
           dtype=object, ndmin=1)], 
        dtype=object
    )


################################################################################
################################################################################
def write_scp(arr, fname):
    """ Write the np.array into SCP file by whatever best possible guess
    """
    f = open(fname, 'w')

    for ii in xrange(0, arr.shape[0]):
        if arr[ii,0] != None:
            f.write(str(arr[ii,0]) + '=')

        f.write(str(arr[ii,1]))
            
        if arr[ii,2] != None:
            if arr[ii,3] != None:
                raise ValueError(str.format("No End time defined for {} record",
                    str(ii)))

            f.write('[' + str(arr[ii,2]) + ',' + str(arr[ii,3]) + ']')

        if arr[ii,4] != None:
            f.write('{' + str(arr[ii,4]) + '}')
        f.write("\n")
    f.close()

def parse_configfile(configfile):
    cfg = {}
    module = None
    with open(configfile) as f:
        lines = f.readlines()
        for line in lines:
            line = line.split("#")[0].strip() #remove comments
            if len(line) == 0: #remove blank lines
              continue
            
            c = [it.strip() for it in line.split("=")]

            if c[0] == "TARGETKIND":
              cc = c[1].split("_")
              module = cc[0].lower()
              for ccc in cc[1:]:
                if ccc == "0":
                  cfg['_'+ccc] = "last"
                else:
                  cfg['_'+ccc] = True
            else:
              if c[1] == "T":
                cfg[c[0]] = True
              elif c[1] == "F":
                cfg[c[0]] = False
              else:
                cfg[c[0]] = c[1]
    if not module:
        raise Exception("TARGETKIND not specified!")
    return module, cfg
