> "Precision in Motion. Insight in Every Move."
# What is Glint?
**Glint** is a modern chess UI powered by neural network analysis, delivering **real-time evaluation of each move** as you play. Whether you’re refining your tactics or training for tournaments, Glint offers a seamless interface, instant feedback, and sonic cues — all wrapped in an elegant, minimalist design.
## How It Works?
Each move is scored and classified in real time. The categories reflect not just computational accuracy, but **strategic depth** and **intent clarity**:

| Score Δ | Label          | 💬 Description                                      |
| ------- | -------------- | --------------------------------------------------- |
| ≥ +150  | **Brilliant**  | A move of exceptional precision and rare depth      |
| ≥ +90   | **Excellent**  | A non-obvious decision with strong strategic effect |
| ≥ +50   | **Great**      | One of the best options                             |
| ≥ +20   | **Good**       | A solid move                                        |
| ≥ +5    | **OK**         | Safe, but passive                                   |
| ≥ 0     | **Reasonable** | Doesn’t improve or worsen the situation             |
| ≥ –50   | **Inaccuracy** | A missed opportunity                                |
| ≥ –150  | **Mistake**    | A significant oversight                             |
| < –150  | **Blunder**    | A critical mistake                                  |
## Why Glint?
A _glint_ is not a beam or a flash. It is a precise spark — fast, focused, and meaningful.  
This project aspires to deliver such moments of recognition, helping players grow not through guesswork, but through structured self-reflection.
Glint is designed for those who don’t just want to play —  
but to understand.
## Installation
### 🪟 Windows
Windows support will be added later :)
### 🧩 Arch Linux (AUR)
Package support will be also added later ;)
### ❄️ Nix/NixOS
Entracte provides a reproducible build via `flake.nix`. To run the app using Nix flakes:
```bash
nix run github:6e6f303216/glint
```
Or build it locally:
```bash
nix build .#glint
```
Make sure you have flakes enabled in your Nix configuration!
### 🐍 Build from Source (Cross-platform, via PyInstaller)
```bash
git clone https://github.com/6e6f303216/glint
cd glint
pip install -r requirements.txt
pyinstaller glint.spec
```
## 🔗 Community & Support
✨ **Wonders are closer than they seem** — [@wondermakers_space](https://t.me/wondermakers_space)
If you enjoy using Entracte and want to support its development:
- 💖 Boosty: [https://boosty.to/wondermakers/donate](https://boosty.to/wondermakers/donate)
- **Crypto donations** welcome:
  - **BTC**: `bc1psxndmtpkr62x0ur59cpglnnln3ksv4s5jrxf36ck3juqawvq5z0qsy6zh7`
  - **ETH/XRP**: `0x40e751968dD0Cd719136239b46B8D4aCE5Fdc7DB`
  - **TON**: `UQCdNwz7E3GJ6fVQKAvZ37b9y585c-oKjfaU9YtyjMWd4cTp`
  - **XMR**: `88kKb7VwHuaLcuhb3LESMFKaUXGp2BMc3CowWcmVBtM9LNPYTdXc2FdGVfz4xbsvKPcewkBhRizTmZ3kH5BgmK3wMLaaTrp`
  - **SOL**: `9M5BLLzq4z7n1xQZBnsaNgzeeAsQiXyY1BBptR5LNJWz`