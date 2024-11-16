import os


class S3Sync:
    """
    This class provides methods to synchronize folders and files with an AWS S3 bucket.
    It uses the AWS CLI to perform the synchronization operations.
    """

    def sync_folder_to_s3(self, folder, aws_bucket_url):

        command = f"aws s3 sync {folder} {aws_bucket_url} "
        os.system(command)

    def sync_file_from_s3(self, folder, aws_bucket_url):

        command = f"aws s3 sync {aws_bucket_url} {folder} "
        os.system(command)
