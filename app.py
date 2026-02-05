import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Gelişmiş Yatırım Asistanı", layout="wide")

# --- BAŞLIK ---
st.title("🚀 Akıllı Yatırım ve Optimizasyon Asistanı")
st.markdown("""
Bu sistem, **gelişmiş algoritmasıyla** yaşınıza ve vadenize göre risk toleransınızı milimetrik hesaplar.
*Orta ve Uzun vade arasındaki strateji farkını net bir şekilde görebilirsiniz.*
""")

# --- YAN MENÜ (KULLANICI GİRDİLERİ) ---
st.sidebar.header("Yatırımcı Profili")
butce = st.sidebar.number_input("Yatırım Bütçeniz (TL)", min_value=1000, value=100000, step=1000)
yas = st.sidebar.slider("Yaşınız", 18, 80, 25)
vade_secimi = st.sidebar.selectbox(
    "Vade Tercihi", 
    ["Kısa Vade (0-1 Yıl)", "Orta Vade (1-3 Yıl)", "Uzun Vade (3+ Yıl)"]
)

# --- HESAPLAMA MANTIĞI (Geliştirilmiş Versiyon) ---
def hesapla(butce, yas, vade_text):
    # 1. Değişkenleri Ayarla
    vade_kodu = ""
    yil_sayisi = 1
    
    if "Uzun" in vade_text:
        vade_kodu = "uzun"
        yil_sayisi = 5  # 5 Yıllık Projeksiyon
    elif "Orta" in vade_text:
        vade_kodu = "orta"
        yil_sayisi = 3  # 3 Yıllık Projeksiyon
    else:
        vade_kodu = "kisa"
        yil_sayisi = 1  # 1 Yıllık

    # 2. Risk Puanı Hesapla
    risk_puani = 0
    
    # Yaş Puanı
    if yas < 30: risk_puani = 50
    elif yas < 50: risk_puani = 30
    else: risk_puani = 10
    
    # Vade Puanı (Fark yaratmak için aralıkları açtık)
    if vade_kodu == 'uzun': risk_puani += 45
    elif vade_kodu == 'orta': risk_puani += 20
    else: risk_puani += 0

    # 3. Profil ve Sepet Belirleme (4 Kademeli)
    dagilim = {}
    profil_adi = ""
    renk_temasi = ""

    if risk_puani >= 80:
        profil_adi = "🔥 Çok Yüksek Risk (Agresif Büyüme)"
        renk_temasi = "red"
        dagilim = {'Bitcoin': 30, 'Borsa': 45, 'Altın': 5, 'Gümüş': 5, 'Dolar': 5, 'Tahvil': 10}
        
    elif risk_puani >= 60:
        profil_adi = "🚀 Yüksek Risk (Büyüme Odaklı)"
        renk_temasi = "orange"
        dagilim = {'Bitcoin': 15, 'Borsa': 40, 'Altın': 15, 'Gümüş': 10, 'Dolar': 10, 'Tahvil': 10}
        
    elif risk_puani >= 40:
        profil_adi = "⚖️ Dengeli (Orta Risk)"
        renk_temasi = "blue"
        dagilim = {'Bitcoin': 5, 'Borsa': 25, 'Altın': 30, 'Gümüş': 10, 'Dolar': 15, 'Tahvil': 15}
        
    else:
        profil_adi = "🛡️ Düşük Risk (Koruma Odaklı)"
        renk_temasi = "green"
        dagilim = {'Bitcoin': 0, 'Borsa': 10, 'Altın': 40, 'Gümüş': 5, 'Dolar': 20, 'Tahvil': 25}

    # 4. Getiri Hesabı
    # Yıllık ortalama getiri varsayımları
    oranlar = {'Bitcoin': 0.60, 'Borsa': 0.35, 'Altın': 0.25, 'Gümüş': 0.20, 'Dolar': 0.15, 'Tahvil': 0.10}
    
    veri_listesi = []
    toplam_kar = 0

    for varlik, yuzde in dagilim.items():
        if yuzde > 0:
            ana_para = butce * (yuzde / 100)
            # Formül: Ana Para * Yıllık Oran * Yıl
            kazanc = ana_para * oranlar[varlik] * yil_sayisi
            toplam_kar += kazanc
            
            veri_listesi.append({
                "Varlık": varlik,
                "Oran (%)": yuzde,
                "Yatırılan Tutar": ana_para,
                "Vade Sonu Kazanç": kazanc,
                "Yıllık Oran": oranlar[varlik]
            })
            
    return pd.DataFrame(veri_listesi), toplam_kar, profil_adi, yil_sayisi

# --- SİTE İÇERİĞİ ---

# Hesaplamayı yap
df, kar, profil, yil = hesapla(butce, yas, vade_secimi)

# 1. Üst Özet Kartları
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"**Yatırımcı Profili:**\n\n{profil}")
with col2:
    st.warning(f"**Hesaplanan Süre:**\n\n{yil} Yıl Boyunca")
with col3:
    st.success(f"**Vade Sonu Tahmini Net Kâr:**\n\n+{kar:,.2f} ₺")

st.divider()

# 2. Grafik ve Tablo Düzeni
col_sol, col_sag = st.columns([4, 5])

with col_sol:
    st.subheader("Portföy Dağılımı")
    
    # Pasta Grafiği
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = ['#f7931a', '#3498db', '#f1c40f', '#bdc3c7', '#2ecc71', '#95a5a6']
    
    ax.pie(df['Oran (%)'], labels=df['Varlık'], autopct='%1.1f%%', 
           startangle=140, colors=colors, textprops={'fontsize': 12})
    ax.set_title(f"{profil}", fontsize=10)
    st.pyplot(fig)

with col_sag:
    st.subheader(f"Detaylı Analiz ({yil} Yıllık)")
    
    # Tabloyu biçimlendirme
    st.dataframe(
        df.style.format({
            "Yatırılan Tutar": "{:,.2f} ₺",
            "Vade Sonu Kazanç": "{:,.2f} ₺",
            "Oran (%)": "%{}",
            "Yıllık Oran": "%{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Toplam Bakiye Gösterimi
    toplam_bakiye = butce + kar
    st.metric(label="Vade Sonu Toplam Cüzdan Bakiyesi", value=f"{toplam_bakiye:,.2f} ₺", delta=f"%{(kar/butce)*100:.1f} Büyüme")

# --- Alt Bilgi ---
st.markdown("---")
st.caption("Not: Kâr oranları geçmiş performans simülasyonlarına dayanır. Gerçek piyasada garanti edilmez.")