stylus:=$(shell npm bin)/stylus --use kouto-swiss
#stylus:=$(shell npm bin)/stylus --compress --sourcemap-inline --use kouto-swiss

stylus:=$(shell npm bin)/stylus

CSS=hanabira/public/css/

serve:
	python ./serve.py confs/development.ini

css: #styles/*.styl
	#$(stylus) < styles/x.styl > x.css

	$(stylus) < styles/bluemoon.styl     > ${CSS}bluemoon.css
	#$(stylus) < styles/burichan.styl     > ${CSS}burichan.css
	$(stylus) < styles/common.styl       > ${CSS}common.css
	$(stylus) < styles/common.mini.styl  > ${CSS}common.mini.css
	$(stylus) < styles/futaba.styl       > ${CSS}futaba.css
	$(stylus) < styles/gurochan.styl     > ${CSS}gurochan.css
	$(stylus) < styles/highlight.styl    > ${CSS}highlight.css
	$(stylus) < styles/jcrop.styl        > ${CSS}jcrop.css
	$(stylus) < styles/kusaba.styl       > ${CSS}kusaba.css
	$(stylus) < styles/photon_blue.styl  > ${CSS}photon_blue.css
	$(stylus) < styles/photon.styl       > ${CSS}photon.css
	$(stylus) < styles/snow.styl         > ${CSS}snow.css
	$(stylus) < styles/snow_static.styl  > ${CSS}snow_static.css
	$(stylus) < styles/std_gray.styl     > ${CSS}std_gray.css
	#$(stylus) < styles/photon_green.styl > ${CSS}photon_green.css

vagrant:
	git clone git@git.assembla.com:dobrochan.git
	cp confs/development.ini.template confs/development.ini
	sed -i "/sqlalchemy.url/c\\sqlalchemy.url = mysql+pymysql://$DBUSER:$DBPASSWD@127.0.0.1/$DBNAME?charset=utf8" confs/development.ini
