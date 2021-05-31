## Перемещение папки Docker'a в другое место ##

[[ исходная инструкция ]](https://www.guguweb.com/2019/02/07/how-to-move-docker-data-directory-to-another-location-on-ubuntu/)

По умолчанию она лежит по адресу `/var/lib/docker`

1. Остановить демон Докера: `sudo systemctl stop docker`
2. Создать по адресу `/etc/docker` файл `daemon.json`.

Содержимое файла:

```
{ 
   "data-root": "/ess_data/docker",
   "storage-driver": "devicemapper",
    "storage-opts": [
        "dm.basesize=20G"
    ]
}
```

`data-root` - путь, по которому следует перемесить папку Докера

`basesize` - максимальный размер, который могут занимать образы

3. Если по старому адресу `/var/lib/docker` есть ценная информация - переместить ее по новому адресу, если нет - можно удалить, Докер сам создаст необходимые папки в новом месте.

4. Запустить демон Докера: `sudo systemctl start docker`

## Монтирование папки с одного сервера на другой ##

[[ исходная инструкция ]](http://debian-help.ru/articles/nastroika-nfs-servera-debian/)

[[ исходная инструкция 2 ]](https://www.tecmint.com/how-to-setup-nfs-server-in-linux/)

На обоих серверах необходимо установить инструменты работы с NFS (если еще не стоят, как это сделать - см. интернет).

1. На файловом сервере в файле `/etc/exports` настраиваются папки, которые будут примонтированы на другом сервере. Если требуемая папка вложена в другую, нужно описать их обе, иначе все примонтируется, но будет ошибка `I/O Error`.

```
/ess_data 10.32.1.23(rw,fsid=1,sync,no_subtree_check,no_root_squash) 
/ess_data/first_interview_videos 10.32.1.23(rw,fsid=2,no_subtree_check,sync,no_root_squash)
```

2. Далее нужно применить сделанные изменения командой `exportfs -ra`.

3. На стороне клиента доступные для монтирования папки можно посмотреть командой `showmount -e 10.32.1.21`.

3. Примонтировать нужную директорию командой `mount -t nfs4 10.32.1.21:/ess_data/first_interview_videos /ess_data/mycandidate/first_interview_videos`.

4. Поместить описание монтируемой директории в файл `/etc/fstab`.

```
10.32.1.21:/ess_data/first_interview_videos /ess_data/mycandidate/first_interview_videos nfs rw,sync
```

### Настройка SSH-ключа для подтягивания изменений deployment'a ###

[[ исходная инструкция ]](https://rtfm.co.ua/github-avtorizaciya-po-ssh-klyucham/)

см. инструкцию ↑