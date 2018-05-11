import boto3
from io import StringIO
import io
import zipfile
import mimetypes

def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    # specifying to and from buckets
    portfolio_bucket = s3.Bucket('portfolio.theravikumar.com')
    build_bucket = s3.Bucket("portfoliobuild1.trks")
    # creating buffer storage
    portfolio_zip = io.BytesIO()
    build_bucket.download_fileobj('portfoliobuild.zip',portfolio_zip)
    #unzipping the file and uploading the content in the bucket
    with zipfile.ZipFile(portfolio_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            portfolio_bucket.upload_fileobj(obj,nm,ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
            portfolio_bucket.Object(nm).Acl().put(ACL = 'public-read')
    return 'Hello from Lambda'

