"""Convert FSB5 single-sample FMOD IMA ADPCM (codec 7) into WAV PCM16.

Only supports mono, common FMOD 36-byte blocks with 64 samples/block,
which are confirmed in this game's archive. Unsupported codecs are reported.
"""
import zipfile, io, wave, struct, pathlib, hashlib, json
STEP = [7,8,9,10,11,12,13,14,16,17,19,21,23,25,28,31,34,37,41,45,50,55,60,66,73,80,88,97,107,118,130,143,157,173,190,209,230,253,279,307,337,371,408,449,494,544,598,658,724,796,876,963,1060,1166,1282,1411,1552,1707,1878,2066,2272,2499,2749,3024,3327,3660,4026,4428,4871,5358,5894,6484,7132,7845,8630,9493,10442,11487,12635,13899,15289,16818,18500,20350,22385,24623,27086,29794,32767]
INDEX = [-1,-1,-1,-1,2,4,6,8,-1,-1,-1,-1,2,4,6,8]
RATE = {1:8000,2:11025,3:12000,4:16000,5:22050,6:24000,7:32000,8:44100,9:48000,10:96000}

def decode(data):
    if data[:4] != b'FSB5': raise ValueError('No FSB5 header')
    version, samples, size_headers, name_bytes, data_size, codec, flags = struct.unpack_from('<7I', data,4)
    if codec != 7 or samples != 1: raise ValueError('Unsupported FSB codec or sample count: %s/%s' % (codec,samples))
    h=struct.unpack_from('<Q',data,60)[0]
    rate=RATE.get((h>>1)&15)
    channels=1+((h>>5)&1)
    n_samples = h>>34
    off = 60+size_headers+name_bytes
    payload=data[off:off+data_size]
    if rate is None or channels!=1 or n_samples%64: raise ValueError('Unsupported FMOD format/length')
    num_blocks=n_samples//64
    if len(payload)<num_blocks*36: raise ValueError('Truncated FSB data')
    if any(payload[num_blocks*36:]): raise ValueError('Unexpected nonzero block padding')
    result=bytearray(n_samples*2)
    dest=0
    for i in range(num_blocks):
        part=payload[i*36:i*36+36]
        predictor, index = struct.unpack_from('<hH', part)
        if index>88: raise ValueError('Invalid IMA step index')
        for byte in part[4:]:
            for n in (byte&15, byte>>4):
                step=STEP[index]
                delta=step>>3
                if n&1:delta+=step>>2
                if n&2:delta+=step>>1
                if n&4:delta+=step
                predictor += -delta if n&8 else delta
                predictor=max(-32768,min(32767,predictor))
                index=max(0,min(88,index+INDEX[n]))
                struct.pack_into('<h',result,dest,predictor)
                dest+=2
    out=io.BytesIO()
    with wave.open(out,'wb') as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(result)
    return out.getvalue(), {'sample_rate':rate,'channels':channels,'decoded_samples':n_samples,'duration_seconds':round(n_samples/rate,5),'codec':'FMOD IMA ADPCM'}

def main():
    src=pathlib.Path('/mnt/data/Elvenar_Build02_Pakete/Elvenar_Build02_02_Audio_Rohdaten_FSB5.zip')
    dst=pathlib.Path('/mnt/data/Elvenar_Build02_06_Audio_WAV_konvertiert.zip')
    reports=[]; errors=[]
    with zipfile.ZipFile(src) as z,zipfile.ZipFile(dst,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
        for n in z.namelist():
            b=z.read(n)
            try:
                wav,meta=decode(b)
            except Exception as e:
                errors.append({'source':n,'reason':str(e),'codec':struct.unpack_from('<I',b,24)[0]})
                continue
            name=pathlib.PurePosixPath(n).name.rsplit('.',1)[0]+'.wav'
            out.writestr('wav/'+name, wav)
            reports.append({'source':n,'wav':'wav/'+name,'sha256':hashlib.sha256(wav).hexdigest(),**meta})
        out.writestr('manifest_audio.json',json.dumps({'codec_scope':'FMOD FSB5 IMA ADPCM mono only','converted':len(reports),'unconverted':len(errors),'files':reports,'unconverted_files':errors},ensure_ascii=False,indent=2).encode('utf8'))
    with zipfile.ZipFile(dst) as z: assert z.testzip() is None
    print(json.dumps({'output':str(dst),'bytes':dst.stat().st_size,'converted':len(reports),'unconverted':len(errors),'rates':{str(k):sum(1 for r in reports if r['sample_rate']==k) for k in RATE.values()},'duration_total':round(sum(r['duration_seconds'] for r in reports),1),'errors':errors},indent=2))
if __name__=='__main__':main()
