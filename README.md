---
title: "Sending automatic emails with attachment using Python, AWS-Lambda and S3"
author: "Danilo Arruda"
date: "May, 2023"
output:
  html_document:
    toc: yes
    toc_depth: '3'
    df_print: paged
    warning: false
  word_document:
    toc: yes
    toc_depth: '3'
  pdf_document:
    includes:
      in_header: header.tex
    toc: yes
    toc_depth: 3
    toc_href: yes
---

# Overview

This script is designed to automatically send an email if specific criteria are met. In the case of the example, the script searches for emails from Paypal notifying that a customer bought a virtual product and then it sends email to the customer with the product attached.

## Installation

In order to implement and run the script, the user must enable Gmail API and properly set up the AWS services: S3, Lambda, and Cloud Watch. In general, setting up the services are straight forward. The workflow is as follows:

1.  Enable Gmail API;

2.  Make an AWS account;

3.  Create a S3 bucket with the files to be sent as attachment and the Python script

    1.  Authorize Lambda to access the bucket (setting up IAM role - [HERE](https://repost.aws/knowledge-center/lambda-execution-role-s3-bucket))

4.  Make a Lambda function by importing the Python script directly from S3 (click upload from)

5.  Schedule the script to run at the desired frequency using CloudWatch

In addition, make sure to properly edit the script including the info about your API and specific bucket.
