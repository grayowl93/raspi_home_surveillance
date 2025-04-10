import boto3
import phonenumbers

accesskey = ""
secretkey = ""
region = "ap-northeast-1"

def sendShortMessage(title,msg):
	print("send to iPhone")
	boto3.set_stream_logger()
	try:
		print("client")
		sns = boto3.client("sns", aws_access_key_id=accesskey, aws_secret_access_key=secretkey, region_name=region)	
		print("publish")
		response = sns.publish(
			PhoneNumber = "",
			Subject = title,
			Message = msg
			)
		print("response")
	except Exception as err:
		print(err.code)

if __name__ == "__main__":
	print("send SMS")
	sendShortMessage("Zushi","Emergency")
	print("done.")

