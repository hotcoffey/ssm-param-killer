import boto3
import string
import logging

FORMAT_STRING = "%(asctime)s [%(levelname)-9s] [%(filename)s]-[%(lineno)d]  %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT_STRING, datefmt="%m/%d/%Y %I:%M:%S %p")
LOGGER = logging.getLogger(__file__)

resources = []
nexttoken = ''

def print_profiles():
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
    for n in range(0,len(response['Parameters'])):
        resources.append(response['Parameters'][n]['Name'])
    next_run(response['NextToken'])

def del_params(l):
    '''
    Deletes all params in a list
    '''
    kill_list = []
    for path in l:
        for item in resources:
            if path in item:
                kill_list.append(item)
    for param in kill_list:
        try:
            LOGGER.info(f"trying to delete {param} ")
            response = client.delete_parameter(Name=param)
            LOGGER.info(response)
        except:
            LOGGER.error(f'Error deleting something.')

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
    print(80*str(delimiter))
    print(message)
    print(80*str(delimiter))
    x = input(prompt)
    while x:
        yield x
        x = input(prompt)

if __name__ == "__main__":
    print_profiles()
    profile = list(map(str, read_input("-> ", '!', 'Enter which AWS CLI Profile you wish to use: ')))
    boto3.session.Session(profile_name=profile[0])
    client = boto3.client('ssm')
    initial_run()
    print(80*'*')
    q = (build_list(resources))
    s = (generate_unique(q))
    r = sorted(s, key = len)
    for item in r:
        if len(item) > 0:
            print(item)
    kill_list = list(map(str, read_input("-> ", '!', 'Enter paths from above for ssm params you wish to destroy, one per line: ')))
    del_params(kill_list)


'''
read profiles and prompt for user to select the right one

'''