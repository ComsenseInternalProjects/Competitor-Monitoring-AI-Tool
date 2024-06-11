from openai import OpenAI
import smtplib
from streamlit import st

def generate_email(change_data, change_type):
    employee_email = "rigveds098@companymail.com"  # Replace with the actual email address
    prompt = f"""You are an experienced email content writer. Write me an email without subject:
            {change_type} Updates
            and write an email to an employee named Rigved, of Compass which is a construction company
            in UAE. The content provided to you is the updates from competitors' site. Your job is to summarize the
            updates and give in points and let the employee know what their competitors are doing. In 3 to 4 lines.
            Do not use this column added or removed or position number of data just add the information you get if there is any link in information 
            then add that to email. In end of mail mention senders name as Suvakanta Rout
            Competitor's News page link : https://aecom.com/press-releases/
            Competitor's Project page link : https://aecom.com/projects/
            Google News Link : https://news.google.com/search?q=aecom&hl=en-IN&gl=IN&ceid=IN%3Aen

            Use above links for reference of individual case. Like for Competitor's News page case its link like this.
            Changes:
            {change_data}
    """

    try:
        # Initialize the OpenAI client
        client = OpenAI(api_key="**********************************")
        # Create a completion request with the combined prompt and parameters
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct-0914",
            prompt=prompt,
            temperature=0,
            max_tokens=700,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["#", ";"]
        )
        # Extract the first choice from the response
        if hasattr(response, 'choices') and response.choices:
            email_body = response.choices[0].text
        else:
            email_body = "No choices found in the response."

        # Send the email
        send_status = send_email("suvakantarout1999@companymail.com", employee_email,"password",f"{change_type} Updates", email_body)
        # Return the email body for display and the send status
        return email_body, send_status
    except Exception as e:
        # If there's an error, return the error message
        return str(e), False
    
def send_email(sender_email, reciever_email, password, subject, body):
 
        try:
 
            # Connect to Gmail's SMTP server
            server = smtplib.SMTP('smtp.office365.com', 587)
            server.starttls()
 
            # Login to Gmail
            server.login(sender_email, password)
 
            # Send email
            message = f"Subject: {subject}\n\n{body}"
            # server.sendmail(sender_email, reciever_email, message.as_string)
            server.sendmail(sender_email, reciever_email, message)
 
            # Close the SMTP server connection
            server.quit()
            st.success("Email Sent Sucessfully")
        except Exception as e:
            st.error("Email Sent Fail")
            raise e