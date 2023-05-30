#Importanting necessary libraries:
import imaplib
import email
import smtplib
import os
import re
from email.utils import parseaddr
import datetime
import csv
from io import StringIO
import os.path
import boto3
import email
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication



def lambda_handler(event,context):

    #Importing custumer_list objects from S3:
    bucket_name = 'automatic-send-scitraining'
    s3_client = boto3.client('s3', 'us-east-2')
    s3 = boto3.resource('s3', 'us-east-2')
    bucket = s3.Bucket(bucket_name)


    # IMAP settings
    IMAP_SERVER =  "imap.gmail.com"  # the hostname of the IMAP server
    IMAP_PORT = 000  # the port number for the IMAP server
    IMAP_USERNAME = 'youremail@gmail.com'  # the email address used to connect to the IMAP server
    IMAP_PASSWORD = 'code'  # the password for the email account used to connect to the IMAP server

    # SMTP settings
    SMTP_SERVER = 'smtp.gmail.com'  # the hostname of the SMTP server
    SMTP_PORT = 000  # the port number for the SMTP server
    SMTP_USERNAME = 'yourmail@gmail.com'  # the email address used to connect to the SMTP server
    SMTP_PASSWORD = 'code'  # the password for the email account used to connect to the SMTP server

    # extract yesterday's date (AWS has a bug here for somereason)
    #This will be used to filter the emails
    todays_date = datetime.datetime.now() - datetime.timedelta(days=1)

    # format the time in a way that is compatible with the IMAP search function
    date_format = todays_date.strftime("%d-%b-%Y")


    # You should define your products and their corresponding emails here:
    #Make dictionaries with needed info for email: search keyword, file address, subject line, message
    def product_1():
        dict_with_info={}
        #The keyword is a unique word that you will receive in the paypal email
        #notifying you that someone has purchased the product
        dict_with_info['keyword'] = 'Performance Analysis Spreadsheet'
        
        #the directory where the file is located. Since we are using a working
        #directory, the file address is the name of the file
        dict_with_info['file_address'] = 'Volleyball Scouting v1.0.xlsx'

        dict_with_info['subject_line'] = 'Performance Analysis Spreadsheet - Sci Training'
        
        dict_with_info['message'] = '''Hello!
    This is Danilo from Sci Training, and I hope you are well and safe.

    Firstly, thank you for acquiring our tool: "Excel Spreadsheet for Performance Analysis in Volleyball." We hope you make good use of this tool and be able to improve your team performance.
    The spreadsheet is attached to this email. Should you have any questions, do not hesitate to contact us.

    We appreciate your trust and hope you have a wonderful week.

    scitraining.com.br/
    facebook.com/OficialSciTraining
    instagram.com/scitraining/
    '''
        return dict_with_info


    def product_2():
        dict_with_info={}
        
        dict_with_info['keyword'] = 'Excel Spreadsheet Training Load Monitoring for Team Sports'
        
        dict_with_info['file_address'] = 'TEAM_TRAINING_LOAD_MONITORING_V1.1.xlsx'

        dict_with_info['subject_line'] = 'Excel Spreadsheet Training Load Monitoring for Team Sports - Sci Training'
        
        dict_with_info['message']='''Hello! 
    This is Gustavo from Sci Training, and I hope you are well and safe.

    Firstly, thank you for acquiring our tool: "Excel Spreadsheet - Training Load Monitoring for Team Sports." We hope you make good use of this tool and be able to improve your team performance. 
    The spreadsheet is attached to this email. Should you have any questions, do not hesitate to contact us.

    We appreciate your confidence and hope you have a wonderful week.

    scitraining.com.br/
    facebook.com/OficialSciTraining 
    instagram.com/scitraining/
    '''
        return dict_with_info



    def send_email(to, subject, body, attachment_key):
        """
        Sends an email with an attachment to a specified recipient.

        :param to: (str) Email address of the recipient.
        :param subject: (str) Subject of the email.
        :param body: (str) Body text of the email.
        :param attachment_key: (str) Key of the S3 bucket object to attach to the email.
        :return: None
        """
        message = MIMEMultipart()
        message['From'] = SMTP_USERNAME
        message['To'] = to
        message['Subject'] = subject
        
        # add body to email
        body_text = MIMEText(body)
        message.attach(body_text)
        bucket = s3.Bucket('automatic-send-scitraining')
        obj = bucket.Object(attachment_key)


        # download file from s3 and add it as an attachment
        response = obj.get()
        file_content = response['Body'].read()
        attachment = MIMEApplication(file_content, Name=os.path.basename(obj.key))
        attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(os.path.basename(obj.key))
        message.attach(attachment)
    
        smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp_server.sendmail(SMTP_USERNAME, to, message.as_string())
        smtp_server.quit()
        print(f"Email sent to the email address: {to} Product: {attachment_key}")

        

    def check_purchase(email):
        """
        This function checks if a customer has already purchased a product before 
        by looking up their email and matching it with the product's keyword they
        are trying to buy. If the customer has already purchased the product, 
        the function prints a message indicating so, and if not, it sends an email
        to the customer, logs a debug message stating that an email has been sent, 
        and stores the customer's information in the customer list file.

        Parameters:
        email (str): The email of the customer attempting to purchase the product.

        Returns:
        None
        """
        global customer_list
        customer_list = s3_client.get_object(
        Bucket=bucket_name,
        Key='customer_list.csv')
        customer_list = customer_list['Body'].read().decode('ISO-8859-1')
        customer_list = StringIO(customer_list)
        customer_list = csv.reader(customer_list)
        
        match_found = False
        for row in customer_list:
            if row[0] == email and product['keyword'] == row[1]:
                print(f"The product has been sent before. Email: {email} Product: {product['keyword']}")
                match_found = True
                break
            
        if not match_found:
            logging.debug(f"Calling function to send email to: {email}")
            send_email(email, product['subject_line'], product['message'], product['file_address'])
            logging.debug(f"Email sent successfully to {email}. Product: {product['subject_line']}")
            store_customer_info(email,product['keyword'])
            

    def store_customer_info(email, prod):
        """
       Store customer information in a CSV file hosted on an S3 bucket. 

       :param email: string, the customer's email address.
       :param prod: string, the product keyword.
       :return: None
       """
        
        emails = [row[0] for row in customer_list]
        products = [row[1] for row in customer_list]
        emails.append(email)
        products.append(product['keyword'])
    
        new_row=[email,prod,todays_date]
        #rows = zip(emails, products)
        
         # download s3 csv file to lambda tmp folder
        local_file_name = '/tmp/customer_list.csv' #
        s3.Bucket(bucket_name).download_file('customer_list.csv',local_file_name)
        
    
        # write the data into '/tmp' folder
        with open('/tmp/customer_list.csv','r',encoding='ISO-8859-1') as infile:
            reader = list(csv.reader(infile))
            reader.insert(0,new_row)
        
        with open('/tmp/customer_list.csv', 'w', newline='',encoding='ISO-8859-1') as outfile:
            writer = csv.writer(outfile)
            for line in (reader):
                writer.writerow(line)
        
        # upload file from tmp to s3 key
        bucket.upload_file('/tmp/customer_list.csv', 'customer_list.csv')
                    

    ## Search the pattern in the emails
    try:
        #re_pattern = r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
        imap_server = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        imap_server.login(IMAP_USERNAME, IMAP_PASSWORD)
        imap_server.select('INBOX')
        # search for emails sent on the current day from the specified email address and subject
        search_query = f'(FROM "service@paypal.com.br" SUBJECT "payment received" SINCE "{date_format}")'
        status, email_ids = imap_server.search(None, search_query)
        if email_ids == [b'']: 
            print(f"The search has not returned results. Product not sold. {date_format}")
        else:
            for email_id in email_ids[0].split():
                _, msg = imap_server.fetch(email_id, '(RFC822)')
                email_msg = email.message_from_bytes(msg[0][1])
                
                if email_msg.is_multipart():
                    body = email_msg.get_payload(0).get_payload(decode=True)
                else:
                    body = email_msg.get_payload(decode=True)
                try:    
                    body = body.decode('utf-8')
                except UnicodeDecodeError:
                    body = body.decode('ISO-8859-1')
                email_matches = parseaddr(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', body)[0])[1]
                print(f"Email matches found: {email_matches}")

                if 'Performance Analysis Spreadsheet' in body:
                    product= product_1()
                    check_purchase(email_matches)

                elif 'Excel Spreadsheet Training Load Monitoring for Team Sports' in body:
                    product = product_2()
                    check_purchase(email_matches)


        # Close the IMAP server connection
        imap_server.close()
        imap_server.logout()
    except Exception as e:
        logging.error(f"Error: {e}")
