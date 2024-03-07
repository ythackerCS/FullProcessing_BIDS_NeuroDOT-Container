cp Dockerfile.base Dockerfile && \
./command2label.py ./xnat/command.json >> Dockerfile && \
docker build --no-cache -t xnat/fullprocessingneurodot_bids:latest .
docker tag xnat/fullprocessingneurodot_bids:latest registry.nrg.wustl.edu/docker/nrg-repo/yash/fullprocessingneurodot_bids:latest
rm Dockerfile