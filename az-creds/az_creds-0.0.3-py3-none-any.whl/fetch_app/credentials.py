#!/usr/bin/env python3

import os

from simple_term_menu import TerminalMenu
from yaml import safe_load

# Author: Jilani Sayyad
# Date: 2022-05-23
# Path: get_aks_credentials.py
# Description: This script is used to get the credentials for the AKS cluster


def get_account():
    get_account = os.popen("az account list -o yaml").read()
    return safe_load(get_account)


def get_subscriptions():
    account_details = get_account()
    len_account_details = len(account_details)
    subscription_list = []
    for i in range(len_account_details):
        subscription_list.append(account_details[i]["name"])
    subscription = TerminalMenu(
        subscription_list, title="subscriptions").show()
    return subscription, subscription_list


def get_credentials(subscription=None, subscription_list=None):
    subscription, subscription_list = get_subscriptions()
    subscription_id = subscription_list[subscription]
    command = "az aks list --subscription {} -o yaml".format(subscription_id)
    cluster_list = os.popen(command).read()
    cluster_list = safe_load(cluster_list)
    resource_groups = [cluster["resourceGroup"] for cluster in cluster_list]
    cluster_list = [cluster["name"] for cluster in cluster_list]
    if len(cluster_list) == 0:
        print("No clusters found")
        exit()
    cluster = TerminalMenu(cluster_list, title="clusters").show()
    cluster_id = cluster_list[cluster]
    resource_group_id = resource_groups[cluster]

    command = (
        "az aks get-credentials --resource-group {} --name {} --subscription {}".format(
            resource_group_id, cluster_id, subscription_id
        )
    )
    print(
        "Updating the kubeconfig file\n\ncluster: {} \nresource group: {} \nsubscription: {} \n".format(
            cluster_id,
            resource_group_id,
            subscription_id,
        )
    )
    os.system(command)
    print("\n\n\n")
    print("Cluster credentials updated successfully")


def main():
    get_credentials()
