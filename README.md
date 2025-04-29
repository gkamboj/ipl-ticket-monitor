# ipl-ticket-monitor
Get notified through Telegram message &amp; email once ticket booking starts for the IPL match of your choice.

# 🎟 IPL Ticket Monitor

Never miss IPL ticket bookings again! Get instant Telegram/email notifications when tickets go on sale for your preferred match.

[![Ticket Monitoring Active](https://img.shields.io/badge/monitoring-active-success)](https://github.com/gkamboj/ipl-ticket-monitor/actions)
![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)


## 🔔 Why I Built This

I created this tool after missing tickets for IPL 2025's [RCB vs DC match in Delhi](https://www.espncricinfo.com/series/ipl-2025-1449924/delhi-capitals-vs-royal-challengers-bengaluru-46th-match-1473483/full-scorecard) twice:
1. First sale: Didn't know when booking started - tickets sold out before I checked
2. Second sale: Tickets sold out in 1 minute despite joining queue immediately

This monitor automatically:
- Checks ticket status every 5 minutes
- Sends instant alerts when booking opens
- Runs 24/7 via GitHub Actions

## ✨ Features

- **Real-time monitoring** (configurable check interval)
- **Multi-channel alerts** (Telegram + email)
- **Status tracking** (remembers previous checks to avoid duplicate alerts)
- **Zero cost** (runs entirely on GitHub's free tier)

## ⚙️ Current Support

| Platform       | Notification Channels | Match Tracking |
|----------------|-----------------------|----------------|
| District.in    | Telegram, Email       | Single match   |

## 🚀 Getting Started

See [DEPLOYMENT.md](./DEPLOYMENT.md) for setup instructions to:
- Run locally on your machine
- Deploy as a GitHub Actions workflow

## 🔮 Future Scope

While the current version solves my immediate need, below are natural extensions:

1. **More Platforms**: BookMyShow and more
2. **Multi-Match Tracking**: Monitor several matches simultaneously
3. **Group Notifications**: Alert multiple recipients
4. **New Channels**: WhatsApp, SMS, Telegram call
5. **Web UI**: For easier configuration

## 🤝 Contributing

While this is primarily a personal project, I welcome:
- Bug reports via Issues
- Platform adapters for other ticketing sites
- Documentation improvements

---

💡 **Pro Tip**: Combine this with [Telegram's notification channels](https://core.telegram.org/api/links#t-me-links) to get alerts even when you're not checking your phone!