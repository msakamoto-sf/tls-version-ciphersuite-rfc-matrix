BASE_IANA_NAMES_TSV = './base-iana-names.tsv'
FROM_TESTSSL_TSV = './from-testssl.tsv'
FROM_CENTOS7_9_TSV = './from-centos7.9-openssl-1.0.2k.txt'
FROM_CENTOS8S_TSV = './from-centos8s-openssl-1.1.1k.txt'

def normalize_opensslname(opensslname):
    if 'EDH' == opensslname[0:3]:
        return 'DHE' + opensslname[3:]
    return opensslname

basedb = {}
with open(BASE_IANA_NAMES_TSV, encoding="utf-8") as f:
    sort_key = 0
    for line in f.readlines():
        items = line.split('\t')
        csval = items[0].strip() # "0xAB,0xCD"
        iananame = items[1].strip() # "TLS_xxx"
        record = {
            'sort_key': sort_key,
            'csval': csval,
            'iananame': iananame,
        }
        basedb[csval] = record
        sort_key += 1

print('###>>>>>>>>>>>>>>>>>>>> START %s' % (FROM_TESTSSL_TSV))
with open(FROM_TESTSSL_TSV, encoding="utf-8") as f:
    index = 0
    for line in f.readlines():
        items = line.split('\t')
        csvaltmp = items[0].strip() # "[0xaB]", "[0xaBcD]"
        opensslname = items[1].strip()
        iana_csval = csvaltmp.replace('[', '').replace(']', '')
        if len(iana_csval) == 4: # "0xaB"
            iana_csval = '0x00,0x' + iana_csval[2:].upper() # "0xAB"
        elif len(iana_csval) > 4: # "0xaBcD"
            csvaltmp1 = '0x' + iana_csval[2:4].upper() # "0xAB"
            csvaltmp2 = '0x' + iana_csval[4:].upper() # "0xCD"
            iana_csval = csvaltmp1 + ',' + csvaltmp2
        if opensslname:
            print("[+] %s => %s : %s" % (csvaltmp, iana_csval, opensslname))
            if iana_csval in basedb:
                record = basedb[iana_csval]
                record['opensslname'] = normalize_opensslname(opensslname)
            else:
                print("!!! WARNING !!! %s not found in base db." % (iana_csval))
        else:
            print("[-] %s => %s : %s" % (csvaltmp, iana_csval, opensslname))

print('###>>>>>>>>>>>>>>>>>>>> START %s' % (FROM_CENTOS7_9_TSV))
with open(FROM_CENTOS7_9_TSV, encoding="utf-8") as f:
    index = 0
    for line in f.readlines():
        items = line.split()
        csvaltmp = items[0].strip() # "0xAB,0xCD"
        opensslname = normalize_opensslname(items[2].strip())
        if csvaltmp in basedb:
            record = basedb[csvaltmp]
            if 'opensslname' in record:
                rv = record['opensslname']
                if rv != opensslname:
                    print("!!! ERROR !!! %s already set opensslname[%s] but differ to %s" % (csvaltmp, rv, opensslname))
                    exit(-1)
            record['opensslname'] = opensslname
        else:
            print("!!! WARNING !!! %s not found in base db." % (csvaltmp))

print('###>>>>>>>>>>>>>>>>>>>> START %s' % (FROM_CENTOS8S_TSV))
with open(FROM_CENTOS8S_TSV, encoding="utf-8") as f:
    index = 0
    for line in f.readlines():
        items = line.split()
        csvaltmp = items[0].strip() # "0xAB,0xCD"
        opensslname = normalize_opensslname(items[4].strip())
        if csvaltmp in basedb:
            record = basedb[csvaltmp]
            if 'opensslname' in record:
                rv = record['opensslname']
                if rv != opensslname:
                    print("!!! ERROR !!! %s already set opensslname[%s] but differ to %s" % (csvaltmp, rv, opensslname))
                    exit(-1)
            record['opensslname'] = opensslname
        else:
            print("!!! WARNING !!! %s not found in base db." % (csvaltmp))

from operator import itemgetter
sorted_records = sorted(basedb.values(), key=itemgetter('sort_key'))
for r in sorted_records:
    opensslname = r.get('opensslname', '')
    print('%s\t%s\t%s' % (r['csval'], r['iananame'], opensslname))
