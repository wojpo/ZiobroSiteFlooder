# Flooder testnr.org – projekt edukacyjny

> ⚠️ **Uwaga:** Ten projekt ma charakter **czysto edukacyjny** i nie powinien być używany do nielegalnych działań ani w celach szkodliwych.

## 📄 Opis

[testnr.org](https://testnr.org) to strona służąca do walidacji numerów zaświadczeń wyborczych. Umożliwia sprawdzenie, czy dane zaświadczenie zostało użyte wielokrotnie. **Nie jest to oficjalne narzędzie państwowe.**

Serwis był niewłaściwie promowany przez Zbigniewa Ziobrę, byłego ministra sprawiedliwości, jako rzeczywiste narzędzie przeznaczone dla komisji wyborczych — co jest nieprawdą i mogło wprowadzać opinię publiczną w błąd.

## 🎯 Cel projektu

Projekt pokazuje:

- jak wygląda komunikacja z API testnr.org,
- jak błędy w implementacji backendu (np. CAPTCHA przesyłana w nagłówkach HTTP) mogą prowadzić do nadużyć,
- jak zautomatyzować interakcję z niedostatecznie zabezpieczonymi usługami.

## ⚙️ Funkcjonalności

- 🔢 Generowanie losowych numerów zaświadczeń oraz numerów telefonów
- 🔐 Pobieranie kodów CAPTCHA z serwera testnr.org
- ✅ Walidacja numerów zaświadczeń z wykorzystaniem otrzymanych kodów CAPTCHA
- 🪵 Szczegółowe logowanie wszystkich operacji (żądania, odpowiedzi, błędy itd.)

## 🧠 Opis działania

1. Skrypt wysyła żądanie o wygenerowanie CAPTCHA.
2. Serwer zwraca kod CAPTCHA **w nagłówkach HTTP** – co stanowi poważną lukę bezpieczeństwa.
3. Skrypt wykorzystuje ten kod do automatycznego sprawdzania numerów.
4. Wszystkie działania są logowane do pliku/logu w konsoli.

## ⚖️ Zastrzeżenia

- Projekt służy **wyłącznie celom edukacyjnym**.
- Nie należy wykorzystywać go do działań niezgodnych z prawem ani do zakłócania działania serwisów internetowych.
- Autorzy nie ponoszą odpowiedzialności za nielegalne, nieetyczne ani szkodliwe wykorzystanie kodu.
