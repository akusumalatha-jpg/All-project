from pathlib import Path


def find_attachment(stakeholder, attachments_folder):
    folder = Path(attachments_folder)
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Attachments folder not found: {attachments_folder}")

    application = str(stakeholder.get("Application", "")).strip()
    preferred_extensions = [".pdf", ".docx", ".xlsx", ".txt", ".html"]

    if application:
        for extension in preferred_extensions:
            candidate = folder / f"{application}{extension}"
            if candidate.exists() and candidate.is_file():
                return candidate

        lower_app = application.lower()
        for candidate in folder.iterdir():
            if not candidate.is_file():
                continue
            if lower_app in candidate.stem.lower():
                return candidate

    attachments = [item for item in folder.iterdir() if item.is_file()]
    if not attachments:
        return None

    return max(attachments, key=lambda path: path.stat().st_mtime)


def read_attachment_bytes(path):
    path = Path(path)
    with path.open("rb") as handle:
        return handle.read()
