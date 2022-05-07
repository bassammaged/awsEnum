import boto3
from numpy import full
from logger import CustomError, logit
from json import dump
from os import path

class aws_service:
    '''
        `aws_service()` is to call the service that needed.
    '''

    def __init__(self,service_name,profile,region,tries,verbose):
        '''
            `aws_service(service_name,profile,region,verbose)`

            Arguments:
                - `string`  service_name
                - `string`  profile
                - `string`  region
                - `int`     tries
                - `boolean` verbose 

            Returns:
                - No returns.

            Process:
                aws_service will run the service enumration based on the `service_name` by using the provided `profile` and `region`.
        
        '''
        self.service_name   = service_name
        self.profile        = profile
        self.region         = region
        self.tries          = tries
        self.verbose        = verbose
        
        # prepare the logging
        self.logit_obj      = logit(self.profile,self.region,self.service_name,self.verbose)
        
        
        # establish aws session
        try:
            self.aws_session    = boto3.Session(profile_name=self.profile,region_name=self.region)
            self.logit_obj.add('i','AWS session has been stablished successfully.')
        except Exception as e:
            self.logit_obj.add('e',"Failed to stablish connection with AWS, ERROR message: {}".format(e))
        
        try:
            if self.service_name == 'ec2':
                obj = ec2(self.aws_session,self.tries,self.logit_obj)   
            else:
                raise CustomError('c','Still under development.')
        except CustomError as e:
                self.logit_obj.add(e.criticality_level,e.message)

        store_results(self.service_name,self.profile,self.region,obj.result,self.logit_obj)

                   

class ec2:
    '''
        ec2 is class written to enumerate the ec2 instances information and store the info into json file.
    '''
    result = []

    def __init__(self,aws_session,tries,logit_obj):
        '''
            `ec2()` takes 3 arguments

            Arguments:
                - `boto3 session object` aws_session
                - `int` tries
                - `logit object` logit_obj
        '''
        self.aws_session    = aws_session
        self.tries          = tries
        self.logit_obj      = logit_obj

        # call the describe_instance method
        self._call_describe_isntance_method()

    def _call_describe_isntance_method(self):
        '''
            `_call_describe_isntance_method()` Designed to request method based on NextToken.
            the response is analyzed by `_extract_ec2_info()`
        '''
        try:
            # -- call service
            client = self.aws_session.client('ec2')
            # -- Call method
            response = client.describe_instances(MaxResults=self.tries)
        except:
            self.logit_obj.add('e','Error happened while calling the ec2 service and describe_instances method')

        self._extract_ec2_info(response)

        # -- Incase of there's NextToken
        if response.get('NextToken'):
            try:
                # -- call service
                client = self.aws_session.client('ec2')
                # -- Call method
                response = client.describe_instances(MaxResults=self.tries,NextToken=response['NextToken'])
            except:
                self.logit_obj.add('e','Error happened while calling the ec2 service and describe_instances method via NextToken')
            
            self._extract_ec2_info(response)

        self.logit_obj.add('i','All EC2 information extracted.')



    def _extract_ec2_info(self,response):
        '''
            `_extract_ec2_info()` is coded to extract the EC2 info out of the AWS method response.
        '''
        try:
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    self.result.append(instance)
        except:
            self.logit_obj.add('e','Failure! Error occurred during extract EC2 info from the response.')
        
        self.logit_obj.add('d','EC2 info has been extracted from the response.')



class store_results:
    def __init__(self,service_name,profile,region,result,logit_obj):
        fullpath = path.join(path.dirname(__file__),'results',profile+'-'+region+'-'+service_name+'.json')
        try:
            with open(fullpath, 'w+') as f:
                dump(result, f, indent=4, default=str)
            logit_obj.add('f','EC2 information is stored at {}'.format(fullpath))
        except Exception as e:
            logit_obj.add('c','Error while storing the EC2 info into {}. Error message: {}'.format(fullpath,e))
