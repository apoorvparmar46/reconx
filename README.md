# 🕵️ ReconX — OSINT Automation Tool

A Python-based OSINT automation tool with a clean web dashboard for cybersecurity reconnaissance.

## Features
- 🌐 Domain WHOIS & DNS Recon
- 📍 IP Geolocation & ISP Intelligence
- 🔓 Email Breach Check (HaveIBeenPwned)
- 🔑 Password Leak Check (k-anonymity)
- 👤 Username Search across 300+ platforms (Sherlock)
- 📄 PDF Report Generator
- 🖥️ Streamlit Web Dashboard

## Installation
git clone https://github.com/apoorvparmar46/reconx.git
cd reconx
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## Usage
streamlit run dashboard.py

## CLI
python main.py domain google.com
python main.py ip 8.8.8.8
python main.py password hello123
python main.py username johndoe
python main.py report google.com

## Tech Stack
Python, Streamlit, Sherlock, ReportLab, Typer, Rich