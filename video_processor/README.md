# Rozpoznawanie i przetwarzanie obrazów

## Źródło danych

Źródłem danych może być albo plik video, albo stream z kamery. W celu ujednolicenia interfejsu dostarczenie obu tych rodzajów źródeł odbywa się przez stream `UDP`.

W celu uruchomienia streamu pliku wystarczą komendy:

```sh
cd video_processor

./test/stream.sh PATH/TO/FILE IP_DEST:PORT

# Przykładowe użycie
./test/stream.sh test/videos/test.mp4 127.0.0.1:8444
```

Aby uruchomić stream z kamery RaspberryPi:

```sh
while :; do sudo raspivid -a 12 -t 0 -w 1920 -h 1080 -hf -vf -ih -fps 30 -o udp://IP_DEST:PORT ;done
```
