# CryptoDashboard

## Overview
CryptoDashboard is an interactive tool designed to provide real-time insights into cryptocurrency portfolios. It leverages APIs from CoinMarketCap and Binance to fetch up-to-date information, offering users a comprehensive view of their digital assets.

## Getting Started

These instructions will guide you through the setup process required to get CryptoDashboard up and running on your local machine for development and testing purposes.

### Prerequisites

What you need to install the software and how to install them:

- Python 3.7 an beyond
- Access to CoinMarketCap and Binance APIs (API keys)
- Git (optional, for cloning the repository)

### Installation

#### Step 1: Clone the Repository

If you have Git installed, clone the repository using:

```bash
git clone https://github.com/yourusername/CryptoDashboard.git
```

Alternatively, you can download the source code directly from the repository page.

### Step 2: Create Configuration File

Navigate to the root directory of the project and create a file named `config.json` with the following content:

```json
{
  "coinmarketcap_api_key": "your_coinmarketcap_api_key",
  "binance_api_key": "your_binance_api_key",
  "binance_api_secret": "your_secret_binance_api_key"
}
```