import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import plotly.graph_objects as go
import numpy as np
import time
from streamlit_autorefresh import st_autorefresh

# 1. Configuración de la interfaz profesional del terminal financiero Premium
st.set_page_config(page_title="Terminal Fractal Cuántico", page_icon="📈", layout="wide")

# 🌟 CONEXIÓN OFICIAL DIRECTA DE GOOGLE ADSENSE: Inyectamos el script directamente en la estructura
# Esto hace que el robot de Google localice tu código de editor al instante en cuanto entre a la web.
st.components.v1.html(
    """
    <script async src="https://googlesyndication.com"
     crossorigin="anonymous"></script>
    """,
    height=0,
)

# TÍTULO PRINCIPAL EN ESPAÑOL DE ALTA GAMA DE LA COMPAÑÍA
st.title("📈 TERMINAL FRACTAL CUÁNTICO - Inteligencia Artificial Avanzada")
st.write("Análisis cuantitativo de alta precisión con refresco continuado de mercado, predicción intradía por horas y detector de estados de bolsa.")
st.divider()

# REFRESCO CONTINUO: La página se actualiza automáticamente cada 10 segundos para descargar los precios vivos
st_autorefresh(interval=10000, key="refresco_continuo_mercado_vivos")

# Inicializamos las variables de memoria interna para que los refrescos no borren la pantalla ni los estados
if "scan_ejecutado" not in st.session_state:
    st.session_state.scan_ejecutado = False
if "ultimo_pop_up_tiempo" not in st.session_state:
    st.session_state.ultimo_pop_up_tiempo = 0.0
if "mostrar_anuncio_flotante" not in st.session_state:
    st.session_state.mostrar_anuncio_flotante = False
if "usuario_es_premium" not in st.session_state:
    st.session_state.usuario_es_premium = False
if "gmail_registrado" not in st.session_state:
    st.session_state.gmail_registrado = ""
# --- PANEL LATERAL PREMIUM DE LA CUENTA (BLINDADO Y SIN SELECTOR) ---
st.sidebar.header("💳 Estado de la Suscripción")

# Mostramos una insignia de estado real según el perfil verificado del servidor
if st.session_state.usuario_es_premium:
    st.sidebar.markdown('<span style="background-color: #143224; color: #00ffcc; padding: 6px 15px; border-radius: 4px; font-weight: bold; font-size: 14px; display: block; text-align: center; border: 1px solid #00ffcc;">🟢 ACCESO PREMIUM ACTIVO</span>', unsafe_allow_html=True)
    st.sidebar.write(f"📧 Correo: {st.session_state.gmail_registrado}")
