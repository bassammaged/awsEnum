import argparse
from aws import aws_service   

# ----- Static & global variables
global _version,_stable, _supported_list
_version = "0.1 Beta"
_supported_list = [
    'ec2',
    'iam',
    's3',
]
def weclome():
    '''
        weclome message and contain the version
    ''' 
    msg = '''
     ▄▄▄▄▄▄ ▄     ▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄    ▄ ▄▄   ▄▄ ▄▄   ▄▄ 
█      █ █ ▄ █ █       █       █  █  █ █  █ █  █  █▄█  █
█  ▄   █ ██ ██ █  ▄▄▄▄▄█    ▄▄▄█   █▄█ █  █ █  █       █
█ █▄█  █       █ █▄▄▄▄▄█   █▄▄▄█       █  █▄█  █       █
█      █       █▄▄▄▄▄  █    ▄▄▄█  ▄    █       █       █
█  ▄   █   ▄   █▄▄▄▄▄█ █   █▄▄▄█ █ █   █       █ ██▄██ █
█▄█ █▄▄█▄▄█ █▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄█  █▄▄█▄▄▄▄▄▄▄█▄█   █▄█
--------------------------------------------------------
If you looking to enumerate AWS services. So, welcome
to awsEnum :) 
--------------------------------------------------------
        developed by bassammaged (@kemet)
                version: {}
--------------------------------------------------------
[!] Make sure you already defined credential profile via AWS CLI.
'''.format(_version)
    print(msg)

def take_arguments():
    '''
        take_argumets() is designed to take the service name and aws profile name
    '''
    # Adding top level parser
    parser = argparse.ArgumentParser()
    # Rearrange the parsing group
    optional    = parser._action_groups.pop()

    # Positional arguments
    parser.add_argument('service',help="Specify the aws service for enumration. Supported services are: {} (default: all)".format(sorted(_supported_list)),default='all',metavar='aws_service_name',choices=_supported_list)
    
    # Global optional arguments 
    optional.add_argument('-p','--profile',help='specify aws credential profile that will be used through the enumeration. (default: default)',default='default',metavar='profile_name')
    optional.add_argument('-r','--region',help='specify aws region. (default: eu-central-1)',default='eu-central-1',metavar='region_name')
    optional.add_argument('-v','--verbose',help="Allows the script to print out the message level start with debug.",action=argparse.BooleanOptionalAction,default=False)
    optional.add_argument('-t','--tries',help="set maximum tries. (default: 1000)",default=1000)


    parser._action_groups.append(optional)
    # parse arguments
    args = parser.parse_args()
    
    # -- call aws_service to run the service enumeration
    aws_service(args.service,args.profile,args.region,args.tries,args.verbose)



        

def main():
    weclome()
    take_arguments()


if __name__ == "__main__":
    main()