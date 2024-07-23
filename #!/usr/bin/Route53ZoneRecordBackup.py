#!/usr/bin/env python3
import boto3
from datetime import datetime
import json

class Route53Gatherer(object):
    def __init__(self):
        self.hosted_zones = None
        self.items = []
        self.r53 = None
        self.final_filename = None
    def Setup(self):
        # setup boto3 r53 client
        self.r53 = boto3.client('route53')
    def Run(self):
        self.Setup()
        self.GatherHostedZones()
        for HostedZone in self.hosted_zones:
            HostedZone["ResourceRecordSets"] = self.GatherHostedZoneRecords(HostedZone["Id"])
            self.items.append(HostedZone)
        self.WriteFile()
    def GatherHostedZones(self):
        self.hosted_zones  = (
            self.r53.get_paginator('list_hosted_zones')
            .paginate()
            .build_full_result()
        )['HostedZones']
    def GatherHostedZoneRecords(self, HostedZoneId):
        return (
            self.r53.get_paginator('list_resource_record_sets')
            .paginate(HostedZoneId=HostedZoneId)
            .build_full_result()
        )['ResourceRecordSets']
    def WriteFile(self):
        time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f"r53_zone_records_all_{time}.json"
        with open(self.filename, 'w') as f:
            json.dump(self.items, f)

if __name__ == "__main__":
    import sys
    if len(sys.argv) >1:
        print("Usage: python3 Route53ZoneRecordBackup.py")
        exit(1)
    x = Route53Gatherer()
    x.Run()
    print(f"ResourceRecords from all HostedZones have been written to {x.filename} ")
