#/bin/bash
docker save moorelab/aliro_dbmongo | gzip > /aliroed/images/aliro_dbmongo.tar.gz
docker save moorelab/aliro_lab | gzip > /aliroed/images/aliro_lab.tar.gz
docker save moorelab/aliro_machine | gzip > /aliroed/images/aliro_machine.tar.gz
