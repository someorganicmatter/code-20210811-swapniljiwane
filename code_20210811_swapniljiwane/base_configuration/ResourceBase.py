from aws_cdk import core
from aws_cdk import core as cdk


class ResourceBase:
    def __init__(self, resource, product, env, region) -> None:
        self.resource = resource
        self.product = product
        self.env = env
        self.region = region

    def get_resource_name(self):
        parameter_list = [
            self.resource, self.product, self.env,
            self.get_region_name(self.region)
        ]
        separator = '-'
        return separator.join(filter(None, parameter_list))

    @staticmethod
    def get_region_name(region):
        switcher = {"us-east-1": "e1", "us-east-2": "e2"}
        return switcher.get(region, "e1")
