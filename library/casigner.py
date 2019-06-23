import requests
import re
import os
from requests_ntlm import HttpNtlmAuth
from ansible.module_utils.basic import *


result = {}

def main():
        fields = {
        "url": {"required": True, "type": "str"},
        "user": {"required": True, "type": "str"},
        "password": {"required": True, "type": "str"},
        "domain": {"required": True, "type": "str"},
        "csr": {"required": True, "type": "raw"},
        # IF not spesify in playbook, this value will be default
        "outpath": {"required": False, "default": "/tmp/certsrv.p7b", "type": "path"},
        }

        module = AnsibleModule(argument_spec=fields)
        url  = module.params['url']
        user = module.params['user']
        password = module.params['password']
        domain = module.params['domain']
        csr = module.params['csr']
        outpath = module.params['outpath']

        myJSONObject = {
        'Mode': 'newreq',
        'CertRequest': csr,
        'CertAttrib': 'CertificateTemplate:UATWebServerSHA2',
        'FriendlyType': 'Saved-Request+Certificate+%28Thursday%2C+February+21%2C+2019+2%3A53%3A21+PM',
        'ThumbPrint': '',
        'TargetStoreFlags': 0,
        'SaveCert': 'yes'
        };

        head = {}
        head['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        head['Content-Type'] = 'application/x-www-form-urlencoded'
        session = requests.Session()
        session.auth = HttpNtlmAuth(domain + '\\' + user, password)
        resp1 = session.get(url + '/certfnsh.asp', headers=head, data=myJSONObject)
        #result['resp1'] = resp1.text
        print "after this concat"
        print re.search(r'ReqID=[^&]*',resp1.text, re.MULTILINE).group()
        print type(resp1)
        head1 = resp1.headers
        '''
        download url
        '''
        reqid = re.search(r'ReqID=[^&]*',resp1.text, re.MULTILINE).group()
        print "print reqid ---"+ reqid
        durl = url + "/certnew.p7b?" + reqid + "&Enc=b64"
        resp2 = session.get(durl, headers=head)
        result['cert_file'] = resp2.text
        with open(outpath, 'wb') as f:
                for chunk in resp2.iter_content(chunk_size=1024):
                        if chunk: # filter out keep-alive new chunks
                                f.write(chunk)
                                f.flush()
                                os.fsync(f.fileno())

        module.exit_json(changed=False,meta=result);

if __name__ == '__main__':
        main()
