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

ACTION = "start"


def lambda_handler(event, context):
    """ start instances """

    for name, data in INSTANCES.items():
        aws.act_instance_ec2(data.get("EC2", None), ACTION)
        aws.act_instance_rds(data.get("RDS", None), ACTION)

    return "Start {} instances".format(ACTION)
