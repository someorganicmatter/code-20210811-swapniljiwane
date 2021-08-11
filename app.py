#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from code_20210811_swapniljiwane.code_20210811_swapniljiwane_stack import Code20210811SwapniljiwaneStack

PUSHNOTIFICATIONEMAIL=""

app = core.App()
Code20210811SwapniljiwaneStack(app, "Code20210811SwapniljiwaneStack", PUSHNOTIFICATIONEMAIL)

app.synth()
