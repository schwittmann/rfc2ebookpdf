docker build -t rfc2pdf . && docker run -v `pwd`/PDF-out:/PDF-out -v `pwd`/RFC-all:/RFC-all --rm rfc2pdf /RFC-all /PDF-out fonts/Hack-Bold.ttf 12 21 False

