import os
from fpdf import FPDF

# Ensure output directory exists
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_invoice():
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("DejaVu", "", "/System/Library/Fonts/Supplemental/Arial.ttf", uni=True)
    try:
        pdf.set_font("DejaVu", "", 12)
    except:
        pdf.set_font("Arial", "", 12)
        
    pdf.set_font_size(24)
    pdf.cell(200, 20, txt="RECHNUNG", ln=True, align='L')
    pdf.set_font_size(12)
    pdf.ln(10)
    
    # Header
    pdf.cell(100, 10, txt="Absender:", ln=0)
    pdf.cell(100, 10, txt="Kunde:", ln=1)
    
    pdf.cell(100, 6, txt="Müller Maschinenbau GmbH", ln=0)
    pdf.cell(100, 6, txt="Schmidt Automobilindustrie AG", ln=1)
    
    pdf.cell(100, 6, txt="Industriestraße 42", ln=0)
    pdf.cell(100, 6, txt="Werkstraße 1", ln=1)
    
    pdf.cell(100, 6, txt="97076 Würzburg", ln=0)
    pdf.cell(100, 6, txt="70546 Stuttgart", ln=1)
    pdf.ln(10)
    
    pdf.cell(100, 6, txt="Rechnungsnummer: RE-2025-4982", ln=0)
    pdf.cell(100, 6, txt="Datum: 15.10.2025", ln=1)
    pdf.ln(10)
    
    # Items
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(90, 10, txt="Beschreibung", border=1, fill=True)
    pdf.cell(30, 10, txt="Menge", border=1, fill=True)
    pdf.cell(35, 10, txt="Einzelpreis", border=1, fill=True)
    pdf.cell(35, 10, txt="Gesamt", border=1, ln=1, fill=True)
    
    pdf.cell(90, 10, txt="CNC Frästeil Type A", border=1)
    pdf.cell(30, 10, txt="50 Stück", border=1)
    pdf.cell(35, 10, txt="120,00 EUR", border=1)
    pdf.cell(35, 10, txt="6.000,00 EUR", border=1, ln=1)
    
    pdf.cell(90, 10, txt="Wartungspauschale Q4", border=1)
    pdf.cell(30, 10, txt="1", border=1)
    pdf.cell(35, 10, txt="450,00 EUR", border=1)
    pdf.cell(35, 10, txt="450,00 EUR", border=1, ln=1)
    
    pdf.ln(10)
    pdf.cell(120, 8, txt="", border=0)
    pdf.cell(35, 8, txt="Nettobetrag:", border=1)
    pdf.cell(35, 8, txt="6.450,00 EUR", border=1, ln=1)
    
    pdf.cell(120, 8, txt="", border=0)
    pdf.cell(35, 8, txt="USt (19%):", border=1)
    pdf.cell(35, 8, txt="1.225,50 EUR", border=1, ln=1)
    
    pdf.set_font_size(14)
    pdf.cell(120, 10, txt="", border=0)
    pdf.cell(35, 10, txt="Bruttobetrag:", border=1)
    pdf.cell(35, 10, txt="7.675,50 EUR", border=1, ln=1)
    
    pdf.output(os.path.join(OUTPUT_DIR, "Rechnung_Mueller_GmbH.pdf"))

def create_nda():
    pdf = FPDF()
    pdf.add_page()
    try:
        pdf.set_font("Arial", "", 12)
    except:
        pass
    pdf.set_font_size(24)
    pdf.cell(200, 20, txt="Geheimhaltungsvereinbarung (NDA)", ln=True, align='C')
    pdf.set_font_size(11)
    pdf.ln(10)
    
    content = """Zwischen
Müller Maschinenbau GmbH, Industriestraße 42, 97076 Würzburg
- nachfolgend "Offenbarende Partei" genannt -

und
Schmidt Automobilindustrie AG, Werkstraße 1, 70546 Stuttgart
- nachfolgend "Empfangende Partei" genannt -

§ 1 Vertragsgegenstand
Die Parteien beabsichtigen eine Zusammenarbeit im Bereich der Entwicklung neuer CNC-Steuerungsverfahren. Im Rahmen dieser Zusammenarbeit wird die Offenbarende Partei der Empfangenden Partei vertrauliche Informationen zugänglich machen.

§ 2 Vertrauliche Informationen
Vertrauliche Informationen im Sinne dieser Vereinbarung sind sämtliche geschäftliche, technische und operative Informationen, die als "Vertraulich" gekennzeichnet sind.

§ 3 Geheimhaltungspflicht
Die Empfangende Partei verpflichtet sich, die Vertraulichen Informationen streng vertraulich zu behandeln, sie ausschließlich für den Vertragszweck zu verwenden und sie ohne vorherige schriftliche Zustimmung nicht an Dritte weiterzugeben.

§ 4 Vertragsstrafe
Für jeden Fall der schuldhaften Zuwiderhandlung gegen die Geheimhaltungspflicht zahlt die Empfangende Partei an die Offenbarende Partei eine Vertragsstrafe in Höhe von 50.000,00 EUR.

Unterschriften:
_______________________             _______________________
Würzburg, 01.10.2025               Stuttgart, 04.10.2025
"""
    pdf.multi_cell(0, 8, txt=content)
    pdf.output(os.path.join(OUTPUT_DIR, "NDA_Mueller_Schmidt.pdf"))

def create_contract():
    pdf = FPDF()
    pdf.add_page()
    try:
        pdf.set_font("Arial", "", 12)
    except:
        pass
    pdf.set_font_size(24)
    pdf.cell(200, 20, txt="Rahmenliefervertrag", ln=True, align='L')
    pdf.set_font_size(11)
    pdf.ln(10)
    
    content = """Vertragsparteien:
Lieferant: Müller Maschinenbau GmbH
Kunde: Schmidt Automobilindustrie AG

1. Vertragsgegenstand
Dieser Vertrag regelt die fortlaufende Lieferung von Präzisionsfrästeilen (Type A und Type B) gemäß den jeweils gültigen Spezifikationen.

2. Lieferbedingungen (Incoterms 2020)
Sofern nicht anders vereinbart, erfolgen alle Lieferungen FCA Würzburg (Free Carrier). Die Gefahr geht bei Übergabe an den ersten Frachtführer auf den Kunden über.

3. Zahlungsbedingungen
Rechnungen sind innerhalb von 30 Tagen nach Rechnungsdatum ohne Abzug zur Zahlung fällig. Bei Zahlung innerhalb von 14 Tagen gewährt der Lieferant 2% Skonto.

4. Gewährleistung und Qualität
Der Lieferant garantiert, dass die gelieferten Teile den vereinbarten Spezifikationen entsprechen. Die Gewährleistungsfrist beträgt 24 Monate ab Lieferung.

5. Laufzeit und Kündigung
Dieser Vertrag tritt am 01.01.2026 in Kraft und wird auf unbestimmte Zeit geschlossen. Er kann von beiden Seiten mit einer Frist von 3 Monaten zum Quartalsende gekündigt werden.
"""
    pdf.multi_cell(0, 8, txt=content)
    pdf.output(os.path.join(OUTPUT_DIR, "Liefervertrag_Rahmen_2026.pdf"))

if __name__ == "__main__":
    create_invoice()
    create_nda()
    create_contract()
    print("Dummy PDFs generated successfully.")
