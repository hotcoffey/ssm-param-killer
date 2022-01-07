## SSM Param Killer

### Purpose

Over the course of your AWS cloud journey SSM Parameters can be left behind and build up over time for one reason or another, especially if you use something like Serverless Framework, Runway, or Stacker and you're stuck having to manually destroy your CloudFormation stacks. The AWS resources are removed, but the SSM Parameters stick around.

# USE AT YOUR OWN RISK
### Arguments
| Switch           | Description                                                                | Format | Required |
| ------------------- | -------------------------------------------------------------------------- | ------ | -------- |
|```-p``` or ```--profile```|  Name of the AWS CLI profile you want to use.| String | No|
|```-s``` or ```--searchstring```| string used to search through parameters you wish to delete | String | No|

---
**NOTE**

I highly recommend using a specific path instead of a search term when it comes to the searchstring. You're more than welcome to use something like ```ccplat``` or ```waf``` but the script will search and destroy accordingly and accross all things in the account, not just things deployed by CCP. 

It's better to use something like ```/serverless/lambda-poc/dev1``` unless you know what you're doing and you're intentionally trying to do something like blow away a namespace or something with a small blast radius like ```dev1```.

---
### Usage Examples
```bash
python3 ssm-pk.py
python3 ssm-pk.py --profile=default
python3 ssm-pk.py --profile=default -s=/ccplat/dynamodb
```

If the ```-p``` or ```--profile``` argument isn't provided, ```ssm-pk.py``` gathers a list of the AWS CLI profiles boto3 can use and allows you to choose which one you want to run the script against, from there it'll grab all SSM Parameters and prompt you with a list of unique paths.


### Example Paths
```bash
/serverless
/stacker
/serverless/lambda-poc
/serverless/lambda-poc/dev1
/serverless/lambda-poc/dev1/python
/serverless/lambda-poc/dev1/javascript
/stacker/appsync
/stacker/appsync/dev0
/stacker/vpc/dev0
```
---
**NOTE**

I intentionally left out the SSM Parameter at the end of each path in order to generate a small list for you to choose from because you could potentially have hundreds of parameters in any given path.

However, if you see something in the generated list like ```/serverless/lambda-poc/dev1/python``` and know for a fact that you only want to delete ```/serverless/lambda-poc/dev1/python/foo``` parameters, there's nothing stopping you from doing that.

It's up to you to know what all you're deleting and I recommend if you don't want to blow away all SSM Params within a given path, you do so via the CLI or AWS Console.

---

If the ```-s``` or ```--searchstring``` argument isn't provided, the script then prompts you to enter the paths containing the SSM Parameters you wish to destroy, one per line. A blank line at the end will execute the part of the script that does the deletions.

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Enter paths from above for ssm params you wish to destroy, one per line: 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
-> 
```

Using the example above, simply entering ```/serverless/lambda-poc``` would handle the deletion of all SSM Parameters in the following paths as well:

```
/serverless/lambda-poc/dev1
/serverless/lambda-poc/dev1/python
/serverless/lambda-poc/dev1/javascript
```

---
**NOTE**

Even though the prompt is asking for a path, you can enter a search string (for example `dev1`) and it'll result in the same functionality.

---
