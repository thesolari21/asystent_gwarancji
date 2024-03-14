# Asystent gwarancji

## Spis treści / Table of contents
* [General info / Informacje o aplikacji](#general-info)
* [Screens / Zrzuty ekranu](#screens)
* [Specs / Technikalia](#specs)
* [Status](#status)
* [Changelog / Lista zmian](#changelog)


## General info
[PL]

Aplikacja w Django służąca do zarządzania gwarancjami na sprzęt. Pomysł zrodził się z racji notorycznego bałaganu autora, który zawsze gdzieś zapodzieje dowód zakupu.
Jest to tym bardziej irytujące jak właśnie sprzęt się popsuje :)

W skrócie:
* Osoba uprawniona (z odpowiednią grupą) loguje się do systemu.
* Wypełnia krótki formularz i załącza zdjęcie.
* Dane są bezpiecznie przechowywane w aplikacji. W razie zgubienia fizycznego paragonu (lub jego wyblaknięcia) mamy dowód w postaci cyfrowej.
* Co pewien okres czasu uruchamiany jest skrypt, który sprawdza czy któraś z gwarancji nie wygasa. Jeśli tak jest, informuje o tym mailowo użytkownika.


[EN]

Soon
	
## Screens

Main

![](https://i.ibb.co/q5sZx72/main.png)

Not log in

![](https://i.ibb.co/Pzk4V5p/login.png)



## To Do
* Dodanie wyszukiwania konkretnej gwarancji
* Rozszerzenie aplikacji na większą liczbę użytkowników (tak aby każdy widział tylko swoje paragony)
* OCR - automatyczne uzupełnianie danych na podstawie zdjęcia pragonu/faktury
* Dodanie statystyk

	
## Specs
* 1 tabela - Receipt.
* Pole Status:
  * 0 - nieaktywne (paragon nie wyświetli się użytkownikowi)
  * 1 - aktywne (domyślnie)
* Do załączania zdjęcia użyty dodatek Django Resized: https://github.com/un1t/django-resized. Domyślnie
pliki trafiają do katalogu /asystent_gwarancji/static/media/
* W main user widzi wszystkie paragony z statusem 1, bez względu czy minąła gwarancja czy nie.
* Aby uzyskać dostęp do aplikacji, SU musi dodać user do odpowiedniej grupy (ag).

## Status
Pre-produkcja

## Changelog
# 1.0
* Działająca aplikacja
