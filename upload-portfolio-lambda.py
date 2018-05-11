import boto3
from io import StringIO
import io
import zipfile
import mimetypes

def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    sns = boto3.resource('sns')
    
    # specifying to and from buckets and SNS Topic
    try:
        portfolio_bucket = s3.Bucket('portfolio.theravikumar.com')
        build_bucket = s3.Bucket("portfoliobuild1.trks")
        topic = sns.Topic('arn:aws:sns:us-east-1:837249601207:deployportfolio1_topic')
        # creating buffer storage
        portfolio_zip = io.BytesIO()
        build_bucket.download_fileobj('portfoliobuild.zip',portfolio_zip)
        #unzipping the file and uploading the content in the bucket
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm,ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL = 'public-read')
        print("Job done!")
        topic.publish(Subject = "Portfolio deployed", Message = "Portflio deployed successfully")
    except:
        topic.publish(Subject ="portfolio deploy failed" , Message = "The portfolio was not deployed successfully")
        raise
    return 'Hello from Lambda'
