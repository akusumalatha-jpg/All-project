import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scripts.attach_documents import find_attachment
from scripts.generate_email import render_email, render_subject
from scripts.logger import CsvLogger
from scripts.read_stakeholders import read_stakeholders
from scripts.send_mail import EmailSendError, EmailSender
from scripts.utils import ensure_folder, load_config, load_text_file


def parse_args():
    parser = argparse.ArgumentParser(description="Data Certification Mailer")
    parser.add_argument(
        "--config",
        default="config/config.json",
        help="Path to the configuration file.",
    )
    parser.add_argument(
        "--stakeholder-file",
        help="Optional override for the stakeholder file path.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Render messages and attachments without sending email.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    config_path = Path(args.config).resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    config = load_config(config_path)
    base_folder = config_path.parent
    stakeholder_file = args.stakeholder_file or config.get("stakeholder_file")
    if not stakeholder_file:
        raise ValueError("stakeholder_file must be provided in config or via --stakeholder-file")

    stakeholder_path = Path(stakeholder_file)
    if not stakeholder_path.is_absolute():
        stakeholder_path = (base_folder / stakeholder_path).resolve()

    attachments_folder = config.get("attachments_folder")
    if not attachments_folder:
        raise ValueError("attachments_folder must be provided in config.")
    attachments_path = Path(attachments_folder)
    if not attachments_path.is_absolute():
        attachments_path = (base_folder / attachments_path).resolve()

    email_template_path = config.get("email_template")
    if email_template_path:
        email_template_path = Path(email_template_path)
    else:
        email_template_path = base_folder / "email_template.html"
    if not email_template_path.is_absolute():
        email_template_path = (base_folder / email_template_path).resolve()
    if not email_template_path.exists():
        raise FileNotFoundError(f"Email template not found: {email_template_path}")

    template = load_text_file(email_template_path)
    output_log = config.get("output_log", "../data/logs/send_log.csv")
    output_log_path = Path(output_log)
    if not output_log_path.is_absolute():
        output_log_path = (base_folder / output_log_path).resolve()
    ensure_folder(output_log_path.parent)

    logger = CsvLogger(output_log_path)
    sender = EmailSender(config)

    stakeholders = read_stakeholders(stakeholder_path)
    if not stakeholders:
        print("No valid stakeholder records were found.")
        return

    success_count = 0
    failure_count = 0

    for stakeholder in stakeholders:
        recipient = stakeholder.get("Email")
        application = stakeholder.get("Application", "Unknown")
        subject = render_subject(config.get("email", {}).get("subject", "Data Certification Reminder"), stakeholder)
        html_body = render_email(template, stakeholder)

        attachment_path = None
        try:
            attachment = find_attachment(stakeholder, attachments_path)
            if attachment is not None:
                attachment_path = attachment
            else:
                print(f"Warning: no attachment found for {recipient} ({application})")

            if args.dry_run:
                print(f"DRY RUN: Would send to {recipient} with subject: {subject}")
                print(f"DRY RUN: Attachment: {attachment_path}")
                logger.log(recipient, application, "DryRun", "No message sent")
                success_count += 1
                continue

            sender.send(recipient, subject, html_body, attachment_path=attachment_path)
            logger.log(recipient, application, "Success", "Email sent")
            success_count += 1
            print(f"Sent: {recipient} ({application})")
        except (EmailSendError, Exception) as exc:
            failure_count += 1
            logger.log(recipient, application, "Failed", str(exc))
            print(f"Failed: {recipient} ({application}) - {exc}")

    print("\nSummary:")
    print(f"  Stakeholders processed: {len(stakeholders)}")
    print(f"  Successes: {success_count}")
    print(f"  Failures: {failure_count}")


if __name__ == "__main__":
    main()
