from asn1crypto import cms, core, pem

import hashlib



def main():
    for fname in (
        "send_hybrid_gov_01~.pdf",
        "send_hybrid_gov_03.pdf"
    ):
        print('*' * 20, fname)
        try:
            data = open(fname, 'rb').read()
        except:
            print("cannot open")
            continue

        cert_dict = my_get_info(data)
        print(cert_dict)
        


def get_issuers(datas, datau):
    signed_data = cms.ContentInfo.load(datas)['content']

    signature = signed_data['signer_infos'][0]['signature'].native
    algo = signed_data['digest_algorithms'][0]['algorithm'].native
    attrs = signed_data['signer_infos'][0]['signed_attrs']
    mdData = getattr(hashlib, algo)(datau).digest()
    if attrs is not None and not isinstance(attrs, core.Void):
        mdSigned = None
        for attr in attrs:
            if attr['type'].native == 'message_digest':
                mdSigned = attr['values'].native[0]
        signedData = attrs.dump()
        signedData = b'\x31' + signedData[1:]
    else:
        mdSigned = mdData
        signedData = datau
    hashok = mdData == mdSigned
    serial = signed_data['signer_infos'][0]['sid'].native['serial_number']
    public_key = None

    results = {}
    for cert in signed_data['certificates']:
        results["issuer"] = cert.native['tbs_certificate']['issuer']
        results["subject"] = cert.native['tbs_certificate']['subject']
    
    return results

def my_get_info(pdfdata):
    results = {}
    n = pdfdata.find(b"/ByteRange")
    while n != -1:
        start = pdfdata.find(b"[", n)
        stop = pdfdata.find(b"]", start)
        assert n != -1 and start != -1 and stop != -1
        br = [int(i, 10) for i in pdfdata[start + 1 : stop].split()]
        contents = pdfdata[br[0] + br[1] + 1 : br[2] - 1]
        bcontents = bytes.fromhex(contents.decode("utf8"))
        data1 = pdfdata[br[0] : br[0] + br[1]]
        data2 = pdfdata[br[2] : br[2] + br[3]]
        signedData = data1 + data2
        results.update(get_issuers(bcontents, signedData))
        n = pdfdata.find(b"/ByteRange", br[2] + br[3])
    
    return results

main()