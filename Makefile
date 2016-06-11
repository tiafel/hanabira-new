.PHONY: serve test vagrant

serve:
	python ./serve.py confs/development.ini

test:
	PYTHONPATH=.:./extlibs py.test --verbose

vagrant:
	git clone git@git.assembla.com:dobrochan.git
	cp confs/development.ini.template confs/development.ini
	sed -i "/sqlalchemy.url/c\\sqlalchemy.url = mysql+pymysql://$DBUSER:$DBPASSWD@127.0.0.1/$DBNAME?charset=utf8" confs/development.ini
