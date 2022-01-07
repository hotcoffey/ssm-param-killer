import boto3
import os
import string
import logging
import argparse

FORMAT_STRING = "%(asctime)s [%(levelname)-9s] [%(filename)s]-[%(lineno)d]  %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT_STRING, datefmt="%m/%d/%Y %I:%M:%S %p")
LOGGER = logging.getLogger(__file__)

parser = argparse.ArgumentParser(description='Uses AWS CLI to find SSM Parameters based on a provided search string and remeove them accordingly.')
parser.add_argument('-p','--profile', help='Name of the AWS CLI profile you wish to use. Defaults to default.', type=str, required=False)
parser.add_argument('-s','--searchstring', help='String used to search for parameters you want destroyed. Example: /ccplat/dynamodb/dev0', type=str, required=False)
args = parser.parse_args()

resources = []
nexttoken = ''

def linebreak(char):
    rows, columns = os.popen('stty size', 'r').read().split()
    print(char*int(columns))

def print_profiles():
    LOGGER.info('Reading Local AWS Profiles...')
    linebreak('-')
    for profile in boto3.session.Session().available_profiles:
        print(profile)

def next_run(token):
    response = client.describe_parameters(MaxResults=50,NextToken=token)
    for n in range(0,len(response['Parameters'])):
        resources.append(response['Parameters'][n]['Name'])
    if 'NextToken' in response:
        next_run(response['NextToken'])
    else:
        l = len(resources)
        LOGGER.info(f'Found {l} ssm parameters.')

def initial_run():
    response = client.describe_parameters(MaxResults=50)
    if len(response['Parameters']) > 0 <=50 and response['NextToken']:
        for n in range(0,len(response['Parameters'])):
            resources.append(response['Parameters'][n]['Name'])
        next_run(response['NextToken'])
    else:
        LOGGER.info("No SSM Parameters found.")
        exit()

def del_params(l):
    '''
    Deletes all params in a list
    '''
    kill_list = []
    for path in l:
        for item in resources:
            if path in item:
                kill_list.append(item)
        linebreak('!')
        for item in kill_list:
            print(item)
        LOGGER.info("The above SSM Parameters will be destroyed.")
    resp = str.lower(input('Do you wish to continue (y/n):\n-> '))
    if resp == 'y':
        for param in kill_list:
            try:
                LOGGER.info(f"trying to delete {param} ")
                response = client.delete_parameter(Name=param)
                LOGGER.info(response)
            except:
                LOGGER.error(f'Error deleting {param}.')

def build_list(l):
    parampaths = []
    for i in l:
        l2 = i.split('/')[1:-1]
        l2[0] = '/' + l2[0]
        for n in range(0,len(l2)):
            if l2[n] not in parampaths:
                parampaths.append('/'.join(l2[0:n]))
    return(parampaths)

def generate_unique(parampaths):
    l = []
    for item in parampaths:
        if item not in l:
            l.append(item)
    return(l)

def read_input(prompt, delimiter, message):
    linebreak(delimiter)
    print(message)
    x = input(prompt)
    while x:
        yield x
        x = input(prompt)

if __name__ == "__main__":
    if args.profile is None:
        print_profiles()
        linebreak('-')
        profile = input('Enter which AWS CLI Profile you wish to use:\n-> ')
    else:
        profile = args.profile
    boto3.session.Session(profile_name=profile)
    client = boto3.client('ssm')
    initial_run()
    linebreak('*')
    popped_list = (build_list(resources))
    unique_list = (generate_unique(popped_list))
    r = sorted(unique_list, key = len)
    if args.searchstring:
        del_params(args.searchstring)
    else:
        for item in r:
            if len(item) > 0:
                print(item)
        kill_list = list(map(str, read_input("-> ", '!', 'Enter paths from above for ssm params you wish to destroy, one per line: ')))
        del_params(kill_list)
    