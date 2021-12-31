## SSM Param Killer

### Purpose

Over the course of your AWS cloud journey SSM Parameters can be left behind and build up over time for one reason or another, especially if you use something like Serverless Framework, Runway, or Stacker and you're stuck having to manually destroy your CloudFormation stacks. The AWS resources are removed, but teh SSM Parameters stick around.

### Usage
```bash
python3 ssm-pk.py
```

```ssm-pk.py``` gathers a list of the available profiles boto3 can use and allows you to choose which one you want to run the script against, from there it'll grab all SSM Parameters and prompt you with a list of unique paths.


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

I intentionally left out the SSM Parameter at the end of each path in order to generate a small list for you to choose from. It's up to you to know what all you're deleting and I recommend if you don't want to blow away all SSM Params within a given path, you do so via the CLI or AWS Console.

---

The script then prompts you to enter the paths containing the SSM Parameters you wish to destroy, one per line. A blank line at the end will execute the part of the script that does the deletions.

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