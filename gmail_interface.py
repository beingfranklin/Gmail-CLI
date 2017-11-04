print "                        TEXT BASED EMAIL INTERFACE"

flag = 1
username = raw_input("Enter your username:")
password = raw_input("Enter your password:")
fromaddress = raw_input("Enter your email ID:")
toaddress = raw_input("Enter the receivers email ID:")


while(flag == 1) :

    print "1.Send email"
    print "2.Show number of unread messages"
    print "3.Read latest email"
    print "4.Forward the oldest email in your inbox"
    print "5.Exit"

    choice = input("Please enter your choice:")

    if(choice == 1) :
        from email.MIMEMultipart import MIMEMultipart
        from email.MIMEText import MIMEText

        fromaddr = fromaddress
        toaddr = toaddress
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = raw_input("Enter subject:")

        f1 = open("file1.txt","w")
        string1 = raw_input("Enter content of the email:")
        f1.write(string1)
        f1.close()
        f2 = open("file1.txt","r")
        body = f2.read()


        msg.attach(MIMEText(body, 'plain'))

        import smtplib

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username, password)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)

        print "Your email has been send!"


    elif(choice == 2) :
        import imaplib


        obj = imaplib.IMAP4_SSL('imap.gmail.com','993')
        obj.login(username,password)
        obj.select()
        obj.search(None,'UnSeen')

        print "Number of unseen email:",len(obj.search(None, 'UnSeen')[1][0].split())

    elif(choice == 3) :
        import urllib
        from bs4 import BeautifulSoup

        import imaplib
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(fromaddress, password)
        mail.list()
        # Out: list of "folders" aka labels in gmail.
        mail.select("inbox") # connect to inbox.

        result, data = mail.search(None, "ALL")

        ids = data[0] # data is a list.
        id_list = ids.split() # ids is a space separated string
        latest_email_id = id_list[-1] # get the latest

        result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID

        raw_email = data[0][1] # here's the body, which is raw text of the whole email
        # including headers and alternate payloads

        result, data = mail.uid('search', None, "ALL") # search and return uids instead
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]

        import email
        email_message = email.message_from_string(raw_email)
        if email_message.is_multipart():
           print email_message.get_payload(0).get_payload()
        else:
           print email_message.get_payload()


    elif(choice == 4) :
        import smtplib
        import imaplib
        import email
        import string

        imap_host = "imap.gmail.com"
        imap_port = 993
        smtp_host = "smtp.gmail.com"
        smtp_port = 587
        user = username
        passwd = password
        msgid = 1
        from_addr = fromaddress
        to_addr = toaddress


        # open IMAP connection and fetch message with id msgid
        # store message data in email_data
        client = imaplib.IMAP4_SSL(imap_host, imap_port)
        client.login(user, passwd)
        client.select()
        typ, data = client.search(None, 'ALL')
        for mail in data[0].split():
            typ, data = client.fetch(msgid, "(RFC822)")
            email_data = data[0][1]
        client.close()
        client.logout()


        # create a Message instance from the email data
        message = email.message_from_string(email_data)


        message.replace_header("From", from_addr)
        message.replace_header("To", to_addr)


        # open authenticated SMTP connection and send message with
        # specified envelope from and to addresses
        smtp = smtplib.SMTP(smtp_host, smtp_port)
        smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(user, passwd)
        smtp.sendmail(from_addr, to_addr, message.as_string())
        smtp.quit()



        print "Your mail has bee forwarded!"



    elif(choice == 5):
        print "Program developed by Joseph Varghese,Franklin Antony,Joseph Mathew"
        exit()


    else :
        print "You have entered wrong choice!"

    ctr = raw_input("Do you want to continue?(Y?N):")
    if(ctr == 'N' or ctr =='n') :
        flag = 0


if(flag == 0) :
    print "Program developed by RoundMelon Studio"
