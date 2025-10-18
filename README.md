## Akıllı Hisse Senedi Alım-Satım Botu – Cursor Ready

Modern veri kaynakları, basit strateji ve geri test (backtest), GUI dashboard ve bildirim altyapısıyla uçtan uca bir alım-satım botu iskeleti. Proje, Cursor ortamına hazır olacak şekilde yapılandırılmıştır.

- **Veri Katmanı**: `yfinance` OHLCV, FinBERT duygu skoru (HuggingFace), makro proxy verileri (DXY, Altın, Petrol, EURUSD)
- **Strateji & Backtest**: SMA crossover örnek strateji ve basit performans metrikleri (Sharpe, max drawdown, getiriler)
- **GUI**: Streamlit ile fiyat/sinyal grafikleri ve özet metrikler
- **Broker Yer Tutucular**: Alpaca ve IB için temel sınıflar
- **Bildirimler**: Telegram ve Discord bildirim yardımcıları

---

## Hızlı Başlangıç

### Gereksinimler
- Python 3.10+
- Linux/macOS/WSL önerilir

### Kurulum
```bash
# (Opsiyonel) Sanal ortam
python3 -m venv .venv
source .venv/bin/activate

# Bağımlılıkların kurulumu (editable mod)
pip install -U pip
pip install -e .

# Örnek .env dosyasını kopyalayın
cp .env.example .env
# .env içindeki anahtarları (örn. Alpaca, Telegram) doldurun
```

### Ortam Değişkenleri
`.env.example` dosyasına bakın. Önemli anahtarlar:
- **ALPACA_API_KEY**, **ALPACA_API_SECRET**, **ALPACA_PAPER_BASE_URL**
- **IB_GATEWAY_HOST**, **IB_GATEWAY_PORT**
- **TELEGRAM_BOT_TOKEN**, **TELEGRAM_CHAT_ID**

Not: GUI/CLI için zorunlu değildir; broker/bildirim özellikleri için gereklidir.

---

## Kullanım
Komutlar için iki seçenekten birini kullanabilirsiniz:
- `trader-bot` komutu (PATH’te ise)
- veya `python3 -m trader_bot.cli`

### Yardım
```bash
python3 -m trader_bot.cli --help
```

### OHLCV Verisi Çekme (yfinance)
```bash
python3 -m trader_bot.cli fetch AAPL -i 1m --period 7d
# CSV kaydetmek için:
python3 -m trader_bot.cli fetch AAPL -i 1m --period 7d --csv data/aapl_1m.csv
```

### SMA Stratejisi ile Backtest
```bash
python3 -m trader_bot.cli backtest AAPL -i 1m --period 7d --fast 10 --slow 30
```

### GUI Dashboard
```bash
# Gömülü komut
python3 -m trader_bot.cli gui

# Alternatif olarak doğrudan Streamlit ile
streamlit run -m trader_bot.gui.app
```

---

## Mimari Genel Bakış

### Veri Katmanı (Data Layer)
- **Piyasalar**: `trader_bot/data/providers/yf.py` – `fetch_ohlcv` ile OHLCV (timestamp, open, high, low, close, volume)
- **Duygu Analizi**: `trader_bot/data/sentiment/finbert.py` – HuggingFace ProsusAI/FinBERT ile metin duygu skoru
- **Makro Proxy**: `trader_bot/data/macro/market_proxies.py` – DXY, Altın, Petrol, EURUSD gibi semboller

### Tahmin ve AI Katmanı
- Örnek strateji SMA üzerinedir (`trader_bot/strategy/sma.py`).
- TFT/GNN/RL gibi ileri modeller için yerleşim alanları mevcuttur (`trader_bot/models/`).
- Açıklanabilirlik (SHAP/LIME) ve anomali tespiti ileride eklenebilir.

### Trade ve Risk Yönetimi
- **Backtest**: `trader_bot/backtest/core.py` – basit performans metrikleri ve equity curve hesaplama
- **Broker Yer Tutucuları**: `trader_bot/execution/alpaca.py`, `trader_bot/execution/ib.py`
- Risk-temelli pozisyon boyutlandırma, stop-loss/take-profit otomasyonu geliştirilebilir.

### GUI & Dashboard
- `trader_bot/gui/app.py` – Streamlit tabanlı etkileşimli grafikler (candlestick + SMA, al/sat işaretleri) ve özet metrikler

### Bildirimler
- **Telegram**: `trader_bot/notify/telegram.py`
- **Discord**: `trader_bot/notify/discord.py`

---

## Klasör Yapısı
```text
src/trader_bot/
  ├─ data/
  │   ├─ providers/        # yfinance vb.
  │   ├─ sentiment/        # FinBERT vb.
  │   └─ macro/            # makro proxy verileri
  ├─ features/             # göstergeler (SMA vb.)
  ├─ strategy/             # strateji tanımları
  ├─ backtest/             # backtest çekirdeği
  ├─ execution/            # broker entegrasyonları (Alpaca/IB placeholder)
  ├─ notify/               # Telegram/Discord yardımcıları
  ├─ gui/                  # Streamlit dashboard
  ├─ config.py             # Pydantic Settings tabanlı konfigürasyon
  └─ logging_config.py     # JSON/insan okunur log formatları
```

---

## Yol Haritası
- **Gerçek zamanlı/tick-level** veri akışı ve kayıt
- **Gelişmiş modeller**: TFT, GNN, RL ile strateji optimizasyonu
- **Açıklanabilirlik**: SHAP/LIME entegrasyonları
- **Anomali tespiti** ve uyarı mekanizmaları (Discord/Telegram/e-posta)
- **Portföy optimizasyonu**: Markowitz + Risk AI katmanı
- **Data replay & backtest** iyileştirmeleri, çok ufuklu tahminler (1m/5m/1h)
- **Canlı trade**: Alpaca/IB üzerinden otomasyon ve risk kontrolleri

---

## Geliştirme
- Kod giriş noktası (CLI): `trader_bot/cli.py`
- Kurulum sonrası `trader-bot` komutu oluşur; PATH’te yoksa `python3 -m trader_bot.cli` kullanın.
- Loglar JSON veya klasik formatta üretilebilir (`--json-logs`).

---

## Uyarı (Sorumluluk Reddi)
Bu proje yalnızca eğitim ve deneme amaçlıdır. Buradaki hiçbir bilgi yatırım tavsiyesi değildir. Finansal piyasalarda işlem yapmak yüksek risk içerir. Tüm kararlar ve sonuçlar kullanıcıya aittir.

---

## Lisans
Bu proje **MIT** lisansı ile lisanslanmıştır. Ayrıntılar için `LICENSE` dosyasına bakın.
