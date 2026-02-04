import smtplib
from email.mime.text import MIMEText

msg = MIMEText('Hi,\n\nI wanted to share a quick update on the Trello Automation integration task:\n\n- We have finalized the list mappings for "To Do," "In Progress," "Done," and "Failed."\n- The task lifecycle event hooks are currently being implemented to automatically create and move cards as tasks progress.\n- Reliable card ID tracking and error handling mechanisms are also in development.\n- Estimated completion is within the next 1 to 3 days.\n\nPlease let me know if you\'d like me to provide any interim demos or status reports.\n\nBest regards,\nMimi.botx')
msg['Subject'] = 'Update on Trello Automation Task'
msg['From'] = 'mimi.botx@gmail.com'
msg['To'] = 'taminagurnett@gmail.com'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('mimi.botx@gmail.com', 'raddeoaxhluexdqf')
server.send_message(msg)
server.quit()
