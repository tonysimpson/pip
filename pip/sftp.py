import os
try:
    import paramiko

    def sftp_download_package(url, target_dir, ssh_keys=None):
        username, hostname, path = split_url(url)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, username=username, key_filename=ssh_keys)
        sftp_client = ssh_client.open_sftp()
        target_file = os.path.join(target_dir, url.rsplit('/',1)[-1])
        sftp_client.get(path, target_file)
        sftp_client.close()
        ssh_client.close()
        return target_file

    def sftp_find_package(url, starts_with, ssh_keys=None):
        username, hostname, path = split_url(url)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, username=username, key_filename=ssh_keys)
        sftp_client = ssh_client.open_sftp()
        for filename in sftp_client.listdir(path):
            if filename.lower().startswith(starts_with):
                print url + '/' + filename
                yield url + '/' + filename
        sftp_client.close()
        ssh_client.close()

    def split_url(url):
        _  = url.split('sftp://')[-1]
        username=None
        if '@' in url:
            username, _ = _.split('@')
        hostname, path = _.split(':',1)
        return username, hostname, path
except ImportError:
    def sftp_download_package(*args, **kwargs):
        raise ImportError('paramiko needed for sftp support')

    def sftp_find_package(*args, **kwargs):
        raise ImportError('paramiko needed for sftp support')

__all__ = ['sftp_download_package', 'sftp_find_package']
