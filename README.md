## Description
`rename_photos.py` is a script developed to help organize family photos efficiently. It renames photo files based on metadata attributes and removes duplicate photos. After executing the 'rename_photos.py" script, all photo files will be organized by date. Aftewards, when photos are sorted by name they will be sorted by date as well.

## Current Functionality
- Renames photo files leveraging metadata attributes.
- Handles exceptions for some photos lacking metadata.
- Identifies and removes duplicate photos.

## Future Functionality
- Integration with Dropbox API for cloud-based organization.
- Enhanced modularization for easier expansion.
- Scheduled daily operations using AWS Lambda.
- E-mail reporting for renaming and photo removal.
- Subfolder for photos to be removed.
