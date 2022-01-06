# Installation
1. Specify `telegram_bot_token` and `admin_ids` in `files/config.json`
2. Create db, just run `db_interaction.py` from console
3. Run `main.py`

# Usage
## Add accounts
Send a message from the account specified in `admin_ids` in the following format: 
```python
{
	"action": "add",
	"accounts": [{"login_one": "shared_secret"}, {"login_two": "shared_secret"}]
}
```

## Get 2fa code
Just send account login, bot send 2fa code in response