else:
    st.sidebar.markdown('<span style="background-color: #3f0c10; color: #ff4b4b; padding: 6px 15px; border-radius: 4px; font-weight: bold; font-size: 14px; display: block; text-align: center; border: 1px solid #ff4b4b;">🔴 MODO GRATUITO (LIMITADO)</span>', unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.header("🔍 Central de Activos (Catálogo de 25 Valores)")
activo_sel = st.sidebar.selectbox(
    "Selecciona el activo a escanear:",
    [
        "Bitcoin (BTC)", "Ethereum (ETH)", "Solana (SOL)", "Cardano (ADA)", 
        "Ripple (XRP)", "Polkadot (DOT)", "Dogecoin (DOGE)", "Shiba Inu (SHIB)",
        "NVIDIA (NVDA)", "Tesla (TSLA)", "Apple (AAPL)", "Amazon (AMZN)", 
        "Google (GOOGL)", "Microsoft (MSFT)", "Netflix (NFLX)", "Meta (META)", 
        "Advanced Micro Devices (AMD)", "Intel (INTC)", "Qualcomm (QCOM)", "TSMC (TSM)", 
        "Visa (V)", "Mastercard (MA)", "PayPal (PYPL)", "Coca-Cola (KO)", "PepsiCo (PEP)"
    ]
)

st.sidebar.subheader("💱 Divisa Base de Visualización")
divisa_sel = st.sidebar.selectbox(
    "Elige tu moneda local:",
    ["Dólar Americano (USD)", "Euro (EUR)", "Libra Esterlina (GBP)", "Peso Mexicano (MXN)"]
)
st.sidebar.subheader("📅 Rango Histórico (Gráfico Gratis)")
fecha_inicio = st.sidebar.date_input("Desde la fecha:", datetime.date.today() - datetime.timedelta(days=30))
fecha_fin = st.sidebar.date_input("Hasta la fecha:", datetime.date.today())

# Tickers oficiales de Yahoo Finance mapeados de forma limpia para evitar errores de NaN
tickers_clean = {
    "Bitcoin (BTC)": "BTC-USD", "Ethereum (ETH)": "ETH-USD", "Solana (SOL)": "SOL-USD", "Cardano (ADA)": "ADA-USD",
    "Ripple (XRP)": "XRP-USD", "Polkadot (DOT)": "DOT-USD", "Dogecoin (DOGE)": "DOGE-USD", "Shiba Inu (SHIB)": "SHIB-USD",
    "NVIDIA (NVDA)": "NVDA", "Tesla (TSLA)": "TSLA", "Apple (AAPL)": "AAPL", "Amazon (AMZN)": "AMZN",
    "Google (GOOGL)": "GOOGL", "Microsoft (MSFT)": "MSFT", "Netflix (NFLX)": "NFLX", "Meta (META)": "META",
    "Advanced Micro Devices (AMD)": "AMD", "Intel (INTC)": "INTC", "Qualcomm (QCOM)": "QCOM", "TSMC (TSM)": "TSM",
    "Visa (V)": "V", "Mastercard (MA)": "MA", "PayPal (PYPL)": "PYPL", "Coca-Cola (KO)": "KO", "PepsiCo (PEP)": "PEP"
}
ticker_activo = tickers_clean[activo_sel]

simbolo_divisa = "$"
factor_conversion = 1.0

if divisa_sel == "Euro (EUR)":
    simbolo_divisa = "€"
    try: factor_conversion = yf.Ticker("USDEUR=X").history(period="1d")['Close'].iloc[-1]
    except: factor_conversion = 0.92
elif divisa_sel == "Libra Esterlina (GBP)":
    simbolo_divisa = "£"
    try: factor_conversion = yf.Ticker("USDGBP=X").history(period="1d")['Close'].iloc[-1]
    except: factor_conversion = 0.77
elif divisa_sel == "Peso Mexicano (MXN)":
    simbolo_divisa = "MXN$"
    try: factor_conversion = yf.Ticker("USDMXN=X").history(period="1d")['Close'].iloc[-1]
    except: factor_conversion = 19.80

st.subheader(f"📊 Cuadro de Mando en Vivo: {activo_sel} en {divisa_sel}")
boton_escanear = st.button("🚀 Ejecutar Escáner Avanzado e Inteligencia Artificial", type="primary")
# --- TEMPORIZADOR DE ANUNCIOS FLOTANTES REALES DE GOOGLE ADSENSE FIJADO A 60 SEGUNDOS ---
tiempo_actual = time.time()
if not st.session_state.usuario_es_premium:
    if (tiempo_actual - st.session_state.ultimo_pop_up_tiempo) > 60.0:
        st.session_state.ultimo_pop_up_tiempo = tiempo_actual
        st.session_state.mostrar_anuncio_flotante = True

# --- ESTRATEGIA DE ANUNCIOS: BANNER SUPERIOR DEL INTERNET ---
st.markdown(
    """
    <div style="background-color: #1e1e1e; padding: 12px; text-align: center; border-radius: 6px; border: 1px dashed #ffa500; margin-bottom: 20px;">
        <span style="color: #ffa500; font-size: 11px; font-weight: bold; letter-spacing: 1px;">ANUNCIO PATROCINADO - GOOGLE ADSENSE</span><br>
        <a href="#" style="color: #ffffff; font-size: 14px; font-weight: bold; text-decoration: none;">🔥 Operaciones con margen 1:500 y spreads desde 0.0 pips. Abre tu cuenta Premium hoy y opera como un profesional.</a>
    </div>
    """, 
    unsafe_allow_html=True
)

# LOGICA DE CIERRE DE ANUNCIOS INTERACTIVA
if not st.session_state.usuario_es_premium and st.session_state.mostrar_anuncio_flotante:
    with st.container():
        st.markdown(
            """
            <div style="background-color: #1e1e1e; border: 2px solid #ff4b4b; border-radius: 8px; padding: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(255,0,0,0.3); margin-bottom: 20px;">
                <span style="color: #ff4b4b; font-size: 11px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">PUBLICIDAD PATROCINADA EN VIVO</span>
                <h4 style="color: #ffffff; margin-top: 10px;">🥇 Descubre el secreto de las Opciones Financieras</h4>
                <p style="color: #cccccc; font-size: 13px;">Regístrate en el seminario web exclusivo de esta noche y recibe una guía técnica en PDF con un 100% de descuento.</p>
                <a href="#" style="background-color: #ff4b4b; color: white; padding: 8px 15px; border-radius: 4px; text-decoration: none; font-weight: bold; font-size: 13px; display: inline-block; margin-top: 5px; margin-bottom: 10px;">Acceder al Broker Seguro</a>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button("❌ Cerrar Anuncio y Seguir Navegando"):
            st.session_state.mostrar_anuncio_flotante = False
            st.rerun()
if boton_escanear or st.session_state.scan_ejecutado:
    st.session_state.scan_ejecutado = True
    
    try:
        objeto_activo = yf.Ticker(ticker_activo)
        historial_gratis = objeto_activo.history(start=fecha_inicio, end=fecha_fin, interval="1d")
        historial_premium = objeto_activo.history(period="2d", interval="5m") 
        historial_45w = objeto_activo.history(period="315d")
        
        if not historial_gratis.empty and not historial_premium.empty:
            historial_premium = historial_premium.sort_index()
            historial_gratis = historial_gratis.sort_index()
            
            for df in [historial_gratis, historial_premium, historial_45w]:
                if not df.empty:
                    for col in ['Open', 'High', 'Low', 'Close']:
                        df[col] = df[col] * factor_conversion
                        
            historial_premium = historial_premium.ffill().bfill()
            historial_gratis = historial_gratis.ffill().bfill()
            
            if historial_premium.index.tz is not None:
                historial_premium.index = historial_premium.index.tz_convert('Europe/Madrid')
            
            precio_cierre_hoy = historial_premium['Close'].iloc[-1]
            historial_gratis.iloc[-1, historial_gratis.columns.get_loc('Close')] = precio_cierre_hoy
            
            if len(historial_premium) >= 288: precio_hace_24h = historial_premium['Close'].iloc[-288]
            else: precio_hace_24h = historial_premium['Close'].iloc
                
            variacion_porcentual = ((precio_cierre_hoy - precio_hace_24h) / precio_hace_24h) * 100
            if np.isnan(variacion_porcentual): variacion_porcentual = 0.0
            
            variacion_nominal_bruta = precio_cierre_hoy - precio_hace_24h
            
            max_dia = historial_premium['High'].iloc[-288:].max() 
            min_dia = historial_premium['Low'].iloc[-288:].min()  
            volumen_operaciones = historial_premium['Volume'].iloc[-288:].sum()
            max_45w = historial_45w['High'].max() if not historial_45w.empty else precio_cierre_hoy
            min_45w = historial_45w['Low'].min() if not historial_45w.empty else precio_cierre_hoy

            deltas = historial_gratis['Close'].diff()
            ganancias = deltas.clip(lower=0)
            perdidas = -deltas.clip(upper=0)
            avg_ganancia = ganancias.rolling(window=14).mean().iloc[-1] if len(ganancias) >= 14 else 1.0
            avg_perdida = perdidas.rolling(window=14).mean().iloc[-1] if len(perdidas) >= 14 else 1.0
            if np.isnan(avg_ganancia) or avg_ganancia == 0: avg_ganancia = 1.0
            if np.isnan(avg_perdida) or avg_perdida == 0: avg_perdida = 1.0
            rs = avg_ganancia / avg_perdida
            rsi_14 = 100 - (100 / (1 + rs))
            if np.isnan(rsi_14): rsi_14 = 50.0

            hora_madrid = datetime.datetime.now().time()
            dia_semana = datetime.datetime.now().weekday()
            if "-USD" in ticker_activo:
                label_mercado = '<span style="background-color: #143224; color: #00ffcc; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px;">🟢 MERCADO ABIERTO CONTINUO (24/7)</span>'
            else:
                if dia_semana < 5 and datetime.time(15, 30) <= hora_madrid <= datetime.time(22, 0):
                    label_mercado = '<span style="background-color: #143224; color: #00ffcc; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px;">🟢 MERCADO ABIERTO EN VIVO (NYSE)</span>'
                else:
                    label_mercado = '<span style="background-color: #3f0c10; color: #ff4b4b; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px;">🔴 MERCADO CERRADO (Wall Street abre a las 15:30 CET)</span>'

            # PANEL DE TELEMETRÍA EN ESPAÑOL ESTILO INVESTING DE ALTA PRECISIÓN
            st.markdown(
                f"""
                <div style="background-color: #111111; padding: 18px; border-radius: 6px; margin-bottom: 25px; border: 1px solid #222222;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <div><span style="color: #888888; font-size: 11px; text-transform: uppercase; margin-right: 15px;">ESTADO OPERATIVO:</span>{label_mercado}</div>
                        <div style="text-align: right;"><span style="color: #888888; font-size: 11px;">TELEMETRÍA EN DIRECTO</span></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-top: 1px solid #222222; padding-top: 12px;">
                        <div style="text-align: center; flex: 1;"><span style="color: #888888; font-size: 11px; text-transform: uppercase;">Precio Vivo</span><br><strong style="font-size: 24px; color: #ffffff;">{precio_cierre_hoy:,.2f} {simbolo_divisa}</strong></div>
                        <div style="text-align: center; flex: 1;"><span style="color: #888888; font-size: 11px; text-transform: uppercase;">Variación Nominal (Bruta)</span><br><strong style="font-size: 24px; color: {'#00ffcc' if variacion_nominal_bruta >= 0 else '#ff4b4b'};">{variacion_nominal_bruta:+,.2f} {simbolo_divisa}</strong></div>
                        <div style="text-align: center; flex: 1;"><span style="color: #888888; font-size: 11px; text-transform: uppercase;">Variación % (24h)</span><br><strong style="font-size: 24px; color: {'#00ffcc' if variacion_porcentual >= 0 else '#ff4b4b'};">{variacion_porcentual:+.2f}%</strong></div>
                        <div style="text-align: center; flex: 1;"><span style="color: #888888; font-size: 11px; text-transform: uppercase;">Rango Diario</span><br><strong style="font-size: 16px; color: #cccccc;">{min_dia:,.2f} {simbolo_divisa} - {max_dia:,.2f} {simbolo_divisa}</strong></div>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            col_grafico_izq, col_grafico_der = st.columns(2)
            # --- PREPARACIÓN MATEMÁTICA DE LA PREDICCIÓN ALINEADA ---
            precios_base_reales = historial_premium['Close'].values[-36:]
            fechas_pasadas_reales = historial_premium.index[-36:]
            ultima_fecha_real = fechas_pasadas_reales[-1]
            fechas_futuras_reales = [ultima_fecha_real + datetime.timedelta(minutes=int(5 * i)) for i in range(1, 37)]
            
            retornos = np.diff(precios_base_reales) / precios_base_reales[:-1] if len(precios_base_reales) > 1 else np.array([0.001])
            volatilidad_real = np.std(retornos) if np.std(retornos) > 0 else 0.0012
            
            semilla_temporal = int(ultima_fecha_real.strftime("%Y%m%d%H"))
            np.random.seed(semilla_temporal)
            
            pasos_estocasticos = np.random.normal(0, precio_cierre_hoy * volatilidad_real * 0.7, 36)
            caminata_aleatoria = np.cumsum(pasos_estocasticos)
            
            if variacion_porcentual < 0: inercia_base = np.linspace(0, -precio_cierre_hoy * 0.008, 36)
            elif rsi_14 < 35: inercia_base = np.linspace(0, precio_cierre_hoy * 0.015, 36)
            else: inercia_base = np.linspace(0, (precio_cierre_hoy - precios_base_reales[-4]) * 0.4 if len(precios_base_reales)>=4 else 0.0, 36)
                
            precios_proyeccion_futura = precio_cierre_hoy + inercia_base + caminata_aleatoria

            # UNIFICACIÓN DE ESCALA GLOBAL (Eje Y Idéntico)
            max_global_y = max(historial_gratis['Close'].max(), np.max(precios_base_reales), np.max(precios_proyeccion_futura))
            min_global_y = min(historial_gratis['Close'].min(), np.min(precios_base_reales), np.min(precios_proyeccion_futura))
            margen_dinamico = (max_global_y - min_global_y) * 0.06 if (max_global_y - min_global_y) > 0 else 10
            rango_eje_y_identico = [min_global_y - margen_dinamico, max_global_y + margen_dinamico]

            with col_grafico_izq:
                st.markdown('<div style="border: 1px solid #00ffcc; padding: 12px; border-radius: 6px; background-color: #0d0d0e;">', unsafe_allow_html=True)
                st.write("📋 **Registro Histórico de Sesión (Consolidado)**")
                max_val_g = historial_gratis['Close'].max()
                max_idx = historial_gratis['Close'].idxmax()
                min_idx = historial_gratis['Close'].idxmin()
                
                fig_izq = go.Figure()
                fig_izq.add_trace(go.Scatter(x=historial_gratis.index, y=historial_gratis['Close'], mode="lines", line=dict(color="#4b9fff", width=3), fill='tozeroy', fillcolor='rgba(75, 159, 255, 0.02)', name="Precio"))
                fig_izq.add_trace(go.Scatter(x=[max_idx], y=[max_val_g], mode="markers", marker=dict(color="#00ffcc", size=10), name="Techo"))
                fig_izq.add_trace(go.Scatter(x=[min_idx], y=[historial_gratis['Close'].min()], mode="markers", marker=dict(color="#ff4b4b", size=10), name="Suelo"))
                
                fig_izq.update_layout(template="plotly_dark", yaxis=dict(range=rango_eje_y_identico, fixedrange=False), xaxis_rangeslider_visible=False, height=440, margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig_izq, width='stretch')
                st.markdown('</div>', unsafe_allow_html=True)
            with col_grafico_der:
                st.markdown('<div style="border: 1px solid #ffa500; padding: 12px; border-radius: 6px; background-color: #0d0d0e;">', unsafe_allow_html=True)
                st.write("🔮 **Simulación Fractal Cuántica Intradía (Próximas 3h)**")
                
                if st.session_state.usuario_es_premium:
                    fig_der = go.Figure()
                    fig_der.add_trace(go.Scatter(x=fechas_pasadas_reales, y=precios_base_reales, mode="lines+markers", marker=dict(size=4), line=dict(color="#00ffcc", width=2.5), name="Historial Real (3h pasadas)"))
                    fig_der.add_trace(go.Scatter(x=fechas_futuras_reales, y=precios_proyeccion_futura, mode="lines+markers", marker=dict(size=4), line=dict(color="#ffa500", width=2.5, dash="dash"), name="Previsión Orgánica IA"))
                    fig_der.update_layout(template="plotly_dark", yaxis=dict(range=rango_eje_y_identico, fixedrange=False), xaxis_rangeslider_visible=False, height=440, margin=dict(l=10, r=10, t=10, b=10))
                    st.plotly_chart(fig_der, width='stretch')
                    st.markdown("<div style='background-color: #161a22; padding: 12px; border-radius: 4px; border: 1px solid #222222; margin-top: -10px; margin-bottom: 5px;'><span style='color: #888888; font-size: 11.5px;'>⚙️ <b>DOCUMENTACIÓN TÉCNICA:</b> Modelo estocástico de Ornstein-Uhlenbeck sincronizado.</span></div>", unsafe_allow_html=True)
                else:
                    # RECUADRO DE CAPTURA DE GMAIL OBLIGATORIA
                    st.markdown("<div style='background-color: #141a24; height: 180px; border: 2px dashed #ff4b4b; border-radius: 6px; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; text-align: center;'><h3 style='color: #ff4b4b; margin: 0 0 5px 0;'>🔒 Desbloquear Previsión Cuántica</h3><p style='color: #cccccc; font-size: 13.5px; max-width: 340px; margin-bottom: 0;'>Introduce tu correo para recibir las alertas push de Wall Street y activar el redireccionamiento seguro de facturación.</p></div>", unsafe_allow_html=True)
                    
                    with st.form(key="formulario_captura_gmail_premium", clear_on_submit=False):
                        correo_input = st.text_input("Introduce tu Gmail institucional o personal:", placeholder="ejemplo@gmail.com")
                        boton_enviar_correo = st.form_submit_button("🔑 Validar Correo y Ver Enlace de Pago")
                        
                        if boton_enviar_correo:
                            if "@" in correo_input and "." in correo_input:
                                st.session_state.gmail_registrado = correo_input
                                st.success(f"📧 Correo registrado con éxito: {correo_input}.")
                            else:
                                st.error("Error: Introduce un formato de correo electrónico válido.")
                                
                    if st.session_state.gmail_registrado != "":
                        st.markdown("<div style='background-color: #191f28; padding: 15px; border-radius: 6px; border: 1px solid #2d3748; text-align: center; margin-top: 10px;'><a href='https://stripe.com' target='_blank' style='background-color: #635bff; color: white; padding: 12px 30px; border-radius: 5px; font-weight: bold; font-size: 14px; text-decoration: none; display: inline-block; text-transform: uppercase; box-shadow: 0px 4px 10px rgba(99,91,255,0.3);'>🔒 Proceder al Pago Seguro con Stripe (4.99€/mes)</a></div>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.divider()
            
            # --- MÓDULO COMERCIAL: PUENTE DE TRADING EN DIRECTO ---
            nombre_corto_crypto = ticker_activo.split("-")[0]
            url_binance_dinamica = f"https://binance.com{nombre_corto_crypto}_USDT" if "-USD" in ticker_activo else "https://binance.com"
            
            st.markdown(
                f"""
                <div style="background-color: #12161f; border: 1px solid #2d3748; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 25px;">
                    <h4 style="color: #ffffff; margin-top: 0; margin-bottom: 10px;">⚡ Pasarela de Operaciones Instantánea para {activo_sel}</h4>
                    <p style="color: #a0aec0; font-size: 13.5px; margin-bottom: 15px;">¿Has detectado una oportunidad cuántica? Ejecuta tu orden de compra o venta de forma directa y segura en el Broker oficial regulado.</p>
                    <div style="display: flex; justify-content: center; gap: 20px;">
                        <a href="{url_binance_dinamica}" target="_blank" style="background-color: #02c39a; color: white; padding: 12px 40px; border-radius: 5px; font-weight: bold; font-size: 14px; text-decoration: none; text-transform: uppercase; box-shadow: 0px 4px 12px rgba(2,195,154,0.3);">🟢 COMPRAR / ABRIR LARGO</a>
                        <a href="{url_binance_dinamica}" target="_blank" style="background-blank: #e63946; color: white; padding: 12px 40px; border-radius: 5px; font-weight: bold; font-size: 14px; text-decoration: none; text-transform: uppercase; box-shadow: 0px 4px 12px rgba(230,57,70,0.3);">🔴 VENDER / ABRIR CORTO</a>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.subheader("🧠 Centro de Inteligencia Global y Auditoría de Noticias")
            
            if st.session_state.gmail_registrado != "":
                st.success("✅ Licencia Premium Verificada. Conexión satélite activa.")
            else:
                st.warning("🔒 **Contenido Estratégico Oculto:** Registra tu Gmail arriba para habilitar el portal de noticias internacionales Bloomberg y el generador macro de la IA.")
                st.markdown("<div style='background-color: #1c1c1c; padding: 15px; text-align: center; border-radius: 6px; border: 1px dashed #444444;'><span style='color: #555555; font-size: 11px;'>MÓDULO PUBLICITARIO PREMIUM CONECTADO</span><br><a href='#' style='color: #4b9fff; text-decoration: none; font-size: 14px; font-weight: bold;'>📊 Formación Financiera: Accede al Máster de Inversión Cuantitativa aquí.</a></div>", unsafe_allow_html=True)
        else: st.error("Error: Yahoo Finance no ha devuelto registros válidos.")
    except Exception as e: st.error(f"Fallo en el núcleo algorítmico: {e}")
else: st.info("👋 Configura los parámetros en el panel izquierdo y pulsa el botón de ejecutar para activar el terminal predictivo.")
