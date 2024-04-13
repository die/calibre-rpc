install:
	@if exist "calibre" ( \
		echo Updating from source... && \
		cd calibre && \
		git fetch https://github.com/kovidgoyal/calibre.git \
	) else ( \
		echo Couldn't find calibre source code, fetching source... && \
		git clone https://github.com/kovidgoyal/calibre.git \
	)

compile:
	calibre-debug -s
	calibre-customize -b .
	calibre-debug -g

zip:
	git ls-files | tar -a -c -f release/calibre-rpc.zip -T -
