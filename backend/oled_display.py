# oled_display.py
from typing import Optional
import time
from pathlib import Path

# Tentativa de importar luma (Raspberry Pi). Se não disponível, usamos fallback simulado.
try:
    from luma.core.interface.serial import i2c, spi
    from luma.oled.device import ssd1306
    LUMA_AVAILABLE = True
except Exception:
    LUMA_AVAILABLE = False

# Para TCA9548A via smbus2
try:
    from smbus2 import SMBus
    SMBUS_AVAILABLE = True
except Exception:
    SMBUS_AVAILABLE = False

TCA_ADDR = 0x70

class OLEDController:
    """
    Abstrai o display e o TCA9548A. Em Raspberry: usa luma + smbus2 quando disponíveis.
    Em Windows/dev: modo simulado (apenas prints).
    """
    def __init__(self, width: int = 128, height: int = 64, oled_addr: int = 0x3C, i2c_bus: int = 1):
        self.width = width
        self.height = height
        self.oled_addr = oled_addr
        self.i2c_bus_num = i2c_bus
        self.device = None
        self._bus = None

        if LUMA_AVAILABLE and SMBUS_AVAILABLE:
            try:
                self._bus = SMBus(self.i2c_bus_num)
                serial = i2c(port=self.i2c_bus_num, address=self.oled_addr)
                self.device = ssd1306(serial, width=self.width, height=self.height)
                print("[OLED] luma.ssd1306 initialized")
            except Exception as e:
                print(f"[OLED] falha ao inicializar luma/smbus: {e}; entrando em modo simulado.")
                self.device = None
        else:
            print("[OLED] luma or smbus not available -> simulation mode")

    def tca_select(self, channel: int):
        if not (0 <= channel <= 7):
            raise ValueError("Canal TCA9548A deve ser 0..7")
        mask = 1 << channel
        if self._bus is not None:
            # escreve máscara no endereço do TCA
            try:
                self._bus.write_byte(TCA_ADDR, mask)
            except Exception as e:
                print(f"[OLED] Erro ao selecionar canal TCA via SMBus: {e}")
        else:
            print(f"[SIM] TCA select canal {channel} (mask=0x{mask:02X})")

    def render_item(self, channel: int, nome: str, preco_str: str, notice: Optional[str] = None, notice_ms: int = 1000):
        """
        Renderiza simples: título canal, nome (até 2 linhas), preço e opcional notice.
        """
        self.tca_select(channel)
        if self.device:
            # Limpa e desenha texto simples (luma usa PIL)
            from PIL import Image, ImageDraw, ImageFont
            image = Image.new('1', (self.width, self.height))
            draw = ImageDraw.Draw(image)
            # Fonte default
            try:
                font = ImageFont.load_default()
            except Exception:
                font = None
            draw.text((0, 0), f"Canal {channel}", font=font, fill=255)
            # Nome em duas linhas
            nome = nome.strip()
            draw.text((0, 12), nome[:16], font=font, fill=255)
            if len(nome) > 16:
                draw.text((0, 22), nome[16:32], font=font, fill=255)
            draw.text((0, 38), preco_str, font=font, fill=255)
            if notice:
                draw.text((0, 54), notice[:20], font=font, fill=255)
            self.device.display(image)
            if notice:
                time.sleep(notice_ms/1000.0)
                # re-render without notice
                self.render_item(channel, nome, preco_str, notice=None)
        else:
            # Simulação textual
            print(f"[SIM OLED] Canal {channel} | {nome} | {preco_str}")
            if notice:
                print(f"[SIM OLED] NOTICE: {notice}")
