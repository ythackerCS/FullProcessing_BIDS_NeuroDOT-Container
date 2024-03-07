cp Dockerfile.base Dockerfile && \
./command2label.py ./xnat/command.json >> Dockerfile && \
docker build --no-cache -t xnat/preprocessingneurodot_bids:latest .
docker tag xnat/preprocessingneurodot_bids:latest registry.nrg.wustl.edu/docker/nrg-repo/yash/preprocessingneurodot_bids:latest
rm Dockerfile