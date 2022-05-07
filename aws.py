import boto3
import argparse
from logger import CustomError,logit

class aws_service:
    '''
        `aws_service()` is to call the service that needed.
    '''

    def __init__(self,service_name,profile,region,verbose):
        '''
            `aws_service(service_name,profile,region,verbose)`

            Arguments:
                - `string`  service_name
                - `string`  profile
                - `string`  region
                - `boolean` verbose 

            Returns:
                - No returns.

            Process:
                aws_service will run the service enumration based on the `service_name` by using the provided `profile` and `region`.
        
        '''
        self.profile        = profile
        self.region         = region
        self.verbose        = verbose
        self.service_name   = service_name
        
        # prepare the logging
        self.logit_obj      = logit(self.profile,self.region,self.service_name,self.verbose)
        
        
        # establish aws session
        try:
            self.aws_session    = boto3.Session(profile_name=self.profile,region_name=self.region)
            print(self.aws_session)
        except Exception as e:
            self.logit_obj.add('e',"Failed to stablish connection with AWS, ERROR message: {}".format(e))



class ec2:
    '''
        ec2 is class written to enumerate the ec2 instances information and store the info into json file.
    '''
    def __init__(self,profile,region):
        print('You are in EC2 enum.')

