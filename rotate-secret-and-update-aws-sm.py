import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_user_name(secret_name):
   sm = boto3.client('secretsmanager')
   response = sm.get_secret_value(SecretId=secret_name)
   id = response['SecretString']
   iam = boto3.client('iam')
   users=iam.list_users()['Users']
   for i in range(0, len(users)):
      access_keys_all = iam.list_access_keys(UserName=users[i]["UserName"])
      for access_key in range (0, len(access_keys_all['AccessKeyMetadata'])):
         if access_keys_all['AccessKeyMetadata'][access_key]['AccessKeyId'] == id:
            user_name = users[i]['UserName']
            logger.info("User access key used in the secret %s is of user %s." % (secret_name, user_name))
         else:
            pass
   return user_name

def delete_old_access_keys(user_name):
   iam = boto3.client('iam')
   response = iam.list_access_keys(UserName=user_name)
   if len(response['AccessKeyMetadata']) > 1:
      logger.info("There are more than one key for this user %s ." % (user_name))
      logger.info("Making the older key Inactive")
      access_key = response['AccessKeyMetadata'][0]['AccessKeyId']
      deactivating_key = iam.update_access_key(UserName=user_name,AccessKeyId=access_key,Status='Inactive')
      logger.info("Deleting the old keys")
      deleting_key = iam.delete_access_key(UserName=user_name,AccessKeyId=access_key)
   else:
      print ("Initiate create_access_keys")


def create_access_keys_and_update_sm(user_name,secret_name):
   iam = boto3.client('iam')
   access_key_pair = iam.create_access_key(UserName=user_name)
   id=access_key_pair['AccessKey']['AccessKeyId']
   secret=access_key_pair['AccessKey']['SecretAccessKey']
   logger.info("Updating aws secret..")
   sm = boto3.client('secretsmanager')
   response_access_key = sm.update_secret(SecretId=secret_name,SecretString=id)
   logger.info("Updating the secret value")
   secret_key_name = secret_name.replace('ACCESS_KEY','SECRET_KEY')
   remove_etc=secret_key_name.split("-")[-1:][0]
   short_name=secret_key_name.split(":")[-1]
   secret_name_short = short_name.replace("-" + remove_etc, "")
   response_secret_key = sm.update_secret(SecretId=secret_name_short,SecretString=secret)
   
def lambda_handler(event, context):
    secret_name = event['SecretId']
    logger.info("This is the secret_name %s " % (secret_name))
    logger.info("Get User Name using the access key")
    user_name = get_user_name(secret_name)
    logger.info("Check if the user already has 2 access_keys delete the older one")
    delete_old_access_keys(user_name)
    logger.info("Create new access keys and update secrets manager") 
    create_access_keys_and_update_sm(user_name,secret_name)
