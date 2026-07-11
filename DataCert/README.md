# Data Certification Mailer

A Python application to automate data certification follow-up emails by:
- reading stakeholder data from CSV or Excel,
- rendering personalized HTML email content,
- attaching application-specific certification documents,
- sending email from a shared mailbox,
- logging success and failure details.

## Project Structure

```
DataCert/
├── config/
│   ├── config.json
│   └── email_template.html
├── data/
│   ├── stakeholders.csv
│   ├── attachments/
│   └── logs/
├── scripts/
│   ├── main.py
│   ├── read_stakeholders.py
│   ├── generate_email.py
│   ├── attach_documents.py
│   ├── send_mail.py
│   ├── logger.py
│   └── utils.py
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.8 or newer
- A Microsoft 365 account with permission to send from the shared mailbox
- For Graph backend: Azure app registration with `Mail.Send` permission
- For Outlook backend: Outlook desktop installed and configured on Windows
- Stakeholder data file in `data/stakeholders.csv` or `data/stakeholders.xlsx`
- Certification document files in `data/attachments/`

## Step-by-Step Guide

### 1. Install dependencies

Open PowerShell in the project folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

### 2. Configure the app

Edit `config/config.json` and update the values for your environment.

Required fields:
- `stakeholder_file`: path to the stakeholder CSV or Excel file
- `attachments_folder`: path to the attachments directory
- `output_log`: path for the log CSV file
- `email_backend`: `graph` or `outlook`
- `email.subject`: email subject line
- `email.from`: sender email address
- `email.reply_to`: reply-to address

Graph backend fields:
- `graph.tenant_id`
- `graph.client_id`
- `graph.client_secret`
- `graph.shared_mailbox`

Outlook backend fields:
- `outlook.shared_mailbox`

Example `config/config.json`:

```json
{
  "stakeholder_file": "../data/stakeholders.csv",
  "attachments_folder": "../data/attachments",
  "output_log": "../data/logs/send_log.csv",
  "email": {
    "subject": "Data Certification Reminder",
    "from": "datacertification@company.com",
    "reply_to": "datacertification@company.com"
  },
  "email_backend": "graph",
  "graph": {
    "tenant_id": "YOUR_TENANT_ID",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "shared_mailbox": "datacertification@company.com"
  },
  "outlook": {
    "shared_mailbox": "datacertification@company.com"
  }
}
```

### 3. Prepare stakeholder data

Place stakeholder data in either `data/stakeholders.csv` or `data/stakeholders.xlsx`.

The file must contain at least these columns:
- `Name`
- `Email`
- `Application`
- `Due Date`

Example `data/stakeholders.csv`:

```csv
Name,Email,Application,Due Date
John Doe,john.doe@company.com,SAP,2026-07-25
Mary Smith,mary.smith@company.com,Oracle,2026-07-26
```

### 4. Add attachments

Put certification documents inside `data/attachments/`.

The script tries to match attachments by application name, e.g. `SAP.pdf` or `Oracle.docx`.
If no exact match is found, it will use the most recently modified file in the folder.

### 5. Customize the email template

Edit `config/email_template.html` to update email content and placeholders.

Supported placeholders include `{{Name}}`, `{{Application}}`, and `{{Due Date}}`.

Example template:

```html
<!DOCTYPE html>
<html>
  <body>
    <p>Hello {{Name}},</p>
    <p>Please complete your Data Certification for <strong>{{Application}}</strong> due on <strong>{{Due Date}}</strong>.</p>
    <p>The latest certification document is attached to this email.</p>
    <p>Regards,<br/>IT Operations</p>
  </body>
</html>
```

### 6. Run a dry run

Before sending real email, verify the workflow with:

```powershell
python scripts/main.py --config config/config.json --dry-run
```

This prints the recipients, subject, and selected attachment without sending actual emails.

### 7. Send emails

When you are ready, run:

```powershell
python scripts/main.py --config config/config.json
```

### 8. Review logs

Send results are recorded in `data/logs/send_log.csv` with columns:
- `Timestamp`
- `Recipient`
- `Application`
- `Status`
- `Message`

## Notes

- If the Graph backend is used, ensure the Azure app has the correct permissions and the shared mailbox is accessible.
- If the Outlook backend is used, Outlook must be installed on the Windows machine where the script runs.
- The script skips any stakeholder row without a valid email address.

## Troubleshooting

- `FileNotFoundError` for `config/config.json`: verify the config path and run from the project root.
- `no attachment found`: confirm your attachment file names match the `Application` values.
- `Invalid recipient email address`: verify the `Email` column values in the stakeholder file.

## Optional command-line options

- `--stakeholder-file <path>`: override the stakeholder file configured in `config.json`
- `--dry-run`: perform a workflow test without sending messages

## Security Best Practices

- Store sensitive credentials outside source code.
- Keep attachment files and stakeholder data secure.
- Review the email template for correctness before sending.
- Run a dry run first to verify content and attachments.

## License

[Add your license information here]

## Support & Contributions

For issues, questions, or contributions, please contact the Certification Team.

## Version History

- **v1.0.0** (2026-07-12) - Initial release
  - Email automation workflow
  - CSV/Excel stakeholder import
  - Attachment selection and logging support
  - Comprehensive logging

---

**Last Updated:** July 12, 2026
