clean:
	find . -name *.pyc |xargs rm
	find . -name *.log |xargs rm
	find . -name *.tar.gz |xargs rm
build:
	git checkout master && git pull
	cd ../ && tar cvzf alice-music/alice-music.tar.gz alice-music/*
upload:
	scp alice-music.tar.gz congying@bj0.wei-ming.me:~/project
.pony:
	clean
