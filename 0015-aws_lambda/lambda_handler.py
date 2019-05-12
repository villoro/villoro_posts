import os
import json

import aws

# add ec2/rds if needed
# fmt: off
INSTANCES = {
    "system_1": {
        "EC2": "i-068e5489acdd4a544",
        "RDS": "db_1"
    },
    "system_2": {
        "EC2": "i-0be4e5d15b667ad16",
        "RDS": "db_2"
    },
}
# fmt: on

ACTIONS = ["start", "stop", "status"]


def check_token(event):
    """ Check the presence of correct token in headers """

    if ("headers" not in event) or ("token" not in os.environ):
        return "Missing 'token' in headers"

    token = event["headers"].get("token", "")

    if token != os.environ["token"]:
        return "Bad token"

    return True


def lambda_handler(event, context):
    """ handle and html request """

    result = check_token(event)

    if result is not True:
        return {"statusCode": 400, "body": json.dumps(result)}

    data = event.get("queryStringParameters", {})

    out = {}
    for name, action in data.items():
        if name not in INSTANCES.keys():
            out[name] = f"name '{name}' not recognized, should be one of {INSTANCES.keys()}"

        elif action not in ACTIONS:
            out[name] = f"action '{action}' not recognized, should be {ACTIONS}"

        else:
            instances_dict = INSTANCES.get(name, {})

            out[name] = {
                "EC2": aws.act_instance_ec2(instances_dict.get("EC2", None), action),
                "RDS": aws.act_instance_rds(instances_dict.get("RDS", None), action),
            }

    return {"statusCode": 200, "body": json.dumps(out)}
