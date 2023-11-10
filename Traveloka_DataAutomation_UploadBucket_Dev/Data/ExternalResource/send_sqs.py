import boto3
import json
import botocore.exceptions


def send_message(queue_url, region_name, reportId, status, inputPath, outputPath, errorDetails):

    sqs = boto3.client('sqs', region_name)

    #Generate file id from outputpath, Get only yyyyMM/filename
    fileIdLen = len(outputPath.split("/"))
    fileId = outputPath.split("/")[fileIdLen-2] + "/" + outputPath.split("/")[fileIdLen-1]
    print(fileId)

    message_data = {
        "reportId": reportId,
        "messageSource": "RPA",
        "status": status,
        "outputPath": outputPath,
        "fileId" : fileId
        #message_data["inputPath"] = inputPath /not used rn
        }

    if status != 'SUCCESS':
        message_data["errorDetails"] = errorDetails
        
    message_body = json.dumps(message_data)
    try :
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody = message_body,
            MessageGroupId = fileId
        )
        return f'{response["ResponseMetadata"]["HTTPStatusCode"]}_{response["MessageId"]}'
    except botocore.exceptions.ClientError as e:
        error_message = e.response['Error']['Message']
        error_code = e.response['Error']['Code']
        return (f'{error_code} : {error_message}')

#region debugging
if __name__ == "__main__": 
    print ('start main')
    queue_url = 'https://sqs.ap-southeast-1.amazonaws.com/105676898724/ecircon-business-partner-files-status-notification-stdq-27ca1bd818ffc2d8.fifo'
    region_name = 'ap-southeast-1'
    reportId = 'PC0600' #report id from bpid
    status = 'SUCCESS'
    inputPath = '.xlsx'
    outputPath = '.csv'
    errorDetails = ''
    response = send_message(queue_url, region_name, reportId, status, inputPath, outputPath, errorDetails)
    print(response)
#endregion