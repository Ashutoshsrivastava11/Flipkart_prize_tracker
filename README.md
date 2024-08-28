#Flipkart prize tracker
--This Python script is designed to monitor the price of a product listed on Flipkart and send an email notification if the price drops below a specified threshold.
--The script uses requests for fetching the product page, BeautifulSoup for parsing the HTML to find the product price, and smtplib to send an email alert.

##How It Works:
--Upon running, the script continuously checks the product price at the specified interval.
--If the product price drops below the threshold_price, an email notification is sent to the specified email address.
--The script handles common errors such as changes in webpage structure and network issues gracefully, providing useful error messages.
