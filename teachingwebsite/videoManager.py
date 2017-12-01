from qiniu import Auth, put_data, etag, urlsafe_base64_encode, BucketManager
import qiniu.config
import urllib

bucketName = 'biolab'
accessKey = 'G-WAWOJ5uxi001CgFuwcI6YRNhcme4QWUFzCj2pI'
secretKey = urllib.request.urlopen('http://nslamgg.top/keys.txt').read()
secretKey = str(secretKey, encoding='utf-8')
secretKey = secretKey.split('\n')[0]
auth = Auth(accessKey, secretKey)


def upload(file):
    token = auth.upload_token(bucketName, None, 3600)
    ret, info = put_data(up_token=token, key=None, data=file)
    # ret, info = put_file(token, key, localfile)
    return getBaseUrl(ret['key'])


def getBaseUrl(key):
    if type(key) is str:
        baseUrl = 'http://qiniu.biolab.sparker.top/' + key
    else:
        raise AttributeError('Invalid key')
    # privateUrl = auth.private_download_url(baseUrl, expires=3600)
    return baseUrl


def delete(key):
    bucket = BucketManager(auth)
    ret, info = bucket.delete(bucketName, key)
    return info
