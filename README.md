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
    code_folding: hide
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

In order to implement and run the script, the user must enable Gmail API and properly set up the AWS services: S3, Lambda, and Cloud Watch. In general, setting up the services are straight forward. In general the workflow is as follows:

1.  Enable Gmail API;

2.  Make an AWS account;

3.  Create a S3 bucket with the files to be sent as attachment

    1.  Authorize Lambda to access the bucket

4.   

## Gmail API

The first thing to do is to request authorization from your Gmail. You can do that by enabling the Gmail API. Since the goal of this readme is not to teach how to set up this API, I won't be explaining it. However, there are plenty of tutorials describing how to do it. Like [this](https://www.thepythoncode.com/article/use-gmail-api-in-python).

## Setting up AWS-S3 and Lambda

Amazon Web Services (AWS) is a comprehensive cloud computing platform provided by Amazon.com. For sending our email with attachment, we will be using S3, which is a cloud storage platform, and Lambda, which allows us to run scripts periodically. Also, you can make an account and use most of AWS services for free.

After you created an account, go to the S3 website and create a bucket (also, plenty of videos showing how to set that up). In the bucket you should include the files that you intend to send as attachment to your emails. In addition, you have to authorize S3 to connect to your Lambda
