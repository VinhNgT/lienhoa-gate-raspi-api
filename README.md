Upgrade packages:

```bash
pip freeze > requirements.txt
sed -i 's/==/>=/g' requirements.txt
pip install -r requirements.txt --upgrade
```
