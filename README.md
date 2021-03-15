# Speedtest Monitor

Monitor your speed test automatically using speedtest.net

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install speedtest_monitor.

```bash
pip install speedtest_monitor
```


Optionaly install a cron to test the speed each 15 minutes with
```bash
speedtest-monitor --install-cron
```

## Usage

```bash
speedtest-monitor
```

The results will be printed and saved to `~/.speedtest/speeedtest.csv` then 
a couple of graphs are generated in `~/.speedtest/graphs`

You can change the default output directory with `--output-dir` argument. Here's
the full script arguments:

```bash
speedtest-monitor --help
```

```bash
usage: speedtest-monitor [-h] [--output-dir OUTPUT_DIR] [--download] [--upload] [--install-cron]

Measure internet speed then save the result and update the graphs

optional arguments:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR
                        Where to save the output. Default to ~/.speedtest
  --download            Wether to measure download speed or not. Defaults to True
  --upload              Wether to measure upload speed or not. Defaults to False
  --install-cron        Install the crontab to the current user and quit. Defaults to False
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
