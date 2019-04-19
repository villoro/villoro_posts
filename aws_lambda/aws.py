import boto3

SESSION = boto3.Session(region_name="eu-west-2")

EC2 = SESSION.client("ec2")
RDS = SESSION.client("rds")


def act_instance_ec2(instance, action):
    """ Act uppon one ec2 instance (start/stop) """

    if instance is None:
        out = "EC2 not configured"

    if action == "start":
        EC2.start_instances(InstanceIds=[instance])
        out = f"EC2 instance '{instance}' started"

    elif action == "stop":
        EC2.stop_instances(InstanceIds=[instance])
        out = f"EC2 instance '{instance}' stopped"

    out = f"action '{action}' not recognized"

    print(f"- {out}")
    return out


def act_instance_rds(instance, action):
    """ Act uppon one rds instance (start/stop) """

    if instance is None:
        out = "ECS not configured"

    # Get rds status
    rds_instance = RDS.describe_db_instances(DBInstanceIdentifier=instance)
    status = rds_instance["DBInstances"][0]["DBInstanceStatus"]

    if action == "start":
        if status == "stopped":
            RDS.start_db_instance(DBInstanceIdentifier=instance)
            out = f"RDS instance '{instance}' started"

        else:
            out = f"RDS instance '{instance}' not started since is '{status}'"

    elif action == "stop":
        if status == "available":
            RDS.stop_db_instance(DBInstanceIdentifier=instance)
            out = f"RDS instance '{instance}' stopped"

        else:
            out = f"RDS instance '{instance}' not stopped since is '{status}'"

    out = f"action '{action}' not recognized"

    print(f"- {out}")
    return out
