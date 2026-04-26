import { create } from 'zustand';

export type Language = 'en' | 'de';

interface I18nStore {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: keyof typeof translations['en']) => string;
}

export const translations = {
  en: {
    title: "Mittelstand Document Agent",
    tagline: "Intelligent Document Analysis for German Mittelstand",
    upload_drop: "Drop PDF here",
    upload_select: "or click to select file",
    uploading: "Uploading...",
    processing: "Processing Document...",
    upload_success: "Document uploaded successfully",
    chat_placeholder: "Ask something about the document...",
    chat_send: "Send",
    pending_review: "Pending Review",
    approved: "Approved",
    approve_all: "Approve All",
    save: "Save",
    re_extract: "Re-extract",
    confidence_high: "High",
    confidence_medium: "Medium",
    confidence_low: "Low — Review Required",
    invoice_number: "Invoice Number",
    date: "Date",
    total_amount: "Total Amount",
    vendor_name: "Vendor Name",
    vendor_address: "Vendor Address",
    customer_name: "Customer Name",
    tax_rate: "Tax Rate",
    currency: "Currency",
    error_occurred: "An error occurred",
    hero_subtitle: "Securely extract, validate, and chat with your business PDFs in seconds.",
    powered_by: "Powered by RAG & GenAI",
    feature1_title: "Hybrid Search",
    feature1_desc: "Combines semantic understanding with exact keyword matches for precise retrieval.",
    feature2_title: "Local & Secure",
    feature2_desc: "Runs on Llama 3 with local embedding models ensuring data privacy.",
    feature3_title: "Human-in-the-Loop",
    feature3_desc: "AI extracts structured data and assigns confidence scores for easy review.",
    doc_intel: "Document Intelligence",
    for_the: "for the",
  },
  de: {
    title: "Mittelstand Dokumenten-Agent",
    tagline: "Intelligente Dokumentenanalyse für den deutschen Mittelstand",
    upload_drop: "PDF hier ablegen",
    upload_select: "oder klicken, um Datei auszuwählen",
    uploading: "Wird hochgeladen...",
    processing: "Dokument wird verarbeitet...",
    upload_success: "Dokument erfolgreich hochgeladen",
    chat_placeholder: "Fragen Sie etwas zum Dokument...",
    chat_send: "Senden",
    pending_review: "Zur Überprüfung",
    approved: "Genehmigt",
    approve_all: "Alle genehmigen",
    save: "Speichern",
    re_extract: "Neu extrahieren",
    confidence_high: "Hoch",
    confidence_medium: "Mittel",
    confidence_low: "Niedrig — Überprüfung erforderlich",
    invoice_number: "Rechnungsnummer",
    date: "Datum",
    total_amount: "Gesamtbetrag",
    vendor_name: "Name des Verkäufers",
    vendor_address: "Adresse des Verkäufers",
    customer_name: "Name des Kunden",
    tax_rate: "Steuersatz",
    currency: "Währung",
    error_occurred: "Ein Fehler ist aufgetreten",
    hero_subtitle: "Extrahieren, validieren und chatten Sie sicher mit Ihren Geschäfts-PDFs in Sekundenschnelle.",
    powered_by: "Unterstützt durch RAG & GenAI",
    feature1_title: "Hybride Suche",
    feature1_desc: "Kombiniert semantisches Verständnis mit exakten Keyword-Treffern für eine präzise Suche.",
    feature2_title: "Lokal & Sicher",
    feature2_desc: "Läuft auf Llama 3 mit lokalen Embedding-Modellen und gewährleistet Datenschutz.",
    feature3_title: "Human-in-the-Loop",
    feature3_desc: "KI extrahiert strukturierte Daten und weist Konfidenzwerte für eine einfache Überprüfung zu.",
    doc_intel: "Dokumenten-Intelligenz",
    for_the: "für den",
  }
};

export const useI18n = create<I18nStore>((set, get) => ({
  language: 'en',
  setLanguage: (lang) => set({ language: lang }),
  t: (key) => translations[get().language][key] || key,
}));
