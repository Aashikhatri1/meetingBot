#import boto3
#s3_client = boto3.client('s3')
#response = s3_client.upload_file(r'C:\Users\Administrator\Documents\GitHub\meetingBot\recording.wav', 'customerexceldata' , 'recording.wav')
import boto3
s3 = boto3.client('s3')
s3.upload_file(r'C:\Users\Administrator\Documents\GitHub\meetingBot\recording.wav', 'meetingbotrecording', 'Recording_file.wav')

