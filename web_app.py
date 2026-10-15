import streamlit as st
import requests

# Sayfa Yapılandırması
st.set_page_config(page_title="Hava Durumu Pro", page_icon="🌦️", layout="centered")

# Modern Tasarım ve Kesintisiz Sıralı Giriş Animasyonu için Gelişmiş CSS Kodları
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1 {
        color: #1e293b;
        text-align: center;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #cbd5e1;
        padding: 10px 15px;
        font-size: 16px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
        border-radius: 12px;
        padding: 10px 24px;
        border: none;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.5);
        transform: translateY(-1px);
    }

    /* Kartların ekrana sırayla ve akıcı bir şekilde gelmesini sağlayan animasyon */
    @keyframes slideInUp {
        0% {
            opacity: 0;
            transform: translateY(50px) scale(0.9);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    .animated-card {
        padding: 16px 10px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 6px 15px rgba(0,0,0,0.07);
        height: 100%;
        opacity: 0;
        animation: slideInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        transition: transform 0.3s ease;
    }
    .animated-card:hover {
        transform: translateY(-5px);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌦️ Hava Durumu Asistanı")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 17px; margin-bottom: 30px;'>Anlık hava koşulları ve 5 günlük detaylı tahminler</p>", unsafe_allow_html=True)

# Hava kodu sözlüğü (Duruma göre renk temaları)
hava_kodlari = {
    0: ("Açık", "☀️", "#fffbeb", "#f59e0b"),
    1: ("Çoğunlukla açık", "🌤️", "#f0fdf4", "#22c55e"),
    2: ("Parçalı bulutlu", "⛅", "#f8fafc", "#64748b"),
    3: ("Kapalı", "☁️", "#f1f5f9", "#475569"),
    45: ("Sisli", "🌫️", "#f1f5f9", "#94a3b8"),
    48: ("Sisli", "🌫️", "#f1f5f9", "#94a3b8"),
    51: ("Hafif çise", "🌧️", "#eff6ff", "#3b82f6"),
    53: ("Çise", "🌧️", "#eff6ff", "#3b82f6"),
    55: ("Yoğun çise", "🌧️", "#dbeafe", "#2563eb"),
    61: ("Hafif yağmurlu", "🌦️", "#eff6ff", "#3b82f6"),
    63: ("Yağmurlu", "🌧️", "#dbeafe", "#1d4ed8"),
    65: ("Şiddetli yağmurlu", "⛈️", "#e0e7ff", "#4338ca"),
    71: ("Hafif karlı", "🌨️", "#f8fafc", "#0284c7"),
    73: ("Karlı", "❄️", "#f0fdfa", "#0d9488"),
    75: ("Yoğun karlı", "❄️", "#ccfbf1", "#0f766e"),
    80: ("Hafif sağanak", "🌦️", "#eff6ff", "#3b82f6"),
    81: ("Sağanak", "🌧️", "#dbeafe", "#1d4ed8"),
    82: ("Şiddetli sağanak", "⛈️", "#e0e7ff", "#4338ca"),
    95: ("Gök gürültülü fırtına", "⚡", "#fef2f2", "#dc2626"),
}

# Kullanıcıdan şehir ismi alan web kutusu
sehir = st.text_input("Şehir Ara", placeholder="Örn: Ankara, İzmir, Londra...")

if st.button("Hava Durumunu Göster") or sehir:
    if sehir.strip() == "":
        st.warning("Lütfen bir şehir adı yazın.")
    else:
        try:
            # 1. Geocoding API ile koordinat bulma
            adres = "https://geocoding-api.open-meteo.com/v1/search"
            istek = requests.get(adres, params={"name": sehir, "count": 1, "language": "tr"}, timeout=10)
            veri = istek.json()

            if "results" not in veri:
                st.error("Şehir bulunamadı, ismi doğru yazdığınızdan emin olun.")
            else:
                konum = veri["results"][0]
                enlem = konum["latitude"]
                boylam = konum["longitude"]
                sehir_adi = konum["name"]
                ulke = konum.get("country", "")

                # 2. Hava Durumu API'si
                hava_adresi = "https://api.open-meteo.com/v1/forecast"
                hava_istegi = requests.get(hava_adresi, params={
                    "latitude": enlem,
                    "longitude": boylam,
                    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
                    "daily": "temperature_2m_max,temperature_2m_min,weather_code",
                    "forecast_days": 5,
                    "timezone": "auto"
                }, timeout=10)
                hava = hava_istegi.json()

                simdiki = hava["current"]
                anlik_durum_kod = simdiki.get("weather_code", 0)
                durum_metni, durum_ikonu, _, _ = hava_kodlari.get(anlik_durum_kod, ("Bilinmiyor", "🌈", "#ffffff", "#3b82f6"))

                # Sonuçları Web Arayüzünde Gösterme
                st.markdown(f"<h2 style='color: #0f172a; text-align: center; margin-top: 25px;'>📍 {sehir_adi}, {ulke}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; font-size: 20px; font-weight: 500; color: #334155;'>{durum_ikonu} {durum_metni}</p>", unsafe_allow_html=True)
                
                # Şık metrik kutuları
                col1, col2, col3 = st.columns(3)
                col1.metric("🌡️ Sıcaklık", f"{simdiki['temperature_2m']} °C")
                col2.metric("💧 Nem", f"%{simdiki['relative_humidity_2m']}")
                col3.metric("🌬️ Rüzgar", f"{simdiki['wind_speed_10m']} km/s")

                st.divider()
                st.markdown("### 📅 5 Günlük Sıralı ve Hareketli Tahminler")

                gunluk = hava["daily"]
                tarihler = gunluk["time"]
                en_yuksek = gunluk["temperature_2m_max"]
                en_dusuk = gunluk["temperature_2m_min"]
                kodlar = gunluk["weather_code"]

                gun_kolonlari = st.columns(5)

                for i in range(len(tarihler)):
                    yil, ay, gun = tarihler[i].split("-")
                    tarih_formatli = f"{gun}.{ay}"
                    durum_bilgi, ikon, arka_renk, kenar_renk = hava_kodlari.get(kodlar[i], ("Bilinmiyor", "❓", "#ffffff", "#3b82f6"))
                    
                    # Her karta artan bir gecikme süresi veriyoruz (1. kart hemen, 2. kart biraz sonra, 3. kart daha sonra...)
                    gecikme_suresi = (i + 1) * 0.2  # 0.2s, 0.4s, 0.6s, 0.8s, 1.0s
                    
                    with gun_kolonlari[i]:
                        st.markdown(f"""
                            <div class="animated-card" style="
                                background: {arka_renk}; 
                                border-top: 5px solid {kenar_renk};
                                animation-delay: {gecikme_suresi}s;
                            ">
                                <div style="font-weight: 700; color: #1e293b; margin-bottom: 5px; font-size: 15px;">{tarih_formatli}</div>
                                <div style="font-size: 32px; margin: 12px 0;">{ikon}</div>
                                <div style="font-size: 12px; color: #334155; font-weight: 600; margin-bottom: 12px; min-height: 35px;">{durum_bilgi}</div>
                                <div style="font-size: 13px; color: #64748b; margin-bottom: 2px;">❄️ {en_dusuk[i]}°C</div>
                                <div style="font-size: 13px; color: #e11d48; font-weight: 600;">☀️ {en_yuksek[i]}°C</div>
                            </div>
                        """, unsafe_allow_html=True)

        except requests.exceptions.RequestException:
            st.error("Bağlantı sorunu! İnternet bağlantınızı kontrol edip tekrar deneyin.")