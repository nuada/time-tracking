# Time tracking

Create time tracing report from Google Calendar using [Secret Address](https://support.google.com/calendar/answer/37648?hl=en).

## Usage

```
echo "http://your.secret.url..." > .secret
python3 report.py [month_offset]
```

`month_offset` by default is `0`, for previous month set to `-1`, etc.

## Install

```
pip3 install -r requirements.txt
```
