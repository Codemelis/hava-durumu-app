
import requests

hava_kodlari = {
    0: "Açık",
    1: "Çoğunlukla açık",
    2: "Parçalı bulutlu",
    3: "Kapalı",
    45: "Sisli",
    48: "Sisli",
    51: "Hafif çise",
    53: "Çise",
    55: "Yoğun çise",
    61: "Hafif yağmurlu",
    63: "Yağmurlu",
    65: "Şiddetli yağmurlu",
    71: "Hafif karlı",
    73: "Karlı",
    75: "Yoğun karlı",
    80: "Hafif sağanak",
    81: "Sağanak",
    82: "Şiddetli sağanak",
    95: "Gök gürültülü fırtına",
}

while True:
    sehir = input("\nHangi şehrin hava durumunu öğrenmek istersiniz? (Çıkmak için q yazın) ")

    if sehir.strip().lower() == "q":
        print("Görüşmek üzere!")
        break

    if sehir.strip() == "":
        print("Lütfen bir şehir adı yazın.")
        continue

    try:
        adres = "https://geocoding-api.open-meteo.com/v1/search"
        istek = requests.get(adres, params={"name": sehir, "count": 1, "language": "tr"}, timeout=10)
        veri = istek.json()

        if "results" not in veri:
            print("Şehir bulunamadı, ismi doğru yazdığınızdan emin olun.")
            continue

        konum = veri["results"][0]
        enlem = konum["latitude"]
        boylam = konum["longitude"]
        sehir_adi = konum["name"]

        hava_adresi = "https://api.open-meteo.com/v1/forecast"
        hava_istegi = requests.get(hava_adresi, params={
            "latitude": enlem,
            "longitude": boylam,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,weather_code",
            "forecast_days": 5,
            "timezone": "auto"
        }, timeout=10)
        hava = hava_istegi.json()

    except requests.exceptions.RequestException:
        print("Bağlantı sorunu! İnternet bağlantınızı kontrol edip tekrar deneyin.")
        continue

    simdiki = hava["current"]

    print()
    print(f"--- {sehir_adi} Hava Durumu ---")
    print(f"Sıcaklık: {simdiki['temperature_2m']} °C")
    print(f"Nem: %{simdiki['relative_humidity_2m']}")
    print(f"Rüzgar: {simdiki['wind_speed_10m']} km/s")

    gunluk = hava["daily"]
    tarihler = gunluk["time"]
    en_yuksek = gunluk["temperature_2m_max"]
    en_dusuk = gunluk["temperature_2m_min"]
    kodlar = gunluk["weather_code"]

    print()
    print("5 Günlük Tahmin (en düşük / en yüksek):")

    for i in range(len(tarihler)):
        yil, ay, gun = tarihler[i].split("-")
        durum = hava_kodlari.get(kodlar[i], "Bilinmiyor")
        print(f"  {gun}.{ay}.{yil}:  {en_dusuk[i]}° / {en_yuksek[i]}°C  -  {durum}")