# Price Checker Script
# This script monitors the price of a product on Flipkart and sends an alert email if the price falls below a set threshold.

import requests  # For sending HTTP requests
import smtplib  # For sending email notifications
from bs4 import BeautifulSoup  # For parsing HTML content
import time  # For scheduling repeated checks

# Product URL and headers to mimic a real user request
flipkart_url = 'https://www.flipkart.com/apple-iphone-15-pro-max-blue-titanium-256-gb/p/itm4a0093df4a3d7'
http_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive'
}

# Set the price below which you want to be notified
threshold_price = 55000.0

# Email configuration settings
sender_email = 'ashutoshsrivastava0501@gmail.com'
recipient_email = 'ashutoshsrivastava0501@gmail.com'
email_app_password = 'your_app_password'  # Replace with your app-specific password


def check_price():
    """Checks the current price of the product and sends an alert if it's below the threshold."""
    try:
        # Request the product page
        response = requests.get(flipkart_url, headers=http_headers)
        response.raise_for_status()  # Ensure the request was successful

        # Parse the page content using BeautifulSoup
        page_content = BeautifulSoup(response.content, 'html.parser')

        # Find the product name
        product_title_element = page_content.find("span", {"class": "_35KyD6"})
        product_title = product_title_element.get_text() if product_title_element else "Unknown Product"

        # Extract the price of the product
        price_element = page_content.find("div", {"class": "_1vC4OE _3qQ9m1"})
        if price_element:
            # Clean the price string and convert it to a float
            price_value = float(price_element.get_text(strip=True)[1:].replace(',', ''))
            print(f"Product: {product_title}\nCurrent Price: ₹{price_value}")

            # If the price is lower than the set threshold, trigger the alert
            if price_value < threshold_price:
                send_alert(price_value)
        else:
            print("Error: Unable to locate the price on the page. The webpage layout may have changed.")

    except requests.HTTPError as http_error:
        print(f"HTTP request error: {http_error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


def send_alert(current_price):
    """Sends an email alert when the price drops below the set threshold."""
    try:
        # Configure and start the SMTP session
        mail_server = smtplib.SMTP('smtp.gmail.com', 587)
        mail_server.ehlo()  # Establish connection with the server
        mail_server.starttls()  # Start TLS encryption
        mail_server.ehlo()

        # Log in to the email account using the app password
        mail_server.login(sender_email, email_app_password)

        # Compose the email content
        email_subject = 'Price Drop Alert!'
        email_content = f"The price of the product has dropped to ₹{current_price}.\nCheck it out here: {flipkart_url}"
        email_message = f"Subject: {email_subject}\n\n{email_content}"

        # Send the email
        mail_server.sendmail(sender_email, recipient_email, email_message)
        print('Notification sent successfully!')

    except smtplib.SMTPException as smtp_error:
        print(f"Failed to send email: {smtp_error}")

    finally:
        mail_server.quit()  # Terminate the SMTP session


# Main loop to regularly check the price
if __name__ == "__main__":
    while True:
        check_price()
        # Wait for one hour before the next check
        time.sleep(60 * 60)
