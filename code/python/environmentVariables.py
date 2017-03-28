import os

##
# This will set the needed environment varibables
# This needs to be filled out to match the rc file form OpenStack
##


def environmentVariables():
    f = open('keys', 'r').read().splitlines()
    os.environ["OS_PASSWORD"] = f[2]
    os.environ["SLACK_KEY"] = f[1]
    os.environ["SLACK_KEY_NOBOT"] = f[0]
    os.environ["OS_AUTH_URL"] = "https://hpc2n.cloud.snic.se:5000/v3"
    os.environ["OS_TENANT_ID"] = "88a342064e8d42789835816db1543405"
    os.environ["OS_TENANT_NAME"] = "SNIC 2017/13-8"
    os.environ["OS_PROJECT_NAME"] = "SNIC 2017/13-8"
    os.environ["OS_USERNAME"] = "s7424"
    os.environ["OS_PROJECT_DOMAIN_NAME"] = "snic"
    os.environ["OS_USER_DOMAIN_NAME"] = "snic"
    os.environ["OS_IDENTITY_API_VERSION"] = "3"
    os.environ["OS_INTERFACE"] = "public"
    os.environ["OS_REGION_NAME"] = "HPC2N"
