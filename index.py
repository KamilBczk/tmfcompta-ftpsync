# ************************************************************************** #
#                                                                            #
#   index.py                                                                 #
#                                                                            #
#   By: kamil.biczyk <kamil.biczyk@kago-group.com>                           #
#                                                                            #
#   Created: 16/06/2024 22:41:31 by kamil.biczyk                             #
#   Updated: 16/06/2024 23:48:55 by kamil.biczyk                             #
#                                                                            #
# ************************************************************************** #

import os
import paramiko
from stat import S_ISDIR
import shutil

sftp_host = 'ftp.app.codabox.com'
sftp_port = 22
sftp_username = '*****'
sftp_password = '*****'
sftp_directory = '/home'
local_directory = './destination_directory'

def connect_sftp(host, port, username, password):
    print("Se connecter au serveur SFTP")
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp

def download_directory(sftp, remote_dir, local_dir):
    try:
        os.makedirs(local_dir, exist_ok=True)
        items = sftp.listdir_attr(remote_dir)
        for item in items:
            remote_path = os.path.join(remote_dir, item.filename).replace('\\', '/')
            local_path = os.path.join(local_dir, item.filename)
            
            if S_ISDIR(item.st_mode):
                download_directory(sftp, remote_path, local_path)
            else:
                sftp.get(remote_path, local_path)
                print(f'Téléchargé: {remote_path} à {local_path}')

    except IOError as e:
        print(f"Erreur d'accès au répertoire {remote_dir}: {e}")

def clear_directory(local_dir):
    """ Supprime tous les fichiers et dossiers dans le répertoire spécifié. """
    if os.path.exists(local_dir):
        shutil.rmtree(local_dir)
        print(f"Tout contenu a été supprimé de {local_dir}")
        os.makedirs(local_dir, exist_ok=True)

def main():
    print("Nettoyage du dossier local avant téléchargement.")
    clear_directory(local_directory)

    sftp = connect_sftp(sftp_host, sftp_port, sftp_username, sftp_password)
    try:
        download_directory(sftp, sftp_directory, local_directory)
    finally:
        sftp.close()
        print('Déconnexion du serveur SFTP.')

if __name__ == '__main__':
    main()
