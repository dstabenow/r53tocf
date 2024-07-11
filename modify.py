#!/usr/bin/env python3
from itertools import groupby
import boto3
import re

def alias_gen(domain):
    r53 = boto3.client('route53')
    zone_id = r53.list_hosted_zones_by_name(DNSName=domain,MaxItems="1")["HostedZones"][0]["Id"]
    items = [x for x in (
        r53.get_paginator('list_resource_record_sets')
        .paginate(HostedZoneId=zone_id)
        .build_full_result()
    )['ResourceRecordSets'] if  "AliasTarget" in x.keys()]

    def group_by_key(data, key):
        grouped = groupby(data, lambda item: item[key])
        return [{"Name": key, "Values":list(values)} for key, values in grouped]

    grouped_items = group_by_key(items, "Name")

    new_items = []
    for item in grouped_items:
        new_items.append({
            "Name": item["Name"],
            "Values": list(set([x["AliasTarget"]["DNSName"] for x in item["Values"]]))
        })

    rrs = []
    def rr_gen(name, target_list):
        comment = ' '.join(target_list)
        if len(target_list) ==1:
            return "%s      1      IN      CNAME      %s ; %s" %(name, target_list[0], comment)
        ordered_patterns = ["us-east-2", "us-east-1", "us-west-2", "us-west-1"]
        for pattern in ordered_patterns:
            x = next((item for item in target_list if pattern in item), None)
            if x != None:
                return "%s      1      IN      CNAME      %s ; %s" %(name, x, comment)
        return "%s      1      IN      CNAME      %s ; %s" %(name, target_list[0], comment)

    for target_list in new_items:
        rrs.append(rr_gen(target_list["Name"],target_list["Values"]))

    return rrs

def remover(filename, domain):
    pattern = r"^((\S+\s+\d+\s+IN\s+(?:NS|SOA)\s+)|(\S+\s+\d+\s+AWS\s+ALIAS\s+))"
    with open(filename, "r+") as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in lines:
            if not re.search(pattern, line):
                f.write(re.sub(r"\.\s+(\d+)\s+IN\s+", f".      1      IN      ", line))
        for line in alias_gen(domain):
            f.write(line)

if __name__ == "__main__":
  import sys
  if len(sys.argv) != 3:
    print("Usage: python3 remove_lines.py <filename> <domain>")
    exit(1)
  remover(sys.argv[1], sys.argv[2])
  print(f"Lines not matching the pattern removed from {filename}. Aliases constructed and added favoring us-east-2.")
